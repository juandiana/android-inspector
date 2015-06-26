# coding=utf-8
import unittest
from components.operations_manager import OperationsManager, NotDefinedError
from components.repositories_manager import RepositoriesManager
from model import DataSource, OperationInfo, DeviceInfo


class MockedDefinitionsDatabase(object):
    def query_operations_info(self, data_type, data_source, device_info):
        op1_id = 'com.example/gmail/email'
        op1_data_type = "EmailMessage"
        op1_data_source = DataSource('Application', {'package_name': 'com.google.gm'})
        op1_supported_device_models = ['XT1053']
        op1_supported_os_versions = ['4.4.4', '5.1']
        op1_info = OperationInfo(op1_id, op1_data_type, op1_data_source, op1_supported_device_models,
                                 op1_supported_os_versions)
        result = list()
        result.append(op1_info)
        return result

    def get_operation_exec_info(self, id_):
        return {
            'extractor_id': 'com.example.extractor1',
            'inspector_id': 'com.example.inspector1',
            'param_values': {
                'package_name': 'com.google.gm'
            }
        }

    def exists_data_type(self, data_type):
        return True

    def exists_data_source_type(self, data_source_type):
        return True


class TestOperationsManager(unittest.TestCase):
    def setUp(self):
        definitions_database = MockedDefinitionsDatabase()
        repositories_manager = RepositoriesManager()
        self.operations_manager = OperationsManager(definitions_database, repositories_manager)

    def test_operations_manager(self):
        data_type = 'EmailMessage'
        data_source = DataSource('Application', {'package_name': 'com.google.gm'})
        device_info = DeviceInfo('4.4.4', 'XT1053')
        try:
            op_info = self.operations_manager.get_operations_info(data_type, data_source, device_info)
            print op_info
        except NotDefinedError as error:
            print error.message


if __name__ == '__main__':
    unittest.main()
