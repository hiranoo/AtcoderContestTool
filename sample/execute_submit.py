#!/usr/bin/python

from execute import Execute

class ExecuteSubmit(Execute):
    def __init__(self):
        super().__init__()

    def mainprocess(self, filename, testcase_number, show_detail):
        self._submit_code(filename, show_detail) 
