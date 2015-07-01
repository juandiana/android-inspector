INSERT INTO data_types (id, name, cybox_object_name) values ('data_type_1', 'EmailMessage','EmailMessageObject');
INSERT INTO data_source_types (id, name, extractor_name) values ('data_source_type_1', 'Application','application_extractor');
INSERT INTO required_params (data_source_type_id, param_name) values ('data_source_type_1', 'package_name');
INSERT INTO operations (id, data_type_id, data_source_type_id, inspector_name) values ('operation_1', 'data_type_1', 'data_source_type_1', 'email_message_inspector');
INSERT INTO device_models (operation_id, model_number) values ('operation_1', 'GT-I9300');
INSERT INTO android_versions (operation_id, from_version, to_version) values ('operation_1', '2.3.7', '5.1.1');
INSERT INTO data_source_params_values (operation_id, param_name, param_value) values ('operation_1', 'package_name', 'com.android.email');
