# coding=utf-8
import os
import unittest

from components.definitions_database_manager import DefinitionsDatabaseManager
from model import DataSource, DeviceInfo, OperationInfo, DataType


class TestDefinitionsDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db_helper = DefinitionsDatabaseManager(os.path.join('test', 'test_definitions.db'),
                                                    'create_db.sql',
                                                    os.path.join('test', 'my_test_insert_default_data_types.sql'),
                                                    os.path.join('test',
                                                                 'my_test_insert_default_data_source_types.sql'),
                                                    os.path.join('test', 'my_test_insert_default_operations.sql'))
        self.dt_email_message = DataType('com.example', 'EmailMessage')
        self.dt_image_file = DataType('com.example', 'ImageFile')
        self.dt_sms_message = DataType('com.example', 'SmsMessage')
        self.dt_non_existent = DataType('com.nothing', 'Non_existent')
        self.ds_aosp_email = DataSource('com.example', 'Application', {'package_name': 'com.android.email'})
        self.ds_facebook = DataSource('com.example', 'Application', {'package_name': 'com.facebook.katana'})
        self.ds_aosp_sms = DataSource('com.example', 'Application', {'package_name': 'com.android.providers.telephony'})
        self.bad_ds = DataSource('com.example', 'Application', {})
        self.dv_info = DeviceInfo('3.0.0', 'GT-I9300')

        self.op_info_email_aosp_email = OperationInfo(1, self.dt_email_message, self.ds_aosp_email, ['GT-I9300'],
                                                      [('2.3.7', '5.1.1')])
        self.op_info_image_aosp_email = OperationInfo(2, self.dt_image_file, self.ds_aosp_email, ['GT-I9300'],
                                                      [('2.3.7', '5.1.1')])
        self.op_info_image_facebook = OperationInfo(3, self.dt_image_file, self.ds_facebook,
                                                    ['GT-I9300', 'XT1053'], [('2.3.7', '5.1.1')])
        self.op_info_sms_aosp_sms = OperationInfo(4, self.dt_sms_message, self.ds_aosp_sms,
                                                  ['GT-I9300', 'LG-D820'], [('2.0', '4.4.4')])

    def tearDown(self):
        os.remove(os.path.join('test', 'test_definitions.db'))

    def test_query_operation_for_email_message(self):
        result = self.db_helper.query_operations_info(self.dt_email_message, self.ds_aosp_email, self.dv_info)
        expected_result = [self.op_info_email_aosp_email]

        self.assertEqualList(result, expected_result)

    def test_query_operation_without_data_type(self):
        result = self.db_helper.query_operations_info(None, self.ds_aosp_email, self.dv_info)
        expected_result = [self.op_info_email_aosp_email, self.op_info_image_aosp_email]

        self.assertEqualList(expected_result, result)

    def test_query_operation_without_data_source(self):
        result = self.db_helper.query_operations_info(self.dt_image_file, None, self.dv_info)
        expected_result = [self.op_info_image_aosp_email, self.op_info_image_facebook]

        self.assertEqualList(result, expected_result)

    def test_query_operation_without_data_type_nor_data_source(self):
        result = self.db_helper.query_operations_info(None, None, self.dv_info)
        expected_result = [self.op_info_email_aosp_email, self.op_info_image_aosp_email,
                           self.op_info_image_facebook, self.op_info_sms_aosp_sms]

        self.assertEqualList(result, expected_result)

    def test_query_operation_for_non_existent_data_type(self):
        self.assertEqual(self.db_helper.query_operations_info(self.dt_non_existent, self.ds_aosp_email, self.dv_info), [])

    def test_get_operation_exec_info(self):
        extractor_id, inspector_id, param_values = self.db_helper.get_operation_exec_info(1)

        self.assertEqual(extractor_id, 'ApplicationExtractor')
        self.assertEqual(inspector_id, 'EmailMessageInspector')
        self.assertEqual(param_values, {'package_name': 'com.android.email'})

    def test_get_operation_exec_info_id_non_existent(self):
        extractor_id, inspector_id, param_values = self.db_helper.get_operation_exec_info('id_non_existent')
        self.assertEqual(extractor_id, '')
        self.assertEqual(inspector_id, '')
        self.assertEqual(param_values, {})

    def test_exists_operation(self):
        self.assertTrue(self.db_helper.exists_operation('SmsMessageAOSPSms'))
        self.assertFalse(self.db_helper.exists_operation('Non_existent'))

    def test_exists_data_type(self):
        self.assertTrue(self.db_helper.exists_data_type(self.dt_email_message))
        self.assertFalse(self.db_helper.exists_data_type(self.dt_non_existent))

    def test_exists_data_source_type(self):
        self.assertTrue(self.db_helper.exists_data_source_type('com.example', 'Application'))
        self.assertFalse(self.db_helper.exists_data_source_type('com.example', 'Non_existent'))

    def test_has_all_required_param_values(self):
        self.assertTrue(self.db_helper.has_all_required_param_values(self.ds_aosp_email))
        self.assertFalse(self.db_helper.has_all_required_param_values(self.bad_ds))

    def assertEqualList(self, expected_result, result):
        self.assertEqual(len(result), len(expected_result))
        for i in range(len(expected_result)):
            self.assertEqual(result[i], expected_result[i])


if __name__ == '__main__':
    unittest.main()
