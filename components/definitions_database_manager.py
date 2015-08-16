# coding=utf-8
from abc import ABCMeta, abstractmethod
from os import path
import sqlite3

from model import OperationInfo, DataSource


class Filter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_join_clause(self):
        pass

    @abstractmethod
    def get_where_clause(self):
        pass


class DataTypeFilter(Filter):
    def __init__(self, dt):
        self.data_type = dt

    def get_join_clause(self):
        return 'JOIN data_types AS dt ON op.data_type_id = dt.id'

    def get_where_clause(self):
        return 'dt.name = "{0}"'.format(self.data_type)


class DataSourceTypeFilter(Filter):
    def __init__(self, dst):
        self.data_source_type = dst

    def get_join_clause(self):
        return 'JOIN data_source_types AS dst ON op.data_source_type_id = dst.id'

    def get_where_clause(self):
        return 'dst.name = "{0}"'.format(self.data_source_type)


class DeviceModelFilter(Filter):
    def __init__(self, dm):
        self.device_model = dm

    def get_join_clause(self):
        return 'JOIN device_models AS dm ON op.id = dm.operation_id'

    def get_where_clause(self):
        return 'dm.model_number = "{0}"'.format(self.device_model)


class AndroidVersionFilter(Filter):
    def __init__(self, os_version):
        self.os_version = os_version

    def get_join_clause(self):
        return 'JOIN android_versions AS av ON op.id = av.operation_id'

    def get_where_clause(self):
        return 'av.from_version <= "{0}" AND "{0}" <= av.to_version'.format(self.os_version)


class QueryMatchingOperationsBuilder(object):
    def __init__(self):
        self.filters = []

    def add_filter(self, f):
        self.filters.append(f)

    def build(self):
        query = 'SELECT op.id FROM operations AS op '
        joins = []
        wheres = []

        for f in self.filters:
            join = f.get_join_clause()
            joins.append(join)
            where = f.get_where_clause()
            wheres.append(where)

        if len(joins) > 0:
            query += ' '.join(joins)
        if len(wheres) > 0:
            query += ' WHERE ' + ' AND '.join(wheres)

        return query


class DefinitionsDatabaseManager(object):
    def __init__(self, db_file_name, create_db_script_path, insert_data_types_script_path,
                 insert_data_source_types_script_path, insert_operations_script_path):
        db_file_path = db_file_name

        if not path.exists(db_file_path):
            # Create the db schema
            execute_sql_script(db_file_path, create_db_script_path)
            # Insert default data_types
            execute_sql_script(db_file_path, insert_data_types_script_path)
            # Insert default data_source_types
            execute_sql_script(db_file_path, insert_data_source_types_script_path)
            # Insert default operations
            execute_sql_script(db_file_path, insert_operations_script_path)

        self.conn = sqlite3.connect(db_file_path)
        # TODO: Close connection, somewhere.

    def query_operations_info(self, data_type, data_source, device_info):
        """
        The data_type exists in definitions.db
        The data_source.type_ exists in definitions.db and has all the required params.
        The device_info contains a model and an os_version.
        :type data_type: string
        :type data_source: DataSource
        :type device_info: DeviceInfo
        :rtype : list(OperationInfo)
        """

        result = []
        c = self.conn.cursor()

        query_builder = QueryMatchingOperationsBuilder()

        if data_type:
            query_builder.add_filter(DataTypeFilter(data_type))
        if data_source:
            query_builder.add_filter(DataSourceTypeFilter(data_source.type_))
        if device_info:
            if device_info.device_model:
                query_builder.add_filter(DeviceModelFilter(device_info.device_model))
            if device_info.os_version:
                query_builder.add_filter(AndroidVersionFilter(device_info.os_version))

        query = query_builder.build()

        c.execute(query)

        if data_source is not None:
            data_source_params = data_source.info

            for row in c:
                op_id = row[0]

                c2 = self.conn.cursor()
                c2.execute("""
                        SELECT param_name, param_value
                        FROM data_source_params_values dspv
                        WHERE dspv.operation_id = ?
                        """, [op_id])

                supported = True

                for pv in c2:
                    if data_source_params.get(pv[0]) != pv[1]:
                        supported = False
                        break

                c2.close()

                if supported:
                    result.append(self.get_operation_info_by_id(op_id))

        else:
            for row in c:
                result.append(self.get_operation_info_by_id(row[0]))

        c.close()
        return result

    def get_operation_info_by_id(self, id_):
        """
        :type id_: int
        :rtype : OperationInfo
        """
        c1 = self.conn.cursor()
        c1.execute("""
                SELECT dt.name, dst.name, o.name
                FROM operations AS o, data_types AS dt, data_source_types AS dst
                WHERE o.data_type_id = dt.id AND o.data_source_type_id = dst.id AND o.id = ?
                """, [id_])

        res = c1.fetchone()
        data_type = res[0]
        data_source_type = res[1]
        op_name = res[2]

        c1.close()

        c2 = self.conn.cursor()
        c2.execute("""
                SELECT param_name, param_value
                FROM data_source_params_values dspv
                WHERE dspv.operation_id = ?
                """, [id_])

        param_values = {}
        for pv in c2:
            param_values[pv[0]] = pv[1]

        c2.close()

        c3 = self.conn.cursor()
        c3.execute('SELECT model_number FROM device_models WHERE operation_id = ?', [id_])

        supported_models = []
        for dm in c3:
            supported_models.append(dm[0])

        c3.close()

        c4 = self.conn.cursor()
        c4.execute('SELECT from_version, to_version FROM android_versions WHERE operation_id = ?', [id_])

        supported_os_versions = []
        for av in c4:
            supported_os_versions.append((av[0], av[1]))

        c4.close()

        return OperationInfo(op_name, data_type, DataSource(data_source_type, param_values),
                             supported_models, supported_os_versions)

    def get_operation_inspector_name(self, op_name):
        """
        :type op_name: string
        :rtype: string
        """
        c = self.conn.cursor()
        c.execute('SELECT o.inspector_name FROM operations AS o WHERE o.name = ?', [op_name])

        row = c.fetchone()
        if row is None:
            return None

        return row[0]

    def get_operation_exec_info(self, name):
        """
        :type name: string
        :rtype : extractor_id: string, inspector_id: string, params_values: dict(string)
        """
        extractor_id = ''
        inspector_id = ''
        param_values = {}

        c = self.conn.cursor()
        c.execute("""
                SELECT o.id, dst.extractor_name, o.inspector_name
                FROM operations AS o, data_source_types AS dst
                WHERE o.data_source_type_id = dst.id AND o.name = ?
                """, [name])

        row = c.fetchone()
        if row is not None:
            extractor_id = row[1]
            inspector_id = row[2]

            c2 = self.conn.cursor()
            c2.execute('SELECT param_name, param_value FROM data_source_params_values dspv WHERE dspv.operation_id = ?',
                       [row[0]])

            for pv in c2:
                param_values[pv[0]] = pv[1]

            c2.close()
        c.close()

        return extractor_id, inspector_id, param_values

    def exists_operation(self, name):
        """
        :type name: string
        :rtype : bool
        """
        c = self.conn.cursor()
        c.execute('SELECT 1 FROM operations AS o WHERE o.name = ?', [name])

        row = c.fetchone()

        c.close()

        return row is not None

    def exists_data_type(self, name):
        """
        :type name: string
        :rtype : bool
        """
        c = self.conn.cursor()
        c.execute('SELECT 1 FROM data_types AS dt WHERE dt.name = ?',
                  [name])

        row = c.fetchone()

        c.close()

        return row is not None

    def exists_data_source_type(self, data_source_type):
        """
        :type data_source_type: string
        :rtype : bool
        """
        c = self.conn.cursor()
        c.execute('SELECT 1 FROM data_source_types AS dst WHERE dst.name = ?',
                  [data_source_type])

        row = c.fetchone()

        c.close()

        return row is not None

    def has_all_required_param_values(self, data_source):
        """
        :type data_source: DataSource
        :rtype : bool
        """
        c = self.conn.cursor()
        c.execute("""
                SELECT param_name FROM data_source_types AS dst, required_params AS rp
                WHERE dst.id = rp.data_source_type_id AND dst.name = ?
                """, [data_source.type_])

        for row in c:
            if not data_source.info.get(row[0]):
                return False

        c.close()

        return True

    def add_operation(self, name, data_type_name, data_source_type_name, inspector_name, param_values, device_models,
                      android_versions):
        """
        :type name: string
        :type data_type_name: string
        :type data_source_type_name: string
        :type inspector_name: string
        :type param_values: dict(string)
        :type device_models: list(string)
        :type android_versions: list((string, string))
        :rtype: bool
        """

        # Get data_type id using the data_type_name
        query = 'SELECT id FROM data_types WHERE name = "{0}"'.format(data_type_name)
        c = self.conn.cursor()
        c.execute(query)

        row = c.fetchone()

        if row is None:
            raise ValueError("'{0}' is not a defined DataType.".format(data_type_name))

        dt_id = row[0]

        # Get data_source_type id using the data_source_type_name
        query = 'SELECT id FROM data_source_types WHERE name = "{0}"'.format(data_source_type_name)

        c.execute(query)

        row = c.fetchone()

        if row is None:
            raise ValueError("'{0}' is not a defined DataSourceType.".format(data_source_type_name))

        dst_id = row[0]

        # Insert a new row in operations table
        insert = """
                INSERT INTO operations (name, data_type_id, data_source_type_id, inspector_name)
                VALUES ("{0}", "{1}", "{2}", "{3}")
                """.format(name, dt_id, dst_id, inspector_name)

        try:
            c.execute(insert)
        except sqlite3.IntegrityError:
            self.conn.rollback()
            raise RuntimeError("The opeartion \''{0}'\' could not be added.".format(name))

        # Get the id of the new operation
        op_id = c.lastrowid

        # Insert the param_values
        insert = """
                INSERT INTO data_source_params_values (operation_id, param_name, param_value)
                VALUES ("{0}", "{1}", "{2}")
                """

        for key in param_values:
            try:
                c.execute(insert.format(op_id, key, param_values[key]))
            except sqlite3.IntegrityError:
                self.conn.rollback()
                raise RuntimeError(
                    "The param_value \''{0}':'{1}'\' could not be inserted.".format(key, param_values[key]))

        # Insert the device_models
        insert = 'INSERT INTO device_models (operation_id, model_number) VALUES ("{0}", "{1}")'

        for dm in device_models:
            try:
                c.execute(insert.format(op_id, dm))
            except sqlite3.IntegrityError:
                self.conn.rollback()
                raise RuntimeError('The device_model \'"{0}"\' could not be inserted.'.format(dm))

        # Insert the android_versions
        insert = """
                INSERT INTO android_versions (operation_id, from_version, to_version)
                VALUES ("{0}", "{1}", "{2}")
                """

        for av in android_versions:
            try:
                c.execute(insert.format(op_id, av[0], av[1]))
            except sqlite3.IntegrityError:
                self.conn.rollback()
                raise RuntimeError(
                    'The android_version \'("{0}"-"{1}")\' could not be inserted.'.format(av[0], av[1]))

        self.conn.commit()
        c.close()

        return True

    def remove_operation(self, name):
        """
        :type name: string
        :rtype: bool
        """

        # Get operation id
        query = 'SELECT id FROM operations WHERE name = "{0}"'.format(name)
        c = self.conn.cursor()
        c.execute(query)

        row = c.fetchone()

        if row is None:
            raise ValueError("'{0}' is not a defined Operation.".format(name))

        op_id = row[0]

        deletes = """
                DELETE FROM device_models WHERE operation_id = '{0}';
                DELETE FROM android_versions WHERE operation_id = '{0}';
                DELETE FROM data_source_params_values WHERE operation_id = '{0}';
                DELETE FROM operations WHERE id = '{0}';
                """.format(op_id)

        try:
            c.executescript(deletes)
        except sqlite3.IntegrityError:
            self.conn.rollback()
            RuntimeError("The operation '{0}' could not be deleted.".format(name))

        self.conn.commit()
        c.close()
        return True

    def add_data_type(self, name, cybox_object_name):
        """
        :type name:string
        :type cybox_object_name: string
        :rtype: bool
        """
        query = 'SELECT 1 FROM data_types dt WHERE dt.name = "{0}"'.format(name)

        c = self.conn.cursor()
        c.execute(query)
        row = c.fetchone()

        if row is not None:
            raise ValueError("The data_type '{0}' already exists.".format(name))

        insert = """
                INSERT INTO data_types (name, cybox_object_name)
                VALUES ("{0}", "{1}")
                """.format(name, cybox_object_name)

        try:
            c.execute(insert)
        except sqlite3.IntegrityError:
            self.conn.rollback()
            raise RuntimeError("The data_type '{0}' could not be added.".format(name))

        self.conn.commit()
        c.close()
        return True

    def remove_data_type(self, name):
        """
        :type name: string
        :rtype: bool
        """
        # Check if the data_type exists
        query = """
                SELECT 1 FROM data_types dt WHERE dt.name = '{0}'
                """.format(name)

        c = self.conn.cursor()
        c.execute(query)
        row = c.fetchone()

        if row is None:
            raise ValueError("'{0}' is not a defined DataType.".format(name))

        # Check if there are operations using this data_type
        query = """
                SELECT 1 FROM operations o, data_types dt
                WHERE o.data_type_id == dt.id AND dt.name = '{0}'
                """.format(name)

        c.execute(query)
        row = c.fetchone()

        if row is not None:
            raise ValueError("The data_type '{0}' cannot be deleted. "
                             "There are existing operations to extract this data_type.".format(name))

        # Delete the data_type
        delete = "DELETE FROM data_types WHERE name = '{0}'".format(name)

        try:
            c.execute(delete)
        except sqlite3.IntegrityError:
            self.conn.rollback()
            raise RuntimeError("The data_type '{0}' could not be deleted.".format(name))

        self.conn.commit()
        c.close()
        return True

    def add_data_source_type(self, name, extractor_name, required_params):
        # Check if the data_source_type already exists.
        """
        :type name: string
        :type extractor_name: string
        :type required_params: dict(string)
        :rtype : bool
        """
        query = 'SELECT 1 FROM data_source_types dt WHERE dt.name = "{0}"'.format(name)

        c = self.conn.cursor()
        c.execute(query)
        row = c.fetchone()

        if row is not None:
            raise ValueError("The data_source_type '{0}' already exists.".format(name))

        # Insert the data_source_type and its param_values.
        query = """
                INSERT INTO data_source_types (name, extractor_name)
                VALUES ("{0}", "{1}")
                """.format(name, extractor_name)

        try:
            c.execute(query)

            dst_id = c.lastrowid

            query = """
                    INSERT INTO required_params (data_source_type_id, param_name)
                    VALUES ("{0}", "{1}")
                    """

            for p in required_params:
                c.execute(query.format(dst_id, p))
        except sqlite3.IntegrityError:
            self.conn.rollback()
            raise RuntimeError("The data_source_type '{0}' could not be added.".format(name))

        self.conn.commit()
        c.close()
        return True

    def remove_data_source_type(self, name):
        # Check if the data_source_type exists.
        """
        :type name: string
        :rtype : bool
        """
        query = """
                SELECT 1 FROM data_source_types dst WHERE dst.name = '{0}'
                """.format(name)

        c = self.conn.cursor()
        c.execute(query)
        row = c.fetchone()

        if row is None:
            raise ValueError("'{0}' is not a defined DataSourceType.".format(name))

        # Check if there are operations using this data_type
        query = """
                SELECT 1 FROM operations o, data_source_types dst
                WHERE o.data_source_type_id == dst.id AND dst.name = '{0}'
                """.format(name)

        c = self.conn.cursor()
        c.execute(query)
        row = c.fetchone()

        if row is not None:
            raise ValueError("The data_source_type '{0}' cannot be deleted. "
                             "There are existing operations to extract this data_source_type.".format(name))

        # Get data_source_type id
        query = 'SELECT id FROM data_source_types WHERE name = "{0}"'.format(name)
        c = self.conn.cursor()
        c.execute(query)

        row = c.fetchone()

        if row is None:
            raise ValueError("'{0}' is not a defined DataSourceType.".format(name))

        dst_id = row[0]

        # Delete the data_source_type
        try:
            c.execute("DELETE FROM required_params WHERE data_source_type_id = '{0}'".format(dst_id))
            c.execute("DELETE FROM data_source_types WHERE name = '{0}'".format(name))
        except sqlite3.IntegrityError:
            self.conn.rollback()
            raise RuntimeError("The data_source_type '{0}' could not be deleted.".format(name))

        self.conn.commit()
        c.close()
        return True


def execute_sql_script(db_file_path, script_file_path):
    f = open(script_file_path, 'r')
    with f:
        sql_statements = f.read()
    conn = sqlite3.connect(db_file_path)
    with conn:
        cursor = conn.cursor()
        cursor.executescript(sql_statements)
        cursor.close()
