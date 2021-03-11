"""
Match Clusters of one Kit (tested person)
"""
from csv import reader
from gds import gds
# from mclusters import mclusters
from links import link
from mtsettings import GDMAX

class mcluster:
    kit_id = None
    haplogroup = ''                                 # Haplogroup identifier of samples
    name = ''                                       # Name of subroup. A cluster of haplogroup.
    links = []                                      # List of tuples: links to other clusters with GD distance


    def __init__(self, kit_id_p, haplogroup_p, name_p):
        """
        :type haplogroup_p: str
        :type name_p: str
        :type fname_p: str
        """
        self.kit_id = kit_id_p
        self.haploroup = haplogroup_p
        self.name = name_p
        self.gds = [[], [], [], []]                 # 4 levels of matches grouped by GD
        self.links = []


    def show(self, debug2_p=False, debug3_p=False):
        """
        :type debug2_p: bool
        :type debug3_p: bool
        """
        i = 0
        for y in self.gds:
            if debug2_p:
                print('GD', i, 'cluster', len(y), 'matches.')
                i += 1
            if debug3_p:
                for z in y:
                    print(z[1], ' ', end='')
                print('')
        print('')

    def show_links(self):
        i = 0
        for v in self.links:
            pdinr(v)

    def get_cluster(self, level=0) -> list:
        """
        :type level: int
        :return: list
        """
        if 0 <= level < GDMAX-1:
            if self.gds[level] != None:
                return self.gds[level]
        else:
            print('Wrong GD-level', level)

    def read_kit_clusters(self, fname_p, kit_id_p, pname_p) -> list:
        """
        :rtype: object
        :type fname_p: str
        :type pname_p: str
        """
        ind = 0
        matches = []
        read_obj = None

        new_mcluster = mcluster(kit_id_p, '', pname_p)
        new_mcluster.gds[0].append(((kit_id_p, '0'), (pname_p,'','','','','','','')))    # Matchlist doesn't contain kits owner. Add him/her.

        try:
            with open(fname_p, 'r') as read_obj:
                csv_reader = reader(read_obj)
                for m in csv_reader:
                    if ind > 0:
                        # See DataFormats.txt
                        m2 = ((kit_id_p, m[0]), (m[1], m[2], m[3], m[4], m[5], m[6], m[7], m[8]))
                        matches.append(tuple(m2))
                        new_mcluster.gds[int(m2[0][1])].append(m2)  # Add matches in different GD-levels
                    ind += 1
        except (IOError, OSError) as err:
            print(err)
            return []
        finally:
            if read_obj is not None:
                read_obj.close()

        return new_mcluster.gds


    def add_link(self, clu_p, gd_dest):
        """
        Adds link to clu_p with GD distance. It's a tuple.
        :param clu_p:
        :param gd_dest:
#        :return:
        """
#        self.links.append(tuple(clu_p, gd_dest))                        # Add a bidirectionally linked
#        clu_p.links.append(fuple(gd_dest, clu_p))                       # -"-

    def add_default_links(self, kitclu_p, ind_p):
        self.links = []
        for i in range(1, 3):
            self.links.append(link(ind_p,ind_p+i,i))

    def show_links(self):
        print('Mclusters show_links')
        if self.links != []:
            for i in self.nclusters[i].links:
                print('Clusters GD', i, 'link', self.links[i])


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
    return result
