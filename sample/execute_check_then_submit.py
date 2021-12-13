#!/usr/bin/python

from execute import Execute

class ExecuteCheckThenSubmit(Execute):
    def __init__(self):
        super().__init__()

    def mainprocess(self, filename, testcase_number, show_detail):
        perfect = self._run_testcases(filename, testcase_number)
        self._display_check_result(filename, testcase_number, show_detail)
        if perfect:
            self._submit_code(filename)
    