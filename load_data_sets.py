#!/usr/bin/env python
# coding=utf-8
import argparse
import os
import shutil
import tarfile

from util import adb


def load_data_set(data_set_name):
    data_set_dir_path = os.path.join('datasets', data_set_name)
    data_set_tar_path = data_set_dir_path + '.tar'
    with tarfile.open(data_set_tar_path) as tar:
        tar.extractall(path=data_set_dir_path)

    try:
        device = adb.get_device()

        for file_name in os.listdir(data_set_dir_path):
            file_path = os.path.join(data_set_dir_path, file_name)
            if os.path.isfile(file_path) and file_name.endswith('.apk'):
                print "Installing '{0}' into the device...".format(file_name)
                package_name = os.path.splitext(file_name)[0]
                if '-' in package_name:
                    package_name = package_name.partition('-')[0]
                device.uninstall(package_name)
                device.install(file_path, replace=True)

        for file_name in os.listdir(data_set_dir_path):
            file_path = os.path.join(data_set_dir_path, file_name)
            if os.path.isdir(file_path):
                try:
                    device.shell(['rm', '-r', '/data/data/' + file_name])
                except RuntimeError:
                    pass

                print "Pushing '{0}' data into the device...".format(file_name)
                device.push(file_path, '/data/data/' + file_name)
    finally:
        shutil.rmtree(data_set_dir_path)

    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Loads the data set to the android emulator.')
    parser.add_argument('--ds', required=True, help='specify the data set')

    args = parser.parse_args()

    success = load_data_set(args.ds)
    if success:
        print "The data set was pushed successfully."
