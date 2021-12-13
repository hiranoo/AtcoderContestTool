import json

class Singleton:
    __instance = None

    @staticmethod 
    def get_instance():
        if Singleton.__instance == None:
            Singleton()
        return Singleton.__instance

    def __init__(self):
        if Singleton.__instance != None:
            raise Exception('Singleton class')
        else:
            Singleton.__instance = self

    def set_conf(self, conf_path):
        with open(conf_path, 'r') as f: self.__conf = json.load(f)

    def get_conf(self):
        return self.__conf
