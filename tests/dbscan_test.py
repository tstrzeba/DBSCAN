import sys
sys.path.append("../db_scan")
from point import Point
from dbscan import DBscan


class DBscanUnitTest(object):
    """
        DBscanUnitTest class provides unit test method for DBscan class
    """

    test_array = [[0, 100],  [0, 200],  [0, 275],  [100, 150],  [200, 100],  [250, 200],  [0, 300],[675, 700],  [675, 710],  [675, 720]]
    proper_cluster = [-1, 1, 1, -1, -1, -1, 1, 2, 2, 2]
    dbscan = 0

    def __init__(self):
        self.dbscan = DBscan()

    # start_test function start unit test for DBscan class. Return False if failed elsewhere return True
    def start_test(self):

        point_array = []
        for p in self.test_array:
            pt = Point(p[0], p[1])
            point_array.append(pt)

        self.dbscan.start(point_array, 100, 3)

        i = 0
        for p in point_array:
            if p.get_clusterID() is not self.proper_cluster[i]:
                print("Clustering algorithm failed")
                return False
            i += 1

        return True

db = DBscanUnitTest()
print(db.start_test())
