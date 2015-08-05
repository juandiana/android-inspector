# coding=utf-8
import hashlib
import os
import subprocess
import sqlite3
import re

import magic
from cybox.objects.file_object import File

from model import OperationError


def sha256_checksum(file_path, block_size=65536):
    sha256sum = hashlib.sha256()

    with open(file_path, 'rb') as fh:
        buf = fh.read(block_size)
        while len(buf) > 0:
            sha256sum.update(buf)
            buf = fh.read(block_size)

    return sha256sum.hexdigest()


def get_source_object(file_path, source_objects):
    for o in source_objects:
        if o.file_path == file_path:
            return o
    return None


def create_file_object(file_path, original_file_path):
    f = File()
    f.file_name = os.path.basename(file_path)
    f.file_extension = os.path.splitext(file_path)[1]
    f.file_path = original_file_path
    f.file_format = magic.from_file(file_path)
    f.size_in_bytes = os.path.getsize(file_path)
    f.sha256 = sha256_checksum(file_path)
    return f


def execute_query(db_file_path, sql_query):
    if not os.path.exists(db_file_path):
        raise OperationError('Inspection failed: {0} not found.'.format(db_file_path))
    conn = sqlite3.connect(db_file_path)
    # Access columns by name instead of by index
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try:
        c.execute(sql_query)
    except (sqlite3.OperationalError, sqlite3.DatabaseError) as error:
        # TODO: Log the error message.
        raise OperationError('Inspection failed: Could not perform SQL query on {0}.'.format(db_file_path))
    return c, conn


def get_app_version_name(apk_file_path):
    command = ['aapt', 'dump', 'badging', apk_file_path]
    try:
        p = subprocess.Popen(command, cwd=os.getcwd(), stdout=subprocess.PIPE)
        for line in p.stdout:
            if line.__contains__('versionName='):
                match = re.search("versionName='(.*?)'", line)
                return match.group(1)
    except subprocess.CalledProcessError:
        raise
