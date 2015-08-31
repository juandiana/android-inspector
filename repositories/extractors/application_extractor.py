# coding=utf-8
import os
import subprocess
import shutil
import time

from util import adb
from model.operation import Extractor, OperationError


class ApplicationExtractor(Extractor):
    def execute(self, extracted_data_dir_path, param_values):
        device = None
        try:
            device = adb.get_device()
        except:
            raise OperationError('No device or multiple devices were found connected.')

        if device is None:
            raise OperationError('Error while attempting to connect to the device.')

        # Wait 500ms to make sure the device is ready.
        time.sleep(0.5)

        if os.path.exists(extracted_data_dir_path):
            shutil.rmtree(extracted_data_dir_path)
        os.mkdir(extracted_data_dir_path)

        app_package_name = param_values['package_name']

        try:
            output = device.shell(['pm', 'path', app_package_name])

            apk_path = self.obtain_apk_path_from_output(app_package_name, output)
            data_path = '/data/data/{0}'.format(app_package_name)

            print "Fetching '{}' file...".format(apk_path)
            device.pull(remote=apk_path, local=extracted_data_dir_path)
        except subprocess.CalledProcessError:
            raise OperationError('Extraction error while attempting to fetch the APK.')

        try:
            print "Fetching '{}' directory...".format(data_path)
            device.pull(remote=data_path, local=extracted_data_dir_path)
        except subprocess.CalledProcessError:
            raise OperationError('Extraction error while attempting to fetch the data.')

    @staticmethod
    def obtain_apk_path_from_output(app_package_name, output):
        for line in output.splitlines():
            if 'package:' in line:
                return line.replace('package:', '')

        raise OperationError('Extraction failed. Could not find the APK for package "{}".'.format(app_package_name))
