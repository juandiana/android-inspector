# coding=utf-8

import subprocess
from model.operation import Extractor, OperationError


class ApplicationExtractor(Extractor):
    @staticmethod
    def __pull__(file_path, output_dir):
        cmd = 'adb pull ' + file_path
        p = subprocess.Popen(cmd.split(), cwd=output_dir, stderr=subprocess.PIPE)
        for line in p.stderr:
            print '\t[adb] {0}'.format(line),

    def execute(self, extracted_data_dir_path, param_values):
        app_package_name = param_values['package_name']

        try:
            cmd = 'adb shell pm path {0}'.format(app_package_name)
            p = subprocess.Popen(cmd.split(), stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            stdout, stderr = p.communicate()

            apk_path = stdout.replace('package:', '')
            data_path = '/data/data/{0}'.format(app_package_name)

            self.__pull__(apk_path, extracted_data_dir_path)
            self.__pull__(data_path, extracted_data_dir_path)
        except subprocess.CalledProcessError:
            raise OperationError('Extraction failed.')
