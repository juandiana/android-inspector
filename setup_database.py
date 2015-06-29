# coding=utf-8
import os
import sqlite3


def main():
    db_file_path = os.path.join(os.getcwd(), 'repositories', 'definitions.db')

    if not os.path.exists(db_file_path):
        conn = sqlite3.connect(db_file_path)
        c = conn.cursor()

        c.executescript("""
            CREATE TABLE data_types ( id TEXT PRIMARY KEY,
                                      name TEXT,
                                      cybox_object_name TEXT);

            CREATE TABLE data_source_types ( id TEXT PRIMARY KEY,
                                             name TEXT,
                                             extractor_name TEXT);

            CREATE TABLE required_params ( data_source_type_id TEXT NOT NULL REFERENCES data_source_types(id),
                                           param_name TEXT,
                                           PRIMARY KEY(data_source_type_id, param_name));

            CREATE TABLE operations (   id TEXT,
                                        data_type_id TEXT NOT NULL REFERENCES data_types(id),
                                        data_source_type_id TEXT NOT NULL REFERENCES data_source_types(id),
                                        inspector_name TEXT,
                                        PRIMARY KEY(id));

            CREATE TABLE device_models ( operation_id TEXT NOT NULL REFERENCES operations(id),
                                         model_number TEXT,
                                         PRIMARY KEY (operation_id, model_number));

            CREATE TABLE android_versions ( operation_id TEXT NOT NULL REFERENCES operations(id),
                                            from_version TEXT,
                                            to_version TEXT,
                                            PRIMARY KEY (operation_id, from_version, to_version));

            CREATE TABLE data_source_params_values ( operation_id TEXT NOT NULL REFERENCES operations(id),
                                                     param_name TEXT,
                                                     param_value TEXT,
                                                     PRIMARY KEY (operation_id, param_name));

            INSERT INTO data_types (id, name, cybox_object_name) values ('data_type_1', 'EmailMessage','EmailMessageObject');
            INSERT INTO data_source_types (id, name, extractor_name) values ('data_source_type_1', 'Application','application_extractor.py');
            INSERT INTO required_params (data_source_type_id, param_name) values ('data_source_type_1', 'package_name');
            INSERT INTO operations (id, data_type_id, data_source_type_id, inspector_name) values ('operation_1', 'data_type_1', 'data_source_type_1', 'email_message_inspector.py');
            INSERT INTO device_models (operation_id, model_number) values ('operation_1', 'GT-I9300');
            INSERT INTO android_versions (operation_id, from_version, to_version) values ('operation_1', '2.0.0', '5.1.0');
            INSERT INTO data_source_params_values (operation_id, param_name, param_value) values ('operation_1', 'package_name', 'com.android.email');

            """)

if __name__ == "__main__":
    main()
