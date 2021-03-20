"""
GD levels of one kit grouped by GD.
"""
from mtsettings import GDMAX

class Gds:
    gd0, gd1, gd2, gd3 = [], [], [], []
    gds = [gd0, gd1, gd2, gd3]
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

    def add(self, i, value_p) -> bool:
        if self.gds is None:
            return False
        if 0 <= i < GDMAX:
            self.gds[i].append(value_p)
            return True
        else:
            print('Error: Gds-index out of range.')
            return False

    def show(self, i=0):
        if 0 <= i < GDMAX:
            if len(self.gd0) > 0:
                for m in self.gd0:
                    m.show()

            if len(self.gd0) > 0:
                for m in self.gd1:
                    m.show()

            if len(self.gd0) > 0:
                for m in self.gd2:
                    m.show()

            if len(self.gd0) > 0:
                for m in self.gd3:
                    m.show()
        else:
            print('Gds Error: Index out of range.')
