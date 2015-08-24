# coding=utf-8

from model import DeviceInfo


class InputParser(object):
    def parse_set_device_info_args(self, arg_line):
        """
        :type arg_line: string
        :rtype DeviceInfo
        """
        return DeviceInfo('4.0', 'XT1053')

    def parse_list_args(self, arg_line):
        """
        :type arg_line: string
        :rtype string, DataSource, DeviceInfo
        """
        return 'EmailMessage', None, DeviceInfo('4.0', 'XT1053')

    def parse_execute_args(self, arg_line):
        """
        :type arg_line: string
        :rtype list(string), DeviceInfo
        """
        return [], DeviceInfo('4.0', 'XT1053')
