"""
Clusters of one Kit (tested person) and Net clusters and M clusters
"""
from gds import Gds
from link import Link
from mtsettings import GDMAX
from match import Match, Name

class Cluster:
    ''' Klusteri on kaikkien mt-dna mätsien joukko, joiden GD keskenään on nolla. '''
    def __init__(self, name_p):
        self.name = name_p                      # Name of subroup. A cluster of haplogroup.
        self.matches = []

    def __getitem__(self, i: int) -> Match:
        """
        Returns a match of index i from Cluster
        :param i:
        :return: Match
        """
        if 0 <= i <= len(self.matches) -1:
            return self.matches[i]
        else:
            print('Cluster error: index out of matches.')

    def add_match(self, m_p: Match):
        ''' Lisää osuma klusteriin '''
        self.matches.append(m_p)

    def remove_match(self, name_p: str) -> bool:
        ''' Poista osuma klusterista '''
        for i in range(len(self.matches)):
            if self.matches[i].Fullname == name_p:
                self.matches.pop(i)
                return True
        return False

    def show(self, debug2_p=False, debug3_p=False):
        ''' Näytä osuma klusterissa '''

        i = 0
        for y in self.matches:
            if debug2_p:
                print(f"GD {i} cluster {len(y)} matches.")
            if debug3_p:
                for z in y:
                    z.show()
            i += 1
        print('')

class KitClusters(Cluster):
    ''' Kittiklusteri '''
    def __init__(self, kit_id_p, name_p):
        ''' Kittiklusteri konstuktori '''

        super().__init__(name_p)                # Name of subroup. A cluster of haplogroup.
        self.kit_id = kit_id_p                  # Id of kit
        self.gds = Gds()                        # 4 levels of matches grouped by GD. Use Gds instead this!

    def show(self, debug2_p=False, debug3_p=False):
        ''' Näytä osuman klusteri '''
        i = 0
        for y in self.gds:
            if debug2_p:
                print(f"GD {i} cluster {len(y)} matches.")
            if debug3_p:
                for z in y:
                    z.show()
            i += 1
        print('')

    def get_cluster(self, level: int=0) -> list:
        ''' Returns a match cluster
        :return: list: list List of matches in one cluster
        '''
        if 0 <= level < GDMAX-1:
            if self.gds[level] is not None:
                return self.gds[level]
        else:
            print('Wrong GD-level', level)

class NetCluster(Cluster):
    ''' Klusteriverkon klusteri. '''

    def __init__(self, name_p: Name=None):
        ''' Konstruktori '''
        super().__init__(name_p)
        self.linksfrom = []                             # Links between two clusters GD 1 - 3
        self.linksto = []                               # Links between two clusters GD 1 - 3


    def add_link(self, clu_p: int=0, gd_dest: int=0):
        ''' Adds link to clu_p with GD distance. It's a tuple. '''

        #        self.links.append(tuple(clu_p, gd_dest))                        # Add a bidirectionally linked
        #        clu_p.links.append(fuple(gd_dest, clu_p))                       # -"-

    def add_default_links(self, ind_p: int=0):  # kitclu_p
        ''' NetCluster add_default_links'''
        # print('NetCluster add_default_links')
        for i in range(1, 3):
            self.linksto.append(Link(ind_p, ind_p + i, i))
            self.linksfrom.append(Link(ind_p + i, ind_p, i))

    def show_links(self):
        ''' Show network cluster links from and to the cluster. '''
        print("'NetCluster show_links")
        for li in self.linksto:
            print('Link to', li.orig, '-', li.dest)
        for li in self.linksfrom:
            print('Link from', li.orig, '-', li.dest)

def is_adjacent(clu1_p: NetCluster, clu2_p: NetCluster) -> bool:
    ''' If cluster1 is adjacent to cluster2 returns True, otherwise False.
    :param clu1_p:        Cluster1 where to search
    :param clu2_p:        Cluster2 where to search
    :return: bool         True if there is at least one same match.
    '''
    for li in clu1_p.linksto:
        if li.to == clu2_p and li.gd == 1:
            return True
    return False

class Mcluster:
    def __init__(self, kit_id_p, name_p):
        """
        :type name_p: str
        :type name_p: str
        """
        self.kit_id = kit_id_p                  # Id of kit
        self.name = name_p                      # Name of subroup. A cluster of haplogroup.
        self.gds = Gds()                        # 4 levels of matches grouped by GD. Use Gds instead this!

    def show(self, debug2_p=False, debug3_p=False):
        """
        Shows data of one match cluster
        :type debug2_p: bool
        :type debug3_p: bool
        """
        i = 0
        for y in self.gds:
            if debug2_p:
                print('GD', i, 'cluster', len(y), 'matches.')
            if debug3_p:
                for z in y:
                    z.show()
            i += 1
        print('')

    def get_cluster(self, level=0) -> list:
        """
        Returns a match cluster.
        :type level: int
        :return: list: list List of matches in one cluster
        """
        if 0 <= level < GDMAX-1:
            if self.gds[level] is not None:
                return self.gds[level]
        else:
            print('Wrong GD-level', level)

    def add_link(self, clu_p, gd_dest):
        """
        Adds link to clu_p with GD distance. It's a tuple.
        :param clu_p:
        :param gd_dest:
        """
#        self.links.append(tuple(clu_p, gd_dest))   # Add a bidirectionally linked
#        clu_p.links.append(fuple(gd_dest, clu_p))  # -"-

    def add_default_links(self, kitclu_p, ind_p):
        self.links = []
        for i in range(1, 3):
            self.links.append(Link(ind_p, ind_p+i, i))

    def show_links(self):
        print('Mclusters show_links')
        if self.links is not None:
            for li in self.links:
                print('Link ', li.orig, '-', li.dest)

    def read_kit_clusters(self, kit_id_p: str, pname_p: str, fname_p: str) -> list:
        ind = 0
        tmp_gds = [[], [], [], []]   # Use Gds instead this!

        try:
            with open(fname_p, 'r') as read_obj:
                csv_reader = reader(read_obj)
                for m in csv_reader:
                    if ind == 0:
                        new_match = Match(kit_id_p, 0, pname_p, '', '', '', '', '')  # bogus match, we don't know
                        self.gds[0].append(new_match)
                    else:
                        # DataFormats.txt     kit       gd         fun   fin   min   lam   email mdka
                        new_match = Basematch(kit_id_p, int(m[0]), m[1], m[2], m[3], m[4], m[5], m[6])
                        tmp_gds = Gds(new_match.gd, new_match)
                    ind += 1
        except (IOError, OSError) as err:
            print(err)
            return None
        finally:
            if read_obj is not None:
                read_obj.close()
        return tmp_gds

# Non member methods / functions

def is_adjacent(cluster1_p, cluster2_p) -> bool:
    """
    If cluster1 is adjacent to cluster2 returns True, otherwise False.
    :param cluster1_p:
        Cluster1 where to search
    :param cluster2_p:
        Cluster2 where to search
    :return: bool
        True if mname_p is in cluster_p.
    """
    same = 0                                            # How many same matches there are in cluster1_p
    for m in cluster1_p.Nclusters:
        for m2 in cluster2_p.Nclusters:
            if m[1] == m2[1]:                           # Are names of matches same?
                same += 1
    result = False
    return result
