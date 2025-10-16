"""
Kit contains kit id and name of tested person and match list date
Maybe some day the parameters are in csv-file
"""

import os
import re
from csv import reader
from mtsettings import DLDIR, KITSFILE, HAPLOGROUP, FENCODING
from match import FileMatch, Match
from gds import Gds

class Kit:
    """FTDNA kit and it's match clusters grouped by GD"""
    def __init__(self, id_p, name_p, day_p, haplogroup_p=None):
        self.id = id_p
        self.name = name_p                                          # Kit owner real name
        self.date = None
        self.haplogroup = HAPLOGROUP if haplogroup_p is None else haplogroup_p
        self.file = DLDIR + id_p + '_MT_DNA_Matches_' + day_p + '.csv' # Matchlist filename
        # print("Luettava tiedosto:", self.file)
        self.gds = Gds()
        self.read_kit_clusters(self.id, self.name, self.file)       # Read match clusters


    def read_kit(self, kit_id_p: str, fname_p: str): # pname_p: str
        """
        Read matches of kit grouped by GD.
        :param kit_id_p: str:   Kit id
        :param pname_p: str:    Name of kit owner
        :param fname_p: str:    File name of kit matches
        """
        try:
            with open(fname_p, 'r', encoding=FENCODING) as read_obj:    # Read kit from file
                ind = 0                                                 # Line of match file
                csv_reader = reader(read_obj)
                print("csv_reader=", csv_reader)
                for m in csv_reader:
                    if ind == 0:
                        # We know now (at this time) only full name of kit owner
                        bogus_match = FileMatch(kit_id_p) # ,"","","", "", "", 0, "")
                        self.gds.add(0, bogus_match)
                        ind += 1
                        continue
                    # DataFormats.txt     kit       gd         fun   fin   min   lam   email mdka
                    new_match = FileMatch(kit_id_p, int(m[0]), m[1], m[2], m[3], m[4], m[5], m[6])
                    self.gds.add(int(m[0]), new_match)
                    ind += 1
        except (IOError, OSError) as err:
            print(err)
        finally:
            if read_obj is not None:
                read_obj.close()



    def read_kit_clusters(self, kit_id_p: str, pname_p: str, fname_p: str): # pname_p: str
        """
        Read matches of kit grouped by GD.
        :param kit_id_p: str:   Kit id
        :param pname_p: str:    Name of kit owner
        :param fname_p: str:    File name of kit matches
        """
        print(pname_p, kit_id_p)
        read_obj = None
        try:
            with open(fname_p, 'r', encoding=FENCODING) as read_obj:
                ind = 0                                               # Line of match file
                csv_reader = reader(read_obj)
                for m in csv_reader:
                    if ind == 0:
                        # print("Bogus m=***", m, "***")
                        # bogus_match=FileMatch(kit_id_p, 0, pname_p, "", "", "", "", "")
                        # self.gds.add(gd_p, bogus_match)
                        ind += 1
                        continue
                    # idx = 0
                    # for mx in m:
                    #     print(f' m{idx} {m[idx]}', end='')
                    #     idx += 1

                    #def __init__(self, fun_p, fin_p="", min_p="", lan_p="",
                    # mdate_p, gd_p="", haplogroup_p="", mdka_p=""):

                                      # fun_p, mdate, gd, haplogroup, mdka
                    new_match = Match(m[0], m[4], m[6], HAPLOGROUP, m[11])
                    print("Filematch:", new_match.name.fullname)
                    # self.gds.add(m[5], new_match)
                    ind += 1
        except (IOError, OSError) as err:
            print(err)
        finally:
            if read_obj is not None:
                read_obj.close()

    def read_kit_clusters2(self, directory: str, pname_p: str):
        # elf, kit_id_p: str, pname_p: str, fname_p: str
        """
        Read all kit match CSV files in the given directory.
        Filenames are expected to be in the form: <kit_id>_MT_DNA_Matches_<yyyymmdd>.csv

        :param directory: str:   Directory path containing the CSV files
        :param pname_p:   str:   Name of kit owner
        """

        # Regex to capture kit ID and date from filename
        pattern = re.compile(r'^(?P<kit_id>B\d+)_MT_DNA_Matches_(?P<date>\d{8})\.csv$')

        # Iterate over all files in directory
        for filename in os.listdir(directory):
            match = pattern.match(filename)
            if not match:
                continue  # Skip files that don't match the expected pattern

            kit_id = match.group('kit_id')
            file_path = os.path.join(directory, filename)

            print(f"Reading file: {file_path}")

            read_obj = None
            try:
                with open(file_path, 'r', encoding='utf-8-sig') as read_obj:
                    csv_reader = reader(read_obj)
                    for ind, m in enumerate(csv_reader):
                        if ind == 0:
                            # First line — add a bogus match with only the owner name
                            bogus_match = FileMatch(kit_id, 0, pname_p, '', '', '', '', '')
                            self.gds.add(0, bogus_match)
                        else:
                            # Read actual match line
                            new_match = FileMatch(
                                kit_id,
                                int(m[0]),
                                m[1], m[2], m[3], m[4], m[5], m[6]
                            )
                            self.gds.add(int(m[0]), new_match)
            except (IOError, OSError) as err:
                print(f"Error reading {file_path}: {err}")
            finally:
                if read_obj is not None:
                    read_obj.close()

    @staticmethod
    def read_kitlist(fname_p='') -> list:
        """
        Reads kits from file.
        :type fname_p: str  File name of kits list
        :return: list       List of kits containing kit id, name of owner and date of matchlist file
        """
        tempkits = []
        filename = KITSFILE         # kits.csv

        if fname_p != '':
            filename = fname_p

        try:
            with open(filename, 'r', encoding=FENCODING) as read_obj:
                csv_reader = reader(read_obj)
                for k in csv_reader:
                    k[1] = k[1].strip() + ' '  # One space after name like match names have
                    tempkits.append(k)
        except (IOError, OSError) as err:
            print(err)
            return []
        finally:
            if read_obj is not None:
                read_obj.close()
        return tempkits

    def show(self, show_clusters_p=False, show_matches_p=False): # debug3_p=False
        ''' Show kit data. '''
        print(f"##### Kit {self.id} ##### {self.name} #####")  # Show only minimal information:

        if show_clusters_p is not False:                              # Print kit id and name
            matches = 0
            if self.gds is not None:
                for c in self.gds.gdses:
                    matches += len(c)
                print(f"Kit has {matches} matches and kit owner.")    # And how many matches it has

                if show_matches_p is not False:    # Print amount of matches by clusters
                    gd_idx = 0
                    for gg in self.gds:
                        print('gd', gd_idx)
                        for m5 in gg:
                            m5.show()
                        gd_idx += 1
