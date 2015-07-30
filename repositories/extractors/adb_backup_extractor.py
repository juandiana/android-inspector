# coding=utf-8
import os
import shutil
import subprocess
import tarfile
from model import Extractor, OperationError


class AdbBackupExtractor(Extractor):
    @staticmethod
    def __adb_backup__(package_name):
        cmd = 'adb backup -apk ' + package_name
        p = subprocess.Popen(cmd.split(), stderr=subprocess.PIPE)
        for line in p.stderr:
            print '\t[adb] {0}'.format(line),

    @staticmethod
    def __unpack__(jar_path):
        cmd = 'java -jar ' + os.path.join(jar_path, 'abe.jar') + ' unpack backup.ab backup.tar'
        p = subprocess.Popen(cmd.split(), stderr=subprocess.PIPE)
        for line in p.stderr:
            print '\t[unpacking] {0}'.format(line),

    @staticmethod
    def __extract_tar__():
        tar_path = os.path.join("backup.tar")
        tar = tarfile.open(tar_path)
        tar.extractall()
        tar.close()

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

        # Delete apps directory and backups files
        shutil.rmtree('apps')
        os.remove('backup.tar')
        os.remove('backup.ab')

        # Rename extracted folders.
        if os.path.exists('db'):
            os.rename('db', 'databases')
        if os.path.exists('f'):
            os.rename('f', 'files')
        if os.path.exists('sp'):
            os.rename('sp', 'shared_prefs')

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

            os.chdir(owd)
        except subprocess.CalledProcessError:
            raise OperationError('Extraction failed.')
