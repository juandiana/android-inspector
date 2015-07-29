# coding=utf-8
import os
import unittest
from repositories.extractors.adb_backup_extractor import AdbBackupExtractor


class TestAdbBackupExtractor(unittest.TestCase):
    def test_execute(self):
        extracted_data_dir = 'application_extractor_data'
        os.mkdir(extracted_data_dir)
        app_extractor = AdbBackupExtractor()
        app_extractor.execute(extracted_data_dir, {'package_name': 'com.android.email'})


if __name__ == '__main__':
    unittest.main()
