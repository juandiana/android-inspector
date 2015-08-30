# coding=utf-8
from importlib import import_module
import re
import os
import shutil

from model import Extractor, Inspector, OperationError


def camel_case_to_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def get_class_from_file(prefix, name, interface_class):
    module = import_module(prefix + camel_case_to_underscore(name))
    concrete_class = getattr(module, name)

    if not issubclass(concrete_class, interface_class):
        raise TypeError("'{0}' must implement the '{1}' interface."
                        .format(concrete_class.__name__, interface_class.__name__))

    return concrete_class


class RepositoriesManager(object):
    def __init__(self, repositories_dir_name):
        self.repositories_dir_name = repositories_dir_name

    def add_file(self, repo_name, file_path):
        """
        :type repo_name: string
        :type file_path: string
        :rtype : None
        """
        dest_path = os.path.join(self.repositories_dir_name, repo_name)
        file_name = os.path.basename(file_path)

        if os.path.exists(os.path.join(dest_path, file_name)):
            raise RuntimeError("The file '{0}' already exists on the repository '{1}'".format(file_name, repo_name))

        shutil.copy(file_path, dest_path)

    def remove_file(self, repo_name, file_name):
        """
        :type repo_name: string
        :type file_name: string
        :rtype : None
        """
        target_path = os.path.join(self.repositories_dir_name, repo_name, file_name)

        if not os.path.exists(target_path):
            return

        os.remove(target_path)

    def get_extractor_instance(self, name):
        """
        :type name: string
        :type : Extractor
        """
        extractor_class = get_class_from_file(self.repositories_dir_name + '.extractors.', name, Extractor)
        return extractor_class()

    def get_inspector_instance(self, name):
        """
        :type name: string
        :rtype : Inspector
        """
        inspector_class = get_class_from_file(self.repositories_dir_name + '.inspectors.', name, Inspector)
        return inspector_class()
