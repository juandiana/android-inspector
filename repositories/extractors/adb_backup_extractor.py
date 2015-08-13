# coding=utf-8
import os
import shutil
import subprocess
import tarfile
import io
import tempfile
import zlib

from util import adb
from model import Extractor, OperationError


class AdbBackupExtractor(Extractor):
    @staticmethod
    def _unpack_ab(ab_path, output_dir_path):
        """
        Unpacks an android backup file to the current directory.

        :param ab_path: Path to the android backup file.
        """
        with open(ab_path, mode='rb') as f:
            # The android backup format consists of a 24-byte header, followed by the content compressed.
            header = f.read(24)
            magic, format_version, compression_flag, encryption_algorithm = header.splitlines()
            if magic != 'ANDROID BACKUP' or format_version != '1':
                raise RuntimeError('Invalid android backup file format')
            if encryption_algorithm != 'none':
                raise RuntimeError('Android backup file is encrypted')
            content = f.read()

        tar_bytestream = zlib.decompress(content)
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
            device = adb.get_device()

            print "Getting the android backup file for '{}'. Please press 'Back up my data' on the device..." \
                .format(app_package_name)
            device.backup(app_package_name, ab_path)

            print 'Unpacking the backup file...'
            self._unpack_ab(ab_path, tmp_dir_path)
            os.remove(ab_path)

            print 'Re-ordering the extracted data...'
            self._reorder_and_copy_data(app_package_name, tmp_dir_path, extracted_data_dir_path)
        except subprocess.CalledProcessError:
            raise OperationError('Extraction failed.')
        finally:
            shutil.rmtree(tmp_dir_path)
