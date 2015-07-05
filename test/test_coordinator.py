# coding=utf-8
from datetime import datetime
import unittest
from components.coordinator import Coordinator
from components.definitions_database import DefinitionsDatabase
from components.operations_manager import OperationsManager
from components.repositories_manager import RepositoriesManager
from model import DeviceInfo


class MyTestCase(unittest.TestCase):
    def setUp(self):
        definitions_database = DefinitionsDatabase('definitions.db',
                                                   'create_db.sql',
                                                   'insert_default_operations.sql')
        repositories_manager = RepositoriesManager('repositories')
        operations_manager = OperationsManager(definitions_database, repositories_manager)
        self.coordinator = Coordinator(operations_manager)

    def test_use_case_batch_mode(self):
        ids = ['operation_1']
        device_info = DeviceInfo('5.1', 'XT1053')
        results_dir_path = 'results'
        self.coordinator.execute_operations(ids, device_info, results_dir_path)


if __name__ == '__main__':
    unittest.main()
