# coding=utf-8
import os
from cybox.common.object_properties import CustomProperties, Property
from cybox.common.vocabs import ObjectRelationship
from cybox.objects.custom_object import Custom
from cybox.utils import set_id_method, IDGenerator
from model import Inspector
from util.inspectors_helper import create_file_object, execute_query, get_source_object


class ContactWhatsAppInspector(Inspector):
    def execute(self, device_info, extracted_data_dir_path, simple_output):
        original_app_path = '/data/data/com.whatsapp'
        wa_db_rel_file_path = os.path.join('databases', 'wa.db')

        original_wa_db_file_path = os.path.join(original_app_path, wa_db_rel_file_path)
        wa_db_file_path = os.path.join(extracted_data_dir_path, wa_db_rel_file_path)

        if simple_output:
            set_id_method(IDGenerator.METHOD_INT)

        source_objects = [create_file_object(wa_db_file_path, original_wa_db_file_path)]

        # Properties to add to Custom Object
        properties = ['display_name', 'given_name', 'family_name', 'number']

        inspected_objects = []

        query = 'SELECT display_name, given_name, family_name, number, jid FROM wa_contacts'

        cursor, conn = execute_query(wa_db_file_path, query)

        for row in cursor:
            custom = Custom()
            custom.custom_name = 'Contact'
            custom.custom_properties = CustomProperties()

            for p in properties:
                if row[p]:
                    prop = Property()
                    prop.name = p
                    prop.value = row[p]
                    custom.custom_properties.append(prop)

            custom.add_related(source_objects[0], ObjectRelationship.TERM_EXTRACTED_FROM, inline=False)

            if row['jid']:
                # Using 'jid' field, create the absolute image_file path.
                attachment_rel_file_path = os.path.join('files', 'Avatars', row['jid'] + '.j')

                # Build image_file absolute file path in extracted_data.
                attachment_file_path = os.path.join(extracted_data_dir_path, attachment_rel_file_path)

                # If there's a file in the extracted_data directory
                if os.path.isfile(attachment_file_path):

                    # Build image_file original file_path in device.
                    original_attachment_file_path = os.path.join(original_app_path, attachment_rel_file_path)

                    image_file = get_source_object(original_attachment_file_path, source_objects)

                    # Create image_file if it does not exist.
                    if image_file is None:
                        image_file = create_file_object(attachment_file_path, original_attachment_file_path)
                        source_objects.append(image_file)

                    # Add profile_picture property, with absolute path to image_file as value.
                    p_profile_picture = Property()
                    p_profile_picture.name = 'profile_picture'
                    p_profile_picture.value = 'file://' + os.path.join(os.getcwd(), attachment_file_path)
                    custom.custom_properties.append(p_profile_picture)

                    custom.add_related(image_file, ObjectRelationship.TERM_RELATED_TO, inline=False)

            inspected_objects.append(custom)

        cursor.close()

        return inspected_objects, source_objects
