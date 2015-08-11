-- Operation to extract EmailMessage from the AOSP application.
INSERT INTO operations (id, name, inspector_name, data_type_id, data_source_type_id)
VALUES (1, 'EmailMessageAOSPEmail', 'EmailMessageInspector', 1, 1);

INSERT INTO device_models (operation_id, model_number)
VALUES (1, 'GT-I9300');
INSERT INTO android_versions (operation_id, from_version, to_version)
VALUES (1, '2.3.7', '5.1.1');
INSERT INTO data_source_params_values (operation_id, param_name, param_value)
VALUES (1, 'package_name', 'com.android.email');
