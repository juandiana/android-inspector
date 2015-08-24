# coding=utf-8


class DataSource(object):
    def __init__(self, type_, info):
        self.type_ = type_
        self.info = info

    def __repr__(self):
        return '{0}:{1}'.format(self.type_, self.info)

    def __eq__(self, other):
        return self.type_ == other.type_ and self.info == other.info


class OperationInfo(object):
    def __init__(self, name, data_type, data_source, supported_device_models, supported_os_versions):
        self.name = name
        self.data_type = data_type
        self.data_source = data_source
        self.supported_device_models = supported_device_models
        self.supported_os_versions = supported_os_versions

    def __repr__(self):  # TODO: Remove this method?
        return '{{\n' \
               '\tname: {0}\n' \
               '\tdata_type: {1}\n' \
               '\tdata_source: {2}\n' \
               '\tsupported_device_models: {3}\n' \
               '\tsupported_os_models: {4}\n' \
               '}}\n' \
            .format(self.name, self.data_type, self.data_source, self.supported_device_models,
                    self.supported_os_versions)

    def __eq__(self, other):
        return self.name == other.name \
               and self.data_type == other.data_type \
               and self.data_source == other.data_source \
               and self.supported_device_models == other.supported_device_models \
               and self.supported_os_versions == other.supported_os_versions

    def to_tuple(self):
        return self.name, self.data_type, self.data_source, self.supported_device_models, self.supported_os_versions


class DeviceInfo(object):
    def __init__(self, os_version, device_model):
        self.os_version = os_version
        self.device_model = device_model
