-- Operation to extract EmailMessage from the AOSP application.
INSERT INTO data_types (id, name, cybox_object_name)
VALUES ('com.example:EmailMessage', 'EmailMessage','EmailMessageObject');
INSERT INTO data_source_types (id, name, extractor_name)
VALUES ('com.example:Application', 'Application','ApplicationExtractor');
INSERT INTO required_params (data_source_type_id, param_name)
VALUES ('com.example:Application', 'package_name');
INSERT INTO operations (id, data_type_id, data_source_type_id, inspector_name)
VALUES ('com.example:EmailMessageAOSPApp', 'com.example:EmailMessage', 'com.example:Application', 'EmailMessageInspector');
INSERT INTO device_models (operation_id, model_number)
VALUES ('com.example:EmailMessageAOSPApp', 'GT-I9300');
INSERT INTO android_versions (operation_id, from_version, to_version)
VALUES ('com.example:EmailMessageAOSPApp', '2.3.7', '5.1.1');
INSERT INTO data_source_params_values (operation_id, param_name, param_value)
VALUES ('com.example:EmailMessageAOSPApp', 'package_name', 'com.android.email');

-- Operation to extract SmsMessage from the AOSP application.
INSERT INTO data_types (id, name, cybox_object_name)
VALUES ('com.example:SmsMessage', 'SmsMessage','SmsMessageObject');
INSERT INTO operations (id, data_type_id, data_source_type_id, inspector_name)
VALUES ('com.example:SmsMessageAOSPSmsApp', 'com.example:SmsMessage', 'com.example:Application', 'SmsMessageInspector');
INSERT INTO device_models (operation_id, model_number)
VALUES ('com.example:SmsMessageAOSPSmsApp', 'GT-I9300');
INSERT INTO device_models (operation_id, model_number)
VALUES ('com.example:SmsMessageAOSPSmsApp', 'Nexus 5');
INSERT INTO android_versions (operation_id, from_version, to_version)
VALUES ('com.example:SmsMessageAOSPSmsApp', '2.0', '4.4.4');
INSERT INTO data_source_params_values (operation_id, param_name, param_value)
VALUES ('com.example:SmsMessageAOSPSmsApp', 'package_name', 'com.android.providers.telephony');
