# coding=utf-8

class DefinitionsDatabase(object):
    def query_operations_info(self, data_type, data_source, device_info):
        pass

    def get_operation_exec_info(self, id_):
        pass

    def exists_data_type(self, data_type):
        pass

    def exists_data_source_type(self, data_source_type):
        pass

    def add_operation(self, id_, data_type_id, data_source_type_id, inspector_id, param_values, device_models, android_versions):
        pass

    def remove_operation(self, id_):
        pass

    def add_data_type(self, name, cybox_object_name):
        pass

    def remove_data_type(self, name):
        pass

    def add_data_source_type(self, id_, name, extractor_name):
        pass

    def remove_data_source_type(self, id_):
        pass

