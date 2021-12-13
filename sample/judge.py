from enum import Enum, auto
from utilities import PyColors

class Judge(str, Enum):
    AC = 'AC'
    WA = 'WA'
    RE = 'RE'
    TLE = 'TLE'
    CE = 'CE'

    def get_judge_message(self, case_number):
        return 'Case {}: {}'.format(case_number, self.__decorate_judge())

    def __decorate_judge(self):
        if self == self.AC: return PyColors.GREEN + PyColors.ACCENT + self.value + PyColors.END
        if self == self.WA: return PyColors.RED + self.value + PyColors.END
        if self == self.RE: return PyColors.RED_FLASH + self.value + PyColors.END
        if self == self.TLE: return PyColors.YELLOW + self.value + PyColors.END
        if self == self.CE: return PyColors.YELLOW + self.value + PyColors.END
