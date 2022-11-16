# coding=utf-8
import json
import os
import shutil
import tarfile
import tempfile
import re

from components.repositories_manager import camel_case_to_underscore


class ExtensionsManager(object):
    def __init__(self, definitions_database_manager, repositories_manager):
        self.definitions_database_manager = definitions_database_manager
        self.repositories_manager = repositories_manager

    def add(self, ex_type, def_path):
        """
        :param ex_type: string
        :param def_path: string
        :rtype: bool
        """
        if not os.path.exists(def_path):
            raise RuntimeError('The definition module specified does not exist.')

        if not def_path.endswith('.tar'):
            raise RuntimeError('The definition module specified is not a .tar file.')

        unpacked_files = tempfile.mkdtemp()

        try:
            with tarfile.open(def_path) as tar:
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner=numeric_owner) 
                    
                
                safe_extract(tar, path=unpacked_files)

            definitions_file_path = os.path.join(unpacked_files, 'definition')

            if not os.path.exists(definitions_file_path):
                raise RuntimeError('The definition module does not contain a definition file.')

            with open(definitions_file_path) as data_file:
                data = json.load(data_file)

            new_component_file_path, repository_name = check_component_name_and_path(ex_type, data, unpacked_files)

            if ex_type == 'data_type':
                self.definitions_database_manager.add_data_type(data['name'], data['cybox_object_name'])
            elif ex_type == 'data_source_type':
                self.definitions_database_manager.add_data_source_type(data['name'], data['extractor_name'],
                                                                       data['required_params'])
            elif ex_type == 'operation':
                os_versions = []
                for av in data['android_versions']:
                    av_split = re.search('(.*)-(.*)', av)
                    os_versions.append((av_split.group(1), av_split.group(2)))

                self.definitions_database_manager.add_operation(data['name'], data['data_type'],
                                                                data['data_source_type'], data['inspector_name'],
                                                                data['data_source_param_values'], data['device_models'],
                                                                os_versions)
            else:
                raise ValueError('Extension type not supported.')

            self.repositories_manager.add_file(repository_name, new_component_file_path)
        finally:
            shutil.rmtree(unpacked_files)

    def remove(self, ex_type, name):
        """
        :param ex_type: string
        :param name: string
        :rtype: bool
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
            raise ValueError('Extension type not supported.')


def check_component_name_and_path(ex_type, definition, unpacked_files_path):
    """
    Check if the component_name matches the .py file name.
    If they match, return the .py file_path and the repository_name. Else, raise OperationError exception.
    
    :param ex_type: string
    :param definition: string
    :param unpacked_files_path: string
    :rtype: (string, string)
    """
    if ex_type == 'data_type':
        component_name = "cybox_object_name"
        repository_name = "custom_cybox_objects"
    elif ex_type == 'data_source_type':
        component_name = "extractor_name"
        repository_name = "extractors"
    else:
        component_name = "inspector_name"
        repository_name = "inspectors"

    new_component_file_name = camel_case_to_underscore(definition[component_name]) + '.py'
    new_component_file_path = os.path.join(unpacked_files_path, new_component_file_name)

    if not os.path.exists(new_component_file_path):
        raise ValueError("The {0} does not match with '{1}'."
                         .format(component_name, new_component_file_name))

    return new_component_file_path, repository_name
