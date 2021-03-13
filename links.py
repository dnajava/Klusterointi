"""
Links between GD-clusters.
"""

class Link:
    orig = None
    dest = None
    gd = 0

    def __init__(self, orig_p=None, dest_p=None, gd_p=0):
        self.orig = orig_p
        self.dest = dest_p
        self.gd = gd_p

