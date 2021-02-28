"""
Network of mt-dna GD clusters. Tools to add nodes, find and delete duplicate clusters, split cluster. Export to
txt, xml or spreadsheet. And make nodes.csv and links.csv to Gephi.
Copyright Ilpo Kantonen 2021. You may use and modify this program. Tell to author.
"""

# FIXME: pip3 install pyexcel-ods3 (doesn't work)
# import pyexcel_ods3
# from pyexel_io import save_data
import json

class nclusters:
    def __init__(self, id_p, gd_p):
        self.id = id_p
        self.names = gd_p                    # This cluster has all clusters of a kit
        self.haplogroup = 'Default'
        self.links = []
        self.ind = 0
        self.nclusters = []

# === Constructors

    def __init__(self):
        self.haplogroup = 'Default'
        self.nclusters = []
        self.ind = 0

# === Show or output clusters

    def show(self):
        print('Net clusters:')
        i = 0
        for a in self.nclusters:
            print('Cluster', i, ' ', end='')
            print(a, end='')
            print(' ')
            i += 1

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
        i = 0
        if cluster_p == None:
            for clu in self.nclusters:
                unknown = 0
                known = 0
                print('\nCluster', i+1)
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
                    unknown = 0
                    known = 0
                    print('\nCluster', i+1)
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

    def amount_unknown_mdkas(self, cluster_p=None):
        i = 0
        if cluster_p == None:
            for clu in self.nclusters:
                unknown = 0
                print('\nCluster', i+1)
                for match in clu:
                    if match[6] == '':
                        unknown += 1
                i += 1
            return unknown
        else:
            for clu in self.nclusters:
                if i == cluster_p:
                    unknown = 0
                    print('\nCluster', i+1)
                    for match in clu:
                        if match[6] == '':
                            unknown += 1
                i = i+1
            return unknown

# === Basic Cluster Operations

    def add(self, cluster_p):
        # First we create a tuple where is node name and then list of persons (oldest mother line mother)
        self.nclusters.append(cluster_p)
        self.ind += 1

    def sort_mdkas(self):
        # This method sorts cluster mdkas to ascending order
        return False

    @staticmethod
    def is_equal_cluster(list_p1, list_p2):
        """
        :param list_p1:
        :param list_p2:
        :return:
        U{https://thispointer.com/python-check-if-all-elements-in-a-list-are-same-or-matches-a-condition/}
        """

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
    def samematch(m1_p, m2_p):
        for m1 in m1_p:
            for m2 in m2_p:
                if m1_p[1] == m2_p[1]:
                    return True
        return False

    @staticmethod
    def samecluster(clu1_p, clu2_p):
        print('samecluster')
        if len(clu1_p) != len(clu2_p):
            return False

        # Both clusters are the same length. Analyze matches deeper.
        i = 0
        for i in range(len(clu1_p)):
            j = 0
            for j in range(len(clu2_p)):
                a = 1
                if nclusters.samematch(clu1_p[i], clu2_p[j]):
                    return True
                j += 1
            i += 1
        return False

    def remove(self, toremove_p):
        if toremove_p < len(self.nclusters):
            self.nclusters.pop(toremove_p)
            return True
        else:
            return False

# === Clusters Processing

    def amountclusters(self):
        i = 0
        for _ in self.nclusters:
            i += 1
        return i

    def copy_extra_matches(self, clu_p1, clu_p2):
        extras = []
        for c2 in clu_p2:
            found = False
            for c1 in clu_p1:
                if c2[1] == c1[1]:
                    found = True
            if not found:
                extras.append(c2)
        if len(extras):
            clu_p1.append(extras)

    def delete_duplicates(self):
        """
        :param debug:
        :return:

        U{https://stackoverflow.com/questions/1388818/how-can-i-compare-two-lists-in-python-and-return-matches}
        """
        if len(self.nclusters) < 1:                      # There are only 1 or 0 clusters
            return False

        # FIXME: Check again if right duplicate clusters are deleted.
        found = False
        ind1 = 0
        for clu in self.nclusters:
            ind2 = ind1 + 1
            for clu2 in self.nclusters[(ind1+1):]:                # Compare first iterable with next to end of list
                if nclusters.samecluster(clu, clu2):
                    found = True
                    self.copy_extra_matches(clu, clu2)            # Cluster to be deleted can contain matches,
                    self.nclusters.pop(ind2)                      # which original cluster don't have
                    ind2 += 1
                    return True
                else:
                    ind2 += 1
            ind1 += 1
        if found:
            return found

    def split_cluster(self, clu_original_p, clu_check_p):
        # Add matches to new cluster. And new cluster to clusters list.
        # FIXME: Test, if this split cluster works.
        new_clu = mclusters()
        for m in clu_check_p:
            for m2 in clu_original_p:
                if m != m2:
                    new_clu.append(m)
        if len(new_clu) < 1:
            return None
        else:
            return new_clu

    def split_clusters(self):
        """
        :param debug:
            Debug mode, prints more information processing data.
        :return:
            If there occurred a split, return True.

        This is maybe most complicated in nclusters and in wholw program.
        You may take a big cup of good coffee. And sit down and think.

        One method: Find all common matches between two clusters. Split other matches to new cluster.
        Do that to every cluster pairs (takes n ** 2 cluster pair comparisons). When there is nothing to split,
        splitting is done and saturated. Sounds good or best of not so good methods. :)
        Split only if there are common uniform set of matches which are in both cluster. If you split
        strange clusters, it's infinite loop. And don't add new cluster to list. It can cause strange
        situation. Add when the loop has run out.

        Second method: Take a match in some cluster. And search it from other clusters. If found, look that
        there all is same GD from original cluster. Hmmm....

        One method is to take one tested and compare it's matches to all other tested. If all tested have same
        GD values to all cluster matches, split is saturated. If not, there is something to split
        """

        found = False
        ind1 = 0
        for clu in self.nclusters:
            ind2 = ind1 + 1
            for clu2 in self.nclusters[(ind1+1):]:                # Compare first iterable with next to end of list
                # Test if the two cluster have matches which have different GD-value than others.
                # So, they belongs to other new cluster
                if compare_cluster_pair(clu, clu2):
                    return True
        return False

# === Output Clusters to other format

    def mk_spreadsheet(self, fname_p='spreadsheet.ods'):
        """
        :param fname_p:
            Filename of spreadsheet to be created.
        :return:
            Nothing.

        Uses pyexel-ods3 package https://pypi.org/project/pyexcel-ods3/
        This function doesn't work yet.

        """

        # ods_save
        sheet = []
        clu = []

        # FIXME: Add code to make a spreadsheet and save it to file

        i = 0
        for x in self.nclusters:
            for x2 in x:
                clu += x2
            sheet += clu
        ods_save.save_data(fname_p, sheet)

    def mk_xml(self):
        """
        :return:
            Nothing

        This function prints XML document of haplogroup MDKAs.
        """

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

# === File operations

    def read(self, fname_p='mt-dna.json'):
        with open(fname_p, 'r') as f:
            self.nclusters = json.load(f)

    def write(self, fname_p='mt-dna.json'):
        """
        :param fname_p:
        :return:
        """
        """ Use Json to save network
        U{https://stackoverflow.com/questions/27745500/how-to-save-a-list-to-a-file-and-read-it-as-a-list-type}
        """

        with open(fname_p, 'w') as f:
            # indent=2 is not needed but makes the file human-readable
            json.dump(self.nclusters, f, indent=2)

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

# END of nclusters


# @staticmethod
# def samematch(m1_p, m2_p):
#     for m1 in m1_p:
#         for m2 in m2_p:
#             if m1_p[1] == m2_p[1]:
#                 if debug1 == True:
#                     print('Same match: ', m1_p[1], ' ', m2_p[2], ' !!')
#                 return True
#     return False


def compare_cluster_pair(clu1_p, clu2_p):
    # TODO: Add code to compare if two clusters are GD uniform or not.
    #  If they are not, move extra matches to new cluster
    return False

