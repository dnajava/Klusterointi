"""
Match Clusters of one Kit (tested person)
"""
from csv import reader
from links import Link
from mtsettings import GDMAX
from gds import Gds

# -------------------------------------------
# Match
# -------------------------------------------
class Match:
    def __init__(self, fun_p, fin_p, min_p, lan_p, email_p, mdka_p):
        """
        :param fun_p:   Full name
        :param fin_p:   First name
        :param min_p:   Middle name
        :param lan_p:   Last name
        :param email_p: Email address
        :param mdka_p:  Most Distant Ancestor
        """
        self.Fullname = fun_p
        self.Firstname = fin_p
        self.Middlename = min_p
        self.Lastname = lan_p
        self.Email = email_p
        self.MDKA = mdka_p

    def show(self):
        print('Match:', self.kit, ' ', self.gd, ' ', self.Fullname, ' ', self.Email, ' ', self.MDKA)

class FileMatch(Match):
    def __init__(self, kit_p, gd_p, fun_p, fin_p, min_p, lan_p, email_p, mdka_p):
        """
        :param kit_p:   Kit id
        :param gd_p:    Genetic Distance from kit owner
        :param fun_p:   Full name
        :param fin_p:   First name
        :param min_p:   Middle name
        :param lan_p:   Last name
        :param email_p: Email address
        :param mdka_p:  Most Distant Ancestor
        """
        super().__init__(fun_p, fin_p, min_p, lan_p, email_p, mdka_p)
        self.kit = kit_p
        self.gd = gd_p

    def show(self):
        print(self.kit, self.gd, self.Fullname, self.Firstname, self.Middlename, self.Lastname, self.Email, self.MDKA)

# -------------------------------------------
# Cluster
# -------------------------------------------
class Cluster:
    def __init__(self, name_p):
        self.name = name_p                      # Name of subroup. A cluster of haplogroup.
        matches = []

    def __getitem__(self, i: int) -> Match:
        """
        Returns a match of index i from Cluster
        :param i:
        :return: Match
        """
        if 0 <= i <= len(self.matches):
            return self.matches[i]
        else:
            print('Cluster error: index out of matches.')

    def add_match(self, m_p: Match):
        self.matches.append(m_p)

    def remove_match(self, name_p: str) -> bool:
        for i in range(len(self.matches)):
            if matches[i].Fullname == name_p:
                matches.pop(i)
                return True
        return False

    def show(self, debug2_p=False, debug3_p=False):
        """
        Shows data of matches in one cluster
        :type debug2_p: bool
        :type debug3_p: bool
        """
        i = 0
        for y in self.matches:
            if debug2_p:
                print('GD', i, 'cluster', len(y), 'matches.')
            if debug3_p:
                for z in y:
                    z.show()
            i += 1
        print('')

class KitClusters(Cluster):
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
                        new_match = Match(kit_id_p, int(m[0]), m[1], m[2], m[3], m[4], m[5], m[6])
                        tmp_gds = Gds(new_match.gd, new_match)
                    ind += 1
        except (IOError, OSError) as err:
            print(err)
            return []
        finally:
            if read_obj is not None:
                read_obj.close()
        return tmp_gds

class NetCluster(Cluster):
    def __init__(self, name_p):
        """
        :type name_p: str
        """
        super().__init__(name_p)
        linksfrom = []
        linksto = []

    def add_link(self, clu_p, gd_dest):
        """
        Adds link to clu_p with GD distance. It's a tuple.
        :param clu_p:
        :param gd_dest:
        """
        #        self.links.append(tuple(clu_p, gd_dest))                        # Add a bidirectionally linked
        #        clu_p.links.append(fuple(gd_dest, clu_p))                       # -"-

    def add_default_links(self, kitclu_p, ind_p):
        print('NetCluster add_default_links')
        self.links = []
        for i in range(1, 3):
            self.links.append(Link(ind_p, ind_p + i, i))

    def show_links(self):
        print('NetCluster show_links')
        if self.links is not None:
            for li in self.links:
                print('Link ', li.orig, '-', li.dest)

def is_adjacent(cluster1_p: NetCluster, cluster2_p: NetCluster) -> bool:
    """
    If cluster1 is adjacent to cluster2 returns True, otherwise False.
    :param cluster1_p:
        Cluster1 where to search
    :param cluster2_p:
        Cluster2 where to search
    :return: bool
        True if there is at least one same match.
    """
    for li in cluster1_p.linksto:
        if li.to == cluster2_p and li.gd == 1:
            return True
    return False
