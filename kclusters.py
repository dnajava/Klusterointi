"""
Match Clusters of one Kit (tested person)
"""
from csv import reader
from links import Link
from mtsettings import GDMAX
from gds import Gds

class Basematch:
    def __init__(self, kit_p, gd_p, fun_p, fin_p, min_p, lan_p, email_p, mdka_p):
        """
        :param fun_p:
        :param fin_p:
        :param min_p:
        :param lan_p:
        :param email_p:
        :param mdka_p:
        """
        self.kit = kit_p
        self.gd = gd_p
        self.Fullname = fun_p
        self.Firstname = fin_p
        self.Middlename = min_p
        self.Lastname = lan_p
        self.Email = email_p
        self.MDKA = mdka_p

    def show(self):
        print('Match:', self.kit, ' ', self.gd, ' ', self.Fullname, ' ', self.Email, ' ', self.MDKA)

class Filematch(Basematch):
    def __init__(self, kit_p, gd_p, fun_p, fin_p, min_p, lan_p, email_p, mdka_p):
        """
        :param kit_p:
        :param gd_p:
        :param fun_p:
        :param fin_p:
        :param min_p:
        :param lan_p:
        :param email_p:
        :param mdka_p:
        """
        self.kit = kit_p
        self.gd = gd_p
        super().__init__(fun_p, fin_p, min_p, lan_p, email_p, mdka_p)


class Clumatch(Basematch):
    def __init__(self, kit_p, gd_p, fun_p, fin_p, min_p, lan_p, email_p, mdka_p):
        """
        :param kit_p:
        :param gd_p:
        :param fun_p:
        :param fin_p:
        :param min_p:
        :param lan_p:
        :param email_p:
        :param mdka_p:
        """
        self.kit = kit_p
        self.GD = gd_p
        super().__init__(kit_p, gd_p, fun_p, fin_p, min_p, lan_p, email_p, mdka_p)

    def show(self):
        print(self.Fullname, self.Firstname, self.Middlename, self.Lastname, self.Email, self.MDKA)


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
#        self.links.append(tuple(clu_p, gd_dest))                        # Add a bidirectionally linked
#        clu_p.links.append(fuple(gd_dest, clu_p))                       # -"-

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
                        new_match = Basematch(kit_id_p, 0, pname_p, '', '', '', '', '')  # bogus match, we don't know
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
