# coding=utf-8
import os
import unittest

from cybox.core import Observables

from model import DeviceInfo, INSPECTED_DATA_FILE_NAME, SOURCE_DATA_FILE_NAME, write_observables_xml_file
from repositories.inspectors.contact_facebook_inspector import ContactFacebookInspector
from repositories.inspectors.contact_stock_inspector import ContactStockInspector
from repositories.inspectors.contact_whatsapp_inspector import ContactWhatsAppInspector
from repositories.inspectors.email_message_inspector import EmailMessageInspector
from repositories.inspectors.sms_message_inspector import SmsMessageInspector


class TestInspectors(unittest.TestCase):
    def setUp(self):
        self.device_info = DeviceInfo('4.4.4', 'XT1053')

    def run_inspector_test(self, inspector, directory_name):
        # Output paths
        output_dir_path = os.path.join('test', 'test_extracted_data', directory_name)
        inspected_data_file_path = os.path.join(output_dir_path, INSPECTED_DATA_FILE_NAME)
        source_data_file_path = os.path.join(output_dir_path, SOURCE_DATA_FILE_NAME)

        # Execute the inspector
        inspected_objects, source_objects = inspector.execute(self.device_info, output_dir_path)

        # write the results
        write_observables_xml_file(Observables(inspected_objects), inspected_data_file_path, simple_output=True)
        write_observables_xml_file(Observables(source_objects), source_data_file_path, simple_output=True)

        # Assert xml files were written
        self.assertTrue(os.path.exists(inspected_data_file_path))
        self.assertTrue(os.path.exists(source_data_file_path))

        # Delete the created files
        os.remove(inspected_data_file_path)
        os.remove(source_data_file_path)

    def test_sms_message_inspector(self):
        self.run_inspector_test(SmsMessageInspector(), 'sms_message')

    def test_email_message_inspector(self):
        self.run_inspector_test(EmailMessageInspector(), 'email_message')

    def test_contact_facebook_inspector(self):
        self.run_inspector_test(ContactFacebookInspector(), 'contact_facebook')

    def test_contact_whatsapp_inspector(self):
        self.run_inspector_test(ContactWhatsAppInspector(), 'contact_whatsapp')

    def test_contact_stock_inspector(self):
        self.run_inspector_test(ContactStockInspector(), 'contact_stock')


if __name__ == '__main__':
    unittest.main()
