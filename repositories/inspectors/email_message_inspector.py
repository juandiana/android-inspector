# coding=utf-8

import os
import sqlite3

from cybox.common import datetime
from cybox.objects.email_message_object import EmailHeader, EmailMessage
from cybox.utils import set_id_method, IDGenerator

from model.operation import Inspector, OperationError
from util.inspectors_helper import create_file_object


class EmailMessageInspector(Inspector):
    def _execute_query(self, headers_db_file_path, sql_query):
        if not os.path.exists(headers_db_file_path):
            raise OperationError('Inspection failed: {0} not found.'.format(headers_db_file_path))
        conn = sqlite3.connect(headers_db_file_path)
        # Access columns by name instead of by index
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        try:
            c.execute(sql_query)
        except (sqlite3.OperationalError, sqlite3.DatabaseError) as error:
            # TODO: Log the error message.
            raise OperationError('Inspection failed: Could not perform SQL query on {0}.'.format(headers_db_file_path))
        return c, conn

    def execute(self, device_info, extracted_data_dir_path, simple_output):
        original_app_path = '/data/data/com.android.email'
        headers_db_rel_file_path = os.path.join('databases', 'EmailProvider.db')
        bodies_db_rel_file_path = os.path.join('databases', 'EmailProviderBody.db')

        original_headers_db_file_path = os.path.join(original_app_path, headers_db_rel_file_path)
        original_bodies_db_file_path = os.path.join(original_app_path, bodies_db_rel_file_path)
        headers_db_file_path = os.path.join(extracted_data_dir_path, headers_db_rel_file_path)
        bodies_db_file_path = os.path.join(extracted_data_dir_path, bodies_db_rel_file_path)

        if simple_output:
            set_id_method(IDGenerator.METHOD_INT)

        source_objects = [
            create_file_object(headers_db_file_path, original_headers_db_file_path),
            create_file_object(bodies_db_file_path, original_bodies_db_file_path)
        ]
        inspected_objects = {}

        cursor, conn = self._execute_query(headers_db_file_path, 'SELECT * FROM message')
        for row in cursor:
            header = EmailHeader()
            header.to = row['toList']
            header.cc = row['ccList']
            header.bcc = row['bccList']
            header.from_ = row['fromList']
            header.subject = row['subject']
            header.in_reply_to = row['replyToList']
            header.date = datetime.fromtimestamp(row['timeStamp'] / 1000)  # Convert from milliseconds to seconds
            header.message_id = row['messageId']

            email = EmailMessage()
            email.header = header
            email.add_related(source_objects[0], 'Extracted_From', inline=not simple_output)

            # Add the email to the inspected_objects dict using its _id value as key.
            email_id = row['_id']
            inspected_objects[email_id] = email
        cursor.close()
        conn.close()

        cursor, conn = self._execute_query(bodies_db_file_path, 'SELECT _id, htmlContent, textContent FROM body')
        for row in cursor:
            email_id = row['_id']
            email = inspected_objects.get(email_id)
            if email is not None:
                if row['htmlContent'] != '':
                    email.raw_body = row['htmlContent']
                    email.header.content_type = 'text/html'
                else:
                    email.raw_body = row['textContent']
                    email.header.content_type = 'text/plain'
                email.add_related(source_objects[1], 'Extracted_From', inline=not simple_output)
        cursor.close()
        conn.close()

        return inspected_objects.values(), source_objects
