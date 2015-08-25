# coding=utf-8
from cmd import Cmd

from components.coordinator import Coordinator
from components.definitions_database_manager import DefinitionsDatabaseManager
from components.input_parser import InputParser
from components.operations_manager import OperationsManager
from components.repositories_manager import RepositoriesManager
from model import OperationError


class InteractiveCommandLine(Cmd):
    def __init__(self, input_parser, coordinator):
        """
        :type input_parser: InputParser
        :type coordinator: Coordinator
        """
        Cmd.__init__(self)
        self.input_parser = input_parser
        self.coordinator = coordinator

    def do_set_device_info(self, arg_line):
        """
        Stores the device info to be used in the session.
        Usage: set_device_info version=<android_version> model=<device_model>

        where:
            <android_version>   is a string representing an android version (e.g. 4.4.4).
            <device_model>      is a string representing a device model (e.g. XT1053).
        """
        try:
            di = self.input_parser.parse_set_device_info_args(arg_line)
            self.coordinator.set_device_info(di)
        except ValueError as error:
            print error

    def do_list(self, arg_line):
        """s
        Lists available operations.
        Usage: list [--type <data_type>] [--source_type <data_source_type> [--source_params <param_values>]]
                    [--version <android_version>] [--model <device_model>]

        where:
            <data_type>         is a string representing a datatype name.
            <data_source_type>  is a string representing a data source type name.
            <param_values>      is a comma separated string list of pairs param:value with the required params of
                                its corresponding data source type.
            <android_version>   is a string representing an android version (e.g. 4.4.4).
            <device_model>      is a string representing a device model (e.g. XT1053).
        """
        try:
            data_type, data_source, device_info = self.input_parser.parse_list_args(arg_line)
            self.coordinator.list_operations(data_type, data_source, device_info)
        except ValueError as error:
            print error

    def do_execute(self, arg_line):
        """
        Executes a set of operations.
        Usage: execute --operations <operation_names> [--version <android_version>] [--model <device_model>]

        where:
            <operation_names>   is a whitespace separated string list representing the names of the operations to execute.
            <android_version>   is a string representing an android version (e.g. 4.4.4).
            <device_model>      is a string representing a device model (e.g. XT1053).
        """
        try:
            ids, device_info = self.input_parser.parse_execute_args(arg_line)
            self.coordinator.execute_operations(ids, device_info, results_dir_path='results')
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

    input_parser = InputParser()
    coordinator = Coordinator(operations_manager)

    InteractiveCommandLine(input_parser, coordinator).cmdloop('Android Inspector v1.0\n')


if __name__ == '__main__':
    main()
