# coding=utf-8


def to_string_list_repr(elements):
    return u'[' + u', '.join(unicode(x) for x in elements) + u']'


def android_versions_repr(versions):
    os_versions = []

    for v in versions:
        if v[0] == v[1]:
            os_versions.append(v[0])
        else:
            os_versions.append(v[0] + '-' + v[1])

    return '[' + ', '.join(os_versions) + ']'


class DataSource(object):
    def __init__(self, type_, info):
        self.type_ = type_
        self.info = info

    def __eq__(self, other):
        return self.type_ == other.type_ and self.info == other.info

    def __str__(self):
        params = []
        for p in self.info:
            params.append(p + ':' + self.info[p])

        return self.type_ + '{' + ', '.join(params) + '}'


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
        return self.name, self.data_type, self.data_source, \
            to_string_list_repr(self.supported_device_models), android_versions_repr(self.supported_os_versions)


class DeviceInfo(object):
    def __init__(self, os_version, device_model):
        self.os_version = os_version
        self.device_model = device_model
