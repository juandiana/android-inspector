# coding=utf-8
from os import path
import sqlite3


class DefinitionsDatabase(object):
    DB_FILE_NAME = 'definitions.db'

    def __init__(self):
        db_file_path = DefinitionsDatabase.DB_FILE_NAME

        if not path.exists(db_file_path):
            # Create the db schema
            execute_sql_script(db_file_path, '../create_db.sql')
            # Insert default operations
            execute_sql_script(db_file_path, '../insert_email_operation.sql')

        self.conn = sqlite3.connect(db_file_path)
        # TODO: Close connection, somewhere.

    def query_operations_info(self, data_type, data_source, device_info):
        cursor = self.conn.cursor()
        cursor.execute('SELECT *'
                       'FROM operations'
                       'WHERE data_type_id = ? AND data_source_id = ?',
                       parameters=(data_type, data_source.type_))
        cursor.close()

        result = []
        # create OperationInfo's

        return result

    def get_operation_exec_info(self, id_):
        pass

    def exists_data_type(self, data_type):
        pass

    def exists_data_source_type(self, data_source_type):
        pass

    def has_all_required_param_values(self, data_source):
        pass

    def add_operation(self, id_, data_type_id, data_source_type_id, inspector_id, param_values, device_models,
                      android_versions):
        pass

    def remove_operation(self, id_):
        pass

    def add_data_type(self, name, cybox_object_name):
        pass

    def remove_data_type(self, name):
        pass

    def add_data_source_type(self, id_, name, extractor_name):
        pass

    def remove_data_source_type(self, id_):
        pass


def execute_sql_script(db_file_path, script_file_path):
    f = open(script_file_path, 'r')
    with f:
        sql_statements = f.read()
    conn = sqlite3.connect(db_file_path)
    with conn:
        cursor = conn.cursor()
        cursor.executescript(sql_statements)
        cursor.close()
