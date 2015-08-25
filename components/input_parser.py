# coding=utf-8
import argparse
import shlex
import re

from model import DeviceInfo, DataSource


class InputParser(object):



    def parse_set_device_info_args(self, arg_line):
        """
        :type arg_line: string
        :rtype DeviceInfo
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('--version', help='specify the android version.')
        parser.add_argument('--model', help='specify the device model.')

        args = parser.parse_args(shlex.split(arg_line))
        return DeviceInfo(args.version, args.model)

    def parse_list_args(self, arg_line):
        """
        :type arg_line: string
        :rtype string, DataSource, DeviceInfo
        """
        dt = None
        ds = DataSource(None, None)
        di = DeviceInfo(None, None)

        parser = argparse.ArgumentParser()
        parser.add_argument('--type', help='specify the data type.')
        parser.add_argument('--source_type', help='specify the data source')
        parser.add_argument('--source_params', nargs='+', help='specify the data source')
        parser.add_argument('--version', help='specify the android version.')
        parser.add_argument('--model', help='specify the device model.')

        args = parser.parse_args(shlex.split(arg_line))

        if args.type:
            dt = args.type

        if args.source_type:
            ds.type_ = args.source_type

        if args.source_params:
            params = {}

            for p in args.source_params:
                p_split = re.search('(.*):(.*)', p)
                params[p_split.group(1)] = p_split.group(2)

            ds.info = params

        if args.model:
            di.device_model = args.model

        if args.version:
            di.os_version = args.version

        return dt, ds, di

    def parse_execute_args(self, arg_line):
        """
        :type arg_line: string
        :rtype list(string), DeviceInfo
        """

        parser = argparse.ArgumentParser()
        parser.add_argument('--ids', nargs='+', help='specify the operations by ids.')
        parser.add_argument('--version', nargs='*', help='specify the android version.')
        parser.add_argument('--model', nargs='*', help='specify the device model.')

        args = parser.parse_args(shlex.split(arg_line))

        ids = args.ids
        di = None

        if args.model and args.version:
            di = DeviceInfo(args.version, args.model)

        return ids, di
