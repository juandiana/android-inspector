# coding=utf-8
import os
import unittest

from util import inspectors_helper


class TestInspectorsHelper(unittest.TestCase):
    def test_get_app_version_name(self):
        version_name = inspectors_helper.get_app_version_name(os.path.join('test', 'com.google.android.gm-2.apk'))
        self.assertEqual('5.4.97372923.release', version_name)


if __name__ == '__main__':
    unittest.main()
