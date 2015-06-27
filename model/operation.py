# coding=utf-8

from abc import abstractmethod, ABCMeta
import os
import errno

INSPECTED_DATA_DIR_NAME = 'inspected_data'
EXTRACTED_DATA_DIR_NAME = 'extracted_data'


class InspectionResult(object):
    def __init__(self, success, inspected_objects=None, source_objects=None):
        self.success = success
        self.inspected_objects = inspected_objects
        self.source_objects = source_objects


class OperationResult(object):
    def __init__(self, success, data_dir_path, error_msg):
        self.success = success
        self.data_dir_path = data_dir_path
        self.error_msg = error_msg


class Extractor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, extracted_data_dir_path, param_values):
        """
        :param extracted_data_dir_path: string
        :param param_values: dict<string, string>
        :rtype : bool
        """
        pass


class Inspector(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, device_info, extracted_data_dir_path):
        """
        :param device_info: DeviceInfo
        :param extracted_data_dir_path: string
        :rtype : InspectionResult
        """
        pass


class Operation(object):
    def __init__(self, extractor, inspector, param_values):
        self.extractor = extractor
        self.inspector = inspector
        self.param_values = param_values

    def execute(self, device_info, data_dir_path):
        """
        :param device_info: DeviceInfo
        :param data_dir_path: string
        :rtype : OperationResult
        """
        extracted_data_dir_path = os.path.join(data_dir_path, EXTRACTED_DATA_DIR_NAME)
        inspected_data_dir_path = os.path.join(data_dir_path, INSPECTED_DATA_DIR_NAME)
        try:
            os.makedirs(extracted_data_dir_path)
            os.makedirs(inspected_data_dir_path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        extraction_succeeded = self.extractor.execute(extracted_data_dir_path, self.param_values)
        if not extraction_succeeded:
            return OperationResult(False, None, 'Extraction failed.')

        inspection_result = self.inspector.execute(device_info, extracted_data_dir_path)
        if not inspection_result.success:
            return OperationResult(False, None, 'Inspection failed.')

        # TODO: Write inspection_result.inspected_objects and inspection_result.source_objects to their dirs.
        # TODO: Deberiamos hacer esto aqui o en el operation manager?
        return OperationResult(True, data_dir_path, None)
