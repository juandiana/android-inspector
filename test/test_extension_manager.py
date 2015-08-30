# coding=utf-8
import os
from twisted.trial import unittest
from components.definitions_database_manager import DefinitionsDatabaseManager
from components.extensions_manager import ExtensionsManager
from components.repositories_manager import RepositoriesManager
from model import OperationError
from nose_parameterized import parameterized


class TestExtensionsManager(unittest.TestCase):
    DB_FILE_PATH = os.path.join('test', 'test_definitions.db')
    DB_REPOSITORIES_PATH = os.path.join('test', 'test_repositories')
    DB_CREATION_SCRIPT_PATH = 'create_db.sql'
    DEFAULT_DATA_TYPES_SCRIPT_PATH = os.path.join('test', 'insert_test_default_data_types.sql')
    DEFAULT_DATA_SOURCE_TYPES_SCRIPT_PATH = os.path.join('test', 'insert_test_default_data_source_types.sql')
    DEFAULT_OPERATIONS_SCRIPT_PATH = os.path.join('test', 'insert_test_default_operations.sql')

    @classmethod
    def setUpClass(cls):
        cls.def_db = DefinitionsDatabaseManager(cls.DB_FILE_PATH,
                                                cls.DB_CREATION_SCRIPT_PATH,
                                                cls.DEFAULT_DATA_TYPES_SCRIPT_PATH,
                                                cls.DEFAULT_DATA_SOURCE_TYPES_SCRIPT_PATH,
                                                cls.DEFAULT_OPERATIONS_SCRIPT_PATH)

        repositories_manager = RepositoriesManager(cls.DB_REPOSITORIES_PATH)
        cls.extension_manager = ExtensionsManager(cls.def_db, repositories_manager)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.DB_FILE_PATH)

    @parameterized.expand([
        ('data_type', 'valid_data_type.tar'),
        ('data_source_type', 'valid_data_source_type.tar'),
        ('operation', 'valid_operation.tar')
    ])
    def test_add(self, ex_type, def_name):
        self.assertTrue(self.extension_manager.add(ex_type, os.path.join('test', 'extension_files', def_name)))

    @parameterized.expand([
        ('operation', 'NuevaOperation'),
        ('data_type', 'NuevoTipoDeDato'),
        ('data_source_type', 'NuevoDataSourceType')
    ])
    def test_remove(self, ex_type, component_name):
        self.assertTrue(self.extension_manager.remove(ex_type, component_name))

    def test_add_non_existing_tar(self):
        self.assertRaisesRegexp(OperationError, 'The definition module specified does not exist.',
                                self.extension_manager.add, 'data_type', 'non_existing_data_type.tar')

    def test_add_with_no_tar_file(self):
        self.assertRaisesRegexp(OperationError, 'The definition module specified is not a .tar file.',
                                self.extension_manager.add, 'data_type',
                                os.path.join('test', 'extension_files', 'not_a_tar_file.txt'))

    def test_add_component_name_does_not_match(self):
        self.assertRaisesRegexp(OperationError,
                                "The {0} does not match with '{1}'.".format('cybox_object_name', 'no_match_name.py'),
                                self.extension_manager.add, 'data_type',
                                os.path.join('test', 'extension_files', 'name_does_not_match.tar'))

    def test_add_no_definition_file_inside_def_module(self):
        self.assertRaisesRegexp(OperationError, 'The definition module does not contain a definition file.',
                                self.extension_manager.add, 'data_type',
                                os.path.join('test', 'extension_files', 'without_definition_file.tar'))

    def test_added_file_already_exists_in_repo(self):
        self.assertRaisesRegexp(OperationError,
                                "The file 'valid_extractor.py' already exists on the repository 'extractors'",
                                self.extension_manager.add, 'data_source_type',
                                os.path.join('test', 'extension_files', 'already_exists_in_repo.tar'))
