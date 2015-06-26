# coding=utf-8

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
        pass

    def get_inspector(self, name):
        """
        :param name: string
        :rtype : Inspector
        """
        pass

    def get_custom_cybox_object(self, name):
        """
        :param name: string
        :rtype : ObjectProperties
        """
        pass
