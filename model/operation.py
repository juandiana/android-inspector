# coding=utf-8

from abc import abstractmethod, ABCMeta
from datetime import datetime
import os
import errno

from cybox.common import MeasureSource, ToolInformation, ToolInformationList, ToolType, Time
from cybox.core import Observables
from cybox.utils import IDGenerator, set_id_method
import subprocess

EXTRACTED_DATA_DIR_NAME = 'extracted_data'
INSPECTED_DATA_FILE_NAME = 'inspected_data.xml'
SOURCE_DATA_FILE_NAME = 'source_data.xml'


def write_observables_xml_file(observables, file_path, simple_output):
    xml_data = observables.to_xml(include_namespaces=not simple_output)
    with open(file_path, mode='w') as _file:
        _file.write(xml_data)


def generate_html_files(data_dir_path):
    absolute_op_dir = os.path.join(os.getcwd(), data_dir_path)
    subprocess.call(['sh', 'stix-to-html.sh', '--indir', absolute_op_dir, '--outdir', absolute_op_dir],
                    cwd='stix-to-html', stdout=subprocess.PIPE)


class Extractor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, extracted_data_dir_path, param_values):
        """
        :param extracted_data_dir_path: string
        :param param_values: dict[string, string]

        """
        pass


class Inspector(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, device_info, extracted_data_dir_path):
        """
        :param device_info: DeviceInfo
        :param extracted_data_dir_path: string
        :rtype: (list[Object], list[FileObject])

        """
        pass


class OperationError(Exception):
    pass


class Operation(object):
    def __init__(self, extractor, inspector, param_values):
        """
        :param extractor: Extractor
        :param inspector: Inspector
        :param param_values: dict[string, string]

        """
        self.extractor = extractor
        self.inspector = inspector
        self.param_values = param_values

    def execute(self, device_info, data_dir_path, simple_output=False, html_output=False):
        """
        :param device_info: DeviceInfo
        :param data_dir_path: string

        """
        extracted_data_dir_path = os.path.join(data_dir_path, EXTRACTED_DATA_DIR_NAME)
        try:
            os.makedirs(extracted_data_dir_path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        self.extractor.execute(extracted_data_dir_path, self.param_values)

        set_id_method(IDGenerator.METHOD_INT if simple_output else IDGenerator.METHOD_UUID)

        inspected_objects, source_objects = self.inspector.execute(device_info, extracted_data_dir_path)
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

        write_observables_xml_file(inspected_observables,
                                   os.path.join(data_dir_path, INSPECTED_DATA_FILE_NAME),
                                   simple_output)
        write_observables_xml_file(source_observables,
                                   os.path.join(data_dir_path, SOURCE_DATA_FILE_NAME),
                                   simple_output)

        if html_output:
            generate_html_files(data_dir_path)
