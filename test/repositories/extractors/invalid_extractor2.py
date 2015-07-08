# coding=utf-8
from model import Extractor


# Extractor should inherit from interface Extractor.
class InvalidExtractor2(object):
    def execute(self, extracted_data_dir_path, param_values):
        pass
