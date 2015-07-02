# coding=utf-8

import subprocess
from model.operation import Extractor, OperationError


class ApplicationExtractor(Extractor):
    def execute(self, extracted_data_dir_path, param_values):
        command_name = "adb"
        command_arg1 = "pull"
        command_arg2 = "/data/data/{0}".format(param_values['package_name'])

        try:
            p = subprocess.Popen([command_name, command_arg1, command_arg2],
                                 cwd=extracted_data_dir_path, stderr=subprocess.PIPE)
            for line in p.stderr:
                print "[adb] {0}".format(line)
        except subprocess.CalledProcessError:
            raise OperationError('Extraction failed.')
