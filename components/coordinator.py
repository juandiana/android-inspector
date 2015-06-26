# coding=utf-8

class Coordinator(object):
    def set_device_info(self, device_info):
        """
        :param device_info: DeviceInfo
        :rtype : None
        """
        pass

    def list_operations(self, data_type, data_source, device_info):
        """
        :param data_type: string
        :param data_source: DataSource
        :param device_info: DeviceInfo
        :rtype : None
        """
        pass

    def execute_operations(self, ids, device_info):
        """
        :param ids: list(UUID)
        :param device_info: DeviceInfo
        :rtype : None
        """
        pass

    def add_data_type(self, def_path):
        """
        :param def_path: string
        :rtype : None
        """
        pass

    def remove_data_type(self, id_):
        """
        :param id_: UUID
        :rtype : None
        """
        pass

    def add_data_source_type(self, def_path):
        """
        :param def_path: string
        :rtype : None
        """
        pass

    def remove_data_source_type(self, id_):
        """
        :param id_: UUID
        :rtype : None
        """
        pass

    def add_operation(self, def_path):
        """
        :param def_path: string
        :rtype : None
        """
        pass

    def remove_operation(self, id_):
        """
        :param id_: UUID
        :rtype : None
        """
        pass