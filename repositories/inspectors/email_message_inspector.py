# coding=utf-8

import hashlib
import os
import sqlite3

from cybox.common import datetime
from cybox.objects.email_message_object import EmailHeader, EmailMessage
from cybox.objects.file_object import File
from cybox.utils import set_id_method, IDGenerator

from model.operation import Inspector, OperationError


def calculate_hash(route, block_size=65536):
    hasher = hashlib.sha256()
    with open(route, 'rb') as a_file:
        buf = a_file.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = a_file.read(block_size)
    return hasher.hexdigest()


class EmailMessageInspector(Inspector):
    def execute(self, device_info, extracted_data_dir_path, simple_output):
        db_message_file_name = 'EmailProvider.db'
        db_body_file_name = 'EmailProviderBody.db'
        db_message_file_path = os.path.join(extracted_data_dir_path, 'databases', db_message_file_name)
        db_body_file_path = os.path.join(extracted_data_dir_path, 'databases', db_body_file_name)

        if not os.path.exists(db_message_file_path):
            raise OperationError('Inspection failed: Message DB do not exists.')

        conn = sqlite3.connect(db_message_file_path)
        c = conn.cursor()

        try:
            c.execute('SELECT * FROM message')
        except (sqlite3.OperationalError, sqlite3.DatabaseError), msg:
            # TODO: Logger
            raise OperationError('Inspection failed: {0}'.format(msg))

        column_names = [d[0] for d in c.description]

        if simple_output:
            set_id_method(IDGenerator.METHOD_INT)

        source_objects = []

        db_message_file_object = File()
        db_message_file_object.file_name = db_message_file_name
        db_message_file_object.file_extension = '.db'
        db_message_file_object.file_path = '/data/data/com.android.email/databases/'
        db_message_file_object.file_format = 'SQLite 3.x database'
        db_message_file_object.size_in_bytes = os.path.getsize(db_message_file_path)
        db_message_file_object.sha256 = calculate_hash(db_message_file_path)

        source_objects.append(db_message_file_object)

        db_body_file_object = File()
        db_body_file_object.file_name = db_message_file_name
        db_body_file_object.file_extension = '.db'
        db_body_file_object.file_path = '/data/data/com.android.email/databases/'
        db_body_file_object.file_format = 'SQLite 3.x database'
        db_body_file_object.size_in_bytes = os.path.getsize(db_message_file_path)
        db_body_file_object.sha256 = calculate_hash(db_message_file_path)

        source_objects.append(db_body_file_object)

        # Auxiliary dictionary that maps android database id to email object.
        # Used to append email's body and content-type connecting to another database.
        aux_inspected_hash = {}

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

            email = EmailMessage()
            email.header = header
            email.add_related(db_message_file_object, 'Extracted_From', inline=not simple_output)
            # TODO: Falta relacionar con la base de datos de los body's

            aux_inspected_hash[row_data['_id']] = email

        c.close()
        conn.close()

        # Connect to EmailMessageBody.db and add email's body.
        if not os.path.exists(db_body_file_path):
            raise OperationError("Inspection failed: Body's DB do not exists.")

        conn = sqlite3.connect(db_body_file_path)
        c = conn.cursor()

        try:
            c.execute('SELECT * FROM body')
        except (sqlite3.OperationalError, sqlite3.DatabaseError), msg:
            # TODO: Logger
            raise OperationError('Inspection failed: {0}'.format(msg))

        column_names = [d[0] for d in c.description]

        inspected_objects = []

        for row in c:
            row_data = dict(zip(column_names, row))

            current_object = aux_inspected_hash.get(row_data['_id'])

            if current_object is not None:
                if row_data['htmlContent'] == '':
                    current_object.raw_body = row_data['htmlContent']
                    current_object.header.content_type = 'html'
                else:
                    current_object.raw_body = row_data['textContent']
                    current_object.header.content_type = 'text'

                inspected_objects.append(current_object)

        return inspected_objects, source_objects
