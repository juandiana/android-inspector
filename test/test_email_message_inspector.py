# coding=utf-8
import os
import unittest
from cybox.core import Observables

from model import DeviceInfo, EXTRACTED_DATA_DIR_NAME, OperationError, INSPECTED_DATA_FILE_NAME, SOURCE_DATA_FILE_NAME
from repositories.inspectors.email_message_inspector import EmailMessageInspector


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.device_info = DeviceInfo('4.4.4', 'XT1053')
        self.inspector = EmailMessageInspector()

    def test_something(self):
        try:
            inspected_objects, source_objects = self.inspector.execute(self.device_info, EXTRACTED_DATA_DIR_NAME, True)
        except OperationError:
            raise

        inspected_xml = Observables(inspected_objects).to_xml(include_namespaces=True)
        source_xml = Observables(source_objects).to_xml(include_namespaces=True)

        with open(INSPECTED_DATA_FILE_NAME, 'w') as file1:
            file1.write(inspected_xml)

        with open(SOURCE_DATA_FILE_NAME, 'w') as file2:
            file2.write(source_xml)


if __name__ == '__main__':
    unittest.main()
