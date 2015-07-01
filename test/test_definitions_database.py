# coding=utf-8
import unittest
from components.definitions_database import DefinitionsDatabase
from model import DataSource, DeviceInfo


class MyTestCase(unittest.TestCase):
    def test_something(self):
        db_helper = DefinitionsDatabase()
        ds = DataSource('Application', 'com.android.email')
        dv_info = DeviceInfo('3.0.0', 'GT-I9300')
        db_helper.query_operations_info('EmailMessage', ds, dv_info)


if __name__ == '__main__':
    unittest.main()
