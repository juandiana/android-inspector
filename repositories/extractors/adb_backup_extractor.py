# coding=utf-8
import os
import shutil
import subprocess
import tarfile
import io
import tempfile
import zlib
import time

from util import adb
from model import Extractor, OperationError


class AdbBackupExtractor(Extractor):
    @staticmethod
    def get_ab(ab_path, app_package_name):
        device = None
        try:
            device = adb.get_device()
        except:
            raise OperationError('No device or multiple devices were found connected.')

        if device is None:
            raise OperationError('Error while attempting to connect to the device.')

        # Wait 500ms to make sure the device is ready.
        time.sleep(0.5)
        device.backup(app_package_name, ab_path)

    @staticmethod
    def _unpack_ab(ab_path, output_dir_path):
        """
        Unpacks an android backup file to the current directory.

        :param ab_path: Path to the android backup file.
        """
        content = None
        is_compressed = False
        with open(ab_path, mode='rb') as f:
            # The android backup format consists of a 24-byte header, followed by the content compressed.
            header = f.read(24)
            magic, format_version, compression_flag, encryption_algorithm = header.splitlines()

            if magic != 'ANDROID BACKUP' or format_version != '1':
                raise RuntimeError('Invalid android backup file format')

            is_compressed = compression_flag == '1'

            if encryption_algorithm != 'none':
                raise RuntimeError('Android backup file is encrypted')

            content = f.read()

        if content is None:
            raise OperationError('Extraction failed. Could not unpack {}.'.format(ab_path))

        tar_bytestream = zlib.decompress(content) if is_compressed else content
        with tarfile.open(fileobj=io.BytesIO(tar_bytestream)) as tar:
            tar.extractall(path=output_dir_path)

    @staticmethod
    def _reorder_and_copy_data(app_package_name, source_path, dest_path):
        app_data_dir_path = os.path.join(source_path, 'apps', app_package_name)
        shutil.copytree(app_data_dir_path, dest_path)

        # Rename extracted folders.
        cwd = os.getcwd()
        os.chdir(dest_path)
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
        os.chdir(cwd)

    def execute(self, extracted_data_dir_path, param_values):
        app_package_name = param_values['package_name']
        tmp_dir_path = tempfile.mkdtemp()
        ab_path = os.path.join(tmp_dir_path, '{}_backup.ab'.format(app_package_name))

        if os.path.exists(extracted_data_dir_path):
            shutil.rmtree(extracted_data_dir_path)

        try:
            print "Getting the android backup file for '{}'...\n" \
                  "** Please press 'Back up my data' on the device to continue **" \
                .format(app_package_name)
            self.get_ab(ab_path, app_package_name)

            print 'Unpacking the backup file...'
            self._unpack_ab(ab_path, tmp_dir_path)
            os.remove(ab_path)

            print 'Re-ordering the extracted data...'
            self._reorder_and_copy_data(app_package_name, tmp_dir_path, extracted_data_dir_path)
        except subprocess.CalledProcessError:
            raise OperationError('Extraction failed.')
        finally:
            shutil.rmtree(tmp_dir_path)
