"""
Testing program. Creates synthetic (or load real) clusters and you can test program with them.
"""
from mtsettings import HAPLOGROUP
from kit import Kit
from link import Link
from cnetwork import Nclusters

if __name__ == '__main__':
    kitlist = Kit.read_kits('kits.csv')
    kits = []
    n = Nclusters()                                             # Network of match clusters

    for k in kitlist:
        new_kit = Kit(k[0], k[1], k[2], HAPLOGROUP)
        kits.append(new_kit)

#    for k in kits:                                             # You can print three level of kit's data
#        k.show(True)                                           # show(), show(True), show(True, True)

    for k in kits:
        n.add_kit(k)                                            # Add clusters of kits to network

#    n.show(True, True)                                         # You can print whole network like kits
                                                                # show(), show(True), show(True, True)

    n.prepare_clusters()                                        # Fill bogus match and add links kit clusters 0 - 3

    """
    Now network of clusters has match clusters from every kit and every GD. And there are double linked gd's
    between clusters. So next we can
    - search same matches containing clusters and mark them same cluster.
    - split clusters. How about first collect all same matches containing clusters to collection and then split?
    - delete duplicate clusters. Is this wise to do when we have links between clusters depending on kits?

    Yes. It's again time to think.
    """

    """
    Search match from whole network and collect cluster containing that match to a collection.
    Then filter non common matches away and split them own clusters. Then you have a common cluster.
    Prepare links to pointing to it. This is maybe a complicated process.
    """

    search_m = n.nclusters[0].matches[0]
    # print(search_m.Fullname)
    integrated = n.search_matches_from_clusters(search_m.Fullname)
    print(integrated)
    for axis in integrated:
        print('axis=', axis)
        for mii in n.nclusters[axis].matches:
            mii.show()

    exit(0)

#    dint = 0
#    while n.delete_duplicates():              # First delete duplicates
#        dint += 1
#    if dint:
#        print('Removed', dint, 'duplicate clusters.')


    #    gui = Gui_mdka()

    # How you can send email easily to every in this haplogroup network
    # email_str = n.mk_email_list()
    # print(email_str)


#    n.write('HAPLOGROUP_duplicated.json')


    print('Network has', len(n.nclusters), 'unduplicated clusters.')
    n.write('U8a1a1b1_unduplicated.json')
    n.show()
