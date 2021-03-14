"""
GD levels of one kit grouped by GD.
"""
from mtsettings import GDMAX

class Gds:
    def ___init___(self, level_p: int, value_p=None):
        """
        Creates new Gds with one match cluster to some level or only a new empty Gds.
        :param level_p:
        :param value_p:
        :return:
        """
        self.gd0, self.gd1, self.gd2, self.gd3 = [], [], [], []
        self.gds = [self.gd0, self.gd1, self.gd2, self.gd3]
        if value_p is not None and 0 <= level_p < GDMAX:
            self.gds[level_p] = value_p

    def ___getitem___(self, i: int):
        return self.gds[i]

    def add(self, idx, value):
        self.gds[idx].append(value)

    def show(self, i=0):
        if 0 <= i < GDMAX:
            print('GD', i, self.gds[i])
        else:
            for a in self.gds:
                for i in range(0, GDMAX, 1):
                    print('GD ', i, a)
