import json
import argparse

from testcase_manager import TestCaseManager
from execute_check_then_submit import ExecuteCheckThenSubmit
from execute_submit import ExecuteSubmit
from execute_check import ExecuteCheck
from execute_display import ExecuteDisplay
from testcase_manager import TestCaseManager
from singleton import Singleton
from session_manager import SessionManager

def main():
    Singleton.get_instance().set_conf('/tmp/config.json')
    conf = Singleton.get_instance().get_conf()

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--submit', help='You can submit your code without check', action='store_true')
    parser.add_argument('-c', '--check', type=int, help='You can only check your code, without submission. Please specify a testcase number. Especially \'0\' means all cases.')
    parser.add_argument('-m', '--minimum', help='Never show error message nor wait judge on atcoder site.', action='store_true')
    parser.add_argument('--init', help='You can initialize this application. Please specify the contest name to register. E.g.) --init abc123')
    parser.add_argument('-f', '--filename', help='Please specify filename if you are needed.')
    args = parser.parse_args()

    if args.init:
        contest_conf = {'contest_name': args.init}
        with open(conf['env']['contest_conf_path'], 'w') as f: json.dump(contest_conf, f)
        TestCaseManager().fetch_and_save_testcases()
    else:
        if args.submit and args.check is not None:
            print('You cannot use \'submit\' and \'check\' options at the same time.')
        elif args.submit:
            print('submit anyway')
            ExecuteSubmit().execute(filename=args.filename, show_detail=(not args.minimum))
        elif args.check is not None:
            print('only check')
            number = None
            if args.check: number = args.check
            ExecuteCheck().execute(filename=args.filename, testcase_number=number, show_detail=(not args.minimum))
        else:
            print('check then submit')
            ExecuteCheckThenSubmit().execute(filename=args.filename, show_detail=(not args.minimum))

if __name__ == '__main__':
    main()