"""
Kit contains kit id and name of tested person and match list date
Maybe some day the parameters are in csv-file
"""

from csv import reader
from mtsettings import DLDIR
from mtsettings import KITSFILE
from mtsettings import HAPLOGROUP
from mclusters import Basematch

class Kit:
    @staticmethod
    def show_gds(gds_p):
        for a in gds_p:
            for b in a:
                b.show()

    def read_kit_clusters(self, kit_id_p: str, pname_p: str, fname_p: str) -> list:
        """

        :param kit_id_p: str:
        :param pname_p: str:
        :param fname_p: str:
        :return: list:
        """
        ind = 0
        tmp_gds = [[], [], [], []]                      # Use Gds instead this!

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
                        tmp_gds[new_match.gd].append(new_match)
                    ind += 1
        except (IOError, OSError) as err:
            print(err)
            return []
        finally:
            if read_obj is not None:
                read_obj.close()
        return tmp_gds

    def __init__(self, id_p, name_p, day_p, haplogroup_p=None):
        self.id = id_p                                                                  # Kit id in FTDNA
        self.name = name_p                                                              # Kit owner real name
        self.date = None
        self.gds = [[], [], [], []]     # Use Gds instead this!
        self.haplogroup = ''
        self.file = ''                                                                  # Matchlist filename

        if haplogroup_p is None:
            self.haplogroup = HAPLOGROUP
        else:
            self.haplogroup = haplogroup_p

        #        self.mclu = mcluster(self.id, self.name)
        self.file = DLDIR + id_p + '_mtDNA_Matches_' + day_p + '.csv'
        self.gds = self.read_kit_clusters(self.id, self.name, self.file)          # Read match clusters

    @staticmethod
    def read_kits(fname_p='') -> list:
        """
        :type fname_p: str
        :return: list
        """
        tempkits = []
        filename = KITSFILE

        if fname_p != '':
            filename = fname_p

        try:
            with open(filename, 'r') as read_obj:
                csv_reader = reader(read_obj)
                for k in csv_reader:
                    k[1] = k[1].strip() + ' '               # One space after name like match names have
                    tempkits.append(k)
        except (IOError, OSError) as err:
            print(err)
            return []
        finally:
            if read_obj is not None:
                read_obj.close()
        return tempkits

    def show(self, debug1_p=False, debug2_p=False, debug3_p=False):
        print('##### Kit', self.id, '#####', self.name, '#####')  # Show only minimal information:

        if debug1_p is not False:                                               # Print kit id and name
            matches = 0
            if self.gds is not None:
                for ix in self.gds:
                    matches += len(ix)
            print('Kit has', matches-1, 'matches amd kit owner.')           # And how many matches it has

            if debug2_p is not False:                                           # Print amount of matches by clusters
                if self.gds is not None:
                    ind = 0
                    for ix in self.gds:
                        print('Cluster', ind, ' has', len(self.gds[ind]), 'matches.')
                        ind += 1
                        if debug3_p is not False:                               # Print also match data too
                            for m5 in ix:
                                m5.show()
