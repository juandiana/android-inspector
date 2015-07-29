# coding=utf-8
import glob
import os
import shutil
import subprocess
from model import Extractor, OperationError


class AdbBackupExtractor(Extractor):
    @staticmethod
    def __adb_backup__(file_path, output_dir):
        cmd = '/home/nacho/Apps/adt-bundle-linux-x86_64-20131030/sdk/platform-tools/adb backup -apk ' + file_path
        p = subprocess.Popen(cmd.split(), cwd=output_dir, stderr=subprocess.PIPE)
        for line in p.stderr:
            print '\t[adb] {0}'.format(line),

    @staticmethod
    def __unpack__(jar_path, output_dir):
        cmd = 'java -jar ' + os.path.join(jar_path, 'abe.jar') + ' unpack backup.ab backup.tar'
        p = subprocess.Popen(cmd.split(), cwd=output_dir, stderr=subprocess.PIPE)
        for line in p.stderr:
            print '\t[unpacking] {0}'.format(line),

    @staticmethod
    def __extract_tar__(output_dir):
        cmd = 'tar -xvf backup.tar'
        p = subprocess.Popen(cmd.split(), cwd=output_dir, stderr=subprocess.PIPE)
        for line in p.stderr:
            print '\t[unpacking] {0}'.format(line),

    @staticmethod
    def __order_data__(package_name, output_dir):
        # Copy extracted files to root output_dir
        for extracted_file in os.listdir(os.path.join(output_dir, 'apps', package_name)):
            current = os.path.join(output_dir, 'apps', package_name, extracted_file)
            destination = os.path.join(output_dir, extracted_file)
            if os.path.isdir(current):
                shutil.copytree(current, destination)
            else:
                shutil.copy2(current, destination)

        # Delete apps directory and backups files
        shutil.rmtree(os.path.join(output_dir, 'apps'))
        os.remove(os.path.join(output_dir, 'backup.tar'))
        os.remove(os.path.join(output_dir, 'backup.ab'))

        # Rename extracted databases folder.
        os.rename(os.path.join(output_dir, 'db'), os.path.join(output_dir, 'databases'))

    def execute(self, extracted_data_dir_path, param_values):
        app_package_name = param_values['package_name']

        try:
            self.__adb_backup__(app_package_name, extracted_data_dir_path)

            jar_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
            self.__unpack__(jar_path, extracted_data_dir_path)

            self.__extract_tar__(extracted_data_dir_path)

            self.__order_data__(app_package_name, extracted_data_dir_path)

        except subprocess.CalledProcessError:
            raise OperationError('Extraction failed.')
