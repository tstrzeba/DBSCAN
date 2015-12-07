import sys
sys.path.append("../db_scan")
from point import Point


class PointUnitTest(object):
    """
        PointUnitTest class provides unit tests method for Point class
    """
    __x1 = 0
    __y1 = 0

    __x2 = 5
    __y2 = 8

    pointA = 0
    pointB = 0

    def __init__(self):
        self.pointA = Point(self.__x1, self.__y1)
        self.pointB = Point(self.__x2, self.__y2)

    # start_test function start unit test for Point class. Return False if test failed elsewhere return True
    def start_test(self):

        if self.__x1 is not self.pointA.get_x():
            print("Method get_x() failed")
            return False

        if self.__y1 is not self.pointA.get_y():
            print("Method get_y() failed")
            return False

        if self.pointA.set_clusterID(5) is not True:
            print("Method set_clusterID() failed")
            return False

        if self.pointA.get_clusterID() is not 5:
            print("Method get_clusterID() failed")
            return False

        if Point.distance_squared(self.pointA, self.pointB) is not 89:
            print("Method distance_squared() failed")
            return False

        return True


# p = PointUnitTest()
# print(p.start_test())

