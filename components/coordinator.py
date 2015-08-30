# coding=utf-8
from os import path
from datetime import datetime

from tabulate import tabulate

from model import OperationError


class CommandError(Exception):
    pass


class Coordinator(object):
    def __init__(self, operations_manager):
        """
        :type operations_manager: operations_manager.OperationsManager
        """
        self.operations_manager = operations_manager
        self.device_info = None

    def _get_device_info(self, device_info):
        if device_info is None and self.device_info is None:
            raise CommandError('The device information must be set or specified in order to execute this command.')
        device_info_to_use = device_info if (device_info is not None) else self.device_info
        return device_info_to_use

    def set_device_info(self, device_info):
        """
        :type device_info: DeviceInfo
        :rtype : None
        """
        self.device_info = device_info
        print "Device model '{0}' running Android version '{1}' was set as the current device information." \
            .format(device_info.device_model, device_info.os_version)

    def list_operations(self, data_type, data_source, device_info):
        """
        :type data_type: string
        :type data_source: DataSource
        :type device_info: DeviceInfo
        :rtype : None
        """
        device_info_to_use = self._get_device_info(device_info)

        op_infos = self.operations_manager.get_operations_info(data_type, data_source, device_info_to_use)
        table = []
        for op_info in op_infos:
            table.append(op_info.to_tuple())
        print tabulate(table, headers=["Name", "Data type", "Data Source", "Supported devices", "Supported Android OS"])

    def execute_operations(self, names, device_info, results_dir_path, simple_output=False):
        """
        :type names: list(string)
        :type device_info: DeviceInfo
        :type results_dir_path: string
        :type simple_output: bool
        :rtype : None
        """
        device_info_to_use = self._get_device_info(device_info)

        op_count = 0
        op_successful_count = 0
        for name in names:
            op_count += 1
            op = self.operations_manager.get_operation(name)
            data_dir_name = '{0}_{1}'.format(name, datetime.now().strftime("%Y%m%d_%H%M%S"))
            data_dir_path = path.join(results_dir_path, data_dir_name)
            print "\n[{0}/{1}] Executing '{2}': ".format(op_count, len(names), name)
            try:
                op.execute(device_info_to_use, data_dir_path, simple_output)
                print "COMPLETED. Data stored to '{0}'.".format(data_dir_path)
                op_successful_count += 1
            except OperationError as error:
                print "FAILED. Reason: '{0}'".format(error.message)

        print '\n{0} operation(s) completed successfully.'.format(op_successful_count)

        if op_successful_count < op_count:
            raise CommandError('At least one operation failed.')

    def add(self, ex_type, def_path):
        """
        :type ex_type: string
        :type def_path: string
        :rtype : None
        """
        pass
    # TODO: Catch ValueError y RuntimeError

    def remove(self, ex_type, name):
        """
        :type ex_type: string
        :type name: string
        :rtype : None
        """
        pass

