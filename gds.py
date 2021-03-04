"""
Matches of one kit grouped by GD.
"""

class gds:
    gdmax = 4                                       # FTDNA lists only GD 0 - 3 matches
    gd0, gd1, gd2, gd3 = [], [], [], []
    gds = [gd0, gd1, gd2, gd3]
    links = []                                      # List of tuples: links to other clusters with GD distance

    def ___init___(self):
        gd0, gd1, gd2, gd3 = [], [], [], []
        gds = [gd0, gd1, gd2, gd3]

    def add(self, idx, value):
        gds[idx].append(value)

    def get(self, idx, value):
        return gds[idx]

    def show(self):
        for a in gds:
            print(a)

    def print_wide(self):
        for a in gds:
            print('GD ', idx, gds[idx])
