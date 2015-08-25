# coding=utf-8
import argparse
import shlex
import re

from model import DeviceInfo, DataSource


class InputParser(object):
    android_version_pattern = re.compile("^[1-9]+\.[0-9]+(\.[0-9]+)?$")

    def parse_set_device_info_args(self, arg_line):
        """
        :type arg_line: string
        :rtype DeviceInfo
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('--version', '-v')
        parser.add_argument('--model', '-m')

        args = parser.parse_args(shlex.split(arg_line))

        if args.model is None:
            raise ValueError("The parameter 'model' is required.")

        if args.version is None:
            raise ValueError("The parameter 'version' is required.")

        if not self.android_version_pattern.match(args.version):
            raise ValueError('The Android version is not valid.')

        return DeviceInfo(args.version, args.model)

    def parse_list_args(self, arg_line):
        """
        :type arg_line: string
        :rtype string, DataSource, DeviceInfo
        """
        dt = None
        ds = None
        di = None

        parser = argparse.ArgumentParser()
        parser.add_argument('--type', '-t')
        parser.add_argument('--source_type', '-st')
        parser.add_argument('--source_params', '-sp', nargs='*')
        parser.add_argument('--version', '-v')
        parser.add_argument('--model', '-m')

        args = parser.parse_args(shlex.split(arg_line))

        if args.type:
            dt = args.type

        if args.source_type:
            ds = DataSource(args.source_type, {})

        if args.source_params:
            params = {}

            for p in args.source_params:
                if ':' not in p:
                    raise ValueError(
                        "The parameter 'source_params' is a whitespace separated list of pairs param_name:param_value.")

                p_split = re.search('(.*):(.*)', p)
                params[p_split.group(1)] = p_split.group(2)

            ds.info = params

        if args.model and args.version:
            if not self.android_version_pattern.match(args.version):
                raise ValueError('The Android version is not valid.')

            di = DeviceInfo(args.version, args.model)
            di.os_version = args.version

        return dt, ds, di

    def parse_execute_args(self, arg_line):
        """
        :type arg_line: string
        :rtype list(string), DeviceInfo
        """

        parser = argparse.ArgumentParser()
        parser.add_argument('--operations', '-op', nargs='+')
        parser.add_argument('--version', '-v')
        parser.add_argument('--model', '-m')

        args = parser.parse_args(shlex.split(arg_line))

        di = None

        if args.operations is None:
            raise ValueError("The parameter 'operations' is required.")

        ops = args.operations

        if args.version and not self.android_version_pattern.match(args.version):
            raise ValueError('The Android version is not valid.')

        if args.model and args.version:
            di = DeviceInfo(args.version, args.model)

        return ops, di