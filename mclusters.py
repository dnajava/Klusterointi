# MCluster is Match Cluster of some Kit (tested person)
from csv import reader

class mclusters:
    gd0 = []
    gd1 = []
    gd2 = []
    gd3 = []
    gd = [gd0, gd1, gd2, gd3]

    def __init__(self):
        self.gdmax = 4
        self.gd0 = []
        self.gd1 = []
        self.gd2 = []
        self.gd3 = []
        self.gd = [self.gd0, self.gd1, self.gd2, self.gd3]

    def __init__(self,name_p,fname_p):
        self.gdmax = 4
        self.gd0 = []
        self.gd1 = []
        self.gd2 = []
        self.gd3 = []
        self.gd = [self.gd0, self.gd1, self.gd2, self.gd3]
        self.name = name_p
        self.fname = fname_p

    def show(self, debug2_p = False, debug3_p = False):
        i = 0
        for y in self.gd:
            if debug2_p:
                print('GD', i, 'cluster and there are', len(y), 'matches.')
                i += 1
            if debug3_p:
                for z in y:
                    print(z[1], ' ', end='')
                print('')
        print('')

    def get_cluster(self, level = 0):
        if level == 0:
            if self.gd0 != None:
                return self.gd0
        if level == 1:
            if self.gd1 != None:
                return self.gd1
        if level == 2:
            if self.gd2 != None:
                return self.gd2
        if level == 3:
            if self.gd3 != None:
                return self.gd3


    def read_clusters(self, fname_p):
        ind = 0
        matches = []

        with open(fname_p, 'r') as read_obj:
            csv_reader = reader(read_obj)
            for m in csv_reader:
                if ind > 0:
                    matches.append(m)
                ind += 1

        for x in matches:
            if x[0] == '0':
                self.gd0.append(x)
            if x[0] == '1':
                self.gd1.append(x)
            if x[0] == '2':
                self.gd2.append(x)
            if x[0] == '3':
                self.gd3.append(x)
