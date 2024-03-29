# coding=utf-8

import os
import re

from cybox.common import datetime
from cybox.common.vocabs import ObjectRelationship
from cybox.objects.email_message_object import EmailHeader, EmailMessage, Attachments

from model.operation import Inspector
from util.inspectors_helper import create_file_object, execute_query


class EmailMessageInspector(Inspector):
    def execute(self, device_info, extracted_data_dir_path):
        original_app_path = '/data/data/com.android.email'
        headers_db_rel_file_path = os.path.join('databases', 'EmailProvider.db')
        bodies_db_rel_file_path = os.path.join('databases', 'EmailProviderBody.db')

        original_headers_db_file_path = os.path.join(original_app_path, headers_db_rel_file_path)
        original_bodies_db_file_path = os.path.join(original_app_path, bodies_db_rel_file_path)
        headers_db_file_path = os.path.join(extracted_data_dir_path, headers_db_rel_file_path)
        bodies_db_file_path = os.path.join(extracted_data_dir_path, bodies_db_rel_file_path)

        source_objects = [
            create_file_object(headers_db_file_path, original_headers_db_file_path),
            create_file_object(bodies_db_file_path, original_bodies_db_file_path)
        ]
        inspected_objects = {}

        cursor, conn = execute_query(headers_db_file_path, 'SELECT * FROM message')
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
            email.add_related(source_objects[0], ObjectRelationship.TERM_EXTRACTED_FROM, inline=False)

            # Add the email to the inspected_objects dict using its _id value as key.
            email_id = row['_id']
            inspected_objects[email_id] = email
        cursor.close()
        conn.close()

        # Add full raw body to emails.
        cursor, conn = execute_query(bodies_db_file_path, 'SELECT _id, htmlContent, textContent FROM body')
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
                email.add_related(source_objects[1], ObjectRelationship.TERM_EXTRACTED_FROM, inline=False)
        cursor.close()

        # Add attachments to emails.
        cursor, conn = execute_query(headers_db_file_path,
                                     'SELECT messageKey, contentUri FROM attachment')

        # Iteration over attachments
        for row in cursor:
            # Get current attachment email_id.
            email_id = row['messageKey']
            # Find email in inspected_objects.
            email = inspected_objects.get(email_id)

            # If email has non attachments, initialize them.
            if email.attachments is None:
                email.attachments = Attachments()

            # Using contentUri, get attachment folder_prefix and file_name.
            attachment_rel_path_dirs = re.search('.*//.*/(.*)/(.*)/.*', row['contentUri'])

            # Group(1): contains attachment folder.
            # Group(2): contains attachment file_name.
            attachment_rel_file_path = os.path.join('databases', attachment_rel_path_dirs.group(1) + '.db_att',
                                                    attachment_rel_path_dirs.group(2))

            # Build attachment absolute file path in extracted_data.
            attachment_file_path = os.path.join(extracted_data_dir_path, attachment_rel_file_path)

            # Build attachment original file_path in device.
            original_attachment_file_path = os.path.join(original_app_path, attachment_rel_file_path)

            # Create attachment source_file.
            attachment = create_file_object(attachment_file_path, original_attachment_file_path)

            # Add attachment to email's attachments.
            email.attachments.append(attachment.parent.id_)

            # Add relation between attachment and it's email.
            attachment.add_related(email, ObjectRelationship.TERM_CONTAINED_WITHIN, inline=False)

            source_objects.append(attachment)

        cursor.close()
        conn.close()

        return inspected_objects.values(), source_objects
