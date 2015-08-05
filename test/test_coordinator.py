# coding=utf-8
import os
import unittest

from components.coordinator import Coordinator
from components.definitions_database_manager import DefinitionsDatabaseManager
from components.operations_manager import OperationsManager
from components.repositories_manager import RepositoriesManager
from model import DeviceInfo


class MyTestCase(unittest.TestCase):
    def setUp(self):
        # TODO: Seguramente debamos borrar esta base de datos en el tearDown
        definitions_database = DefinitionsDatabaseManager(os.path.join('test', 'test_definitions.db'),
                                                          'create_db.sql',
                                                          'insert_default_operations.sql')
        repositories_manager = RepositoriesManager('repositories')
        operations_manager = OperationsManager(definitions_database, repositories_manager)
        self.coordinator = Coordinator(operations_manager)

    def test_use_case_batch_mode(self):
        ids = ['com.example:EmailMessageAOSPEmailApp']
        device_info = DeviceInfo('5.1', 'XT1053')
        results_dir_path = os.path.join('test', 'results')

        self.coordinator.execute_operations(ids, device_info, results_dir_path)


if __name__ == '__main__':
    unittest.main()
