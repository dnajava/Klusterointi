'''
One net cluster.
Copyright Ilpo Kantonen 2025-10-25. You may use and modify this program. Tell to author.
'''


from mtsettings import GDMAX, HAPLOGROUP, FENCODING
from link import Link
from cluster import Cluster
from kit import Kit
from match import Match

class NetCluster(Cluster):
    '''
    On3 Network cluster. Tools to add nodes, find and delete duplicate clusters, split cluster. Export to
    txt, xml or spreadsheet. And make nodes.csv and links.csv to Gephi.
    '''

    matches: list                               # List of matches in this cluster


    def __init__(self,name_p:str="Cluster"):
        """
        Constructor of netcluster.
        :param name_p:              Name of this cluster
        :param haplogroup_p:        Haplogroup of this cluster
        """
        super().__init__(name_p)


    def add_matches(self, matches_p:list):
        if matches_p is None:
            return
        else:
            self.metches = matches_p



    ''' === File operations '''

    def set_name(self, name_p: str="Cluster"):
        self.name = name_p

    def get_name(self):
        return self.name

    def count(self) -> int:
        return len(self.matches)

    # === Show or output clusters

    def show_cluster_matches(self, i=0):
        ''' Show cluster matches '''
        for match in self.matches:
            match.show()

    def show_mdkas(self):
        for match in self.matches:
            print("MDKA ", match.mdka)


    def mk_txt(self, cluster_p=None):
        ''' make text '''
        if cluster_p is None:
            print("MDKAs of GD-clusters")
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
            print('MDKAs of GD-', end='')
            line1 = True
            i = 0
            for c2 in self.nclusters:
                if i == cluster_p:
                    # Now we are in right cluster
                    for m in c2:
                        if m[6] != '':
                            if line1:
                                print('Cluster', i, '\n', end='')
                            print(' ' + m[6].strip(','))
                            line1 = False
                i += 1

    ''' === Basic Cluster Operations '''

    def search_matches_from_clusters(self, name_p: Match = None) -> list:
        """
        Search match from whole network and collect cluster containing that match to a collection.
        Then filter non common matches away and split them own clusters. Then you have a common cluster.
        Prepare links to pointing to it. This is maybe a complicated process.

        :return: list
        """
        if name_p is None:
            return None

        tmp_integrated = []
        cind = 0
        for c in self.nclusters:
            for m in c.matches:
                if m.Fullname == name_p:
                    tmp_integrated.append(cind)
            cind += 1
        return tmp_integrated

    def add_kit_gd(self, match_cluster:dict=None):
        ''' Add one kit match cluster to netcluster '''
        # print("kit_p tyyppi=", type(kit_p))
        self.matches = match_cluster

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
        '''Returns true if the contents of matches are equal '''
        # print('Cnetwork is_same_match:\n', m1_p,'\n', m2_p)
        for i in range(1, len(m1_p)):                       # Index begins from 1, since 0 is GD which can vary
            if m1_p[i] != m2_p[i]:
                # print('No, field', i, 'was different', m1_p[i], m2_p[i])
                return False
        # print('Yes, match is same.')
        return True


''' General operations of clusters '''

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
    ''' Is same cluster '''
    if clu1_p != clu2_p:
        return False

    # Both clusters are the same length. Analyze if matches are same as pairs.
        for _ in range(len(clu1_p)):
            for _ in range(len(clu2_p)):
                for ix in range(1, 9):                      # First field GD can vary, ignore it
                    if not Nclusters.is_same_match(clu1_p[ix], clu2_p[ix]):
                        return False
        # print('Yes, clusters are same.')
        return True

    def remove(self, toremove_p):
        ''' Remove from nclusters '''
        code = False
        if toremove_p < len(self.nclusters):
            self.nclusters.pop(toremove_p)
            code=True
        return code

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
        ''' Deletes one duplicate pair and returns true. If not duplicates found, returns False '''
        # U{https://stackoverflow.com/questions/1388818/how-can-i-compare-two-lists-in-python-and-return-matches}
        if self.nclusters is None:                      # There are only 1 or 0 clusters, can't find duplicates.
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
        ''' Split cluster '''
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
        '''
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
        '''

        # found = False
        ind1 = 0
        if self.nclusters is None:
            return False
        for clu in self.nclusters:
            # ind2 = ind1 + 1
            for clu2 in self.nclusters[(ind1 + 1):]:                # Compare first iterable with next to end of list
                # Test if the two cluster have matches which have different GD-value than others.
                # So, they belongs to other new cluster
                if compare_cluster_pair(clu, clu2):
                    return True
        return False

    def search_match(self, mname_p) -> bool:
        '''If mname_p is in cluster_p return True, otherwise False. '''
        for c in self.nclusters:
            for m in c:
                if m[1] == mname_p:
                    return True
        return False

    # @staticmethod
    def add_first_kit_cluster_data(self, ind_p) -> bool:
        '''
        Searches and copies kit owner data from some match of network. Why? Read documents.
        :return: bool Did the kit owner match get all fields from some other match?
        '''
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
                    if m.Fullname == search_name and m.firstname != '':
                        bogus_match.firstname = m.firstname
                        bogus_match.Middlename = m.Middlename
                        bogus_match.lastname = m.lastname
                        bogus_match.Email = m.Email
                        bogus_match.MDKA = m.MDKA
                        # bogus_match.Date = m.Date
                        self.nclusters[ind_p].matches.insert(0, bogus_match)
                        return True
            # else:
            #   print('Cnetwork add_first_kit_cluster_data() Cluster', ind_p, ' is empty.')
        return False

    ''' === Network operations '''

    def add_gd_links(self, debug=False):
        ''' Add GD links '''
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

    ''' === Output Clusters to other format '''

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
        ''' This function prints XML document of haplogroup MDKAs. '''
        print('<clusters>')                                 # Start of xml
        for c in self.nclusters:
            # line1 = True
            print('<cluster>')                              # Start of cluster
            for m in c:
                if m[6] != '':
                    print('<match>', end='')
                    print(m[6].strip(','), end='')
                    print('</match>')
            print('</cluster>')
        print('</clusters>')                                 # End of XML

    def gephi(self):
        ''' Write nodes.csv and links.csv '''
        # TODO: Add links between clusters.

        link_weight_persons = 80
        # link_weight_hubs = 200
        i = 0
        nodesfile = open("nodes.csv", "w")
        nodesfile.write('Id, Label, timeset\n')
        linksfile = open("links.csv", "w")
        linksfile.write('Source, Target, Type, Id, Label, timeset, Weight\n')

        for c in self.nclusters:
            stri = str(i) + ', M' + str(i) + ',\n'  # Write  node id  1,M1 2,M2 ...
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
                    str2 = str(i) + ', ' + match[6].replace(',', '') + ',\n'  # Take commas away from MDKA's
                    nodesfile.write(str2)
                    i += 1
                    # Source, Target, Type, Id, Label, timeset, Weight
                    str4 = str(i) + ',' + str(cur_node) + ',Directed,' + str(link_id) + ',,,'
                    str4 += str(link_weight_persons) + '\n'
                    linksfile.write(str4)
                    link_id += 1
        nodesfile.close()
        linksfile.close()

def compare_cluster_pair(clu1_p, clu2_p):
    ''' Vertaile klusteriparia. Ilmeisesti, ovatko ne samankaltaiset.  '''
    # TODO: Add code to compare if two clusters are GD uniform or not.
    #  If they are not, move extra matches to new cluster
    if clu1_p is not clu2_p:
        pass  # nonsense if, because no error messages
    return False

def is_adjacent(cluster1_p, cluster2_p) -> bool:
    """
    If cluster1 is adjacent to cluster2 returns True, otherwise False.
    :param cluster1_p:
        Cluster1 where to search
    :param cluster2_p:
        Cluster2 where to search
    :return: bool
        True if mname_p is in cluster_p.
    """
    same = 0                                            # How many same matches there are in cluster1_p
    for m in cluster1_p.Nclusters:
        for m2 in cluster2_p.Nclusters:
            if m[1] == m2[1]:                           # Are names of matches same?
                same += 1
    result = False
    return result



