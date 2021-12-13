import os, sys
import glob
import json
import string
import requests as rq
from bs4 import BeautifulSoup
import pickle
import time
from singleton import Singleton

class SessionManager:
    def __init__(self):
        self.__conf = Singleton.get_instance().get_conf()
        self.__cookies_path = self.__conf['env']['cookies_path']
        self.__contest_conf_path = self.__conf['env']['contest_conf_path']
        try:
            with open (self.__contest_conf_path, 'r') as f:
                self.__contest_conf = json.load(f)
        except:
            print('No contest is registered yet. Please register it.')
            sys.exit(0)
        self.__session = rq.session()

    def get(self, url, params=None):
        return self.__session.get(url, params=params)

    def post(self, url, data=None):
        return self.__session.post(url, data=data)

    def login(self):
        if self.__load_cookies() and self.__check_logging_in():
            return
        login_url = '{}/login'.format(self.__conf['atcoder']['atcoder_top_url'])
        csrf_token = self.__scrape_csrf_token(login_url)
        login_data = {
            'csrf_token': csrf_token,
            'username': self.__conf['atcoder']['username'],
            'password': self.__conf['atcoder']['password']
        }
        response = self.__session.post(login_url, data=login_data)
        response.raise_for_status()
        self.__save_cookies()
        # self.__save_csrf_token(csrf_token)

    def __load_cookies(self):
        try:
            with open(self.__cookies_path, 'rb') as f:
                self.__session.cookies = pickle.load(f)
            return True
        except:
            return False
    
    def __save_cookies(self):
        with open(self.__cookies_path, 'wb') as f: pickle.dump(self.__session.cookies, f)

    def __save_csrf_token(self, csrf_token):
        self.__contest_conf['csrf_token'] = csrf_token
        with open(self.__contest_conf_path, 'w') as f: json.dump(self.__contest_conf, f)

    def __check_logging_in(self):
        # if time.time() - os.path.getmtime(self.__contest_conf_path) < 86400:
        #     return True
        # return False
        check_url = '{}/home'.format(self.__conf['atcoder']['atcoder_top_url'])
        response = self.get(check_url)
        response.raise_for_status()
        return response.text.find('Sign in') == -1

    def __scrape_csrf_token(self, url):
        response = self.__session.get(url)
        response.raise_for_status()
        page = BeautifulSoup(response.content, 'html.parser')
        csrf_token = page.find(attrs={'name':'csrf_token'}).get('value')
        return csrf_token
        
    def get_csrf_token(self, url):
        # if self.__check_logging_in():
        #     return self.__contest_conf['csrf_token']
        return self.__scrape_csrf_token(url)