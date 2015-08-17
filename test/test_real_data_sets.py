# coding=utf-8
import os
import tempfile
from unittest import TestCase
from components.coordinator import Coordinator
from components.definitions_database_manager import DefinitionsDatabaseManager
from components.operations_manager import OperationsManager
from components.repositories_manager import RepositoriesManager
from model import DeviceInfo, EXTRACTED_DATA_DIR_NAME, INSPECTED_DATA_FILE_NAME, SOURCE_DATA_FILE_NAME


class TestRealDataSets(TestCase):
    def setUp(self):
        def_db_manager = DefinitionsDatabaseManager(os.path.join('test', 'definitions.db'),
                                                               'create_db.sql',
                                                               'insert_default_data_types.sql',
                                                               'insert_default_data_source_types.sql',
                                                               'insert_default_operations.sql')
        repositories_manager = RepositoriesManager('repositories')
        self.device_info = DeviceInfo('4.3', 'GT-i9300')
        self.data_dir_path = tempfile.mkdtemp()
        self.coordinator = Coordinator(OperationsManager(def_db_manager, repositories_manager))

    def test_sms_inspector(self):
        self.coordinator.execute_operations(['SmsMessageAOSPSms', 'ContactFacebook', 'ContactWhatsapp',
                                             'ContactAOSPAgenda'], self.device_info, self.data_dir_path)

        self.assertTrue(os.path.exists(os.path.join(self.data_dir_path, EXTRACTED_DATA_DIR_NAME)))
        self.assertTrue(os.path.exists(os.path.join(self.data_dir_path, INSPECTED_DATA_FILE_NAME)))
        self.assertTrue(os.path.exists(os.path.join(self.data_dir_path, SOURCE_DATA_FILE_NAME)))