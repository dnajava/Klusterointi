"""
Match Clusters of one Kit (tested person)
"""
from csv import reader

class mclusters:
    haplogroup = ''                                 # Haplogroup identifier of samples
    name = ''                                       # Name of subroup. A cluster of haplogroup.
    gdmax = 4                                       # FTDNA lists only GD 0 - 3 matches
    gd0, gd1, gd2, gd3 = [], [], [], []
    gds = [gd0, gd1, gd2, gd3]

    def __init__(self, haplogroup_p=''):
        """
        :type haplogroup_p: str
        """
        if haplogroup_p != '':
            haplogroup = haplogroup_p

    def __init__(self, haplogroup_p='', name_p='', fname_p=''):
        """
        :type haplogroup_p: str
        :type name_p: str
        :type fname_p: str
        """
        self.haploroup = haplogroup_p
        self.name = name_p
        self.fname = fname_p

    def show(self, debug2_p=False, debug3_p=False):
        """
        :type debug2_p: bool
        :type debug3_p: bool
        """
        i = 0
        for y in self.gds:
            if debug2_p:
                print('GD', i, 'cluster and there are', len(y), 'matches.')
                i += 1
            if debug3_p:
                for z in y:
                    print(z[1], ' ', end='')
                print('')
        print('')

    def get_cluster(self, level=0) -> list:
        """
        :type level: int
        :return: list
        """
        if 0 <= level < self.gdmax-1:
            if self.gds[level] != None:
                return self.gds[level]
        else:
            print('Wrong GD-level', level)

    def read_kit_clusters(self, fname_p, pname_p):
        """
        :type fname_p: str
        :type pname_p: str
        """
        ind = 0
        matches = []
        read_obj = None

        self.gd0.append(('0',pname_p,'','','','','','',''))     # Matchlist doesn't contain kits owner. Add him/her.
        # TODO: Add the rest data to first only name cluster, if it possible.

        try:
            with open(fname_p, 'r') as read_obj:
                csv_reader = reader(read_obj)
                for m in csv_reader:
                    if ind > 0:
                        # print('read kit clusters: ', m)
                        matches.append(tuple(m))
                    ind += 1
        except (IOError, OSError) as err:
            print(err)
            return             # []
        finally:
            if read_obj is not None:
                read_obj.close()

        for x in matches:
            self.gds[int(x[0])].append(x)                           # Add matches in different GD-levels
