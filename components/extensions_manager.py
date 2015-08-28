# coding=utf-8
from importlib import import_module
import json
import os
import shutil
import tarfile
from components.repositories_manager import camel_case_to_underscore
from model import OperationError


def underscore_to_camel_case(name):
    return ''.join(x.capitalize() or '_' for x in name.split('_'))


class ExtensionsManager(object):
    def __init__(self, definitions_database_manager, repositories_manager):
        self.definitions_database_manager = definitions_database_manager
        self.repositories_manager = repositories_manager

    def add_data_type(self, def_path):
        """
        :type def_path: string
        :rtype : bool
        """
        if not os.path.exists(def_path):
            raise OperationError('The definition module specified does not exist.')

        if not def_path.endswith('.tar'):
            raise OperationError('The definition module specified is not a .tar file.')

        unpacked_files = 'temp_new_data_type'

        with tarfile.open(def_path) as tar:
            tar.extractall(path=unpacked_files)

        definitions_file_path = os.path.join(unpacked_files, 'definition')

        if not os.path.exists(definitions_file_path):
            shutil.rmtree(unpacked_files)
            raise OperationError('The definition module does not contain a definition file.')

        with open(definitions_file_path) as data_file:
            data = json.load(data_file)

        cybox_object_file_name = camel_case_to_underscore(data['cybox_object_name']) + '.py'
        cybox_object_file_path = os.path.join(unpacked_files, cybox_object_file_name)

        if not os.path.exists(cybox_object_file_path):
            shutil.rmtree(unpacked_files)
            raise OperationError('The cybox_object_name does not match with the CybOX object file name.')

        self.repositories_manager.add_file('custom_cybox_objects', os.path.join(unpacked_files, cybox_object_file_name))

        shutil.rmtree(unpacked_files)

        try:
            self.definitions_database_manager.add_data_type(data['name'], data['cybox_object_name'])
        except (ValueError, RuntimeError):
            self.repositories_manager.remove_file('custom_cybox_objects',
                                                  os.path.join(unpacked_files, cybox_object_file_name))
            raise

        return True

    def remove_data_type(self, name):
        """
        :type name: string
        :rtype : bool
        """
        pass

    def add_data_source_type(self, def_path):
        """
        :type def_path: string
        :rtype : bool
        """
        pass

    def remove_data_source_type(self, name):
        """
        :type name: string
        :rtype : bool
        """
        pass

    def add_operation(self, def_path):
        """
        :type def_path: string
        :rtype : bool
        """
        pass

    def remove_operation(self, name):
        """
        :type name: string
        :rtype : bool
        """
        pass
