import execute
from execute_check_then_submit import ExecuteCheckThenSubmit
from execute_submit import ExecuteSubmit
from execute_check import ExecuteCheck
from execute_display import ExecuteDisplay
from singleton import Singleton
from session_manager import SessionManager

if __name__ == '__main__':
    Singleton.get_instance().set_conf('/tmp/config.json')
    # switch processes depending on commandline arguments

    e = ExecuteCheckThenSubmit()
    e.execute()
    # s = SessionManager()
    # s.login()
