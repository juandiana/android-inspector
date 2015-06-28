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

        if SIMPLE_OUTPUT:
            set_id_method(IDGenerator.METHOD_INT)

        source_objects = []

        db_file_object = File()
        db_file_object.file_name = db_file_name
        db_file_object.file_path = '/data/data/com.android.email/databases/'
        db_file_object.file_format = 'SQLite 3.x database'
        db_file_object.size_in_bytes = os.path.getsize(db_file_path)
        db_file_object.add_hash(calculate_hash(db_file_path))

        source_objects.append(db_file_object)

        inspected_objects = []

        for row in c:
            row_data = dict(zip(column_names, row))

            header = EmailHeader()
            header.to = row_data['toList']
            header.cc = row_data['ccList']
            header.bcc = row_data['bccList']
            header.from_ = row_data['fromList']
            header.subject = row_data['subject']
            header.in_reply_to = row_data['replyToList']
            header.date = datetime.fromtimestamp(row_data['timeStamp'] / 1000)  # Convert from milliseconds to seconds
            header.message_id = row_data['messageId']
            header.content_type = 'text/html'

            email = EmailMessage()
            email.header = header
            email.add_related(db_file_object, "Extracted From", inline=not SIMPLE_OUTPUT)

            inspected_objects.append(email)

        c.close()
        conn.close()

        return InspectionResult(True, inspected_objects, source_objects)
