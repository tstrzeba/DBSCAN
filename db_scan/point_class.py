class Point(object):
# float number coordinate
    __coordinate = []
    __in_cluster = False
    __cluster_name = None
    __is_edge = False

    def __init__(self, *cor):
        self.__coordinate = cor

    def set_coordinate(self, *arg):
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
            if self.__in_cluster:
                print("Previous cluster: %s, currently set: %s" % (self.__cluster_name, cname))
            else:
                raise Exception('Incorrect class name. Name should be a string variable')
            
            self.__cluster_name = cname
            self.__in_cluster = True
            return True

    def set_edge(self):
        self.__is_edge = True

    def is_edge(self):
        return self.__is_edge
            


