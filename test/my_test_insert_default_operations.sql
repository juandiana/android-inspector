-- Operation: EmailMessage from AOSP email application.
INSERT INTO operations (name, data_type_id, data_source_type_id, inspector_name)
VALUES ('EmailMessageAOSPEmail', 1, 1, 'EmailMessageInspector');
INSERT INTO device_models (operation_id, model_number)
VALUES (1, 'GT-I9300');
INSERT INTO android_versions (operation_id, from_version, to_version)
VALUES (1, '2.3.7', '5.1.1');
INSERT INTO data_source_params_values (operation_id, param_name, param_value)
VALUES (1, 'package_name', 'com.android.email');

-- Operation: Images from the AOSP email application.
INSERT INTO operations (name, data_type_id, data_source_type_id, inspector_name)
VALUES ('ImageFileAOSPEmail', 2, 1, 'ImageFileAOSPEmailInspector');
INSERT INTO device_models (operation_id, model_number)
VALUES (2, 'GT-I9300');
INSERT INTO android_versions (operation_id, from_version, to_version)
VALUES (2, '2.3.7', '5.1.1');
INSERT INTO data_source_params_values (operation_id, param_name, param_value)
VALUES (2, 'package_name', 'com.android.email');

-- Operation: Images from Facebook application.
INSERT INTO operations (name, data_type_id, data_source_type_id, inspector_name)
VALUES ('ImageFileFacebook', 2, 1, 'ImageFileFacebookInspector');
INSERT INTO device_models (operation_id, model_number)
VALUES (3, 'GT-I9300');
INSERT INTO device_models (operation_id, model_number)
VALUES (3, 'XT1053');
INSERT INTO android_versions (operation_id, from_version, to_version)
VALUES (3, '2.3.7', '5.1.1');
INSERT INTO data_source_params_values (operation_id, param_name, param_value)
VALUES (3, 'package_name', 'com.facebook.katana');

-- Operation to extract SmsMessage from the AOSP SMS messages application.
INSERT INTO operations (name, data_type_id, data_source_type_id, inspector_name)
VALUES ('SmsMessageAOSPSms', 3, 1, 'SmsMessageInspector');
INSERT INTO device_models (operation_id, model_number)
VALUES (4, 'GT-I9300');
INSERT INTO device_models (operation_id, model_number)
VALUES (4, 'LG-D820');
INSERT INTO android_versions (operation_id, from_version, to_version)
VALUES (4, '2.0', '4.4.4');
INSERT INTO data_source_params_values (operation_id, param_name, param_value)
VALUES (4, 'package_name', 'com.android.providers.telephony');

-- Operation to extract SmsMessage from the AOSP application for old Android Versions.
INSERT INTO operations (name, data_type_id, data_source_type_id, inspector_name)
VALUES ('SmsMessageAOSPSms_old', 3, 1, 'SmsMessageInspector_old');
INSERT INTO device_models (operation_id, model_number)
VALUES (5, 'Nexus 1');
INSERT INTO android_versions (operation_id, from_version, to_version)
VALUES (5, '1.0', '2.0');
INSERT INTO data_source_params_values (operation_id, param_name, param_value)
VALUES (5, 'package_name', 'com.android.providers.telephony');