# coding=utf-8
import os
import unittest
import sqlite3

from components.definitions_database_manager import DefinitionsDatabaseManager
from model import DataSource, DeviceInfo, OperationInfo


class TestDefinitionsDatabaseManager(unittest.TestCase):
    DB_FILE_PATH = os.path.join('test', 'test_definitions.db')
    DB_CREATION_SCRIPT_PATH = 'create_db.sql'
    DEFAULT_DATA_TYPES_SCRIPT_PATH = os.path.join('test', 'insert_test_default_data_types.sql')
    DEFAULT_DATA_SOURCE_TYPES_SCRIPT_PATH = os.path.join('test', 'insert_test_default_data_source_types.sql')
    DEFAULT_OPERATIONS_SCRIPT_PATH = os.path.join('test', 'insert_test_default_operations.sql')

    @classmethod
    def setUpClass(cls):
        cls.db_helper = DefinitionsDatabaseManager(cls.DB_FILE_PATH,
                                                   cls.DB_CREATION_SCRIPT_PATH,
                                                   cls.DEFAULT_DATA_TYPES_SCRIPT_PATH,
                                                   cls.DEFAULT_DATA_SOURCE_TYPES_SCRIPT_PATH,
                                                   cls.DEFAULT_OPERATIONS_SCRIPT_PATH)

        cls.ds_aosp_email = DataSource('Application', {'package_name': 'com.android.email'})
        cls.ds_facebook = DataSource('Application', {'package_name': 'com.facebook.katana'})
        cls.ds_aosp_sms = DataSource('Application', {'package_name': 'com.android.providers.telephony'})
        cls.bad_ds = DataSource('Application', {})
        cls.dv_info = DeviceInfo('3.0.0', 'GT-I9300')

        cls.op_info_email_aosp_email = OperationInfo('EmailMessageAOSPEmail', 'EmailMessage', cls.ds_aosp_email,
                                                     ['GT-I9300'], [('2.3.7', '5.1.1')])
        cls.op_info_image_aosp_email = OperationInfo('ImageFileAOSPEmail', 'ImageFile', cls.ds_aosp_email,
                                                     ['GT-I9300'], [('2.3.7', '5.1.1')])
        cls.op_info_image_facebook = OperationInfo('ImageFileFacebook', 'ImageFile', cls.ds_facebook,
                                                   ['GT-I9300', 'XT1053'], [('2.3.7', '5.1.1')])
        cls.op_info_sms_aosp_sms = OperationInfo('SmsMessageAOSPSms', 'SmsMessage', cls.ds_aosp_sms,
                                                 ['GT-I9300', 'LG-D820'], [('2.0', '4.4.4')])

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.DB_FILE_PATH)

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

    def test_query_operation_for_data_source_with_missing_params(self):
        self.assertFalse(self.db_helper.has_all_required_param_values(DataSource('Application', None)))

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
        op_name = 'newOperation'
        dt_name = 'EmailMessage'
        dst_name = 'Application'
        param_values = {'package': 'com.example.email'}
        inspector_name = 'new_op_inspector'
        dev_models = ['GT-i9300']
        os_versions = [('2.2.0', '4.4.4')]

        ds = DataSource(dst_name, param_values)
        dev_info = DeviceInfo('4.3', dev_models[0])

        self.db_helper.add_operation(op_name, dt_name, dst_name, inspector_name, param_values, dev_models, os_versions)

        result = self.db_helper.query_operations_info(dt_name, ds, dev_info)

        self.assertEqualList(result, [OperationInfo(op_name, dt_name, ds, dev_models, os_versions)])

    def test_add_operation_with_non_existent_data_type(self):
        self.assertRaisesRegexp(ValueError, "'dt_non_existent' is not a defined DataType.",
                                self.db_helper.add_operation,
                                'newOperation', 'dt_non_existent', 'Application', 'new_op_inspector',
                                {'package': 'com.example.email'}, ['GT-i9300'], [('2.2.0', '4.4.4')]
                                )

    def test_remove_operation(self):
        op_name = 'EmailMessageAOSPEmail'
        self.db_helper.remove_operation(op_name)

        ext_id, ins_id, params = self.db_helper.get_operation_exec_info(op_name)

        self.assertEqual(ext_id, '')
        self.assertEqual(ins_id, '')
        self.assertEqual(params, {})

    def test_remove_operation_with_non_existing_operation(self):
        self.assertRaisesRegexp(ValueError, "'non_existent' is not a defined Operation.",
                                self.db_helper.remove_operation, 'non_existent')

    def test_add_data_type(self):
        dt_name = 'newDataType'
        self.db_helper.add_data_type(dt_name, 'newCyboxObject')
        self.assertTrue(self.db_helper.exists_data_type(dt_name))

    def test_add_data_type_that_already_exists(self):
        data_type_name = 'existingDataType'
        cybox_object_name = 'existingCyboxObject'
        self.db_helper.add_data_type(data_type_name, cybox_object_name)
        self.assertRaisesRegexp(ValueError, "The data_type '{0}' already exists.".format(data_type_name),
                                self.db_helper.add_data_type, data_type_name, cybox_object_name)

    def test_remove_data_type(self):
        data_type_name = 'removeDataType'
        self.db_helper.add_data_type(data_type_name, 'removeCyboxObject')
        self.db_helper.remove_data_type(data_type_name)
        self.assertFalse(self.db_helper.exists_data_type(data_type_name))

    def test_remove_data_type_with_non_existing_data_type(self):
        self.assertRaisesRegexp(ValueError, "'non_existent' is not a defined DataType.",
                                self.db_helper.remove_data_type, 'non_existent')

    def test_remove_data_type_with_used_by_operation_data_type(self):
        self.assertRaisesRegexp(ValueError, "The data_type 'EmailMessage' cannot be deleted. "
                                            "There are existing operations to extract this data_type.",
                                self.db_helper.remove_data_type, 'EmailMessage')

    def test_add_data_source_type(self):
        data_source_type_name = 'newDataSourceType'
        extractor_name = 'newExtractor'
        param_values = ['param1', 'param2']

        self.db_helper.add_data_source_type(data_source_type_name, extractor_name, param_values)

        with sqlite3.connect(self.DB_FILE_PATH) as conn:
            rows = conn.execute(
                """
                SELECT rp.param_name
                FROM data_source_types dst, required_params rp
                WHERE dst.id = rp.data_source_type_id AND dst.name = ?
                AND dst.extractor_name = ?
                """,
                [data_source_type_name, extractor_name]
            )

        params = []
        for rp in rows:
            params.append(rp[0])

        self.assertEqualList(param_values, params)

    def test_add_data_source_type_that_already_exists(self):
        data_source_type_name = 'existing'
        extractor_name = 'existingExtractor'
        params = ['param1']
        self.db_helper.add_data_source_type(data_source_type_name, extractor_name, params)
        self.assertRaisesRegexp(ValueError, "The data_source_type '{0}' already exists.".format(data_source_type_name),
                                self.db_helper.add_data_source_type, data_source_type_name, extractor_name, params)

    def test_remove_data_source_type(self):
        data_source_type_name = 'removeDataType'
        self.db_helper.add_data_source_type(data_source_type_name, 'removeExtractor', ['param1'])
        self.db_helper.remove_data_source_type(data_source_type_name)

        with sqlite3.connect(self.DB_FILE_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                      SELECT * FROM data_source_types
                      WHERE name = ?
                      """,
                      [data_source_type_name]
                      )

            dst = c.fetchone()

            c.execute('SELECT 1 FROM required_params '
                      'WHERE data_source_type_id NOT IN (SELECT id FROM data_source_types)')
            rp = c.fetchone()

            c.close()

        self.assertTrue(dst is None and rp is None)

    def test_remove_data_source_type_with_non_existing_data_source_type(self):
        self.assertRaisesRegexp(ValueError, "'non_existent' is not a defined DataSourceType.",
                                self.db_helper.remove_data_source_type, 'non_existent')

    def test_remove_data_source_type_with_used_by_operation_data_source_type(self):
        self.assertRaisesRegexp(ValueError, "The data_source_type 'Application' cannot be deleted. "
                                            "There are existing operations to extract this data_source_type.",
                                self.db_helper.remove_data_source_type, 'Application')

    def assertEqualList(self, expected_result, result):
        self.assertEqual(len(expected_result), len(result))
        for i in range(len(expected_result)):
            self.assertEqual(expected_result[i], result[i])


if __name__ == '__main__':
    unittest.main()
