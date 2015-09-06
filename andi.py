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
    intro = '\nAndroid Inspector v1.0'
    doc_header = 'Commands list'
    undoc_header = None
    ruler = '-'

    def __init__(self, input_parser, coordinator, simple_output):
        """
        :type input_parser: InputParser
        :type coordinator: Coordinator
        """
        Cmd.__init__(self)
        self.input_parser = input_parser
        self.coordinator = coordinator
        self.simple_output = simple_output

        if simple_output:
            self.intro += '\nNote: Simplified output for CybOX content is enabled.'

    def print_topics(self, header, cmds, cmdlen, maxcol):
        if header is not None:
            Cmd.print_topics(self, header, cmds, cmdlen, maxcol)

    def emptyline(self):
        pass

    def do_exit(self, arg_line):
        return True

    def help_exit(self):
        print 'Description: Finishes the interactive session.'

    do_EOF = do_exit

    def do_set_device_info(self, arg_line):
        try:
            di = self.input_parser.parse_set_device_info_args(arg_line)
            self.coordinator.set_device_info(di)
        except (ValueError, CommandError) as error:
            print error

    def help_set_device_info(self):
        print '\n'.join([
            'Description: Stores the device info to be used in the session.',
            'Usage: set_device_info model=<device_model> version=<android_version>',
            '',
            '\t- <device_model>    is a string representing a device model (e.g. XT1053).',
            '\t- <android_version> is a string representing an android version (e.g. 4.4.4).'
        ])

    def do_list(self, arg_line):
        try:
            data_type, data_source, device_info = self.input_parser.parse_list_args(arg_line)
            self.coordinator.list_operations(data_type, data_source, device_info)
        except (ValueError, CommandError) as error:
            print error

    def help_list(self):
        print '\n'.join([
            'Description: Lists available operations.',
            'Usage: list [--data_type <data_type>] [--source_type <data_source_type> [--source_params <param_values>]]'
            ' [--model <device_model>] [--version <android_version>]',
            '',
            '\t- <data_type>        is a string representing a data type name.',
            '\t- <data_source_type> is a string representing a data source type name.',
            '\t- <param_values>     is a comma separated string list of pairs param:value with the required params of'
            ' its corresponding data source type.',
            '\t- <device_model>     is a string representing a device model (e.g. XT1053).',
            '\t- <android_version>  is a string representing an android version (e.g. 4.4.4).'
        ])

    def do_execute(self, arg_line):
        try:
            ids, device_info, html_output = self.input_parser.parse_execute_args(arg_line)
            self.coordinator.execute_operations(ids, device_info, 'results', self.simple_output, html_output)
        except (ValueError, CommandError) as error:
            print error

    def help_execute(self):
        print '\n'.join([
            'Description: Executes a set of operations.',
            'Usage: execute --operations <operation_names> [--model <device_model>] [--version <android_version>]',
            '',
            '\t- <operation_names> is a whitespace separated string list representing the names of the operations to'
            ' execute.',
            '\t- <device_model>    is a string representing a device model (e.g. XT1053).',
            '\t- <android_version> is a string representing an android version (e.g. 4.4.4).'
        ])

    def do_add_ext(self, arg_line):
        try:
            ex_type, def_path = self.input_parser.parse_add_ext_args(arg_line)
            self.coordinator.add_ext(ex_type, def_path)
        except (ValueError, RuntimeError) as error:
            print error

    def help_add_ext(self):
        print '\n'.join([
            'Description: Adds an extension to the system.',
            'Usage: add_ext --type <extension_type> --path <def_path>',
            '',
            '\t- <extension_type> is either \'data_type\', \'data_source_type\' or \'operation\'.',
            '\t- <def_path>       is an absolute path to the .tar file definition.'
        ])

    def do_rm_ext(self, arg_line):
        try:
            ex_type, name = self.input_parser.parse_rm_ext_args(arg_line)
            self.coordinator.rm_ext(ex_type, name)
        except (ValueError, RuntimeError) as error:
            print error

    def help_rm_ext(self):
        print '\n'.join([
            'Description: Removes an extension from the system.',
            'Usage: rm_ext --type <extension_type> --name <extension_name>',
            '',
            '\t- <extension_type> is either \'data_type\', \'data_source_type\' or \'operation\'.',
            '\t- <extension_name> is the name of the extension to be removed.'
        ])


def main():
    simple_output = False
    if len(sys.argv) > 1 and sys.argv[1] == '--simple_output':
        simple_output = True
        sys.argv.remove(sys.argv[1])

    repositories_manager = RepositoriesManager('repositories')
    definitions_database = DefinitionsDatabaseManager('definitions.db',
                                                      'create_db.sql',
                                                      'insert_default_data_types.sql',
                                                      'insert_default_data_source_types.sql',
                                                      'insert_default_operations.sql')
    operations_manager = OperationsManager(definitions_database, repositories_manager)

    extensions_manager = ExtensionsManager(definitions_database, repositories_manager)

    input_parser = InputParser()
    coordinator = Coordinator(operations_manager, extensions_manager)

    if len(sys.argv) > 1:
        InteractiveCommandLine(input_parser, coordinator, simple_output).onecmd(' '.join(sys.argv[1:]))
    else:
        InteractiveCommandLine(input_parser, coordinator, simple_output).cmdloop()


if __name__ == '__main__':
    main()
