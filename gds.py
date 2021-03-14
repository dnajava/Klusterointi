"""
Matches of one kit grouped by GD.
"""

from mtsettings import GDMAX

class Gds:
    links = []                                      # List of tuples: links to other clusters with GD distance

    def ___init___(self):
        self.gd0, self.gd1, self.gd2, self.gd3 = [], [], [], []
        self.gds = [self.gd0, self.gd1, self.gd2, self.gd3]

    def add(self, idx, value):
        self.gds[idx].append(value)

    def get(self, idx):
        return self.gds[idx]

    def show(self):
        for a in self.gds:
            print(a)

    def print_wide(self):
        for i in range(0, GDMAX, 1):
            print('GD ', i, self.gds[i])
