INSERT INTO data_source_types (id, namespace, name, extractor_name)
VALUES (1, 'com.example', 'Application', 'ApplicationExtractor');
INSERT INTO required_params (data_source_type_id, param_name)
VALUES (1, 'package_name');
