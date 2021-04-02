"""
Links between GD-clusters.
"""

class Link:
    orig = None
    dest = None
    gd = 0

    def __init__(self, orig_p, dest_p, gd_p=0):
        self.orig = orig_p
        self.dest = dest_p
        self.gd = gd_p

    def show(self):
        print('Link', self.orig, '->', self.dest)