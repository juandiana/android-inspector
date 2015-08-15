CREATE TABLE data_types (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  name              TEXT,
  cybox_object_name TEXT
);

CREATE TABLE data_source_types (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  name           TEXT,
  extractor_name TEXT
);

CREATE TABLE required_params (
  data_source_type_id INTEGER NOT NULL REFERENCES data_source_types (id),
  param_name          TEXT,
  PRIMARY KEY (data_source_type_id, param_name)
);

CREATE TABLE operations (
  id                  INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  data_type_id        INTEGER NOT NULL REFERENCES data_types (id),
  data_source_type_id INTEGER NOT NULL REFERENCES data_source_types (id),
  inspector_name      TEXT
);

CREATE TABLE device_models (
  operation_id INTEGER NOT NULL REFERENCES operations (id),
  model_number TEXT,
  PRIMARY KEY (operation_id, model_number)
);

CREATE TABLE android_versions (
  operation_id INTEGER NOT NULL REFERENCES operations (id),
  from_version TEXT,
  to_version   TEXT,
  PRIMARY KEY (operation_id, from_version, to_version)
);

CREATE TABLE data_source_params_values (
  operation_id INTEGER NOT NULL REFERENCES operations (id),
  param_name   TEXT,
  param_value  TEXT,
  PRIMARY KEY (operation_id, param_name)
);
