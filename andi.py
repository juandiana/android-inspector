#!/usr/bin/env python
# coding=utf-8
from cmd import Cmd
import sys

from components.coordinator import Coordinator, CommandError
from components.definitions_database_manager import DefinitionsDatabaseManager
from components.extensions_manager import ExtensionsManager
from components.input_parser import InputParser
from components.operations_manager import OperationsManager
from components.repositories_manager import RepositoriesManager


class InteractiveCommandLine(Cmd):
    prompt = '(Andi) '
    intro = 'Android Inspector v1.0\n'
    doc_header = 'Commands list'
    ruler = '-'

    def __init__(self, input_parser, coordinator):
        """
        :type input_parser: InputParser
        :type coordinator: Coordinator
        """
        Cmd.__init__(self)
        self.input_parser = input_parser
        self.coordinator = coordinator

    def do_EOF(self, arg_line):
        """
        Exits the program cleanly.
        """
        return True

    def do_exit(self, arg_line):
        """
        Exits the program cleanly.
        """
        return True

    def do_set_device_info(self, arg_line):
        """
        Stores the device info to be used in the session.
        Usage: set_device_info model=<device_model> version=<android_version>

        where:
            <device_model>      is a string representing a device model (e.g. XT1053).
            <android_version>   is a string representing an android version (e.g. 4.4.4).
        """
        try:
            di = self.input_parser.parse_set_device_info_args(arg_line)
            self.coordinator.set_device_info(di)
        except (ValueError, CommandError) as error:
            print error

    def do_list(self, arg_line):
        """
        Lists available operations.
        Usage: list [--data_type <data_type>] [--source_type <data_source_type> [--source_params <param_values>]]
                    [--model <device_model>] [--version <android_version>]
        where:
            <data_type>         is a string representing a data type name.
            <data_source_type>  is a string representing a data source type name.
            <param_values>      is a comma separated string list of pairs param:value with the required params of
                                its corresponding data source type.
            <device_model>      is a string representing a device model (e.g. XT1053).
            <android_version>   is a string representing an android version (e.g. 4.4.4).
        """
        try:
            data_type, data_source, device_info = self.input_parser.parse_list_args(arg_line)
            self.coordinator.list_operations(data_type, data_source, device_info)
        except (ValueError, CommandError) as error:
            print error

    def do_execute(self, arg_line):
        """
        Executes a set of operations.
        Usage: execute --operations <operation_names> [--model <device_model>] [--version <android_version>]

        where:
            <operation_names>   is a whitespace separated string list representing the names of the operations to execute.
            <device_model>      is a string representing a device model (e.g. XT1053).
            <android_version>   is a string representing an android version (e.g. 4.4.4).
        """
        try:
            ids, device_info = self.input_parser.parse_execute_args(arg_line)
            self.coordinator.execute_operations(ids, device_info, results_dir_path='results')
        except (ValueError, CommandError) as error:
            print error

    def do_add_ext(self, arg_line):
        """
        Adds a data_type, data_source_type or operation.
        Usage: add_ext --type <data_type|data_source_type|operation> --path <def_path>

        where:
            <def_path>      is an absolute path to the .tar file definition.
        """
        try:
            ex_type, def_path = self.input_parser.parse_add_ext_args(arg_line)
            self.coordinator.add_ext(ex_type, def_path)
        except (ValueError, RuntimeError) as error:
            print error

    def do_rm_ext(self, arg_line):
        """
        Removes a data_type, data_source_type or operation.
        Usage: rm_ext --type <data_type|data_source_type|operation> --name <component_name>

        where:
            <component_name>    is the name of the extension to be removed.
        """
        try:
            ex_type, name = self.input_parser.parse_rm_ext_args(arg_line)
            self.coordinator.rm_ext(ex_type, name)
        except (ValueError, RuntimeError) as error:
            print error


def main():
    repositories_manager = RepositoriesManager('repositories')
    definitions_database = DefinitionsDatabaseManager('definitions.db',
                                                      'create_db.sql',
                                                      'insert_default_data_types.sql',
                                                      'insert_default_data_source_types.sql',
                                                      'insert_default_operations.sql')
    operations_manager = OperationsManager(definitions_database, repositories_manager)

    extensions_manager = ExtensionsManager(definitions_database,repositories_manager)

    input_parser = InputParser()
    coordinator = Coordinator(operations_manager, extensions_manager)

    if len(sys.argv) > 1:
        InteractiveCommandLine(input_parser, coordinator).onecmd(' '.join(sys.argv[1:]))
    else:
        InteractiveCommandLine(input_parser, coordinator).cmdloop()


if __name__ == '__main__':
    main()
