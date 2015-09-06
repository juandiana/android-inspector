# coding=utf-8

from model import Operation


class OperationsManager(object):
    def __init__(self, definitions_database, repositories_manager):
        """
        :type definitions_database: DefinitionsDatabase
        :type repositories_manager: RepositoriesManager
        """
        self.definitions_database = definitions_database
        self.repositories_manager = repositories_manager

    def get_operations_info(self, data_type, data_source, device_info):
        """
        :type data_type: DataType
        :type data_source: DataSource
        :type device_info: DeviceInfo
        :rtype: list[OperationInfo]
        """
        if device_info is None:
            raise ValueError("get_operations_info must always receive a DeviceInfo instance.")

        if data_type is not None and not self.definitions_database.exists_data_type(data_type):
            raise ValueError("'{0}' is not a defined DataType.".format(data_type))

        if data_source is not None and not self.definitions_database.exists_data_source_type(data_source.type_):
            raise ValueError("'{0}' of the specified DataSource is not a defined DataSourceType."
                             .format(data_source.type_))

        if data_source is not None and not self.definitions_database.has_all_required_param_values(data_source):
            raise ValueError("DataSource with type '{0}' must specify all its corresponding parameters."
                             .format(data_source.type_))

        return self.definitions_database.query_operations_info(data_type, data_source, device_info)

    def get_operation(self, name):
        """
        :type name: string
        :rtype: Operation
        """
        if not self.definitions_database.exists_operation(name):
            raise ValueError("'{0}' is not a defined Operation.".format(name))

        extractor_name, inspector_name, param_values = self.definitions_database.get_operation_exec_info(name)

        try:
            extractor = self.repositories_manager.get_extractor_instance(extractor_name)
        except (ImportError, AttributeError, TypeError):
            raise RuntimeError('Could not instantiate the operation\'s extractor class')

        try:
            inspector = self.repositories_manager.get_inspector_instance(inspector_name)
        except (ImportError, AttributeError, TypeError):
            raise RuntimeError('Could not instantiate the operation\'s inspector class')

        return Operation(extractor, inspector, param_values)
