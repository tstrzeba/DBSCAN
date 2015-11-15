import math
from cluster_class import Cluster
from point_class import PointArray
from point_class import Point


class DBscan(object):

    __start_point_index = 0
    __cluster_map = None
    __point_array = None
    __current_index = 0
    __epsilon = 0
    __start_point = None

    def __init__(self, point_array, start_point_index, cluster_map, epsilon):
        self.__start_point = start_point_index
        self.__cluster_map = cluster_map
        self.__point_array = point_array
        self.__epsilon = epsilon
        self.__start_point = point_array.get_point(start_point_index)

    #def get_next_point(self):

    #in new iteration find firs free point which has no cluster

    def calculate_dis(self, pt1, pt2):
        return math.sqrt((pt2.get_x()-pt1.get_x())**2 + (pt2.get_y() - pt1.get_y())**2)

    def start(self):
        cluster = Cluster("A")
        print(cluster.get_name())
        nxtpt = self.__point_array.get_next_point(self.__start_point)
        i = 0
        while nxtpt != False:
            i+=1
            if self.calculate_dis(self.__start_point, nxtpt) <= self.__epsilon: #and self.__start_point.is_in_cluster() == False:
                self.__start_point.set_cluster(cluster.get_name())
                print(nxtpt.show_point())
            nxtpt = self.__point_array.get_next_point(nxtpt)
            #print(i)

                #tutaj mozna jeszcze sprawdzac czy punkt ma dostarczajaca ilosc sasiadaow, inkrementowac jakas zmienna



import test_array

parr = PointArray(test_array.tablica)
db = DBscan(parr, 0, None, 4)
db.start()

#print(db.calculate_dis(parr.get_point(0),parr.get_point(3)))





