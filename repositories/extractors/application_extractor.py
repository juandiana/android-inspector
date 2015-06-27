# coding=utf-8

import subprocess
from model.operation import Extractor

class ApplicationExtractor(Extractor):
    def execute(self, route, param_values):
        cmd = 'adb pull /data/data/' + param_values['package_name']

        try:
            subprocess.check_call(cmd, shell=True, cwd=route)
            return True
        except subprocess.CalledProcessError:
            print "Extraction failed."
            return False
