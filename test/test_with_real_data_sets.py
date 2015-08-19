# coding=utf-8
import os
import shutil
import tempfile
from unittest import TestCase

from components.coordinator import Coordinator
from components.definitions_database_manager import DefinitionsDatabaseManager
from components.operations_manager import OperationsManager
from components.repositories_manager import RepositoriesManager
from load_data_sets import load_data_set
from model import DeviceInfo, EXTRACTED_DATA_DIR_NAME, INSPECTED_DATA_FILE_NAME, SOURCE_DATA_FILE_NAME


class TestWithRealDataSets(TestCase):
    def setUp(self):
        def_db_manager = DefinitionsDatabaseManager(os.path.join('test', 'definitions.db'),
                                                    'create_db.sql',
                                                    'insert_default_data_types.sql',
                                                    'insert_default_data_source_types.sql',
                                                    'insert_default_operations.sql')
        repositories_manager = RepositoriesManager('repositories')
        self.coordinator = Coordinator(OperationsManager(def_db_manager, repositories_manager))
        self.results_dir_path = tempfile.mkdtemp()

    def test_sms_inspector(self):
        success = load_data_set('HTC_Evo_3D')
        self.assertTrue(success)

        operations = ['SmsMessageAOSPSms', 'ContactFacebook', 'ContactWhatsApp']  # TODO: Agregar 'ContactAOSPAgenda'
        device_info = DeviceInfo('4.3', 'GT-i9300')
        self.coordinator.execute_operations(operations, device_info, self.results_dir_path)

        for dir_name in os.listdir(self.results_dir_path):
            self.assertTrue(os.path.exists(os.path.join(self.results_dir_path, dir_name, EXTRACTED_DATA_DIR_NAME)))
            self.assertTrue(os.path.exists(os.path.join(self.results_dir_path, dir_name, INSPECTED_DATA_FILE_NAME)))
            self.assertTrue(os.path.exists(os.path.join(self.results_dir_path, dir_name, SOURCE_DATA_FILE_NAME)))

    def tearDown(self):
        shutil.rmtree(self.results_dir_path)
