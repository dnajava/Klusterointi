"""
GD levels of one kit grouped by GD.
"""
from mtsettings import GDMAX

class Gds:
    def __init__(self):
        """
        Creates new empty Gds.
        """
        self.gd0, self.gd1, self.gd2, self.gd3 = [], [], [], []
        self.gdses = [self.gd0, self.gd1, self.gd2, self.gd3]

    def __init__(self, level_p:int = 0, value_p=None):
        """
        Creates new Gds with one match cluster to some level or only a new empty Gds.
        :param level_p:
        :param value_p:
        :return:
        """
        self.gd0, self.gd1, self.gd2, self.gd3 = [], [], [], []
        self.gdses = [self.gd0, self.gd1, self.gd2, self.gd3]
        if value_p is not None and 0 <= level_p < GDMAX:
            self.gdses[level_p] = value_p

    def __getitem__(self, i: int):
        return self.gdses[i]

    def add(self, level_p, value_p):
        return self.gdses[level_p].append(value_p)

    def show(self, i=0, debug1=False):
        if i == GDMAX:
            for x in self.gdses:
                if len(x) > 0:
                    if debug1 is True:
                        for m in x:
                            m.show()
                    else:
                        print('GD', len(self.gdses[i]), 'matches')
        else:
            if 0 <= i < GDMAX:
                if len(self.gdses[i]) > 0:
                    if debug1 is True:
                        for m in self.gdses[i]:
                            m.show()
                    else:
                        print('GD', len(self.gdses[i]), 'matches')
            else:
                print('Gd Error: Index out of range.')
