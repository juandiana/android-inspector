# coding=utf-8
import os
from cybox.common.object_properties import CustomProperties, Property
from cybox.common.vocabs import ObjectRelationship
from cybox.objects.custom_object import Custom
from model import Inspector
from util.inspectors_helper import create_file_object, execute_query


class ContactFacebookInspector(Inspector):
    def execute(self, device_info, extracted_data_dir_path, simple_output):
        original_app_path = '/data/data/com.facebook.katana'
        fb_db_rel_file_path = os.path.join('databases', 'fb.db')

        original_fb_db_file_path = os.path.join(original_app_path, fb_db_rel_file_path)
        fb_db_file_path = os.path.join(extracted_data_dir_path, fb_db_rel_file_path)

        source_objects = [create_file_object(fb_db_file_path, original_fb_db_file_path)]

        inspected_objects = []

        properties = ['display_name', 'first_name', 'last_name', 'cell', 'email',
                      'user_image_url', 'birthday_day', 'birthday_month', 'birthday_year']

        query = 'SELECT ' + ', '.join(properties) + ' FROM friends'

        cursor, conn = execute_query(fb_db_file_path, query)

        for row in cursor:
            custom = Custom()
            custom.custom_name = 'Contact'
            custom.custom_properties = CustomProperties()

            for p in properties:
                if row[p]:
                    prop = Property()
                    prop.name = p
                    prop.value = str(row[p])
                    custom.custom_properties.append(prop)

            custom.add_related(source_objects[0], ObjectRelationship.TERM_EXTRACTED_FROM, inline=False)

            inspected_objects.append(custom)

        cursor.close()

        return inspected_objects, source_objects
