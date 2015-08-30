# coding=utf-8
import json
import os
import shutil
import tarfile
import tempfile
from components.repositories_manager import camel_case_to_underscore
from model import OperationError


class ExtensionsManager(object):
    def __init__(self, definitions_database_manager, repositories_manager):
        self.definitions_database_manager = definitions_database_manager
        self.repositories_manager = repositories_manager

    def add(self, ex_type, def_path):
        """
        :type ex_type: string
        :type def_path: string
        :rtype : bool
        """
        if not os.path.exists(def_path):
            raise OperationError('The definition module specified does not exist.')

        if not def_path.endswith('.tar'):
            raise OperationError('The definition module specified is not a .tar file.')

        unpacked_files = tempfile.mkdtemp()

        try:
            with tarfile.open(def_path) as tar:
                tar.extractall(path=unpacked_files)

            definitions_file_path = os.path.join(unpacked_files, 'definition')

            if not os.path.exists(definitions_file_path):
                raise OperationError('The definition module does not contain a definition file.')

            with open(definitions_file_path) as data_file:
                data = json.load(data_file)

            new_component_file_path, repository_name = check_component_name_and_path(ex_type, data, unpacked_files)

            if ex_type == 'data_type':
                self.definitions_database_manager.add_data_type(data['name'], data['cybox_object_name'])
            elif ex_type == 'data_source_type':
                self.definitions_database_manager.add_data_source_type(data['name'], data['extractor_name'],
                                                                       data['required_params'])
            elif ex_type == 'operation':
                self.definitions_database_manager.add_operation(data['name'], data['data_type'],
                                                                data['data_source_type'], data['inspector_name'],
                                                                data['data_source_param_values'], data['device_models'],
                                                                data['android_versions'])
            else:
                raise OperationError('Extension type not supported.')

            self.repositories_manager.add_file(repository_name, new_component_file_path)
        finally:
            shutil.rmtree(unpacked_files)

        return True

    def remove(self, ex_type, name):
        """
        :type ex_type: string
        :type name: string
        :rtype : bool
        """
        if ex_type == 'data_type':
            custom_cybox_object_name = self.definitions_database_manager.get_data_type_custom_cybox_object_name(name)
            self.definitions_database_manager.remove_data_type(name)
            self.repositories_manager.remove_file('custom_cybox_objects',
                                                  camel_case_to_underscore(custom_cybox_object_name) + '.py')
        elif ex_type == 'data_source_type':
            extractor_name = self.definitions_database_manager.get_data_source_type_extractor_name(name)
            self.definitions_database_manager.remove_data_source_type(name)
            self.repositories_manager.remove_file('extractors', camel_case_to_underscore(extractor_name) + '.py')
        elif ex_type == 'operation':
            inspector_name = self.definitions_database_manager.get_operation_inspector_name(name)
            self.definitions_database_manager.remove_operation(name)
            self.repositories_manager.remove_file('inspectors', camel_case_to_underscore(inspector_name) + '.py')
        else:
            raise OperationError('Extension type not supported.')

        return True


def check_component_name_and_path(ex_type, definition, unpacked_files_path):
    """
    Check if the component_name matches the .py file name.
    If they match, return the .py file_path and the repository_name. Else, raise OperationError exception.
    :type ex_type: string
    :type definition: string
    :type unpacked_files_path: string
    :rtype: (string, string)
    """
    if ex_type == 'data_type':
        component_name = 'cybox_object_name'
        repository_name = 'custom_cybox_objects'
    elif ex_type == 'data_source_type':
        component_name = 'extractor_name'
        repository_name = 'extractors'
    else:
        component_name = 'inspector_name'
        repository_name = 'inspectors'

    new_component_file_name = camel_case_to_underscore(definition[component_name]) + '.py'
    new_component_file_path = os.path.join(unpacked_files_path, new_component_file_name)

    if not os.path.exists(new_component_file_path):
        raise OperationError(
            "The {0} does not match with '{1}'.".format(component_name, new_component_file_name))

    return new_component_file_path, repository_name
