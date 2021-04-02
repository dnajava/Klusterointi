"""
Network of mt-dna GD clusters. Tools to add nodes, find and delete duplicate clusters, split cluster. Export to
txt, xml or spreadsheet. And make nodes.csv and links.csv to Gephi.
Copyright Ilpo Kantonen 2021. You may use and modify this program. Tell to author.
"""
from mtsettings import GDMAX
from mtsettings import HAPLOGROUP
from link import Link
from clusters import Match
from clusters import NetCluster
import json
# import pyexcel_ods3
# from pyexel_io import save_data
# import copy

class Nclusters:
    """Cluster network and it's operations"""
    nclusters = None                                # Clusters from kits gd clusters

    def __init__(self, haplogroup_p=HAPLOGROUP):
        """
        Constructs cluster network.
        :param haplogroup_p:
        """
        self.ind = 0
        self.haplogroup = haplogroup_p

    # === Show or output clusters

    def show_cluster_matches(self, i=0):
        for match in self.nclusters[i].matches:
            match.show()

    def show(self, wide: bool = False, extra_wide: bool = False, links_p: bool = False):
        if self.nclusters is None:
            print('Cluster network is empty.')
            pass
        else:
            print('Net clusters of', self.haplogroup, ':')
            i = 0
            for a in self.nclusters:
                if i < 10:
                    print('Cluster ', i, end=''),
                else:
                    print('Cluster', i, end=''),
                print(' has', len(a.matches), 'matches.')

                if wide:
                    for b in a.matches:
                        b.show()

                i += 1

                if links_p:
                    if len(a.linksfrom) > 0:
                        print('Cluster links from', self.haplogroup, ':')
                        for li in a.linksfrom:
                            li.show()
                        # self.show_links()
                    else:
                        print('No links from this cluster', self.haplogroup, 'network.')

                    if len(a.linksto) > 0:
                        print('Cluster links to', self.haplogroup, ':')
                        for li in a.linksto:
                            li.show()
                        # self.show_links()
                    else:
                        print('No links to this cluster', self.haplogroup, 'network.')


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

    def add_kit(self, kit_p):
        # First we create a tuple where is node name and then list of persons (oldest mother line mother)
        if self.nclusters is None:
            self.nclusters = []

        for g in kit_p.gds:
            nc = NetCluster('Noname')
            for m in g:
                nc.add_match(m)
            self.nclusters.append(nc)                    # Modify KitClusters to NetClusters and add to list

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
    def is_same_match(m1_p: Match, m2_p: Match) -> bool:
        """
        Returns true if the contents of matches are equal
        :param m1_p:    Match 1
        :param m2_p:    Match 2
        :return: bool   Are the content of matches equal?
        """
        # print('Cnetwork is_same_match:\n', m1_p,'\n', m2_p)
        for i in range(1, len(m1_p)):                       # Index begins from 1, since 0 is GD which can vary
            if m1_p[i] != m2_p[i]:
                # print('No, field', i, 'was different', m1_p[i], m2_p[i])
                return False
        # print('Yes, match is same.')
        return True

    def prepare_clusters(self):
        """
        Fill the kit owners bogus match. And add links to NetClusters grouped by KitClusters 0 - 3.
        :return:
        """
        i = 0
        for c in self.nclusters:
            if i % 4 == 0:  # Is that kit cluster 0 ?
                # print('Prepare cluster', i)
                self.add_first_kit_cluster_data(i)                  # Add kit owners bogus match full of data
                for j in range(1, 3):                               # Add doublelinks to kit gd clusters 0 - 3.
                    lif = Link(c, self.nclusters[i + j], j)
                    lit = Link(self.nclusters[i + j], c, j)
                    c.linksfrom.append(lif)   # self.nclusters[i]
                    c.linksto.append(lit)
                    self.nclusters[i + j].linksfrom.append(lit)
                    self.nclusters[i + j].linksto.append(lif)
            i += 1

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

#    @staticmethod
    def add_first_kit_cluster_data(self, ind_p) -> bool:
        """
        Searches and copies kit owner data from some match of network. Why? Read documents.
        :return: bool Did the kit owner match get all fields from some other match?
        """
        if self.nclusters is None:
            return False

        # FIXME: Network has 4 empty kit clusters. How is kit owners names and other data?

        if not 0 <= ind_p < len(self.nclusters):
            print('Cnetwork add_first_kit_cluster_data: parameter index out of ncluster list.')
            return False

        if not ind_p % 4 == 0:                              # Is cluster kit cluster 0 (kit owners cluster 0)
            print('Cnetwork add_first_kit_cluster_data: Index', ind_p, 'not kit cluster 0.')
            return False

        search_name = self.nclusters[ind_p].matches[0].Fullname     # Kit owner cluster 0 first match has kit owner name
        bogus_match = self.nclusters[ind_p].matches.pop(0)          # Take away and keep bogus match

        # print('Add_first... sname=', search_name, ' bogus=', bogus_match.Fullname)
        for c in self.nclusters:
            if len(c.matches) > 0:
                for m in c.matches:
                    if m.Fullname == search_name and m.Firstname != '':
                        bogus_match.Firstname = m.Firstname
                        bogus_match.Middlename = m.Middlename
                        bogus_match.Lastname = m.Lastname
                        bogus_match.Email = m.Email
                        bogus_match.MDKA = m.MDKA
                        # bogus_match.Date = m.Date
                        self.nclusters[ind_p].matches.insert(0, bogus_match)
                        return True
#            else:
#                print('Cnetwork add_first_kit_cluster_data() Cluster', ind_p, ' is empty.')
        return False

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
