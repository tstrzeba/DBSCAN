class Point(object):
    """
        Class representing 2D coordinate as one Point object
    """

    # static field describing point cluster type
    NOISE = -1
    UNCLASSIFIED = 0
    ClusterId = 0

    # static field containing point coordinate
    __x = 0
    __y = 0

    # Point object constructor
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    # return point x coordinate
    def get_x(self):
        return self.__x

    # return point y coordinate
    def get_y(self):
        return self.__y

    # calculate square distance between two points in 2D
    @staticmethod
    def distance_squared(pt1, pt2):
        return (pt2.get_x()-pt1.get_x())**2 + (pt2.get_y() - pt1.get_y())**2

    # set value for static field ClusterId
    def set_clusterID(self, ids):
        self.ClusterId = ids
        return True

    # get value of static field ClusterId
    def get_clusterID(self):
        return self.ClusterId

    # return point coordinate
    def show(self):
        return [self.__x, self.__y]
