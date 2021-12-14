#!/usr/bin/python

""" 
Template Method Pattern + Adapter Pattern
"""

from abc import ABCMeta, abstractmethod
from code_manager import CodeManager

class Execute(metaclass=ABCMeta):
    def __init__(self):
        self.impl = CodeManager()

    def execute(self, filename=None, testcase_number=None, show_detail=True):
        try:
            filename, preprocess_is_necessary = self.__search_code(filename)
            if not filename:
                print('No file was found.')
                return
            print('Searched code: ', filename, preprocess_is_necessary)
            if preprocess_is_necessary and self.__preprocess(filename):
                print('Compile done')
            self.mainprocess(filename, testcase_number, show_detail)
        except e:
            print(e)

    def __search_code(self, filename):
        return self.impl.search_code(filename)

    def __preprocess(self, filename):
        return self.impl.preprocess(filename)

    def _run_testcases(self, filename, testcase_number):
        print('run testcases')
        return self.impl.run_testcases(filename, testcase_number)

    def _display_check_result(self, filename, testcase_number, show_detail):
        print('display check result')
        return self.impl.display_check_result(filename, testcase_number, show_detail)

    def _submit_code(self, filename, show_detail):
        print('submit code')
        return self.impl.submit_code(filename, show_detail)

    @abstractmethod
    def mainprocess(self, filename, testcase_number, show_detail):
        pass

    