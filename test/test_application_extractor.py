# coding=utf-8
import os
import unittest
import shutil

from model import OperationError
from repositories.extractors.adb_backup_extractor import AdbBackupExtractor
from repositories.extractors.application_extractor import ApplicationExtractor


class TestApplicationExtractor(unittest.TestCase):
    def setUp(self):
        self.output_path = os.path.join('test', 'application_extractor_data')
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path)
        os.mkdir(self.output_path)

    def test_default_application_extractor(self):
        app_package_name = 'com.google.android.gm'
        ApplicationExtractor().execute(os.path.join(self.output_path, app_package_name),
                                       {'package_name': app_package_name})

    def test_alternative_application_extractor(self):
        app_package_name = 'com.android.email'
        AdbBackupExtractor().execute(os.path.join(self.output_path, app_package_name),
                                     {'package_name': app_package_name})

    def test_non_existent_app_package(self):
        app_package_name = 'non.existent.package.name'
        self.assertRaises(OperationError,
                          ApplicationExtractor().execute, self.output_path,
                          {'package_name': app_package_name})

    def tearDown(self):
        shutil.rmtree(self.output_path)

if __name__ == '__main__':
    unittest.main()
