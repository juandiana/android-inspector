# coding=utf-8

import os
import tempfile
import unittest
import shutil

from cybox.common import Hash, DateTime
from cybox.objects.email_message_object import EmailMessage
from cybox.objects.file_object import File

from model import Extractor, Inspector, DeviceInfo, Operation, EXTRACTED_DATA_DIR_NAME


# TODO: @implements?
class MockedApplicationExtractor(Extractor):
    def execute(self, extracted_data_dir_path, param_values):
        pass


class MockedEmailInspector(Inspector):
    def __get_source_objs(self):
        f1 = File()
        f1.file_name = 'emailprovider.db'
        f1.file_path = '/data/data/com.android.providers.email/databases/'
        f1.file_format = 'SQLite 3.x database'
        f1.size_in_bytes = '2374'
        f1.add_hash(Hash("a7a0390e99406f8975a1895860f55f2f"))
        return [f1]

    def __get_inspected_objs(self, source_file):
        email1 = EmailMessage()
        email1.from_ = 'email1@example.com'
        email1.to = 'email2@example.com'
        email1.subject = 'Subject1'
        email1.date = DateTime('21-06-2015T19:52:00')
        email1.add_related(source_file, "Extracted_From", inline=False)
        return [email1]

    def execute(self, device_info, extracted_data_dir_path, simple_output):
        source_objects = self.__get_source_objs()
        inspected_objects = self.__get_inspected_objs(source_objects[0])
        return inspected_objects, source_objects


class TestOperation(unittest.TestCase):
    def setUp(self):
        self.extractor = MockedApplicationExtractor()
        self.inspector = MockedEmailInspector()
        self.param_values = {'package_name': 'com.android.email'}
        self.device_info = DeviceInfo('4.4.4', 'XT1053')
        self.data_dir_path = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.data_dir_path)

    def test_operation(self):
        op = Operation(self.extractor, self.inspector, self.param_values)
        op.execute(self.device_info, self.data_dir_path)

        self.assertTrue(os.path.exists(os.path.join(self.data_dir_path, EXTRACTED_DATA_DIR_NAME)))


if __name__ == "__main__":
    unittest.main()
