# coding=utf-8

import hashlib
import os
import sqlite3

from cybox.common import datetime
from cybox.objects.email_message_object import EmailHeader, EmailMessage
from cybox.objects.file_object import File
from cybox.utils import set_id_method, IDGenerator

from model.operation import Inspector, InspectionResult

SIMPLE_OUTPUT = True


def calculate_hash(route, block_size=65536):
    hasher = hashlib.sha256()
    with open(route, 'rb') as a_file:
        buf = a_file.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = a_file.read(block_size)

    return hasher.hexdigest()


class EmailMessageInspector(Inspector):
    def execute(self, device_info, extracted_data_dir_path):
        db_file_name = 'EmailProvider.db'
        db_file_path = os.path.join(extracted_data_dir_path, 'databases', db_file_name)

        if not os.path.exists(db_file_path):
            return InspectionResult(False)

        conn = sqlite3.connect(db_file_path)
        c = conn.cursor()

        try:
            c.execute('SELECT * FROM message')
        except (sqlite3.OperationalError, sqlite3.DatabaseError), msg:
            # TODO: Logger
            return InspectionResult(False)

        column_names = [d[0] for d in c.description]

        if simple_output:
            set_id_method(IDGenerator.METHOD_INT)

        # Source data
        source_data = []

        source_file = File()
        source_file.file_name = db_file_name
        source_file.file_path = '/data/data/com.android.email/databases/'
        source_file.file_format = 'SQLite 3.x database'
        source_file.size_in_bytes = os.path.getsize(db_file_path)
        source_file.add_hash(calculate_hash(db_file_path))

        source_data.append(source_file)

        # Inspected data
        inspected_data = []

        for row in c:
            # build dict
            info = dict(zip(column_names, row))

            header = EmailHeader()
            header.to = info['toList']
            header.cc = info['ccList']
            header.bcc = info['bccList']
            header.from_ = info['fromList']
            header.subject = info['subject']
            header.in_reply_to = info['replyToList']
            header.date = datetime.fromtimestamp(info['timeStamp'] / 1000)  # Convert from milliseconds to seconds
            header.message_id = info['messageId']
            header.content_type = 'text/html'

            email = EmailMessage()
            email.header = header
            email.add_related(source_file, "Extracted From", inline=not simple_output)

            inspected_data.append(email)

        c.close()
        conn.close()

        return InspectionResult(True, inspected_data, source_data)
