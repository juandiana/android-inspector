# coding=utf-8

from abc import abstractmethod, ABCMeta
from datetime import datetime
import os
import errno

from cybox.common import MeasureSource, ToolInformation, ToolInformationList, ToolType, Time
from cybox.core import Observables

EXTRACTED_DATA_DIR_NAME = 'extracted_data'
INSPECTED_DATA_FILE_NAME = 'inspected_data.xml'
SOURCE_DATA_FILE_NAME = 'source_data.xml'


class Extractor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, extracted_data_dir_path, param_values):
        """
        :type extracted_data_dir_path: string
        :type param_values: dict<string, string>
        :rtype : None
        """
        pass


class Inspector(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, device_info, extracted_data_dir_path, simple_output):
        """
        :type device_info: DeviceInfo
        :type extracted_data_dir_path: string
        :type simple_output: bool
        :rtype : (list(Object), list(FileObject))
        """
        pass


class OperationError(Exception):
    pass


class Operation(object):
    def __init__(self, extractor, inspector, param_values):
        """
        :type extractor: Extractor
        :type inspector: Inspector
        :type param_values: dict<string, string>
        """
        self.extractor = extractor
        self.inspector = inspector
        self.param_values = param_values

    def execute(self, device_info, data_dir_path, simple_output=False):
        """
        :type device_info: DeviceInfo
        :type data_dir_path: string
        :rtype : None
        """
        extracted_data_dir_path = os.path.join(data_dir_path, EXTRACTED_DATA_DIR_NAME)
        try:
            os.makedirs(extracted_data_dir_path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        try:
            self.extractor.execute(extracted_data_dir_path, self.param_values)
            inspected_objects, source_objects = self.inspector.execute(device_info, extracted_data_dir_path,
                                                                       simple_output)
        except OperationError as error:
            raise

        inspected_observables = Observables(inspected_objects)
        source_observables = Observables(source_objects)

        tool_info = ToolInformation()
        tool_info.name = 'Android Inspector'
        tool_info.version = '1.0'

        measure_source = MeasureSource()
        measure_source.tool_type = ToolType.TERM_DIGITAL_FORENSICS
        measure_source.tools = ToolInformationList([tool_info])
        measure_source.time = Time(produced_time=datetime.now().isoformat())

        inspected_observables.observable_package_source = measure_source
        source_observables.observable_package_source = measure_source

        inspected_xml = inspected_observables.to_xml(include_namespaces=not simple_output)
        source_xml = source_observables.to_xml(include_namespaces=not simple_output)

        with open(os.path.join(data_dir_path, INSPECTED_DATA_FILE_NAME), 'w') as file1:
            file1.write(inspected_xml)

        with open(os.path.join(data_dir_path, SOURCE_DATA_FILE_NAME), 'w') as file2:
            file2.write(source_xml)
