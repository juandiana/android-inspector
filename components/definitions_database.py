# coding=utf-8
from os import path
import sqlite3
from model import OperationInfo


class DefinitionsDatabase(object):
    DB_FILE_NAME = 'definitions.db'

    def __init__(self):
        db_file_path = DefinitionsDatabase.DB_FILE_NAME

        if not path.exists(db_file_path):
            # Create the db schema
            execute_sql_script(db_file_path, '../create_db.sql')
            # Insert default operations
            execute_sql_script(db_file_path, '../insert_default_operations.sql')

        self.conn = sqlite3.connect(db_file_path)
        # TODO: Close connection, somewhere.

    def query_operations_info(self, data_type, data_source, device_info):
        c = self.conn.cursor()
        data_source_type = data_source.type_
        c.execute("""
                SELECT o.id as id, dt.name as data_type, dst.name as data_source_type
                FROM operations AS o, data_types AS dt, data_source_types AS dst
                WHERE o.data_type_id = dt.id AND o.data_source_type_id = dst.id AND dt.name = ? AND dst.name = ?
                """, [data_type, data_source_type])

        result = []

        for row in c:
            c2 = self.conn.cursor()
            c2.execute('SELECT model_number FROM device_models WHERE operation_id = ?', [row[0]])

            models = []
            for op_model_row in c2:
                models.append(op_model_row[0])

            if device_info.device_model in models:
                c3 = self.conn.cursor()
                c3.execute('SELECT from_version, to_version FROM android_versions WHERE operation_id = ?', [row[0]])

                os_versions = []
                supported = False

                for android_v in c3:
                    if android_v[0] <= device_info.os_version <= android_v[1]:
                        supported = True
                        break

                c3.close()

                if supported:
                    op_info = OperationInfo(row[0], row[1], row[2], ', '.join(models), ', '.join(os_versions))
                    result.append(op_info)

            c2.close()
        c.close()

        return result

    def get_operation_exec_info(self, id_):
        result = {}
        c = self.conn.cursor()
        c.execute("""
                SELECT o.id, dst.extractor_name, o.inspector_name
                FROM operations AS o, data_source_types AS dst
                WHERE o.data_source_type_id = dst.id and o.id = ?
                """, [id_])

        row = c.fetchone()
        if row is not None:
            result['extractor_id'] = row[1].__str__()
            result['inspector_id'] = row[2].__str__()

            c2 = self.conn.cursor()
            c2.execute('SELECT param_name, param_value FROM data_source_params_values dspv WHERE dspv.operation_id = ?', [row[0]])

            param_values = {}

            for pv in c2:
                param_values[pv[0]] = pv[1]

            result['param_values'] = param_values
        return result

    def exists_data_type(self, data_type):
        c = self.conn.cursor()
        c.execute('SELECT 1 FROM data_types AS dt WHERE dt.name = ?', [data_type])

        row = c.fetchone()

        return row is not None

    def exists_data_source_type(self, data_source_type):
        c = self.conn.cursor()
        c.execute('SELECT 1 FROM data_source_types AS dst WHERE dst.name = ?', [data_source_type])

        row = c.fetchone()

        return row is not None

    def has_all_required_param_values(self, data_source):
        c = self.conn.cursor()
        c.execute("""
                SELECT param_name FROM data_source_types AS dst, required_params AS rp
                WHERE dst.id = rp.data_source_type_id and dst.name = ?
                """, [data_source.type_])

        for row in c:
            if not data_source.info.get(row[0]):
                return False
        return True

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
