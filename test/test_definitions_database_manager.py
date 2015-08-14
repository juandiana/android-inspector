# coding=utf-8
import os
import unittest

from components.definitions_database_manager import DefinitionsDatabaseManager
from model import DataSource, DeviceInfo, OperationInfo


class TestDefinitionsDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db_helper = DefinitionsDatabaseManager(os.path.join('test', 'test_definitions.db'),
                                                    'create_db.sql',
                                                    os.path.join('test', 'my_test_insert_default_data_types.sql'),
                                                    os.path.join('test',
                                                                 'my_test_insert_default_data_source_types.sql'),
                                                    os.path.join('test', 'my_test_insert_default_operations.sql'))
        self.ds_aosp_email = DataSource('Application', {'package_name': 'com.android.email'})
        self.ds_facebook = DataSource('Application', {'package_name': 'com.facebook.katana'})
        self.ds_aosp_sms = DataSource('Application', {'package_name': 'com.android.providers.telephony'})
        self.bad_ds = DataSource('Application', {})
        self.dv_info = DeviceInfo('3.0.0', 'GT-I9300')

        self.op_info_email_aosp_email = OperationInfo('EmailMessageAOSPEmail', 'EmailMessage', self.ds_aosp_email,
                                                      ['GT-I9300'], [('2.3.7', '5.1.1')])
        self.op_info_image_aosp_email = OperationInfo('ImageFileAOSPEmail', 'ImageFile', self.ds_aosp_email,
                                                      ['GT-I9300'], [('2.3.7', '5.1.1')])
        self.op_info_image_facebook = OperationInfo('ImageFileFacebook', 'ImageFile', self.ds_facebook,
                                                    ['GT-I9300', 'XT1053'], [('2.3.7', '5.1.1')])
        self.info = OperationInfo('SmsMessageAOSPSms', 'SmsMessage', self.ds_aosp_sms, ['GT-I9300', 'LG-D820'],
                                  [('2.0', '4.4.4')])
        self.op_info_sms_aosp_sms = self.info

    def tearDown(self):
        self.db_helper.conn.close()
        os.remove(os.path.join('test', 'test_definitions.db'))

    def test_query_operation_for_email_message(self):
        result = self.db_helper.query_operations_info('EmailMessage', self.ds_aosp_email, self.dv_info)
        expected_result = [self.op_info_email_aosp_email]

        self.assertEqualList(result, expected_result)

    def test_query_operation_without_data_type(self):
        result = self.db_helper.query_operations_info(None, self.ds_aosp_email, self.dv_info)
        expected_result = [self.op_info_email_aosp_email, self.op_info_image_aosp_email]

        self.assertEqualList(expected_result, result)

    def test_query_operation_without_data_source(self):
        result = self.db_helper.query_operations_info('ImageFile', None, self.dv_info)
        expected_result = [self.op_info_image_aosp_email, self.op_info_image_facebook]

        self.assertEqualList(result, expected_result)

    def test_query_operation_without_data_type_nor_data_source(self):
        result = self.db_helper.query_operations_info(None, None, self.dv_info)
        expected_result = [self.op_info_email_aosp_email, self.op_info_image_aosp_email,
                           self.op_info_image_facebook, self.op_info_sms_aosp_sms]

        self.assertEqualList(result, expected_result)

    def test_query_operation_for_non_existent_data_type(self):
        self.assertEqual(self.db_helper.query_operations_info('Non_existent', self.ds_aosp_email, self.dv_info), [])

    def test_get_operation_exec_info(self):
        extractor_id, inspector_id, param_values = self.db_helper.get_operation_exec_info('EmailMessageAOSPEmail')

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
        self.assertTrue(self.db_helper.exists_data_type('EmailMessage'))
        self.assertFalse(self.db_helper.exists_data_type('Non_existent'))

    def test_exists_data_source_type(self):
        self.assertTrue(self.db_helper.exists_data_source_type('Application'))
        self.assertFalse(self.db_helper.exists_data_source_type('Non_existent'))

    def test_has_all_required_param_values(self):
        self.assertTrue(self.db_helper.has_all_required_param_values(self.ds_aosp_email))
        self.assertFalse(self.db_helper.has_all_required_param_values(self.bad_ds))

    def test_add_operation(self):
        self.assertTrue(self.db_helper.add_operation('newOperation', 'EmailMessage', 'Application', 'new_op_inspector',
                                                     {'package': 'com.example.email'}, ['GT-i9300'],
                                                     [('2.2.0', '4.4.4')]))

    def test_add_operation_with_non_existent_data_type(self):
        self.assertRaisesRegexp(ValueError, "'dt_non_existent' is not a defined DataType",
                                self.db_helper.add_operation,
                                'newOperation', 'dt_non_existent', 'Application', 'new_op_inspector',
                                {'package': 'com.example.email'}, ['GT-i9300'], [('2.2.0', '4.4.4')]
                                )

    def assertEqualList(self, expected_result, result):
        self.assertEqual(len(result), len(expected_result))
        for i in range(len(expected_result)):
            self.assertEqual(result[i], expected_result[i])


if __name__ == '__main__':
    unittest.main()
