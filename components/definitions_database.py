# coding=utf-8
from os import path
import sqlite3
from model import OperationInfo


class DefinitionsDatabase(object):
    def __init__(self, db_file_name, create_db_script_path, insert_default_operations_script_path):
        db_file_path = db_file_name

        if not path.exists(db_file_path):
            # Create the db schema
            execute_sql_script(db_file_path, create_db_script_path)
            # Insert default operations
            execute_sql_script(db_file_path, insert_default_operations_script_path)

        self.conn = sqlite3.connect(db_file_path)
        # TODO: Close connection, somewhere.

    def query_operations_info(self, data_type, data_source, device_info):
        result = []
        c = self.conn.cursor()

        query = """
                SELECT o.id as id, dt.name as data_type, dst.name as data_source_type
                FROM operations AS o, data_types AS dt, data_source_types AS dst, device_models AS dm,
                     android_versions AS av
                WHERE o.data_type_id = dt.id AND o.data_source_type_id = dst.id AND o.id = dm.operation_id
                        AND o.id = av.operation_id
                """
        if data_type is not None:
            query += ' AND dt.name = {0}'.format(data_type)
        if data_source is not None:
            query += ' AND dst.name = {0}'.format(data_source.type_)
        if device_info.device_model is not None:
            query += ' AND dm.model_number = {0}'.format(device_info.device_model)
        if device_info.os_version is not None:
            query += ' AND {0} between av.from_version AND av.to_version)'.format(device_info.os_version)

        c.execute(query)

        data_source_params = data_source.info

        for row in c:
            op_id = row[0]
            c2 = self.conn.cursor()
            c2.execute("""
                    SELECT param_name, param_value
                    FROM data_source_param_values dtpv
                    WHERE dspv.operation_id = ?
                    """, [op_id])

            supported = True
            for pv in c2:
                if data_source_params.get(pv[0]) != pv[1]:
                    supported = False
                    break

            c2.close()

            if supported:
                # TODO: Buscar info de device_models y android_versions, y armar los OperationInfo
                pass

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

    def exists_operation(self, id_):
        c = self.conn.cursor()
        c.execute('SELECT 1 FROM operations AS o WHERE o.id = ?', [id_])

        row = c.fetchone()

        return row is not None

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
