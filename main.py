# Cluster network program
# import kit
from kit import kit
# from datetime import date
# import mclusters
import nclusters
__author__="Ilpo Kantonen"
__date__ ="$20.1.2021 2:01:51$"
if __name__ == '__main__':
    kits = []                                           # This is list of kits. First empty.
    kits_to_list = kit.read_kits()                      # Read information of kits from kits.csv.

    for k in kits_to_list:
        new_kit = kit(k[0], k[1], k[2])                 # Create kit which have information and clustered matches.
        kits.append(new_kit)                            # Add to list.

    netclusters = nclusters.nclusters()
    for k in kits:                                      # Add every kits every GD clusters to netclusters
        for i in range(0,4):
            if(k.mclu.gd[i] != None):
                netclusters.add(k.mclu.get_cluster(i))

    # netclusters.show_all_mdkas()
    # netclusters.show_cluster_mdkas(1)                   # Print cluster 1 mdkas or unknown

#    while True:                                         # Do while duplicate clusters
#        todelete = netclusters.clusteramount()
#        if todelete == None:
#            break
#        netclusters.remove(todelete)
#        # FIXME: Test this, that it works

#    while True:                                         # Do while nodes which should be splitted
#        node =  netclusters.to_be_splitted()
#        if node == None:
#            break
#        netclusters.split(node)
#        # FIXME: Test this, that it works

#   netclusters.write_gephi_sources()
