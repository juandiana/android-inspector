# coding=utf-8
import os
import subprocess
import shutil

import adb_wrapper
from model.operation import Extractor, OperationError


class ApplicationExtractor(Extractor):
    def __init__(self):
        self.device = adb_wrapper.get_device()

    def execute(self, extracted_data_dir_path, param_values):
        if os.path.exists(extracted_data_dir_path):
            shutil.rmtree(extracted_data_dir_path)
        os.mkdir(extracted_data_dir_path)

        app_package_name = param_values['package_name']

        try:
            output = self.device.shell(['pm', 'path', app_package_name])

            apk_path = self.obtain_apk_path_from_output(app_package_name, output)
            data_path = '/data/data/{0}'.format(app_package_name)

            print "Fetching '{}' file...".format(apk_path)
            self.device.pull(remote=apk_path, local=extracted_data_dir_path)

            print "Fetching '{}' directory...".format(data_path)
            self.device.pull(remote=data_path, local=extracted_data_dir_path)

            print 'Extraction finished.'
        except subprocess.CalledProcessError:
            raise OperationError('Extraction failed.')

    @staticmethod
    def obtain_apk_path_from_output(app_package_name, output):
        for line in output.splitlines():
            if line.__contains__('package:'):
                return line.replace('package:', '')

        raise OperationError("Extraction failed. Could not find the APK for package '{}'.".format(app_package_name))
