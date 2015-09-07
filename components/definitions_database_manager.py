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


class MatchingOperationsQueryBuilder(object):
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


def execute_sql_script(db_file_path, script_file_path):
    with open(script_file_path, 'r') as f:
        sql_statements = f.read()
        with sqlite3.connect(db_file_path) as conn:
            conn.executescript(sql_statements)


class DefinitionsDatabaseManager(object):
    def __init__(self, db_file_name, create_db_script_path, insert_data_types_script_path,
                 insert_data_source_types_script_path, insert_operations_script_path):
        self.db_file_path = db_file_name

        if not path.exists(self.db_file_path):
            execute_sql_script(self.db_file_path, create_db_script_path)
            execute_sql_script(self.db_file_path, insert_data_types_script_path)
            execute_sql_script(self.db_file_path, insert_data_source_types_script_path)
            execute_sql_script(self.db_file_path, insert_operations_script_path)

    def query_operations_info(self, data_type, data_source, device_info):
        """
        The data_type exists in definitions.db
        The data_source.type_ exists in definitions.db and has all the required params.
        The device_info contains a model and an os_version.
        :param data_type: string or None
        :param data_source: DataSource or None
        :param device_info: DeviceInfo
        :rtype: list[OperationInfo]

        """
        result = []
        with sqlite3.connect(self.db_file_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            query_builder = MatchingOperationsQueryBuilder()

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
                    op_id = row['id']

                    c2 = conn.cursor()
                    c2.execute(
                        """
                        SELECT param_name, param_value
                        FROM data_source_params_values dspv
                        WHERE dspv.operation_id = ?
                        """, [op_id]
                    )

                    supported = True

                    for pv in c2:
                        if data_source_params.get(pv['param_name']) != pv['param_value']:
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
        :param id_: int
        :rtype: OperationInfo

        """
        with sqlite3.connect(self.db_file_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute(
                """
                SELECT dt.name AS dt_name, dst.name AS dst_name, o.name AS o_name
                FROM operations AS o, data_types AS dt, data_source_types AS dst
                WHERE o.data_type_id = dt.id AND o.data_source_type_id = dst.id AND o.id = ?
                """, [id_]
            )

            res = c.fetchone()
            data_type = res['dt_name']
            data_source_type = res['dst_name']
            op_name = res['o_name']

            c.execute(
                """
                SELECT param_name, param_value
                FROM data_source_params_values dspv
                WHERE dspv.operation_id = ?
                """, [id_]
            )

            param_values = {}
            for pv in c:
                param_values[pv['param_name']] = pv['param_value']

            c.execute('SELECT model_number FROM device_models WHERE operation_id = ?', [id_])

            supported_models = []
            for dm in c:
                supported_models.append(dm['model_number'])

            c.execute('SELECT from_version, to_version FROM android_versions WHERE operation_id = ?', [id_])

            supported_os_versions = []
            for av in c:
                supported_os_versions.append((av['from_version'], av['to_version']))

            c.close()

            return OperationInfo(op_name, data_type, DataSource(data_source_type, param_values),
                                 supported_models, supported_os_versions)

    def get_data_type_custom_cybox_object_name(self, dt_name):
        """
        :param dt_name: string
        :rtype: string

        """
        with sqlite3.connect(self.db_file_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT dt.cybox_object_name AS name FROM data_types AS dt WHERE dt.name = ?', [dt_name])

            row = c.fetchone()
            if row is None:
                return None

            return row['name']

    def get_data_source_type_extractor_name(self, dst_name):
        """
        :param dst_name: string
        :rtype: string

        """
        with sqlite3.connect(self.db_file_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT dst.extractor_name AS name FROM data_source_types AS dst WHERE dst.name = ?', [dst_name])

            row = c.fetchone()
            if row is None:
                return None

            return row['name']

    def get_operation_inspector_name(self, op_name):
        """
        :param op_name: string
        :rtype: string

        """
        with sqlite3.connect(self.db_file_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT o.inspector_name AS name FROM operations AS o WHERE o.name = ?', [op_name])

            row = c.fetchone()
            if row is None:
                return None

            return row['name']

    def get_operation_exec_info(self, name):
        """
        :param name: string
        :rtype: (string, string, dict[string])

        """
        extractor_id = ''
        inspector_id = ''
        param_values = {}

        with sqlite3.connect(self.db_file_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute(
                """
                SELECT o.id AS id, dst.extractor_name AS ext_name, o.inspector_name AS ins_name
                FROM operations AS o, data_source_types AS dst
                WHERE o.data_source_type_id = dst.id AND o.name = ?
                """, [name]
            )

            row = c.fetchone()
            if row is not None:
                extractor_id = row['ext_name']
                inspector_id = row['ins_name']

                c2 = conn.cursor()
                c2.execute('SELECT param_name, param_value '
                           'FROM data_source_params_values dspv '
                           'WHERE dspv.operation_id = ?', [row['id']])

                for pv in c2:
                    param_values[pv['param_name']] = pv['param_value']

                c2.close()
            c.close()

        return extractor_id, inspector_id, param_values

    def exists_operation(self, name):
        """
        :param name: string
        :rtype: bool

        """
        with sqlite3.connect(self.db_file_path) as conn:
            c = conn.cursor()
            c.execute('SELECT 1 FROM operations AS o WHERE o.name = ?', [name])

            row = c.fetchone()

            c.close()

            return row is not None

    def exists_data_type(self, name):
        """
        :param name: string
        :rtype: bool

        """
        with sqlite3.connect(self.db_file_path) as conn:
            c = conn.cursor()
            c.execute('SELECT 1 FROM data_types AS dt WHERE dt.name = ?',
                      [name])

            row = c.fetchone()

            c.close()

            return row is not None

    def exists_data_source_type(self, data_source_type):
        """
        :param data_source_type: string
        :rtype: bool

        """
        with sqlite3.connect(self.db_file_path) as conn:
            c = conn.cursor()
            c.execute('SELECT 1 FROM data_source_types AS dst WHERE dst.name = ?',
                      [data_source_type])

            row = c.fetchone()

            c.close()

            return row is not None

    def has_all_required_param_values(self, data_source):
        """
        :param data_source: DataSource
        :rtype: bool

        """
        with sqlite3.connect(self.db_file_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("""
                    SELECT param_name FROM data_source_types AS dst, required_params AS rp
                    WHERE dst.id = rp.data_source_type_id AND dst.name = ?
                    """, [data_source.type_])

            if data_source.info is None and c.fetchone() is not None:
                return False

            for row in c:
                if not data_source.info.get(row['param_name']):
                    return False

            c.close()

            return True

    def add_operation(self, name, data_type_name, data_source_type_name, inspector_name, param_values, device_models,
                      android_versions):
        """
        :param name: string
        :param data_type_name: string
        :param data_source_type_name: string
        :param inspector_name: string
        :param param_values: dict[string]
        :param device_models: list[string]
        :param android_versions: list[(string, string)]
        :rtype: bool

        """
        with sqlite3.connect(self.db_file_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            # Get data_type id using the data_type_name
            c.execute('SELECT id FROM data_types WHERE name = ?', [data_type_name])

            row = c.fetchone()

            if row is None:
                raise ValueError("'{0}' is not a defined DataType.".format(data_type_name))

            dt_id = row['id']

            # Get data_source_type id using the data_source_type_name
            c.execute('SELECT id FROM data_source_types WHERE name = ?', [data_source_type_name])

            row = c.fetchone()

            if row is None:
                raise ValueError("'{0}' is not a defined DataSourceType.".format(data_source_type_name))

            dst_id = row['id']

            # Insert a new row in operations table
            try:
                c.execute(
                    """
                    INSERT INTO operations (name, data_type_id, data_source_type_id, inspector_name)
                    VALUES (?, ?, ?, ?)
                    """,
                    [name, dt_id, dst_id, inspector_name]
                )
            except sqlite3.IntegrityError:
                conn.rollback()
                raise RuntimeError("The opeartion \''{0}'\' could not be added.".format(name))

            # Get the id of the new operation
            op_id = c.lastrowid

            # Insert the param_values
            for key in param_values:
                try:
                    c.execute(
                        """
                        INSERT INTO data_source_params_values (operation_id, param_name, param_value)
                        VALUES (?, ?, ?)
                        """,
                        [op_id, key, param_values[key]]
                    )
                except sqlite3.IntegrityError:
                    conn.rollback()
                    raise RuntimeError(
                        "The param_value \''{0}':'{1}'\' could not be inserted.".format(key, param_values[key]))

            # Insert the device_models.
            for dm in device_models:
                try:
                    c.execute(
                        """
                        INSERT INTO device_models (operation_id, model_number)
                        VALUES ('{0}', '{1}')
                        """.format(op_id, dm))
                except sqlite3.IntegrityError:
                    conn.rollback()
                    raise RuntimeError('The device_model \'"{0}"\' could not be inserted.'.format(dm))

            # Insert the android_versions.
            for av in android_versions:
                try:
                    c.execute(
                        """
                        INSERT INTO android_versions (operation_id, from_version, to_version)
                        VALUES (?, ?, ?)
                        """,
                        [op_id, av[0], av[1]]
                    )
                except sqlite3.IntegrityError:
                    conn.rollback()
                    raise RuntimeError(
                        'The android_version \'("{0}"-"{1}")\' could not be inserted.'.format(av[0], av[1]))

            conn.commit()
            c.close()

    def remove_operation(self, name):
        """
        :param name: string
        :rtype: bool

        """
        with sqlite3.connect(self.db_file_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            # Get operation id
            c.execute('SELECT id FROM operations WHERE name = ?', [name])

            row = c.fetchone()

            if row is None:
                raise ValueError("'{0}' is not a defined Operation.".format(name))

            op_id = row['id']
            try:
                c.execute('DELETE FROM device_models WHERE operation_id = ?', [op_id])
                c.execute('DELETE FROM android_versions WHERE operation_id = ?', [op_id])
                c.execute('DELETE FROM data_source_params_values WHERE operation_id = ?', [op_id])
                c.execute('DELETE FROM operations WHERE id = ?', [op_id])
            except sqlite3.IntegrityError:
                conn.rollback()
                RuntimeError("The operation '{0}' could not be deleted.".format(name))

            conn.commit()
            c.close()

    def add_data_type(self, name, cybox_object_name):
        """
        :param name:string
        :param cybox_object_name: string
        :rtype: bool

        """
        with sqlite3.connect(self.db_file_path) as conn:
            c = conn.cursor()

            # Check if the data_type already exists.
            c.execute('SELECT 1 FROM data_types dt WHERE dt.name = ?', [name])
            row = c.fetchone()

            if row is not None:
                raise ValueError("The data_type '{0}' already exists.".format(name))

            try:
                c.execute(
                    """
                    INSERT INTO data_types (name, cybox_object_name)
                    VALUES (?, ? )
                    """,
                    [name, cybox_object_name]
                )
            except sqlite3.IntegrityError:
                conn.rollback()
                raise RuntimeError("The data_type '{0}' could not be added.".format(name))

            conn.commit()
            c.close()

    def remove_data_type(self, name):
        """
        :param name: string
        :rtype: bool

        """
        with sqlite3.connect(self.db_file_path) as conn:
            c = conn.cursor()

            # Check if the data_type exists
            c.execute('SELECT 1 FROM data_types dt WHERE dt.name = ?', [name])
            row = c.fetchone()

            if row is None:
                raise ValueError("'{0}' is not a defined DataType.".format(name))

            # Check if there are operations using this data_type
            c.execute(
                """
                SELECT 1 FROM operations o, data_types dt
                WHERE o.data_type_id == dt.id AND dt.name = ?
                """, [name]
            )

            row = c.fetchone()
            if row is not None:
                raise ValueError("The data_type '{0}' cannot be deleted. "
                                 "There are existing operations to extract this data_type.".format(name))

            # Delete the data_type
            try:
                c.execute('DELETE FROM data_types WHERE name = ?', [name])
            except sqlite3.IntegrityError:
                conn.rollback()
                raise RuntimeError("The data_type '{0}' could not be deleted.".format(name))

            conn.commit()
            c.close()

    def add_data_source_type(self, name, extractor_name, required_params):
        """
        :param name: string
        :param extractor_name: string
        :param required_params: dict[string]
        :rtype: bool

        """
        with sqlite3.connect(self.db_file_path) as conn:
            c = conn.cursor()

            # Check if the data_source_type already exists.
            c.execute('SELECT 1 FROM data_source_types dt WHERE dt.name = ?', [name])

            row = c.fetchone()
            if row is not None:
                raise ValueError("The data_source_type '{0}' already exists.".format(name))

            # Insert the data_source_type and its param_values.
            try:
                c.execute(
                    """
                    INSERT INTO data_source_types (name, extractor_name)
                    VALUES (?, ?)
                    """,
                    [name, extractor_name]
                )

                dst_id = c.lastrowid
                for p in required_params:
                    c.execute(
                        """
                        INSERT INTO required_params (data_source_type_id, param_name)
                        VALUES (?, ?)
                        """,
                        [dst_id, p]
                    )
            except sqlite3.IntegrityError:
                conn.rollback()
                raise RuntimeError("The data_source_type '{0}' could not be added.".format(name))

            conn.commit()
            c.close()

    def remove_data_source_type(self, name):
        """
        :param name: string
        :rtype: bool

        """
        with sqlite3.connect(self.db_file_path) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()

            # Check if the data_source_type exists.
            c.execute('SELECT 1 FROM data_source_types dst WHERE dst.name = ?', [name])
            row = c.fetchone()

            if row is None:
                raise ValueError("'{0}' is not a defined DataSourceType.".format(name))

            # Check if there are operations using this data_type
            c.execute(
                """
                SELECT 1 FROM operations o, data_source_types dst
                WHERE o.data_source_type_id == dst.id AND dst.name = ?
                """, [name]
            )

            row = c.fetchone()

            if row is not None:
                raise ValueError("The data_source_type '{0}' cannot be deleted. "
                                 "There are existing operations to extract this data_source_type.".format(name))

            # Get data_source_type id
            c.execute('SELECT id FROM data_source_types WHERE name = ?', [name])

            row = c.fetchone()

            if row is None:
                raise ValueError("'{0}' is not a defined DataSourceType.".format(name))

            dst_id = row['id']

            # Delete the data_source_type
            try:
                c.execute('DELETE FROM required_params WHERE data_source_type_id = ?', [dst_id])
                c.execute('DELETE FROM data_source_types WHERE name = ?', [name])
            except sqlite3.IntegrityError:
                conn.rollback()
                raise RuntimeError("The data_source_type '{0}' could not be deleted.".format(name))

            conn.commit()
            c.close()
