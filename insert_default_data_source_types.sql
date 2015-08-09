INSERT INTO data_source_types (id, name, extractor_name)
VALUES ('com.example:Application', 'Application','ApplicationExtractor');
INSERT INTO required_params (data_source_type_id, param_name)
VALUES ('com.example:Application', 'package_name');