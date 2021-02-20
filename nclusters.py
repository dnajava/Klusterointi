# Network clusters. Tools to add nodes, find duplicate clusters, delete duplicate clusters, split cluster.
# Copyright Ilpo Kantonen 2021.

class nclusters:
    def __init__(self, id_p, gd_p):
        self.id = id_p
        self.names = gd_p                    # This cluster has all clusters of a kit
        self.links = []
        self.ind = 0
        self.nclusters = []

    def __init__(self):
        self.nclusters = []
        self.ind = 0

    def add(self, cluster_p):
        # First we create a tuple where is node name and then list of persons (oldest mother line mother)
        self.nclusters.append(cluster_p)
        self.ind += 1

    def amountclusters(self):
        i = 0
        for _ in self.nclusters:
            i += 1
        return i


# === Show or output clusters

    def show(self):
        print('Net clusters:')
        i = 0
        for a in self.nclusters:
            print('Cluster', i, ' ', end='')
            print(a, end='')
            print(' ')
            i += 1
        exit(0)

    def mk_txt(self, cluster_p=None):
        if cluster_p is None:
            print('MDKAs of GD-clusters')
            i = 0
            for c in self.nclusters:
                line1 = True
                for m in c:
                    if m[6] != '':
                        if line1:
                            print('Cluster', i)
                        print(' ' + m[6].strip(','))
                        line1 = False
                i += 1
        else:
            print('MDKAs of GD-', end=''),
            line1 = True
            i = 0
            for c2 in self.nclusters:
                if i == cluster_p:
                    # Now we are in right cluster
                    for m in c2:
                        if m[6] != '':
                            if line1:
                                print('Cluster', i, '\n', end=''),
                            print(' ' + m[6].strip(','))
                            line1 = False
                i += 1

    def show_mdkas(self, cluster_p=None):
        unknown = known = 0
        i = 0
        if cluster_p == None:
            for clu in self.nclusters:
                print('\nCluster', i + 1)
                for match in clu:
                    if match[6] == '':
                        unknown += 1
                    else:
                        known += 1
                        print(match[6])
                if unknown:
                    if known:
                        print('And ', end=''),
                    print(unknown, 'unknown MDKAs')
                i += 1

        else:
            for clu in self.nclusters:
                if i == cluster_p:
                    print('Cluster', i+1)
                    for match in clu:
                        if match[6] == '':
                            unknown += 1
                        else:
                            known += 1
                            print(match[6])
                i = i+1
            if unknown:
                if known:
                    print('And ', end=''),
                print(unknown, 'unknown MDKAs')

    def write_gephi_sources(self):
        # Write nodes.csv and links.csv
        # TODO: Add links between clusters.

        link_weight_persons = 80
        # link_weight_hubs = 200
        i = 0
        nodesfile = open("nodes.csv", "w")
        nodesfile.write('Id, Label, timeset\n')
        linksfile = open("links.csv", "w")
        linksfile.write('Source, Target, Type, Id, Label, timeset, Weight\n')

        for c in self.nclusters:
            stri = str(i) + ', M' + str(i) + ',\n'                                  # Write  node id  1,M1 2,M2 ...
            nodesfile.write(stri)
            i += 1
            cur_node = i

            link_id = 0
            for match in c:
                if match[6] == '':
                    str2 = str(i) + ', Unkwnown MDKA,' + '\n'
                    nodesfile.write(str2)
                    i += 1
                    # Source, Target, Type, Id, Label, timeset, Weight
                    str4 = str(i) + ',' + str(cur_node) + ',Directed,' + str(link_id)
                    str4 += ',,,' + str(link_weight_persons) + '\n'
                    linksfile.write(str4)
                    link_id += 1
                else:
                    str2 = str(i) + ', ' + match[6].replace(',', '') + ',\n'          # Take commas away from MDKA's
                    nodesfile.write(str2)
                    i += 1
                    # Source, Target, Type, Id, Label, timeset, Weight
                    str4 = str(i) + ',' + str(cur_node) + ',Directed,' + str(link_id) + ',,,'
                    str4 += str(link_weight_persons) +'\n'
                    linksfile.write(str4)
                    link_id += 1
        nodesfile.close()
        linksfile.close()

    # Not working yet
    def mk_spreadsheet(self):
        # TODO: Add code to make a spreadsheet
        # Spreadsheet header
        for c in self.nclusters:
            line1 = True
            for m in c:
                if m[6] != '':
                    if line1:
                        print('Cluster', m[0])
                    txt = ' ' + m[6].strip(',')
                    print(txt)
                    line1 = False
        # Spreadsheet end

    def mk_xml(self):
        # TODO: Add code to output other fields of match than mdka
        # Spreadsheet header

        print('<clusters>')                                 # Start of xml
        for c in self.nclusters:
            # line1 = True
            print('<cluster>')                              # Start of cluster
            for m in c:
                if m[6] != '':
                    print('<match>', end=''),
                    print(m[6].strip(','), end=''),
                    print('</match>')
            print('</cluster>')
        print('</clusters>')                                 # End of XML


# === Cluster operations

    def sort_mdkas(self):
        # This method sorts cluster mdkas to ascending order
        return False

    @staticmethod
    def is_equal_cluster(list_p1, list_p2):
        # https://thispointer.com/python-check-if-all-elements-in-a-list-are-same-or-matches-a-condition/
        if len(list_p1) != len(list_p2):
            return False
        i = 0
        for e in list_p1:
            if e == list_p2[i]:
                i += 1
            else:
                return False
        return True

    @staticmethod
    def samematch(m1_p, m2_p, debug1=False):
        for m1 in m1_p:
            for m2 in m2_p:
                if m1_p[1] == m2_p[1]:
                    if debug1 == True:
                        print('Same match: ', m1_p[1], ' ', m2_p[2], ' !!')
                    return True
        return False


    @staticmethod
    def samecluster(clu1_p, clu2_p, debug1=False):
        if len(clu1_p) != len(clu2_p):
            if debug1:
                print('nclusters.samecluster(): Different clusters, not as long.')
            return False

        # Both clusters are the same length. Analyze matches deeper.
        i = 0
        for i in range(len(clu1_p)):
            j = 0
            for j in range(len(clu2_p)):
                if nclusters.samematch(clu1_p[i], clu2_p[j], False):
                    if debug1:
                        print('nclusters.samecluster(): Same cluster because there is at least one same name.')
                    return True
                j += 1
            i += 1
        return False

    def delete_duplicates(self, debug=False):
        # https://stackoverflow.com/questions/1388818/how-can-i-compare-two-lists-in-python-and-return-matches
        # Do you want sorting? Sort cluster_p, sort clusters in nclusters if you are not using above method.

        # FIXME: Check that it deletes right duplicate clusters
        # FIXME: If there is only one cluster, or none.
        found = False
        if(debug):
            print('Nclusters delete_duplicates()')

        ind1 = 0
        for clu in self.nclusters:
            ind2 = ind1 + 1
            for clu2 in self.nclusters[(ind1+1):]:                # Compare first iterable with next to end of list
                if debug:
                    print('O =', ind1, ', I =', ind2)
                    print(clu, '\n', clu2)

                if nclusters.samecluster(clu, clu2, debug):
                    found = True
                    if debug:
                        print('Clusters were similair! Before popping lenght =', len(self.nclusters))

                    self.nclusters.pop(ind2)
                    if debug:
                        print('After popping lenght =', len(self.nclusters))

                    ind2 += 1
                    return True
                else:
                    if debug:
                        print('Clusters were different.\n')
                    ind2 += 1
            ind1 += 1
        if found:
            return found

    def remove(self, toremove_p):
        if toremove_p < len(self.nclusters):
            self.nclusters.pop(toremove_p)
            return True
        else:
            return False

    @staticmethod
    def to_be_splitted():
        # TODO: Add code to search clusters, which need split
        return False

    @staticmethod
    def split_cluster():
        # TODO: Add code to split cluster when needed
        print("Coming soon!")
        return


# Network operations

    def addlink(self, another_p):
        self.links.append(another_p)
