# coding=utf-8
from os import path
from datetime import datetime

from model import OperationError
from operations_manager import OperationsManager


class Coordinator(object):
    def __init__(self, operations_manager):
        """
        :type operations_manager: OperationsManager
        """
        self.operations_manager = operations_manager
        self.device_info = None

    def set_device_info(self, device_info):
        """
        :type device_info: DeviceInfo
        :rtype : None
        """
        self.device_info = device_info

    def list_operations(self, data_type, data_source, device_info):
        """
        :type data_type: string
        :type data_source: DataSource
        :type device_info: DeviceInfo
        :rtype : None
        """
        device_info_to_use = device_info if (device_info is None) else self.device_info
        return self.operations_manager.get_operations_info(data_type, data_source, device_info_to_use)

    def execute_operations(self, ids, device_info, results_dir_path):
        """
        :type ids: list(UUID)
        :type device_info: DeviceInfo
        :type results_dir_path: string
        :rtype : None
        """
        if device_info is None and self.device_info is None:
            print "No device information set."
            return

        device_info_to_use = device_info if (device_info is None) else self.device_info

        op_count = 0
        op_successful_count = 0
        for id_ in ids:
            op_count += 1
            op = self.operations_manager.get_operation(id_)
            data_dir_name = datetime.now().strftime("%Y%m%d_%H%M%S")
            data_dir_path = path.join(results_dir_path, data_dir_name)
            print "[{0}/{1}] Executing... ".format(op_count, len(ids))
            try:
                op.execute(device_info_to_use, data_dir_path)
                op_successful_count += 1
            except OperationError as error:
                print "Failed. Reason: {0}".format(error.message)
            print "Completed. Data stored to {0}".format(data_dir_path)

        if op_successful_count < op_count:
            # TODO: Debemos atrapar esto en la parte de UI.
            raise RuntimeError

    def add_data_type(self, def_path):
        """
        :type def_path: string
        :rtype : None
        """
        pass

    def remove_data_type(self, id_):
        """
        :type id_: UUID
        :rtype : None
        """
        pass

    def add_data_source_type(self, def_path):
        """
        :type def_path: string
        :rtype : None
        """
        pass

    def remove_data_source_type(self, id_):
        """
        :type id_: UUID
        :rtype : None
        """
        pass

    def add_operation(self, def_path):
        """
        :type def_path: string
        :rtype : None
        """
        pass

    def remove_operation(self, id_):
        """
        :type id_: UUID
        :rtype : None
        """
        pass
