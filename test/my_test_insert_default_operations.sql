
-- Operation: EmailMessage from AOSP email application.
INSERT INTO operations (id, data_type_id, data_source_type_id, inspector_name)
VALUES ('com.example:EmailMessageAOSPEmailApp', 'com.example:EmailMessage', 'com.example:Application', 'EmailMessageInspector');
INSERT INTO device_models (operation_id, model_number)
VALUES ('com.example:EmailMessageAOSPEmailApp', 'GT-I9300');
INSERT INTO android_versions (operation_id, from_version, to_version)
VALUES ('com.example:EmailMessageAOSPEmailApp', '2.3.7', '5.1.1');
INSERT INTO data_source_params_values (operation_id, param_name, param_value)
VALUES ('com.example:EmailMessageAOSPEmailApp', 'package_name', 'com.android.email');

-- Operation: Images from the AOSP email application.
INSERT INTO operations (id, data_type_id, data_source_type_id, inspector_name)
VALUES ('com.example:ImageFileAOSPEmailApp', 'com.example:ImageFile', 'com.example:Application', 'ImageFileAOSPEmailInspector');
INSERT INTO device_models (operation_id, model_number)
VALUES ('com.example:ImageFileAOSPEmailApp', 'GT-I9300');
INSERT INTO android_versions (operation_id, from_version, to_version)
VALUES ('com.example:ImageFileAOSPEmailApp', '2.3.7', '5.1.1');
INSERT INTO data_source_params_values (operation_id, param_name, param_value)
VALUES ('com.example:ImageFileAOSPEmailApp', 'package_name', 'com.android.email');

-- Operation: Images from Facebook application.
INSERT INTO operations (id, data_type_id, data_source_type_id, inspector_name)
VALUES ('com.example:ImageFileFacebook', 'com.example:ImageFile', 'com.example:Application', 'ImageFileFacebookInspector');
INSERT INTO device_models (operation_id, model_number)
VALUES ('com.example:ImageFileFacebook', 'GT-I9300');
INSERT INTO device_models (operation_id, model_number)
VALUES ('com.example:ImageFileFacebook', 'XT1053');
INSERT INTO android_versions (operation_id, from_version, to_version)
VALUES ('com.example:ImageFileFacebook', '2.3.7', '5.1.1');
INSERT INTO data_source_params_values (operation_id, param_name, param_value)
VALUES ('com.example:ImageFileFacebook', 'package_name', 'com.facebook.katana');

-- Operation to extract SmsMessage from the AOSP SMS messages application.
INSERT INTO operations (id, data_type_id, data_source_type_id, inspector_name)
VALUES ('com.example:SmsMessageAOSPSmsApp', 'com.example:SmsMessage', 'com.example:Application', 'SmsMessageInspector');
INSERT INTO device_models (operation_id, model_number)
VALUES ('com.example:SmsMessageAOSPSmsApp', 'GT-I9300');
INSERT INTO device_models (operation_id, model_number)
VALUES ('com.example:SmsMessageAOSPSmsApp', 'LG-D820');
INSERT INTO android_versions (operation_id, from_version, to_version)
VALUES ('com.example:SmsMessageAOSPSmsApp', '2.0', '4.4.4');
INSERT INTO data_source_params_values (operation_id, param_name, param_value)
VALUES ('com.example:SmsMessageAOSPSmsApp', 'package_name', 'com.android.providers.telephony');

-- Operation to extract SmsMessage from the AOSP application for old Android Versions.
INSERT INTO operations (id, data_type_id, data_source_type_id, inspector_name)
VALUES ('com.example:SmsMessageAOSPSmsApp_oldAndroidVersions', 'com.example:SmsMessage', 'com.example:Application', 'SmsMessageInspector_oldAndroidVersions');
INSERT INTO device_models (operation_id, model_number)
VALUES ('com.example:SmsMessageAOSPSmsApp_oldAndroidVersions', 'Nexus 1');
INSERT INTO android_versions (operation_id, from_version, to_version)
VALUES ('com.example:SmsMessageAOSPSmsApp_oldAndroidVersions', '1.0', '2.0');
INSERT INTO data_source_params_values (operation_id, param_name, param_value)
VALUES ('com.example:SmsMessageAOSPSmsApp_oldAndroidVersions', 'package_name', 'com.android.providers.telephony');