# coding=utf-8
import os

from cybox.common.vocabs import ObjectRelationship

from model import Inspector
from repositories.custom_cybox_objects.contact_object import Contact
from util import inspectors_helper


class ContactWhatsappInspector(Inspector):
    def execute(self, device_info, extracted_data_dir_path):
        original_app_path = '/data/data/com.whatsapp'
        wa_db_rel_file_path = os.path.join('databases', 'wa.db')

        original_wa_db_file_path = os.path.join(original_app_path, wa_db_rel_file_path)
        wa_db_file_path = os.path.join(extracted_data_dir_path, wa_db_rel_file_path)

        source_objects = [inspectors_helper.create_file_object(wa_db_file_path, original_wa_db_file_path)]

        inspected_objects = []

        query = 'SELECT display_name, given_name, family_name, number, jid FROM wa_contacts'

        cursor, conn = inspectors_helper.execute_query(wa_db_file_path, query)

        for row in cursor:
            contact = Contact()

            if row['display_name']:
                contact.display_name = row['display_name']
            if row['given_name']:
                contact.first_name = row['given_name']
            if row['family_name']:
                contact.last_name = row['family_name']
            if row['number']:
                contact.phone_number = row['number']

            contact.add_related(source_objects[0], ObjectRelationship.TERM_EXTRACTED_FROM, inline=False)

            if row['jid']:
                # Using 'jid' field, create the absolute image_file path.
                profile_picture_rel_file_path = os.path.join('files', 'Avatars', row['jid'] + '.j')

                # Build image_file absolute file path in extracted_data.
                profile_picture_file_path = os.path.join(extracted_data_dir_path, profile_picture_rel_file_path)

                # If there's a file in the extracted_data directory
                if os.path.isfile(profile_picture_file_path):

                    # Build image_file original file_path in device.
                    original_profile_picture_file_path = os.path.join(original_app_path, profile_picture_rel_file_path)

                    image_file = inspectors_helper.get_source_object(original_profile_picture_file_path, source_objects)

                    # Create image_file if it does not exist.
                    if image_file is None:
                        image_file = inspectors_helper.create_file_object(profile_picture_file_path,
                                                                          original_profile_picture_file_path)
                        source_objects.append(image_file)

                    # Add profile_picture property.
                    contact.profile_picture = 'file://' + original_profile_picture_file_path

                    contact.add_related(image_file, ObjectRelationship.TERM_RELATED_TO, inline=False)

            inspected_objects.append(contact)

        cursor.close()
        conn.close()

        return inspected_objects, source_objects
