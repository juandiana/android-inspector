# coding=utf-8
import unittest
from cybox.core import Observables

from model import DeviceInfo, EXTRACTED_DATA_DIR_NAME, OperationError
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

        print Observables(inspected_objects).to_xml(include_namespaces=False)
        print Observables(source_objects).to_xml(include_namespaces=False)

if __name__ == '__main__':
    unittest.main()
