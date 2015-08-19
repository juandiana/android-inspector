# coding=utf-8
from os import path
from datetime import datetime

from model import OperationError


class Coordinator(object):
    def __init__(self, operations_manager):
        """
        :type operations_manager: operations_manager.OperationsManager
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

    def execute_operations(self, names, device_info, results_dir_path):
        """
        :type names: list(string)
        :type device_info: DeviceInfo
        :type results_dir_path: string
        :rtype : None
        """
        if device_info is None and self.device_info is None:
            print 'No device information set.'
            return

        device_info_to_use = device_info if (device_info is None) else self.device_info

        op_count = 0
        op_successful_count = 0
        for name in names:
            op_count += 1
            op = self.operations_manager.get_operation(name)
            data_dir_name = '{0}_{1}'.format(name, datetime.now().strftime("%Y%m%d_%H%M%S"))
            data_dir_path = path.join(results_dir_path, data_dir_name)
            print "\n[{0}/{1}] Executing '{2}': ".format(op_count, len(names), name)
            try:
                op.execute(device_info_to_use, data_dir_path)
                print "COMPLETED. Data stored to '{0}'.".format(data_dir_path)
                op_successful_count += 1
            except OperationError as error:
                print "FAILED. Reason: '{0}'".format(error.message)

        print '\n{0} operation(s) completed successfully.'.format(op_successful_count)

        if op_successful_count < op_count:
            # TODO: Debemos atrapar esto en la parte de UI.
            raise RuntimeError('At least one operation failed.')

    def add_data_type(self, def_path):
        """
        :type def_path: string
        :rtype : None
        """
        pass

    def remove_data_type(self, name):
        """
        :type name: string
        :rtype : None
        """
        pass

    def add_data_source_type(self, def_path):
        """
        :type def_path: string
        :rtype : None
        """
        pass

    def remove_data_source_type(self, name):
        """
        :type name: string
        :rtype : None
        """
        pass

    def add_operation(self, def_path):
        """
        :type def_path: string
        :rtype : None
        """
        pass

    def remove_operation(self, name):
        """
        :type name: string
        :rtype : None
        """
        pass
