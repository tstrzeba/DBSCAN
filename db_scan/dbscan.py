import math
from cluster_class import Cluster
from cluster_class import ClusterMap
from point_class import PointArray
from point_class import Point

CLUSTER_INDEX = 0

class DBscan(object):

    __start_point_index = 0
    __cluster_map = None
    __point_array = None
    __current_index = 0
    __epsilon = 0
    __start_point = None
    __min_neighbour_count = 1

    def __init__(self, point_array, start_point_index, cluster_map, epsilon, min_neighbour):
        self.__start_point = start_point_index
        self.__cluster_map = cluster_map
        self.__point_array = point_array
        self.__epsilon = epsilon
        self.__start_point = point_array.get_point(start_point_index)
        self.__min_neighbour_count = min_neighbour

    #def get_next_point(self):

    #in new iteration find firs free point which has no cluster

    def calculate_dist(self, pt1, pt2):
        return math.sqrt((pt2.get_x()-pt1.get_x())**2 + (pt2.get_y() - pt1.get_y())**2)

    def start(self, cind):
        cluster_name = None
        cluster_index = cind
        nxtpt = self.__point_array.get_next_point(self.__start_point)

        while nxtpt:
            i = 0
            while nxtpt:
                if self.calculate_dist(self.__start_point, nxtpt) <= self.__epsilon: #and self.__start_point.is_in_cluster() == False:

                    if not self.__start_point.is_in_cluster():
                        c = Cluster(str(cluster_index))
                        cluster_index += 1
                        cluster_name = c.get_name()
                        self.__start_point.set_cluster(cluster_name)

                    if nxtpt.is_in_cluster() and cluster_name != nxtpt.get_cluster():
                        self.__cluster_map.add_map(cluster_name, nxtpt.get_cluster())
                    else:
                        nxtpt.set_cluster(cluster_name)

                    i += 1
                    #nxtpt.show_point()

                nxtpt = self.__point_array.get_next_point(nxtpt)

                #print(i)
            if i < (self.__min_neighbour_count-1):
                self.__cluster_map.add_map(cluster_name, ["NOISE", i])

            nxtpt = self.__point_array.find_unclustered_point(self.__start_point)
            if nxtpt is not False:
                self.__start_point = nxtpt;
                #nxtpt.show_point()

        return cluster_index

    def merge_clusters(self):
        self.__cluster_map.reduce_cluster()
        print(self.__cluster_map.print_map())
        pop_index = 0;
        for map in self.__cluster_map:
            pop_index += 1
            new_name = map[0]
            old_name = map[1]

            if old_name == "NOISE":
                #self.__cluster_map.remove_cluster(old_name)
                continue
            #print("NN: %s, OO: %s" % (new_name, old_name))

            for p in self.__point_array:
                if p.get_cluster() == old_name:
                    print("OLD:"+p.get_cluster())
                    p.set_cluster(new_name)
                    print("NEW:"+p.get_cluster())

            self.__cluster_map.remove_map(new_name, old_name)
            #self.__cluster_map.pop(pop_index-1)
            self.__cluster_map.remove_cluster(new_name) #dwie poniższe liniki są istotne (nimi manipulować) !!!
        #self.reduce_clusters()




    def reduce_clusters(self):
        cname = self.__cluster_map.get_noise_cluster()
        while cname:
            self.__point_array.remove_points_from_cluster(cname)
            self.__cluster_map.remove_cluster(cname)
            cname = self.__cluster_map.get_noise_cluster()


import test_array

parr = PointArray(test_array.tablica)
clustmap = ClusterMap()
db = DBscan(parr, 0, clustmap, 2, 7)
CLUSTER_INDEX = db.start(CLUSTER_INDEX)
print("Cluster index is: %d" % CLUSTER_INDEX)
#db.reduce_clusters()
#db.merge_clusters()

for x in range(0, CLUSTER_INDEX):
#x=0
    print("Cluster %d contains points:" % x)
    for ii in range(len(parr)-1):
        p = parr.get_point(ii)
        if p.get_cluster() == str(x):
            p.show_point()


clustmap.print_map()
clustmap.reduce_cluster()
clustmap.print_map()
print("")

#print(db.calculate_dis(parr.get_point(0),parr.get_point(3)))





