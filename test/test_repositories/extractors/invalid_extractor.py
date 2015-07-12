# coding=utf-8
from model import Extractor


# Plugin class should have the same name as its module.
class NotTheSameAsModuleNameExtractor(Extractor):
    def execute(self, extracted_data_dir_path, param_values):
        pass
