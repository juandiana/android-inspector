# coding=utf-8
import os
import shutil
import subprocess
import tarfile

import adb_wrapper
from model import Extractor, OperationError


class AdbBackupExtractor(Extractor):
    @staticmethod
    def __adb_backup__(package_name):
        print 'Please press "Back up my data" on the device.'
        device = adb_wrapper.get_device()
        print device.backup(package_name)

    @staticmethod
    def __unpack__(jar_path):
        # TODO: Unpack using deflater. http://stackoverflow.com/a/29055723
        print 'Unpacking backup...'
        cmd = 'java -jar ' + os.path.join(jar_path, 'abe.jar') + ' unpack backup.ab backup.tar'
        p = subprocess.Popen(cmd.split(), stderr=subprocess.PIPE)
        for line in p.stderr:
            print '\t[unpacking] {0}'.format(line),
        os.remove('backup.ab')

    @staticmethod
    def __extract_tar__():
        print 'Untaring file...'
        tar_path = os.path.join('backup.tar')
        tar = tarfile.open(tar_path)
        tar.extractall()
        tar.close()
        os.remove('backup.tar')

    @staticmethod
    def __order_data__(package_name):
        app_data_dir_path = os.path.join('apps', package_name)
        # Copy extracted files to root output_dir
        for current_node in os.listdir(app_data_dir_path):
            current = os.path.join(app_data_dir_path, current_node)
            destination = os.path.join(os.getcwd(), current_node)
            if os.path.isdir(current):
                shutil.copytree(current, destination)
            else:
                shutil.copy2(current, destination)

        # Delete apps directory
        shutil.rmtree('apps')

        # Rename extracted folders.
        if os.path.exists('db'):
            os.rename('db', 'databases')
        if os.path.exists('f'):
            os.rename('f', 'files')
        if os.path.exists('sp'):
            os.rename('sp', 'shared_prefs')
        if os.path.exists('a'):
            for _file in os.listdir('a'):
                shutil.move(os.path.join('a', _file), '.')
            os.rmdir('a')

    def execute(self, extracted_data_dir_path, param_values):
        app_package_name = param_values['package_name']
        jar_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

        owd = os.getcwd()
        os.chdir(extracted_data_dir_path)

        try:
            self.__adb_backup__(app_package_name)
            self.__unpack__(jar_path)
            self.__extract_tar__()
            self.__order_data__(app_package_name)
        except subprocess.CalledProcessError:
            raise OperationError('Extraction failed.')

        os.chdir(owd)
