# coding=utf-8
import hashlib
import os

import magic
from cybox.objects.file_object import File


def sha256_checksum(file_path, block_size=65536):
    sha256sum = hashlib.sha256()

    with open(file_path, 'rb') as fh:
        buf = fh.read(block_size)
        while len(buf) > 0:
            sha256sum.update(buf)
            buf = fh.read(block_size)

    return sha256sum.hexdigest()


def create_source_object(file_path, original_file_path):
    f = File()
    f.file_name = os.path.basename(file_path)
    f.file_extension = os.path.splitext(file_path)[1]
    f.file_path = original_file_path
    f.file_format = magic.from_file(file_path)
    f.size_in_bytes = os.path.getsize(file_path)
    f.sha256 = sha256_checksum(file_path)
    return f
