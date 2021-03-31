"""
Kit contains kit id and name of tested person and match list date
Maybe some day the parameters are in csv-file
"""

from csv import reader
from mtsettings import DLDIR
from mtsettings import KITSFILE
from mtsettings import HAPLOGROUP
from kclusters import Match
from gds import Gds

class Kit:
    """FTDNA kit and it's match clusters grouped by GD"""
    def __init__(self):
        self.id = ''
        self.name = ''                                                                  # Kit owner real name
        self.date = None
        self.haplogroup = HAPLOGROUP
        self.file = ''
        self.gds = Gds()

    def __init__(self, id_p, name_p, day_p, haplogroup_p=None):
        self.id = id_p
        self.name = name_p                                                              # Kit owner real name
        self.date = None
        self.haplogroup = HAPLOGROUP if haplogroup_p is None else haplogroup_p
        self.file = DLDIR + id_p + '_mtDNA_Matches_' + day_p + '.csv'                   # Matchlist filename
        self.gds = Gds()
        self.read_kit_clusters(self.id, self.name, self.file)                           # Read match clusters

    def read_kit_clusters(self, kit_id_p: str, pname_p: str, fname_p: str):
        """
        Read matches of kit grouped by GD.
        :param kit_id_p: str:
        :param pname_p: str:
        :param fname_p: str:
        :return: list:
        """
        try:
            with open(fname_p, 'r') as read_obj:
                ind = 0                                                         # Line of match file
                csv_reader = reader(read_obj)
                for m in csv_reader:
                    if ind == 0:
                        bogus_match = Match(kit_id_p, 0, pname_p, '', '', '', '', '')  # We know full name of kit owner
                        self.gds.add(0, bogus_match)
                        ind += 1
                        continue
                    else:
                        # DataFormats.txt     kit       gd         fun   fin   min   lam   email mdka
                        new_match = Match(kit_id_p, int(m[0]), m[1], m[2], m[3], m[4], m[5], m[6])
                        self.gds.add(int(m[0]), new_match)
                        ind += 1
        except (IOError, OSError) as err:
            print(err)
        finally:
            if read_obj is not None:
                read_obj.close()

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

    def show(self, show_clusters_p=False, show_matches_p=False, debug3_p=False):
        print('##### Kit', self.id, '#####', self.name, '#####')  # Show only minimal information:

        if show_clusters_p is not False:                                       # Print kit id and name
            matches = 0
            if self.gds is not None:
                for c in self.gds.gdses:
                    matches += len(c)
                print('Kit has', matches, 'matches and kit owner.')  # And how many matches it has

                if show_matches_p is not False:                                # Print amount of matches by clusters
                    gd_idx = 0
                    for gg in self.gds:
                        print('gd', gd_idx)
                        for m5 in gg:
                            m5.show()
                        gd_idx += 1
