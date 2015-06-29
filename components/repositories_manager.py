# coding=utf-8
from importlib import import_module
import re
import os
import shutil


def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class RepositoriesManager(object):
    def add_file(self, repo_name, file_path):
        """
        :type repo_name: string
        :type file_path: string
        :rtype : bool
        """

        file_name = os.path.basename(file_path)

        try:
            shutil.copyfile(file_path, os.path.join(os.getcwd(), 'repositories', file_name))
            return True
        except IOError:
            print 'The file ' + file_name + 'was not copied to the ' + repo_name + ' repository.'
            return False

    def remove_file(self, repo_name, file_name):
        """
        :type repo_name: string
        :type file_name: string
        :rtype : bool
        """

        try:
            os.remove(os.path.join(os.getcwd(), repo_name, file_name))
            return True
        except OSError:
            print 'The file ' + file_name + 'was not deleted from the ' + repo_name + ' repository.'
            return False

    def get_extractor(self, name):
        """
        :type name: string
        :type : Extractor
        """
        module_name = convert(name)
        module = import_module('repositories.extractors.' + module_name)
        return getattr(module, name)()

    def get_inspector(self, name):
        """
        :type name: string
        :rtype : Inspector
        """
        module_name = convert(name)
        module = import_module('repositories.inspectors.' + module_name)
        return getattr(module, name)()

    def get_custom_cybox_object(self, name):
        """
        :type name: string
        :rtype : ObjectProperties
        """
        module_name = convert(name)
        module = import_module('repositories.custom_cybox_objects.' + module_name)
        return getattr(module, name)()
