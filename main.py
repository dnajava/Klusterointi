# Cluster network program

import kit
from kit import kit
from datetime import date
import mclusters
import nclusters

# *****************************************************************************************************************
#       MAIN
# *****************************************************************************************************************
if __name__ == '__main__':
    print('Hello, this looks to work, but it is not ready yet.')

    kits = []                                           # This is list of kits. First empty.
    kits_to_list = kit.read_kits()                      # Read information of kits from kits.csv.

    for k in kits_to_list:
        uusi_kit = kit(k[0],k[1])                       # Create kit which have information and clustered matches.
        kits.append(uusi_kit)                           # Add to list.

    netclusters = nclusters.nclusters()
    for k in kits:                                      # Add every kits every GD clusters to netclusters
        for i in range(0,4):
            if(k.mclu.gd[i] != None):
                netclusters.add(k.mclu.get_cluster(i))

    while True:                                         # Do while duplicate clusters
        todelete = netclusters.find_duplicates()
        if todelete == None:
            break
        netclusters.remove(todelete)

    while True:                                         # Do while nodes which should be splitted
        node =  netclusters.to_be_splitted()
        if node == None:
            break
        netclusters.split(node)

    exit(0)

    # Now network of GD clusters is ready to display!