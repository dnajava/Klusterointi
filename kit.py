# Kit contains kit id and name of tested person and match list date

from csv import reader
from datetime import date
import mclusters

class kit:
    dl_directory = '/home/user/Downloads/'
    kfname = 'kits.csv'
    file = ''
    mclu = None

    def __init__(self, id_p, name_p, day_p):
        self.id = id_p
        self.name = name_p
        self.date = day_p
        self.file = self.dl_directory + id_p + '_mtDNA_Matches_' + day_p + '.csv'
        self.mclu = mclusters.mclusters(self.name, self.file)
        self.mclu.read_clusters(self.file)                                                        # Read kit's mt-dna matches

    def mk_mclu(self, name_p, file_p):
        mclu = mclusters.mclusters(self.name, self.file)
        self.file = self.dl_directory + self.id + '_mtDNA_Matches_' + self.date + '.csv'
        self.mclu = mclusters.mclusters(self.name, self.file)
        self.mclu.read_clusters(self.file)  # Read kit's mt-dna matches

    def __init__(self,id_p,name_p, day_p):
        self.date = day_p
        self.id = id_p
        self.name = name_p
        self.mk_mclu(self.name, self.file)

    def read_kits():
        tempkits = []
        with open('kits.csv', 'r') as read_obj:
            csv_reader = reader(read_obj)
            for k in csv_reader:
                    tempkits.append(k)
        return tempkits

    def getname(self):
        return self.name

    def getfilen(self):
        return self.file

    def show(self, debug1_p = False, debug2_p = False, debug3_p = False):
        if debug1_p != False:
            print('##### Kit', self.id, '#####', self.name, '#####')           # Show only minimal information:
            if debug2_p != False:                                              # Kit id and name.
                if self.mclu != None:                                          # If there are matches.
                        self.mclu.show(debug2_p,debug3_p)                      # dbg2: print clusters and amount.
                else:                                                          # dbg3: print match names too.
                    print('This kit has no mt-dna matches.')
        else:
            print('Program has read information of one kit.')
