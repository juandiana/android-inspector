# coding=utf-8
import os
import unittest

from components.definitions_database_manager import DefinitionsDatabaseManager
from components.operations_manager import OperationsManager
from components.repositories_manager import RepositoriesManager
from model import DataSource, OperationInfo, DeviceInfo


class MockedDefinitionsDatabaseManager(object):
    def query_operations_info(self, data_type, data_source, device_info):
        op_info = OperationInfo(
            name='com.example:EmailGMail',
            data_type='EmailMessage',
            data_source=DataSource('Application', {'package_name': 'com.google.gm'}),
            supported_device_models=['XT1053'],
            supported_os_versions=['4.4.4', '5.1']
        )
        return [op_info]

    def get_operation_exec_info(self, id_):
        return 'com.example.extractor1', 'com.example.inspector1', {'package_name': 'com.google.gm'}

    def exists_data_type(self, name):
        return True

    def exists_data_source_type(self, data_source_type):
        return True

    def has_all_required_param_values(self, data_source):
        return True


class TestOperationsManager(unittest.TestCase):
    def setUp(self):
        real_definitions_database = DefinitionsDatabaseManager(os.path.join('test', 'definitions.db'),
                                                               'create_db.sql',
                                                               'insert_default_data_types.sql',
                                                               'insert_default_data_source_types.sql',
                                                               'insert_default_operations.sql')
        mocked_definitions_database = MockedDefinitionsDatabaseManager()
        repositories_manager = RepositoriesManager('repositories')
        self.real_operations_manager = OperationsManager(real_definitions_database, repositories_manager)
        self.mocked_operations_manager = OperationsManager(mocked_definitions_database, repositories_manager)

    def test_get_operation_info(self):
        data_type = 'EmailMessage'
        data_source = DataSource('Application', {'package_name': 'com.google.gm'})
        device_info = DeviceInfo('4.4.4', 'XT1053')

        op_info = self.mocked_operations_manager.get_operations_info(data_type, data_source, device_info)
        self.assertEqual(len(op_info), 1)

    def test_defined_data_type_but_not_used_in_any_operation(self):
        data_type = 'ImageFile'
        data_source = None
        device_info = DeviceInfo('4.4.4', 'XT1053')

        op_info = self.real_operations_manager.get_operations_info(data_type, None, device_info)
        self.assertEqual(op_info, [])

    def tearDown(self):
        os.remove(os.path.join('test', 'definitions.db'))


if __name__ == '__main__':
    unittest.main()
