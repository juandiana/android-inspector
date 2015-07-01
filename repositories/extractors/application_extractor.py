# coding=utf-8

import subprocess
from model.operation import Extractor, OperationError


class ApplicationExtractor(Extractor):
    def execute(self, route, param_values):
        cmd = 'adb pull /data/data/' + param_values['package_name']

        try:
            p = subprocess.Popen(cmd, shell=True, bufsize=64, stdin=subprocess.PIPE,
                                 stderr=subprocess.PIPE, stdout=subprocess.PIPE)

            for line in p.stdout:
                print("[adb]" + str(line.rstrip()))
                p.stdout.flush()
        except subprocess.CalledProcessError:
            raise OperationError('Extraction failed.')
