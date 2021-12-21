#!/usr/bin/python

import subprocess
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
from language import Language
from judge import Judge
from utilities import PyColors

class CodeManager(FileManager):
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
        self.__check_result_path = self.__conf['env']['check_result_path']
        self.__extention_language_dict = self.__conf['code']['extention_language_dict']
        self.__timeout = self.__conf['code']['timeout']
        super().__init__()

    def search_code(self, filename):
        if filename:
            if os.path.exists(self._get_full_path(filename)):
                return filename
            raise OSError('No such file found error')
        filename = self.__get_lastly_modified_code()
        return filename

    def __get_lastly_modified_code(self):
        target_path_list = glob.glob(f'{self.__contest_dir_path}/**', recursive=True)
        latest_file_path = None
        latest_modified_time = 0
        for path in target_path_list:
            lang = self._get_language(path)
            if not lang: continue
            if latest_modified_time < os.path.getmtime(path):
                latest_modified_time = os.path.getmtime(path)
                latest_file_path = path
        if latest_file_path:    
            return self._get_relative_path(latest_file_path)
        return None



    def preprocess(self, filename):
        # change permission
        os.chmod(self._get_full_path(filename), 0o755)
        # compilable lang?
        lang = self._get_language(filename)
        command = lang.get_preprocess_command(self._get_full_path(filename))
        if command is None: return True
        if self.__judge_already_preprocessed(filename): return True
        try:
            proc = subprocess.run(command, stderr=subprocess.PIPE)
            proc.check_returncode()
            if proc.stderr:
                print(proc.stderr.decode('utf-8'))
                print(PyColors.PURPLE + PyColors.ACCENT + 'COMPILE ERROR' + PyColors.END)
                return False
            else:
                return True            
        except:
            print(proc.stderr.decode())
            print(PyColors.PURPLE + PyColors.ACCENT + 'COMPILE ERROR' + PyColors.END)
            return False
        preprocessed_filename = lang.get_preprocessed_filename(filename)
        if os.getcwd() != self.__contest_dir_path: shutil.move('{}/{}'.format(os.getcwd(), preprocessed_filename), f'{self.__contest_dir_path}/{preprocessed_filename}')
        return True
    
    def __judge_already_preprocessed(self, filename):
        preprocessed_filepath = self.__get_preprocessed_filepath(filename)
        if os.path.exists(preprocessed_filepath) and os.path.getmtime(preprocessed_filepath) >= os.path.getmtime(self._get_full_path(filename)):
            return True
        return False

    def __get_preprocessed_filepath(self, filename):
        lang = self._get_language(filename)
        return '{}/{}'.format(self.__contest_dir_path, lang.get_preprocessed_filename(filename))


    def run_testcases(self, filename, testcase_number):
        taskname = self._get_taskname(filename)
        task_screen_name = self._get_task_screen_name(filename)
        command = self._get_language(filename).get_run_command(self.__get_preprocessed_filepath(filename))
        input_filepath_list = sorted(glob.glob(f'{self.__testcase_dir_path}/{taskname}*in.txt'))
        output_filepath_list = sorted(glob.glob(f'{self.__testcase_dir_path}/{taskname}*out.txt'))
        if len(input_filepath_list) != len(output_filepath_list):
            print('Invalid testcases error')
            sys.exit(0)
        testcase_size = len(input_filepath_list)
        if testcase_number:
            case_number_list = [testcase_number]
        else:
            case_number_list = range(1, testcase_size+1)

        run_arguments = []
        run_result_dict = self.__load_result()
        # if not task_screen_name in run_result_dict: run_result_dict[task_screen_name] = {}
        run_result_dict[task_screen_name] = {}
        for case_number in case_number_list:
            run_arguments.append([command, case_number, input_filepath_list[case_number-1], output_filepath_list[case_number-1]])             
        if len(case_number_list) > 1:
            p = mp.Pool(testcase_size)
            for res in p.map(self._run_a_testcase, run_arguments):
                run_result_dict[task_screen_name][res['case_number']] = res
        elif len(case_number_list) == 1:
            res = self._run_a_testcase(run_arguments[0])
            run_result_dict[task_screen_name][res['case_number']] = res
        else:
            print('No testcases found error')
            return False

        with open(self.__check_result_path, 'w') as f: json.dump(run_result_dict, f)
        return self.__evaluate_code(run_result_dict, task_screen_name)

    def _run_a_testcase(self, inputs):
        command, case_number, input_filepath, output_filepath = inputs
        result = {'case_number': case_number}
        with open(input_filepath, 'r') as input_f:
            try:
                proc = subprocess.run(command, stdin=input_f, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=5, shell=True)
                proc.check_returncode
            except subprocess.CalledProcessError as e:
                result['judge'] = Judge.RE
                result['your_output'] = e.stdout.decode('utf-8')
                result['error'] = e.stderr.decode('utf-8')
                return result
            except subprocess.TimeoutExpired:
                result['judge'] = Judge.TLE
                result['your_output'] = e.stdout.decode('utf-8')
                result['error'] = e.stderr.decode('utf-8')
                return result

        result['your_output'] = proc.stdout.decode('utf-8')
        with open(output_filepath, 'r') as f: result['correct_answer'] = f.read()
        if result['your_output'] != result['correct_answer']: result['judge'] = 'WA'
        else: result['judge'] = 'AC'
        return result

    def __load_result(self):
        try:
            with open(self.__check_result_path, 'r') as f: return json.load(f)
        except:
            return {}

    def __evaluate_code(self, result_dict, task_screen_name):
        for case_number in result_dict[task_screen_name].keys():
           if result_dict[task_screen_name][case_number]['judge'] != Judge.AC.value: return False
        return True


    def display_check_result(self, filename, testcase_number, show_detail=True):
        result = self.__load_result()
        task_screen_name = self._get_task_screen_name(filename)
        if testcase_number is None:
            for case_number in sorted(result[task_screen_name].keys()):
                self.__display_a_testcase_result(result[task_screen_name], str(case_number), show_detail)
        else:
            self.__display_a_testcase_result(result[task_screen_name], str(testcase_number), show_detail)

    def __display_a_testcase_result(self, result, testcase_number, show_detail=True):
        judge = Judge[result[testcase_number]['judge']]
        if 'your_output' in result[testcase_number]: your_output = result[testcase_number]['your_output']
        if 'correct_answer' in result[testcase_number]: correct_answer = result[testcase_number]['correct_answer']
        if 'error' in result[testcase_number]: error = result[testcase_number]['error']

        print(judge.get_judge_message(int(testcase_number)))
        if show_detail:
            if judge != Judge.AC:
                print('Your Output:')
                print(your_output)
            if judge == Judge.RE or judge == Judge.TLE:
                print('Error Message:')
                print(error)
            if judge == Judge.WA: 
                print('Correct Answer:')
                print(correct_answer)


    def submit_code(self, filename, wait_judge=True):
        filepath = self._get_full_path(filename)
        if not os.path.exists(filepath) or os.path.isdir(filepath):
            print('There\'s no code to submit')
            return False
        
        submit_page_url = f'{self.__contest_page_url}/submit'
        source_code = None
        with open(filepath, 'r') as f:
            source_code = f.read()
        if not source_code:
            print('Cannot submit an empty code')
            return False
        
        sm = SessionManager()
        sm.login()
        lang = self._get_language(filepath)
        csrf_token = sm.get_csrf_token(submit_page_url)
        submit_data = {
            'csrf_token': csrf_token,
            'data.TaskScreenName': self._get_task_screen_name(filename),
            'data.LanguageId': lang.get_language_code(),
            'sourceCode': source_code
        }
        response = sm.post(submit_page_url, data=submit_data)
        response.raise_for_status()

        if wait_judge:
            print('Being judged...')
            self.__print_judge_result(sm, self._get_task_screen_name(filename))

    def __print_judge_result(self, session_manager_instance, task_screen_name):
        submission_page_url = f'{self.__contest_page_url}/submissions/me'
        status = self.__fetch_judge_status(session_manager_instance, submission_page_url, task_screen_name)
        print(status)
        if status != 'AC': print(submission_page_url)

    def __fetch_judge_status(self, session_manager_instance, submission_page_url, task_screen_name):
        status = 'WJ'
        while status == 'WJ':
            # session_manager_instance.check_login()
            response = session_manager_instance.get(submission_page_url, params={'f.Task': task_screen_name})
            page = BeautifulSoup(response.text, 'html.parser')
            submission = page.find('tbody').find('tr').find_all('td')
            fetched_status = submission[6].text
            for judge in ['AC', 'WA', 'RE', 'TLE', 'MLE', 'CE']:
                if judge in fetched_status:
                    status = judge
                    break
            time.sleep(1)
        return status




