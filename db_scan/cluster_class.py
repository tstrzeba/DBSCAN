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
    __iterator = 0

    def __init__(self):
        if self.__map_list:
            print("Exist")

    def __len__(self):
        return len(self.__map_list)

    def __iter__(self):
        return self #self.__map_list

    def __next__(self):
        if self.__iterator > len(self.__map_list)-1:
            self.__iterator = 0
            raise StopIteration
        else:
            self.__iterator += 1
            return self.__map_list[self.__iterator-1]


    def add_map(self, cn1, cn2):
        self.__map_list.append([cn1, cn2])

    def rename_map(self, index, cn1, cn2):
        self.__map_list.pop(index)
        self.__map_list.insert(index,[cn1,cn2])

    def __compare__(self, x, y):
        if x is None or y is None:
            return False

        if self.__map_list[x][0] == self.__map_list[y][0] and self.__map_list[x][1] == self.__map_list[y][1]:
            return True
        elif self.__map_list[x][0] == self.__map_list[y][1] and self.__map_list[x][1] == self.__map_list[y][0]:
            return True
        else:
            return False

    def reduce_cluster(self):
        reduce_count = 0
        index1 = 0
        index2 = 1
        print("LEN IS:"+str(len(self.__map_list)))
        while True:
            if index1 == len(self.__map_list)-1:
                break

            while True:
                if index2 == len(self.__map_list)-1:
                    break

                #print("I1 %d, I2 %d" % (index1, index2))
                if self.__compare__(index1, index2):
                    self.__map_list.pop(index2)
                    reduce_count += 1

                index2 += 1
            index1 += 1
            index2 = index1+1

        return reduce_count

    def remove_cluster(self, cname):
        index = 0

        for map in self.__map_list:
            if map[0] == "NOISE" and map[1] == cname:
                self.__map_list.pop(index)
                return True
            elif map[1] == "NOISE" and map[0] == cname:
                self.__map_list.pop(index)
                return True
            index += 1
        return False

    def remove_noise_cluster(self):
        index = 0

        for map in self.__map_list:
            if map[0] == "NOISE" or map[1] == "NOISE":
                self.__map_list.pop(index)
            index += 1
        return True

    def remove_map(self, cname1, cname2):
        index = 0

        for map in self.__map_list:
            if map[0] == cname1 and map[1][0] == cname2:
                self.__map_list.pop(index)
                self.__map_list.insert(index, [None, None])
                return True
            index += 1
        return False

    def get_noise_cluster(self):
        for map in self.__map_list:
            if map[0] == "NOISE":
                return map[1]
            elif map[1][0] == "NOISE":
                return map[0]
        return False

    def pop(self, index):
        self.__map_list.pop(index)

    def print_map(self):
        print(self.__map_list)

    def get_map(self):
        return self.__map_list



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

