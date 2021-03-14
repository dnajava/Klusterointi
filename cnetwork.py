"""
Network of mt-dna GD clusters. Tools to add nodes, find and delete duplicate clusters, split cluster. Export to
txt, xml or spreadsheet. And make nodes.csv and links.csv to Gephi.
Copyright Ilpo Kantonen 2021. You may use and modify this program. Tell to author.
"""

# FIXME: pip3 install pyexcel-ods3 (doesn't work)
# import pyexcel_ods3
# from pyexel_io import save_data
import json
from mtsettings import GDMAX
from mtsettings import HAPLOGROUP
from links import Link


class Nclusters:
    links = []                                      # Links between two clusters GD 1 - 3
    nclusters = None                                # Clusters from kits gd clusters

    def __init__(self, haplogroup_p=HAPLOGROUP):
        """
        Constructs cluster network.
        :param haplogroup_p:
        """
        self.ind = 0
        self.haplogroup = haplogroup_p

# === Show or output clusters

    def show_links(self, debug=False):
        for v in self.links:
            if debug:
                print('nclusters show_link: v=', v)
            else:
                print(v)

    def show_cluster_matches(self, i=0, wide=False):

        if wide:
            print(' matches:')
        else:
            print('Cluster', i, 'matches:')

        for match in self.nclusters[i]:
            match.show()

    def show(self, wide: bool = False):
        if self.nclusters is None:
            print('Cluster network is empty.')
            pass
        else:
            print('Net clusters of', self.haplogroup, ':')
            i = 0
            for a in self.nclusters:
                if i < 10:
                    print('Cluster ', i, '\t', end=''),
                else:
                    print('Cluster', i, '\t', end=''),

                if len(a) < 10:
                    print('', len(a), 'matches.', end=''),
                else:
                    print(len(a), 'matches.', end=''),

                if wide:
                    self.show_cluster_matches(i, True)
                else:
                    print()
                i += 1

            if len(self.links) > 0:
                print('Cluster links in', self.haplogroup, ':')
                self.show_links()
            else:
                print('No links between clusters in', self.haplogroup, 'network.')

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

    def mk_email_list(self) -> str:
        """
        Returns list of emails in network.
        :return: str List of emails with ; in network
        """
        email_list = []
        for c in self.nclusters:
            for m in c:
                email_list.append(m.Email)
        """
        Remove duplicate emails before returning
        U{https://www.w3schools.com/python/python_howto_remove_duplicates.asp}
        """
        email_list = list(dict.fromkeys(email_list))
        e_list = ''
        for em in email_list:
            e_list += em + '; '
        return e_list

    def show_mdkas(self, cluster_p=None):
        known, unknown = 0, 0
        i = 0
        # FIXME: Known and unknown problem. Is that individual match or total all matches?

        if cluster_p is None:
            for clu in self.nclusters:
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
        unknown = 0
        i = 0
        if cluster_p is None:
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

        if self.nclusters is None:
            self.nclusters = []

        self.nclusters.append(cluster_p)
        self.ind += 1

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
    def is_same_match(m1_p, m2_p):
        # print('is same match:\n', m1_p,'\n', m2_p)
        if len(m1_p) != len(m2_p):
            # print('No, they are different length.')
            return False

        i = 1                                                   # Index begins from 1, since 0 is GD which can vary
        for m1 in m1_p:
            if m1_p[i] != m2_p[i]:
                # print('No, field', i, 'was different', m1_p[i], m2_p[i])
                return False
        # print('Yes, match is same.')
        return True

    @staticmethod
    def is_same_cluster(clu1_p, clu2_p):
        if len(clu1_p) != len(clu2_p):
            return False

        # Both clusters are the same length. Analyze if matches are same as pairs.
        for i in range(len(clu1_p)):
            for j in range(len(clu2_p)):
                for ix in range(1, 9):                      # First field GD can vary, ignore it
                    if not Nclusters.is_same_match(clu1_p[ix], clu2_p[ix]):
                        return False
        # print('Yes, clusters are same.')
        return True

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

    @staticmethod
    def copy_extra_matches(clu_p1, clu_p2):
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
        Deletes one duplicate pair and returns true. If not duplicates found, returns False.
        :param:
        :return:

        U{https://stackoverflow.com/questions/1388818/how-can-i-compare-two-lists-in-python-and-return-matches}
        """
        if len(self.nclusters) < 1:                      # There are only 1 or 0 clusters, can't find duplicates.
            return False

        # FIXME: Check again if right duplicate clusters are deleted.
        found = False
        ind1 = 0
        for clu1 in self.nclusters:
            ind2 = ind1 + 1
            for clu2 in self.nclusters[(ind1+1):]:                # Compare first iterable with next to end of list
                if Nclusters.is_same_cluster(clu1, clu2):
                    # found = True
                    # print('Found same clusters',ind1,'(',len(clu),') and ',ind2,'(',len(clu2),')')
                    issamematch = True
                    for ix in range(0, len(clu1)):
                        if clu1[ix] != clu2[ix]:
                            issamematch = False
                    if issamematch:
                        # found = True
                        # print('Same matches paired.')
                        pass
                    else:
                        # found = False
                        # print('Not same matches.')
                        pass
#                   self.copy_extra_matches(clu, clu2)            # Cluster to be deleted can contain matches,
                    self.nclusters.pop(ind2)                      # which original cluster don't have
                    # print('Removed cluster', ind2)
                    ind2 += 1
                    return True
                else:
                    ind2 += 1
            ind1 += 1
        if found:
            return found

    @staticmethod
    def split_cluster(clu_original_p, clu_check_p):
        # Add matches to new cluster. And new cluster to clusters list.
        # FIXME: Test, if this split cluster works.
        new_clu = []
        # mcluster()
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
        :return: bool
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

        # found = False
        ind1 = 0
        for clu in self.nclusters:
            # ind2 = ind1 + 1
            for clu2 in self.nclusters[(ind1 + 1):]:                # Compare first iterable with next to end of list
                # Test if the two cluster have matches which have different GD-value than others.
                # So, they belongs to other new cluster
                if compare_cluster_pair(clu, clu2):
                    return True
        return False

    def search_match(self, mname_p) -> bool:
        """
            If mname_p is in cluster_p return True, otherwise False.
        :param mname_p:
            Search match name
        :return: bool
            True if mname_p is in cluster_p.
        """
        for c in self.nclusters:
            for m in c:
                if m[1] == mname_p:
                    return True
        return False

    @staticmethod
    def add_first_kit_cluster_data(nclus_p, ind_p):
        """
        Searches and copies kit owner data from some match of network. Why? Read documents.
        :return:
        """
        print(nclus_p[ind_p])

#        search_name = nclus_p[ind_p][0][1][0]  # Kit owner is on the first cluster
        search_name = 'Ilpo Kantonen'
        c1 = 0
        if len(nclus_p[ind_p]) > 0:                             # Is kit owner cluster empty?
            for c in nclus_p:
                c1 += 1
                m2 = 0
                for m in c:
                    m2 += 1
#                    if m[1][0] == search_name:
                    print('Etsitään klusterin ensimmäistä mätsin kokonimeä. Se on', m.Fullname)
                    if m[0] == search_name:
                        if (m2 - 1 != ind_p) and him_not_empty(m):
                            him = nclus_p[c1 - 1][m2 - 1][1]    # This is bogus tuple in full flavor from found tuple
                            removed_cluster = nclus_p.pop(ind_p)            # Remove cluster containing bogus match
                            bogusmatch = removed_cluster[0][0][0]           # Extract bogus match
                            temp3 = (bogusmatch, '0')
                            tempmatch = (temp3, him)                                  # nclus_p[c1 - 2][m2 - 1][1])
                            temptuplelist = []
                            temptuplelist.append(tempmatch)
                            for ix in range(1, len(removed_cluster)):
                                temptuplelist.append(removed_cluster[ix])
                            nclus_p.insert(ind_p, temptuplelist)
                            return
        return

    # === Network operations

    def add_gd_links(self, debug=False):
        if debug:
            print('cnetwork.add_gd_links: Begins adding links to network clusters.')
        for i in range(0, len(self.nclusters), 4):
            if debug:
                print('To every fourth cluster:', i)
            for j in range(1, GDMAX):
                if debug:
                    print('cnetwork.add_gd_links: clu', i, 'r', j, ':\t', i, '->', i+j)
                if (self.nclusters[i] is not None) and (self.nclusters[i+j] is not None):
                    #  tmp_link = Link(i, i+j, j)
                    #  self.add_gd_links(i, i+j, j)
                    pass
                else:
                    if debug:
                        print('List item', i, 'or', j, 'was None.')
        print('add_gd_links: done.')

    def add_link(self, clu1_p, clu2_p, dist_p):

        tmp_link = Link(clu1_p, clu2_p, dist_p)
        self.links.append(tmp_link)

    #    if clu2_p not in clu1_p.links[0]:                               # Is there already a link
    #        clu1_p.links.append(tuple(clu2_p, dist_p))
    #        clu2_p.links.add(tuple(clu1_p, dist_p))

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

        for x in self.nclusters:
            for x2 in x:
                clu += x2
            sheet += clu
        # pyexel_ods3.save_data(fname_p, sheet)

        with open(fname_p, 'w') as f:
            # indent=2 is not needed but makes the file human-readable
            sheet.save_data(f, 'w')              # This doesn't work, but...



    def mk_xml(self):
        """
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

    def gephi(self):
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
                    str4 += str(link_weight_persons) + '\n'
                    linksfile.write(str4)
                    link_id += 1
        nodesfile.close()
        linksfile.close()

# END of nclusters

def compare_cluster_pair(clu1_p, clu2_p):
    # TODO: Add code to compare if two clusters are GD uniform or not.
    #  If they are not, move extra matches to new cluster
    if clu1_p is not clu2_p:
        pass  # nonsense if, because no error messages
    return False


def him_not_empty(m_p: tuple) -> bool:
    notempty = False
    for i in range(1, 7):
        if m_p[1][i] != '':
            notempty = True
    return notempty

def show_him(m_p: tuple):
    print('Him:', end=''),
    for i in range(1, 7):
        print(m_p[1][i], 'x', end=''),
    print()
