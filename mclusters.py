"""
Match Clusters of one Kit (tested person)
"""
from csv import reader

class mclusters:
    kitcluster = False                              # Is this GD 0 cluster to a kit?
    kit_id = None
    haplogroup = ''                                 # Haplogroup identifier of samples
    name = ''                                       # Name of subroup. A cluster of haplogroup.
    gdmax = 4                                       # FTDNA lists only GD 0 - 3 matches
    gd0, gd1, gd2, gd3 = [], [], [], []
    gds = [gd0, gd1, gd2, gd3]
    links = []                                      # List of tuples: links to other clusters with GD distance

    def __init__(self, kit_id_p=False, kit_p=None, haplogroup_p=''):
        """
        :type haplogroup_p: str
        """
        if haplogroup_p != '':
            haplogroup = haplogroup_p
        if kit_id_p:
            self.kit_id = True
        if kit_p:
            self.kitcluster = True
        self.links = None

    def __init__(self, kit_p=False, haplogroup_p='', kit_id_p=None, name_p='', fname_p=''):
        """
        :type haplogroup_p: str
        :type name_p: str
        :type fname_p: str
        """
        self.kit_id = kit_id_p
        if kit_p:
           self.kitcluster = True
        self.haploroup = haplogroup_p
        self.name = name_p
        self.fname = fname_p
        self.links = None

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

    def read_kit_clusters(self, fname_p, pname_p, kit_id_p=None):
        """
        :type fname_p: str
        :type pname_p: str
        """
        ind = 0
        matches = []
        read_obj = None

        self.gd0.append(((kit_id_p, '0'), (pname_p,'','','','','','','')))    # Matchlist doesn't contain kits owner. Add him/her.
        # TODO: Add the rest data to first only name cluster, if it possible.

        try:
            with open(fname_p, 'r') as read_obj:
                csv_reader = reader(read_obj)
                for m in csv_reader:
                    if ind > 0:
                        # See DataFormats.txt
                        m2 = ((kit_id_p, m[0]), (m[1], m[2], m[3], m[4], m[5], m[6], m[7], m[8]))
                        # 1print('read kit clusters: ', m2)
                        matches.append(tuple(m2))
                    ind += 1
        except (IOError, OSError) as err:
            print(err)
            return             # []
        finally:
            if read_obj is not None:
                read_obj.close()

        for x in matches:
            self.gds[int(x[0][1])].append(x)                        # Add matches in different GD-levels

    def add_link(self, clu_p, gd_diff):
        """
        Adds link to clu_p with GD distance. It's a tuple.
        :param clu_p:
        :param gd_diff:
#        :return:
        """
        self.links.append(tuple(clu_p, gd_diff))                        # Add a bidirectionally linked
        clu_p.links.append(fuple(self, gd_diff))                        # -"-

# Non member methods / functions

def is_adjacent(cluster1_p, cluster2_p) -> bool:
    """
        If cluster1 is adjacent to cluster2 returns True, otherwise False.
    :param cluster_p:
        Cluster1 where to search
    :param cluster_p:
        Cluster2 where to search
    :param mname_p:
        Search match name
    :return: bool
        True if mname_p is in cluster_p.
    """
    same = 0                                            # How many same matches there are in cluster1_p

    for m in cluster1_p.nclusters:
        for m2 in cluster2_p.nclusters:
            if m[1] == m2[1]:                           # Are names of matches same?
                same += 1

    result = False
    if same:
        if cluster1_p in self.links:
            if gd == 1:
                result = True
    return result
