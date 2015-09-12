-- Operation to extract EmailMessage from the AOSP Email application.
INSERT INTO operations (name, inspector_name, data_type_id, data_source_type_id)
VALUES ('EmailMessageAOSPEmail', 'EmailMessageInspector', 1, 1);

INSERT INTO device_models (operation_id, model_number)
VALUES (1, 'X515m');
INSERT INTO android_versions (operation_id, from_version, to_version)
VALUES (1, '4.1', '4.3');
INSERT INTO data_source_params_values (operation_id, param_name, param_value)
VALUES (1, 'package_name', 'com.android.email');

-- Operation to extract SmsMessage from the AOSP Sms application.
INSERT INTO operations (name, inspector_name, data_type_id, data_source_type_id)
VALUES ('SmsMessageAOSPSms', 'SmsMessageInspector', 2, 1);

INSERT INTO device_models (operation_id, model_number)
VALUES (2, 'X515m');
INSERT INTO android_versions (operation_id, from_version, to_version)
VALUES (2, '4.1', '4.3');
INSERT INTO data_source_params_values (operation_id, param_name, param_value)
VALUES (2, 'package_name', 'com.android.providers.telephony');
