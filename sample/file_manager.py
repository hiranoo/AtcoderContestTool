#!/usr/bin/python

import json
from singleton import Singleton
from language import Language

class FileManager:
    def __init__(self):
        self.conf = Singleton.get_instance().get_conf()
        with open (self.conf['env']['contest_conf_path'], 'r') as f:
            self.contest_conf = json.load(f)
        self.contest_name = self.contest_conf['contest_name']
        self.contest_dir_path = '{}/{}'.format(self.conf['env']['basedir_path'], self.contest_name)
        self.extention_language_dict = self.conf['code']['extention_language_dict']

    def _get_full_path(self, filename):
        return f'{self.contest_dir_path}/{filename}'

    def _get_relative_path(self, fullpath):
        return fullpath.replace(f'{self.contest_dir_path}/', '')

    def _get_language(self, path):
        if not path:
            return None
        if '.' in path:
            extention = (path.split('.'))[-1]
            if extention in self.extention_language_dict.keys():
                return Language[self.extention_language_dict[extention]]
        return None

    def _get_task_screen_name(self, relative_path):
        return '{}_{}'.format(self.contest_name, self._get_taskname(relative_path))

    def _get_taskname(self, relative_path):
        return (((relative_path.split('/'))[0]).split('.'))[0]

        
        