class Cluster(object):

    __cluster_name = None
    __is_mapped = False

    def __init__(self, cname):
        self.__cluster_name = cname

    def get_name(self):
        return self.__cluster_name

    def set_map(self):
        self.__is_mapped = True

    def is_mapped(self):
        return self.__is_mapped


class ClusterMap(object):

    __map_list = []

    def __init__(self):
        if self.__map_list:
            print("Exist")

    def add_map(self,cn1, cn2):
        self.__map_list.append([cn1, cn2])

    def __compare__(self, x, y):
        if self.__map_list[x][0] == self.__map_list[y][0] and self.__map_list[x][1] == self.__map_list[y][1]:
            return True
        elif self.__map_list[x][0] == self.__map_list[y][1] and self.__map_list[x][1] == self.__map_list[y][0]:
            return True
        else:
            return False

    def reduce_cluster(self):
        reduce_count = 0
        for index1 in range(0, len(self.__map_list)-1):
            for index2 in range(index1+1, len(self.__map_list)-1):
                if self.__compare__(index1, index2):
                    self.__map_list.pop(index2)
                    reduce_count += 1
        return reduce_count

    def print_map(self):
        print(self.__map_list)



# cm = ClusterMap()
# clus1 = Cluster("abc")
# clus2 = Cluster("xyz")
#
# clus3 = Cluster("xyz")
# clus4 = Cluster("abc")
#
# clus5 = Cluster("abc")
# clus6 = Cluster("sdf")
#
# clus7 = Cluster("rw")
# clus8 = Cluster("xyz")
#
# clus9 = Cluster("xyz")
# clus10 = Cluster("abc")
#
# cm.add_map(clus1.get_name(), clus2.get_name())
# cm.add_map(clus3.get_name(), clus4.get_name())
# cm.add_map(clus5.get_name(), clus6.get_name())
# cm.add_map(clus7.get_name(), clus8.get_name())
#
# cm.add_map(clus9.get_name(), clus10.get_name())
#
# cm.print_map()
#
# print("Reduced row count: %d" % cm.reduce_cluster())
# print("Reduced row count: %d" % cm.reduce_cluster())
# cm.print_map()

