#!/usr/bin/python

import execute

class ExecuteCheck(execute.Execute):
    def __init__(self):
        super().__init__()

    def mainprocess(self, filename, testcase_number, show_detail):
        self._run_testcases(filename, testcase_number)
        self._display_check_result(filename, testcase_number, show_detail)
    