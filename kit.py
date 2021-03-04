"""
Kit contains kit id and name of tested person and match list date
Maybe some day the parameters are in csv-file
"""

from csv import reader
from mclusters import mcluster

class kit:
    id = ''                                                                               # Kit id in FTDNA
    name = ''                                                                             # Kit's owner real name
    haplogroup = ''
#    date = None
    dl_directory = '/home/ilpo/Lataukset/'
    kfname = 'kits.csv'
    file = ''                                                                             # Matchlist filename
    mclu = None

    def __init__(self, id_p, name_p, day_p, haplogroup_p):
        self.id = id_p
        self.name = name_p
        self.date = None
        self.haplogroup = haplogroup_p
        # self.date = date.today().strftime("%Y%m%d")  # Today in FTDNA's matchlist format
        self.file = self.dl_directory + id_p + '_mtDNA_Matches_' + day_p + '.csv'
        self.mclu = mcluster(self.id, self.haplogroup, self.name)
        self.mclu.gds = self.mclu.read_kit_clusters(self.file, self.id, self.name)
#        print('CLUSTERS',self.mclu)

    def read_kits(fname_p = '') -> list:
        """
        :type fname_p: str
        :return: list
        """
        tempkits = []
        filename = 'kits.csv'

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

    def getname(self):
        return self.name

    def getfilen(self):
        return self.file

    def show(self, debug1_p=False, debug2_p=False, debug3_p=False):
        print('##### Kit', self.id, '#####', self.name, '#####')  # Show only minimal information:
        if debug1_p != False:
            if debug2_p != False:                                              # Kit id and name.
                if self.mclu != None:                                          # If there are matches.
                        self.mclu.show(debug2_p,debug3_p)                      # dbg2: print clusters and amount.
                else:                                                          # dbg3: print match names too.
                    print('This kit has no mt-dna matches.')
            if self.mclu != None:
                print('### KIT SHOW #####')
                print(self.mclu)
            else:
                print('No clusters data.')

