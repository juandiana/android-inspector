# coding=utf-8
import os
from cybox.common.vocabs import ObjectRelationship
from cybox.utils import set_id_method, IDGenerator
import re
from model import Inspector
from repositories.custom_cybox_objects.contact import Contact
from util import inspectors_helper


class ContactStockInspector(Inspector):
    def execute(self, device_info, extracted_data_dir_path, simple_output):
        original_app_path = '/data/data/com.android.providers.telephony'
        contacts_db_rel_file_path = os.path.join('databases', 'contacts2.db')

        original_contacts_db_file_path = os.path.join(original_app_path, contacts_db_rel_file_path)
        contacts_db_file_path = os.path.join(extracted_data_dir_path, contacts_db_rel_file_path)

        if simple_output:
            set_id_method(IDGenerator.METHOD_INT)

        source_objects = [inspectors_helper.create_file_object(contacts_db_file_path, original_contacts_db_file_path)]

        inspected_objects = []

        query = """
                SELECT pp.display_name AS display_name, pp.display_name_alt AS alt_name,
                       pp.account_name AS account_name, pp.account_type AS account_type,
                       c.photo_id AS photo_id, ph.number AS phone_number
                FROM view_v1_people pp, view_v1_phones ph, contacts c
                WHERE pp._id = c._id AND c._id = ph.person
                """

        cursor, conn = inspectors_helper.execute_query(contacts_db_file_path, query)

        for row in cursor:
            contact = Contact()
            if row['display_name']:
                contact.display_name = row['display_name']

            if row['alt_name'] and ',' in row['alt_name']:
                alt_name = re.search('(.*),(.*)', row['alt_name'])
                contact.first_name = alt_name.group(2)
                contact.last_name = alt_name.group(1)

            if row['phone_number']:
                contact.phone_number = row['phone_number']

            # if row['account_type'] and row['account_name']:
            #     if 'google' in row['account_name'] or 'yahoo' in row['account_name']:
            #         contact.email = row['account_name']  # TODO: FIX

            if row['photo_id']:
                profile_picture_rel_file_path = os.path.join('files', 'thumbnail_photo_' + str(row['photo_id']) + '.jpg')
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

            contact.add_related(source_objects[0], ObjectRelationship.TERM_EXTRACTED_FROM, inline=False)

            inspected_objects.append(contact)

        cursor.close()
        conn.close()

        return inspected_objects, source_objects
