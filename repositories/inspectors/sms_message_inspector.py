# coding=utf-8
from datetime import datetime
import os

from cybox.objects.sms_message_object import SMSMessage
from cybox.common.vocabs import ObjectRelationship

from model import Inspector
from util.inspectors_helper import create_file_object, execute_query


class SmsMessageInspector(Inspector):
    def execute(self, device_info, extracted_data_dir_path):
        original_app_path = '/data/data/com.android.providers.telephony'
        sms_db_rel_file_path = os.path.join('databases', 'mmssms.db')

        original_sms_db_file_path = os.path.join(original_app_path, sms_db_rel_file_path)
        sms_db_file_path = os.path.join(extracted_data_dir_path, sms_db_rel_file_path)

        source_objects = [create_file_object(sms_db_file_path, original_sms_db_file_path)]

        inspected_objects = []

        cursor, conn = execute_query(sms_db_file_path, 'SELECT * FROM sms')
        for row in cursor:
            sms = SMSMessage()
            if row['type'] == 1:
                sms.sender_phone_number = row['address']
            else:
                sms.recipient_phone_number = row['address']
            sms.sent_datetime = datetime.fromtimestamp(row['date'] / 1000)  # Convert from milliseconds to seconds
            sms.body = row['body']
            sms.length = len(row['body'])
            sms.add_related(source_objects[0], ObjectRelationship.TERM_EXTRACTED_FROM, inline=False)

            inspected_objects.append(sms)

        cursor.close()
        conn.close()

        return inspected_objects, source_objects
