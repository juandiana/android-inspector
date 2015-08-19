-- Operation to extract EmailMessage from the AOSP Email application.
INSERT INTO operations (name, inspector_name, data_type_id, data_source_type_id)
VALUES ('EmailMessageAOSPEmail', 'EmailMessageInspector', 1, 1);

INSERT INTO device_models (operation_id, model_number)
VALUES (1, 'GT-I9300');
INSERT INTO device_models (operation_id, model_number)
VALUES (1, 'XT1053');
INSERT INTO android_versions (operation_id, from_version, to_version)
VALUES (1, '2.3.7', '5.1.1');
INSERT INTO data_source_params_values (operation_id, param_name, param_value)
VALUES (1, 'package_name', 'com.android.email');

-- Operation to extract SmsMessage from the AOSP Sms application.
INSERT INTO operations (name, inspector_name, data_type_id, data_source_type_id)
VALUES ('SmsMessageAOSPSms', 'SmsMessageInspector', 2, 1);

INSERT INTO device_models (operation_id, model_number)
VALUES (2, 'GT-I9300');
INSERT INTO device_models (operation_id, model_number)
VALUES (2, 'XT1053');
INSERT INTO android_versions (operation_id, from_version, to_version)
VALUES (2, '2.2.0', '4.4.4');
INSERT INTO data_source_params_values (operation_id, param_name, param_value)
VALUES (2, 'package_name', 'com.android.providers.telephony');

-- TODO: Ver si dejamos estas operaciones por defecto (al igual que el tipo de dato Contact).
-- Operation to extract Contacts from the Facebook.
INSERT INTO operations (name, inspector_name, data_type_id, data_source_type_id)
VALUES ('ContactFacebook', 'ContactFacebookInspector', 3, 1);

INSERT INTO device_models (operation_id, model_number)
VALUES (3, 'GT-I9300');
INSERT INTO device_models (operation_id, model_number)
VALUES (3, 'XT1053');
INSERT INTO device_models (operation_id, model_number)
VALUES (3, 'Nexus 5');
INSERT INTO android_versions (operation_id, from_version, to_version)
VALUES (3, '4.1', '4.4.4');
INSERT INTO data_source_params_values (operation_id, param_name, param_value)
VALUES (3, 'package_name', 'com.facebook.katana');

-- Operation to extract Contacts from the Facebook.
INSERT INTO operations (name, inspector_name, data_type_id, data_source_type_id)
VALUES ('ContactWhatsApp', 'ContactWhatsAppInspector', 3, 1);

INSERT INTO device_models (operation_id, model_number)
VALUES (4, 'GT-I9300');
INSERT INTO device_models (operation_id, model_number)
VALUES (4, 'XT1053');
INSERT INTO android_versions (operation_id, from_version, to_version)
VALUES (4, '4.1', '4.4.4');
INSERT INTO data_source_params_values (operation_id, param_name, param_value)
VALUES (4, 'package_name', 'com.whatsapp');

-- Operation to extract Contacts from the Facebook.
INSERT INTO operations (name, inspector_name, data_type_id, data_source_type_id)
VALUES ('ContactAOSPAgenda', 'ContactAOSPAgendaInspector', 3, 1);

INSERT INTO device_models (operation_id, model_number)
VALUES (5, 'GT-I9300');
INSERT INTO device_models (operation_id, model_number)
VALUES (5, 'XT1053');
INSERT INTO android_versions (operation_id, from_version, to_version)
VALUES (5, '2.3', '4.4.4');
INSERT INTO data_source_params_values (operation_id, param_name, param_value)
VALUES (5, 'package_name', 'com.android.providers.contacts');
