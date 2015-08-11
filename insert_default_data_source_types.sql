INSERT INTO data_source_types (id, name, namespace, extractor_name)
VALUES (1, 'Application', 'com.example','ApplicationExtractor');
INSERT INTO required_params (data_source_type_id, param_name)
VALUES (1, 'package_name');
