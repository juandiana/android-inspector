# coding=utf-8
import unittest
from components.definitions_database import DefinitionsDatabase
from model import DataSource, DeviceInfo, OperationInfo

# TODO: Poner inicializaciones en el SetUp.
# TODO: Poner OperationInfo usadas en expected_results tambien en el SetUp.
# TODO: Dividir en métodos las pruebas.

class MyTestCase(unittest.TestCase):
    def test_something(self):
        db_helper = DefinitionsDatabase('test_definitions.db',
                                        'my_test_create_db.sql',
                                        'my_test_insert_default_operations.sql')
        ds_aosp_email = DataSource('Application', {'package_name': 'com.android.email'})
        ds_facebook = DataSource('Application', {'package_name': 'com.facebook.katana'})
        ds_aosp_sms = DataSource('Application', {'package_name': 'com.android.providers.telephony'})
        bad_ds = DataSource('Application', {})
        dv_info = DeviceInfo('3.0.0', 'GT-I9300')

        result = db_helper.query_operations_info('EmailMessage', ds_aosp_email, dv_info)
        expected_result = [
            OperationInfo('com.example:EmailMessageAOSPEmailApp', 'EmailMessage', ds_aosp_email, ['GT-I9300'],
                          [('2.3.7', '5.1.1')])]

        self.assertListEqual(result, expected_result)

        result = db_helper.query_operations_info(None, ds_aosp_email, dv_info)
        expected_result = [
            OperationInfo('com.example:EmailMessageAOSPEmailApp', 'EmailMessage', ds_aosp_email, ['GT-I9300'],
                          [('2.3.7', '5.1.1')]),
            OperationInfo('com.example:ImageFileAOSPEmailApp', 'ImageFile', ds_aosp_email, ['GT-I9300'],
                          [('2.3.7', '5.1.1')])]

        self.assertEqualList(expected_result, result)

        result = db_helper.query_operations_info('ImageFile', None, dv_info)
        expected_result = [OperationInfo('com.example:ImageFileAOSPEmailApp', 'ImageFile', ds_aosp_email, ['GT-I9300'],
                                         [('2.3.7', '5.1.1')]),
                           OperationInfo('com.example:ImageFileFacebook', 'ImageFile', ds_facebook,
                                         ['GT-I9300', 'XT1053'], [('2.3.7', '5.1.1')])]

        self.assertListEqual(result, expected_result)

        result = db_helper.query_operations_info(None, None, dv_info)
        expected_result = [OperationInfo('com.example:EmailMessageAOSPEmailApp', 'EmailMessage', ds_aosp_email,
                                         ['GT-I9300'], [('2.3.7', '5.1.1')]),
                           OperationInfo('com.example:ImageFileAOSPEmailApp', 'ImageFile', ds_aosp_email, ['GT-I9300'],
                                         [('2.3.7', '5.1.1')]),
                           OperationInfo('com.example:ImageFileFacebook', 'ImageFile', ds_facebook,
                                         ['GT-I9300', 'XT1053'], [('2.3.7', '5.1.1')]),
                           OperationInfo('com.example:SmsMessageAOSPSmsApp', 'SmsMessage', ds_aosp_sms,
                                         ['GT-I9300', 'LG-D820'], [('2.0', '4.4.4')])]

        self.assertListEqual(result, expected_result)

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
        self.assertFalse(db_helper.has_all_required_param_values(bad_ds))

    def assertEqualList(self, expected_result, result):
        self.assertEqual(len(result), len(expected_result))
        for i in range(len(expected_result)):
            self.assertEqual(result[i], expected_result[i])


if __name__ == '__main__':
    unittest.main()
