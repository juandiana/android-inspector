# coding=utf-8
import unittest
from components.definitions_database import DefinitionsDatabase
from model import DataSource, DeviceInfo, OperationInfo


class MyTestCase(unittest.TestCase):
    def test_something(self):
        db_helper = DefinitionsDatabase('test_definitions.db',
                                        'my_test_create_db.sql',
                                        'my_test_insert_default_operations.sql')
        ds_aosp_email = DataSource('Application', {'package_name': 'com.android.email'})
        ds_facebook = DataSource('Application', {'package_name': 'com.facebook.katana'})
        bad_ds = DataSource('Application', {})
        dv_info = DeviceInfo('3.0.0', 'GT-I9300')

        item1 = db_helper.query_operations_info('EmailMessage', ds_aosp_email, dv_info)
        item2 = [OperationInfo('com.example:EmailMessageAOSPEmailApp', 'EmailMessage', ds_aosp_email, 'GT-I9300',
                               ['2.3.7-5.1.1'])]
        self.assertTrue(item1.__eq__(item2))

        item1 = db_helper.query_operations_info(None, ds_aosp_email, dv_info)
        item2 = [OperationInfo('com.example:EmailMessageAOSPEmailApp', 'EmailMessage', ds_aosp_email, 'GT-I9300',
                               ['2.3.7-5.1.1']),
                 OperationInfo('com.example:ImageFileAOSPEmailApp', 'ImageFile', ds_aosp_email, 'GT-I9300',
                               ['2.3.7-5.1.1'])]
        self.assertTrue(item1.__eq__(item2))

        item1 = db_helper.query_operations_info('ImageFile', None, dv_info)
        item2 = [OperationInfo('com.example:ImageFileFacebook', 'ImageFile', ds_facebook, 'GT-I9300', ['2.3.7-5.1.1']),
                 OperationInfo('com.example:ImageFileAOSPEmailApp', 'ImageFile', ds_aosp_email, 'GT-I9300',
                               ['2.3.7-5.1.1'])]
        self.assertTrue(item1.__eq__(item2))

        item1 = db_helper.query_operations_info(None, None, dv_info)
        item2 = [OperationInfo('com.example:ImageFileFacebook', 'ImageFile', ds_facebook, 'GT-I9300', ['2.3.7-5.1.1']),
                 OperationInfo('com.example:ImageFileAOSPEmailApp', 'ImageFile', ds_aosp_email, 'GT-I9300',
                               ['2.3.7-5.1.1']),
                 OperationInfo('com.example:ImageFileAOSPEmailApp', 'ImageFile', ds_aosp_email, 'GT-I9300',
                               ['2.3.7-5.1.1']),
                 OperationInfo('com.example:SmsMessageAOSPSmsApp', 'SmsMessage', ds_aosp_email, 'GT-I9300',
                               ['2.3.7-5.1.1'])]
        self.assertTrue(item1.__eq__(item2))

        self.assertEqual(db_helper.query_operations_info('Non_existent', ds_aosp_email, dv_info), [])

        self.assertEqual(db_helper.get_operation_exec_info('com.example:EmailMessageAOSPEmailApp'),
                         {'extractor_id': 'ApplicationExtractor', 'inspector_id': 'EmailMessageInspector',
                          'param_values': {'package_name': 'com.android.email'}})
        self.assertEqual(db_helper.get_operation_exec_info('id_non_existent'), {})

        self.assertTrue(db_helper.exists_operation('com.example:EmailMessageAOSPEmailApp'))
        self.assertFalse(db_helper.exists_operation('Non_existent'))

        self.assertTrue(db_helper.exists_data_type('EmailMessage'))
        self.assertFalse(db_helper.exists_data_type('Non_existent'))

        self.assertTrue(db_helper.exists_data_source_type('Application'))
        self.assertFalse(db_helper.exists_data_source_type('Non_existent'))

        self.assertTrue(db_helper.has_all_required_param_values(ds_aosp_email))
        self.assertFalse(db_helper.has_all_required_param_values(bad_ds_aosp_email))


if __name__ == '__main__':
    unittest.main()
