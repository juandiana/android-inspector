-- Operation to extract EmailMessage from the AOSP application.
INSERT INTO operations (id, data_type_id, data_source_type_id, inspector_name)
VALUES ('com.example:EmailMessageAOSPEmailApp', 'com.example:EmailMessage', 'com.example:Application', 'EmailMessageInspector');
INSERT INTO device_models (operation_id, model_number)
VALUES ('com.example:EmailMessageAOSPEmailApp', 'GT-I9300');
INSERT INTO android_versions (operation_id, from_version, to_version)
VALUES ('com.example:EmailMessageAOSPEmailApp', '2.3.7', '5.1.1');
INSERT INTO data_source_params_values (operation_id, param_name, param_value)
VALUES ('com.example:EmailMessageAOSPEmailApp', 'package_name', 'com.android.email');
