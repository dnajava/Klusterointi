# Network clusters. Tools to add nodes, find duplicate clusters, delete duplicate clusters, split cluster.

class nclusters:
    def __init__(self, id_p, gd_p):
        self.id = id_p
        self.names = gd_p                    # This cluster has all kits of mcluster
        self.links = []
        self.ind = 0
        self.nclusters = []

    def __init__(self):
        self.nclusters = []
        self.ind = 0

    def add(self, cluster_p=[]):
        # First we create a tuple whwre is node name and then list of persons (oldest mother line mother)
        netnode = (self.ind, cluster_p)
        self.nclusters.append(netnode)
        self.ind += 1

    def show(self):
        print('NETCLUSTERS ===================================================')
        for a in self.nclusters:
            print(a)
            print('----------')
        print('NETCLUSTERS ===================================================')

    def find_duplicates(self):
        # https: // stackoverflow.com / questions / 1388818 / how - can - i - compare - two - lists - in -python - and -
        # return -matches

        print("Don't work yet. Bye.")
        return False

        found = False

        # Try to find duplicate cluster in nclusters list. If found and it's id is not same as searching tuple, it
        # should be deleted as duplicate.

        for clu in self.nclusters:
            if clu == cluster_p:
                if clu[0] != cluster_p[0]:
                    found = True
                    self.nclusers.remove(clu)
        if found:
            return found

    def remove(self, toremove_p):
        print("Cluster list remove don't work yet! Bye.")
        return False

    def to_be_splitted(self):
        return False

    def split(self, node_p):
        return False

    def clusteramount(self):
        i = 0
        for a in self.nclusters:
            i += 1
        return i


    def addlink(self,another):
        self.links.add(another)

    def split_cluster(self):
        print("Coming soon!")
        return

    def mdkalist(self):

        for clu in self.nclusters:
            print(clu[0])                   # clu id
            mli = clu[1]
            for b in mli:
                print(a[5])                 # mdka



