__author__ = "Ilpo Kantonen"
__date__ = "$20.1.2021 2:01:51$"
# Cluster network program. It makes nodes.csv and links.csv to Gephi. Gephi can display a network of mt-dna matches
# in one haplogroup. The match clusters can be subgroups to that haplogroup. Grouping depends on GD values between
# matches. You can also print MDKA:s as txt and xml file and a spreadsheet.

# This is the main purpose to this program. You can do other things with this program too. Be free to modify code.
# If you think you know better methods to do something, feel free to contact and tell to Ilpo at ilpo@iki.fi.

# Input to this program are downloaded mt-dna match lists from FTDNA. Output are nodes.csv and links.csv. With Gephi
# you can do bautiful graphs of GD network.

# Version 0.1.1.

from kit import kit
import nclusters

if __name__ == '__main__':
    kits = []                                           # This is list of kits. First empty.
    kits_to_list = kit.read_kits()                      # Read information of kits from kits.csv.

    for k in kits_to_list:
        new_kit = kit(k[0], k[1], k[2])                 # Create kit which have information and clustered matches.
        kits.append(new_kit)                            # Add to list.

    netclusters = nclusters.nclusters()
    for k in kits:                                      # Add every kits every GD clusters to netclusters
        for i in range(0, len(kits)+1):
            if(k.mclu.gd[i] != None):
                netclusters.add(k.mclu.get_cluster(i))

    # netclusters.write('U8a1a1b1_duplicated.json')

    dint = 0
    while netclusters.delete_duplicates():              # First delete duplicates
        dint += 1
    if dint:
        print('Removed', dint, 'duplicate clusters.')

    # netclusters.write('U8a1a1b1_unduplicated.json')

    sint = 0
    while netclusters.split_clusters(True):             # Then split non GD uniform clusters
        sint += 1
    if sint:
        print('Splitted', sint, ' clusters.')

    # netclusters.write('U8a1a1b1_splitted.json')

#    netclusters.show_mdkas()                            # Print all clusters (MDKAs)

    # netclusters.mk_txt(1)                             # Print one cluster (MDKAs)
    # netclusters.mk_xml()                              # Print in XML form

    # netclusters.write_gephi_sources()                   # Write nodes.csv and links.csv to Gephi

