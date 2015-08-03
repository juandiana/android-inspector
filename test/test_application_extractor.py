# coding=utf-8
import os
import unittest
import shutil

from model import OperationError
from repositories.extractors.adb_backup_extractor import AdbBackupExtractor
from repositories.extractors.application_extractor import ApplicationExtractor


class TestApplicationExtractor(unittest.TestCase):
    def setUp(self):
        self.extracted_data_dir = 'application_extractor_data'
        if os.path.exists(self.extracted_data_dir):
            shutil.rmtree(self.extracted_data_dir)
        os.mkdir(self.extracted_data_dir)

    def test_default_application_extractor(self):
        ApplicationExtractor().execute(self.extracted_data_dir, {'package_name': 'com.google.android.gm'})

    def test_alternative_application_extractor(self):
        AdbBackupExtractor().execute(self.extracted_data_dir, {'package_name': 'com.android.email'})

    def test_non_existent_app_package(self):
        self.assertRaises(OperationError,
                          ApplicationExtractor().execute, self.extracted_data_dir,
                          {'package_name': 'non.existent.package'})


if __name__ == '__main__':
    unittest.main()
