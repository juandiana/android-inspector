# coding=utf-8
import os
from twisted.trial import unittest
from components.definitions_database_manager import DefinitionsDatabaseManager
from components.extensions_manager import ExtensionsManager
from components.repositories_manager import RepositoriesManager
from model import OperationError


class TestOperation(unittest.TestCase):
    def setUp(self):
        self.def_db = DefinitionsDatabaseManager(os.path.join('test', 'test_definitions.db'),
                                                 'create_db.sql',
                                                 os.path.join('test', 'my_test_insert_default_data_types.sql'),
                                                 os.path.join('test', 'my_test_insert_default_data_source_types.sql'),
                                                 os.path.join('test', 'my_test_insert_default_operations.sql'))
        repositories_manager = RepositoriesManager(os.path.join('test', 'test_repositories'))
        self.extension_manager = ExtensionsManager(self.def_db, repositories_manager)

    # def tearDown(self):
    #     self.def_db.conn.close()
    #     os.remove(os.path.join('test', 'test_definitions.db'))

    def test_add_data_type(self):
        self.assertTrue(
            self.extension_manager.add_data_type(os.path.join('test', 'extension_files', 'valid_data_type.tar')))
        os.remove(os.path.join('test', 'test_repositories', 'custom_cybox_objects', 'nuevo_tipo_de_dato_object.py'))

    def test_non_existing_data_type(self):
        self.assertRaisesRegexp(OperationError, 'The definition module specified does not exist.',
                                self.extension_manager.add_data_type, 'non_existing_data_type')

    def test_with_no_tar_file(self):
        self.assertRaisesRegexp(OperationError, 'The definition module specified is not a .tar file.',
                                self.extension_manager.add_data_type,
                                os.path.join('test', 'extension_files', 'not_a_tar_file.txt'))

    def test_cybox_object_name_does_not_match(self):
        self.assertRaisesRegexp(OperationError, 'The cybox_object_name does not match with the CybOX object file name.',
                                self.extension_manager.add_data_type,
                                os.path.join('test', 'extension_files', 'name_does_not_match.tar'))

    def test_no_definition_file_inside_def_module(self):
        self.assertRaisesRegexp(OperationError, 'The definition module does not contain a definition file.',
                                self.extension_manager.add_data_type,
                                os.path.join('test', 'extension_files', 'without_definition_file.tar'))

    def test_remove_data_type(self):
        self.extension_manager.add_data_type(os.path.join('test', 'extension_files', 'remove_data_type.tar'))
        self.assertTrue(self.extension_manager.remove_data_type('RemoveDataType'))
