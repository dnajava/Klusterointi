__author__ = "Ilpo Kantonen"
__date__ = "$20.1.2021 2:01:51$"
# Cluster network program

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

    sint = 0
    while netclusters.split_clusters(True):             # Then split non GD uniform clusters
        sint += 1
    if sint:
        print('Splitted', sint, ' clusters.')

    netclusters.write('U8a1a1b1_unduplicated.json')

#    print('Popped', aint, 'duplicate clusters. After it there are', netclusters.amountclusters(), 'clusters.')
#    netclusters.show_mdkas()                            # Print all clusters (MDKAs)

    # netclusters.mk_txt(1)                             # Print one cluster (MDKAs)
    # netclusters.mk_xml()                              # Print in XML form

    # netclusters.write_gephi_sources()                   # Write nodes.csv and links.csv to Gephi

