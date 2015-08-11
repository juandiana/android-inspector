CREATE TABLE data_types ( id INT PRIMARY KEY,
                          name TEXT,
                          namespace TEXT,
                          cybox_object_name TEXT);
CREATE INDEX dt_name_index ON data_types (name, namespace);

CREATE TABLE data_source_types ( id INT PRIMARY KEY,
                                 name TEXT,
                                 namespace TEXT,
                                 extractor_name TEXT);
CREATE INDEX dst_name_index ON data_source_types (name, namespace);

CREATE TABLE required_params ( data_source_type_id INT NOT NULL REFERENCES data_source_types(id),
                               param_name TEXT,
                               PRIMARY KEY(data_source_type_id, param_name));

CREATE TABLE operations (   id INT,
                            data_type_id INT NOT NULL REFERENCES data_types(id),
                            data_source_type_id INT NOT NULL REFERENCES data_source_types(id),
                            name TEXT,
                            namespace TEXT,
                            inspector_name TEXT,
                            PRIMARY KEY(id));

CREATE TABLE device_models ( operation_id INT NOT NULL REFERENCES operations(id),
                             model_number TEXT,
                             PRIMARY KEY (operation_id, model_number));

CREATE TABLE android_versions ( operation_id INT NOT NULL REFERENCES operations(id),
                                from_version TEXT,
                                to_version TEXT,
                                PRIMARY KEY (operation_id, from_version, to_version));

CREATE TABLE data_source_params_values ( operation_id INT NOT NULL REFERENCES operations(id),
                                         param_name TEXT,
                                         param_value TEXT,
                                         PRIMARY KEY (operation_id, param_name));
