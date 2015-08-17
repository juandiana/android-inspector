# coding=utf-8
import argparse
import os
from util import adb


def load_data_set(data_set_path):
    device = adb.get_device()

    for f in os.listdir(data_set_path):
        source = os.path.join(data_set_path, f)
        destination = '/data/data/' + f

        try:
            device.shell(['rm', '-r', destination])
        except RuntimeError:
            pass

        print "Pushing package '{0}'".format(f)
        device.push(source, destination)

    print "The data set was pushed successfully."

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Loads the data set to the android emulator.')
    parser.add_argument('--ds', required=True, help='specify the data set')

    args = parser.parse_args()

    load_data_set(args.ds)
