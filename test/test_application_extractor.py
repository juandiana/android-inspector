# coding=utf-8
import os
import unittest
from repositories.extractors.application_extractor import ApplicationExtractor


class TestApplicationExtractor(unittest.TestCase):
    def test_execute(self):
        extracted_data_dir = 'application_extractor_data'
        os.mkdir(extracted_data_dir)
        app_extractor = ApplicationExtractor()
        app_extractor.execute(extracted_data_dir, {'package_name': 'com.google.android.gm'})


if __name__ == '__main__':
    unittest.main()
