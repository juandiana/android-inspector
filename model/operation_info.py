# coding=utf-8

class DataSource(object):
    def __init__(self, type_, info):
        self.type_ = type_
        self.info = info

    def __repr__(self):
        return '{0}:{1}'.format(self.type_, self.info)


class OperationInfo(object):
    def __init__(self, id_, data_type, data_source, supported_device_models, supported_os_versions):
        self.id_ = id_
        self.data_type = data_type
        self.data_source = data_source
        self.supported_device_models = supported_device_models
        self.supported_os_versions = supported_os_versions

    def __repr__(self):
        return '{{\n' \
               '\tid: {0}\n' \
               '\tdata_type: {1}\n' \
               '\tdata_source: {2}\n' \
               '\tsupported_device_models: {3}\n' \
               '\tsupported_os_models: {4}\n' \
               '}}\n' \
            .format(self.id_, self.data_type, self.data_source, self.supported_device_models,
                    self.supported_os_versions)


class DeviceInfo(object):
    def __init__(self, os_version, device_model):
        self.os_version = os_version
        self.device_model = device_model
