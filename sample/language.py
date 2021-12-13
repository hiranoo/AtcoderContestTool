from enum import Enum
from singleton import Singleton

class Language(str, Enum):
    CPP = 'CPP'
    PYTHON = 'PYTHON'
    JAVA = 'JAVA'

    def get_language_code(self):
        conf = Singleton.get_instance().get_conf()
        return conf['atcoder']['language_code'][self.name]

    def get_preprocess_command(self, filepath):
        if self == self.PYTHON: return None
        if self == self.CPP: return ['g++', '-std=c++17', '-O', filepath]
        if self == self.Java: return ['javac', filepath]

    def get_preprocessed_filename(self, filename):
        if self == self.CPP: return 'a.out'
        return filename

    def get_run_command(self, filepath, input_file):
        if self == self.CPP: return [filepath]
        if self == self.PYTHON: return ['python3', filepath]
        if self == self.JAVA: return ['java', filepath]