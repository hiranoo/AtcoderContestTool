#!/usr/bin/python

import json
from singleton import Singleton
from language import Language

class FileManager:
    def __init__(self):
        self.__conf = Singleton.get_instance().get_conf()
        with open (self.__conf['env']['contest_conf_path'], 'r') as f:
            self.__contest_conf = json.load(f)
        self.__contest_name = self.__contest_conf['contest_name']
        self.__contest_dir_path = '{}/{}'.format(self.__conf['env']['basedir_path'], self.__contest_name)
        self.__testcase_dir_path = '{}/{}'.format(self.__contest_dir_path, self.__conf['env']['testcase_dir_name'])
        self.__extention_language_dict = self.__conf['code']['extention_language_dict']

    def _get_full_path(self, filename):
        return f'{self.__contest_dir_path}/{filename}'

    def _get_relative_path(self, fullpath):
        return fullpath.replace(f'{self.__contest_dir_path}/', '')

    def _get_language(self, path):
        if not path:
            return None
        if '.' in path:
            extention = (path.split('.'))[-1]
            if extention in self.__extention_language_dict.keys():
                return Language[self.__extention_language_dict[extention]]
        return None

    def _get_task_screen_name(self, relative_path):
        return '{}_{}'.format(self.__contest_name, self._get_taskname(relative_path)).replace('-', '_')

    def _get_taskname(self, relative_path):
        return (((relative_path.split('/'))[0]).split('.'))[0].replace('-', '_')

    def _create_testcase_path(self, taskname, testcase_number, in_or_out):
        return '{}/{}_{}_{}.txt'.format(self.__testcase_dir_path, taskname, testcase_number, in_or_out)

        
        