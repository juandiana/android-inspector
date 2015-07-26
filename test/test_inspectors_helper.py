# coding=utf-8
import unittest
from util import inspectors_helper


class TestInspectorsHelper(unittest.TestCase):
    def test_get_app_version_name(self):
        version_name = inspectors_helper.get_app_version_name('Facebook-16.apk')
        self.assertEqual('16.0.0.20.15', version_name)


if __name__ == '__main__':
    unittest.main()
