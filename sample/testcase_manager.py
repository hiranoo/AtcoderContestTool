#!/usr/bin/python
# coding: utf-8

import os
import sys
import glob
import shutil
import time
import json
from bs4 import BeautifulSoup
import multiprocessing as mp

from singleton import Singleton
from file_manager import FileManager
from session_manager import SessionManager

class TestCaseManager(FileManager):
    def __init__(self):
        self.__conf = Singleton.get_instance().get_conf()
        try:
            with open (self.__conf['env']['contest_conf_path'], 'r') as f:
                self.__contest_conf = json.load(f)
        except:
            print('No contest is registered yet. Please register it.')
            sys.exit(0)
        self.__contest_name = self.__contest_conf['contest_name']
        self.__contest_page_url = '{}/contests/{}'.format(self.__conf['atcoder']['atcoder_top_url'], self.__contest_name)
        self.__contest_dir_path = '{}/{}'.format(self.__conf['env']['basedir_path'], self.__contest_name)
        self.__testcase_dir_path = '{}/{}'.format(self.__contest_dir_path, self.__conf['env']['testcase_dir_name'])
        self.__session_manager_instance = SessionManager()
        super().__init__()

    def fetch_and_save_testcases(self):
        os.makedirs(self.__testcase_dir_path, exist_ok=True)
        for url in self.__scrape_task_url_list():
            inputs, outputs = self.__scrape_testcases(url)
            if len(inputs) != len(outputs):
                print(f'Cannot fetch testcases from {url}')
                continue
            
            taskname = (url.split('_'))[-1]
            for i in range(len(inputs)):
                with open(self._create_testcase_path(taskname, i+1, 'in'), 'w') as f: f.write(inputs[i])
                with open(self._create_testcase_path(taskname, i+1, 'out'), 'w') as f: f.write(outputs[i])

            self.__copy_template_code(taskname)

    def __scrape_task_url_list(self):
        page = self.__fetch_page_html(f'{self.__contest_page_url}/tasks')
        task_table = page.find('tbody').find_all('a')
        task_url_list = ['{}{}'.format(self.__conf['atcoder']['atcoder_top_url'], tag.get('href')) for i, tag in enumerate(task_table) if i%3 == 0]
        return task_url_list

    def __scrape_testcases(self, url):
        page = self.__fetch_page_html(url)
        parts = page.select('div.part')
        inputs = []
        outputs = []
        for part in parts:
            if '入力例' in part.text:
                if part.find('pre') is None:
                    inputs = []
                    outputs = []
                    break
                inputs.append((part.find('pre').text).lstrip('\r\n'))
            if '出力例' in part.text:
                if part.find('pre') is None:
                    inputs = []
                    outputs = []
                    break
                outputs.append((part.find('pre')).text.lstrip('\r\n'))

        if len(inputs) == 0:
            print(f'Could not fetch sample data from {url}')
        return inputs, outputs

    def __fetch_page_html(self, url):
        self.__session_manager_instance.login()
        response = self.__session_manager_instance.get(url)
        response.raise_for_status()
        page = BeautifulSoup(response.text, 'html.parser')
        time.sleep(1)
        return page

    def __copy_template_code(self, taskname):
        original_path = '{}/{}'.format(self.__conf['env']['app_path'], self.__conf['env']['template_filename'])
        copy_path = '{}/{}.cpp'.format(self.__contest_dir_path, taskname)
        if not os.path.exists(copy_path): shutil.copy(original_path, copy_path)
