#!/usr/bin/python

import execute

class ExecuteDisplay(execute.Execute):
    def __init__(self):
        super().__init__()

    def mainprocess(self, filename, testcase_number, show_detail):
        self._display_check_result(filename, testcase_number, show_detail)