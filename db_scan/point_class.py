class Point(object):
# float number coordinate
    __coordinate = None
    __in_cluster = False
    __cluster_name = None
    __is_edge = False
    __point_index = 0

    def __init__(self, cor):
        self.__coordinate = cor

    def set_coordinate(self, arg):
        self.__coordinate = arg

    def show_point(self):
        print(self.__coordinate)
        
    def is_in_cluster(self):
        return self.__in_cluster
        
    def get_cluster(self):
        if self.__in_cluster:
            return self.__cluster_name
        else:
            return None
            
    def set_cluster(self, cname):
        if isinstance(cname, str):
            #if self.__in_cluster:
                #print("Previous cluster: %s, currently set: %s" % (self.__cluster_name, cname))

            self.__cluster_name = cname
            self.__in_cluster = True
            return True
        else:
                raise Exception('Incorrect class name. Name should be a string variable')

    def set_edge(self):
        self.__is_edge = True

    def is_edge(self):
        return self.__is_edge

    def set_index(self, index):
        self.__point_index = index

    def get_index(self):
        return self.__point_index

    def get_x(self):
        return self.__coordinate[0]

    def get_y(self):
        return self.__coordinate[1]


class PointArray(object):

    __point_array = []

    def __init__(self, points):
        index = 0
        for p in points:
            #print(p)
            pt = Point(p)
            pt.set_index(index)
            self.__point_array.append(pt)
            index += 1

    def show(self):
        print(self.__point_array)

    def get_point(self, index):
        return self.__point_array.__getitem__(index)

    #def __find_pint(self):

    def get_next_point(self, current_point):
        ''' TODO - add iteration over previos point in case of multicore test (in case of start first point in the middle of
            array (eg. index 10) - remember that index 9 and less are not tested
        '''
        if current_point.get_index() < len(self.__point_array)-1:
            return self.get_point(current_point.get_index()+1)
        else:
            return False





# import test_array
#
#
# pa = PointArray(test_array.tablica)
# pt = (pa.get_point(5))
# px = pa.get_next_point(pt)
# print(px.get_index())
# print("-----")
#
#


