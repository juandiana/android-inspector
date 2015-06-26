# coding=utf-8
from importlib import import_module
import re


def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

class RepositoriesManager(object):
    def add_file(self, repo_name, file_path):
        """
        :param repo_name: string
        :param file_path: string
        :rtype : bool
        """
        pass

    def remove_file(self, repo_name, file_name):
        """
        :param repo_name: string
        :param file_name: string
        :rtype : bool
        """
        pass

    def get_extractor(self, name):
        """
        :param name: string
        :rtype : Extractor
        """
        module_name = convert(name)
        module = import_module('repositories.extractors.' + module_name)
        return getattr(module, name)()

    def get_inspector(self, name):
        """
        :param name: string
        :rtype : Inspector
        """
        module_name = convert(name)
        module = import_module('repositories.inspectors.' + module_name)
        return getattr(module, name)()

    def get_custom_cybox_object(self, name):
        """
        :param name: string
        :rtype : ObjectProperties
        """
        module_name = convert(name)
        module = import_module('repositories.custom_cybox_objects.' + module_name)
        return getattr(module, name)()
