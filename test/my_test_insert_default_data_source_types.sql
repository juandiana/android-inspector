INSERT INTO data_source_types (id, name, extractor_name)
VALUES (1, 'Application', 'ApplicationExtractor');
INSERT INTO required_params (data_source_type_id, param_name)
VALUES (1, 'package_name');
