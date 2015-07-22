# coding=utf-8
import os
from cybox.common import Date
from cybox.common.object_properties import CustomProperties, Property
from cybox.common.vocabs import ObjectRelationship
from cybox.objects.custom_object import Custom
from cybox.utils import set_id_method, IDGenerator
from model import Inspector
from repositories.custom_cybox_objects.contact import Contact
from util.inspectors_helper import create_file_object, execute_query


class ContactFacebookInspector(Inspector):
    def execute(self, device_info, extracted_data_dir_path, simple_output):
        original_app_path = '/data/data/com.facebook.katana'
        fb_db_rel_file_path = os.path.join('databases', 'fb.db')

        original_fb_db_file_path = os.path.join(original_app_path, fb_db_rel_file_path)
        fb_db_file_path = os.path.join(extracted_data_dir_path, fb_db_rel_file_path)

        if simple_output:
            set_id_method(IDGenerator.METHOD_INT)

        source_objects = [create_file_object(fb_db_file_path, original_fb_db_file_path)]

        inspected_objects = []

        query = """
                SELECT display_name, first_name, last_name, cell, email,
                       user_image_url, birthday_day, birthday_month, birthday_year
                FROM friends
                """

        cursor, conn = execute_query(fb_db_file_path, query)

        for row in cursor:
            contact = Contact()
            if row['display_name']:
                contact.display_name = row['display_name']
            if row['first_name']:
                contact.first_name = row['first_name']
            if row['last_name']:
                contact.last_name = row['last_name']
            if row['cell']:
                contact.phone_number = row['cell']
            if row['email']:
                contact.email = row['email']
            if row['user_image_url']:
                contact.profile_picture = row['user_image_url']

            birthday = []
            if not (row['birthday_day'] == -1 or row['birthday_month'] == -1):
                birthday.append(str(row['birthday_day']))
                birthday.append(str(row['birthday_month']))

                if row['birthday_year'] != -1:
                    birthday.append(str(row['birthday_year']))

                contact.birthday = '/'.join(birthday)

            contact.add_related(source_objects[0], ObjectRelationship.TERM_EXTRACTED_FROM, inline=False)

            inspected_objects.append(contact)

        cursor.close()
        conn.close()

        return inspected_objects, source_objects
