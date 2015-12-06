import math
import test_array


class Point(object):
    NOISE = -1
    UNCLASSIFIED = 0
    __x = 0
    __y = 0
    ClusterId = 0

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def calculate_dist(self, pt1, pt2):
        return math.sqrt((pt2.get_x()-pt1.get_x())**2 + (pt2.get_y() - pt1.get_y())**2)

    @staticmethod
    def distance_squared(pt1, pt2):
        return (pt2.get_x()-pt1.get_x())**2 + (pt2.get_y() - pt1.get_y())**2

    def set_clusterID(self, ids):
        self.ClusterId = ids

    def get_clusterID(self):
        return self.ClusterId

    def show(self):
        return [self.__x, self.__y]


class DBscan(object):

    __point_array = []


    def __init__(self, point_array):
        self.__point_array = point_array


    def get_region(self, points, pt, eps):
        region = [] #list of point

        for i in range(len(points)-1): #sprawdzić czy czase nie iteruje od 1 do N zamiast 0 do N-1
            #print(points[i].show())
            distSquared = Point.distance_squared(pt, points[i])
            if distSquared <= eps:
                region.append(points[i])
        return region

    def expand_cluster(self, points, pt, clusterID, eps, minPts):
        seeds = self.get_region(points, pt, eps)

        if (len(seeds)-1) < minPts:
            pt.set_clusterID(Point.NOISE)
            return False

        else:
            for i in range(len(seeds)-1):
                seeds[i].set_clusterID(clusterID)
            seeds.remove(pt)

            while (len(seeds)-1) > 0:
                currentP = seeds[0]
                result = self.get_region(points, currentP, eps)
                if (len(result)-1) >= minPts:
                    for i in range(len(result)-1):
                        resultP = result[i]
                        if resultP.get_clusterID() == Point.UNCLASSIFIED or resultP.get_clusterID() == Point.NOISE:
                            if resultP.get_clusterID() == Point.UNCLASSIFIED:
                                seeds.append(resultP)
                            resultP.set_clusterID(clusterID)
                seeds.remove(currentP)
            return True


    def get_cluster(self, points, eps, minPts):
        if points is None:
            return None

        clusters = []
        eps = eps**2
        clusterID = 1

        for i in range(len(points)-1):
            p = points[i]
            if p.get_clusterID() == Point.UNCLASSIFIED:
                if self.expand_cluster(points, p, clusterID, eps, minPts):
                    clusterID += 1

        temp_pt_lst = sorted(points, key=lambda x: x.ClusterId)

        maxClusterId = temp_pt_lst[-1].get_clusterID()
        if maxClusterId<1:
            return clusters # or better null
        print("maxClusterId = "+str(maxClusterId))
        for i in range(maxClusterId):
            clusters.append([None])
            print(i)

        for p in points:
            if p.get_clusterID() > 0:
                clusters[p.get_clusterID()-1].append(p)
        return clusters

    def start(self, points, eps, minPts):
        clusters = self.get_cluster(points, eps, minPts)
        print("Number of points: "+str(len(points)))


        total = 0

        for i in range(len(clusters)-1):#-1
            count = len(clusters[i])-1
            total += count
            print("Cluster "+str(i+1) + " consists of the following " + str(count) + " points")

           # print(len(clusters))
            #print(clusters[2][1].show())
            # for p in clusters[i]:
            #     print(p.show())

        total = len(point_array)-total
        if total > 0:
            print("Following points are NOISE or UNCLASIFIED: "+str(total))
            for pp in points:
                if pp.get_clusterID() == Point.NOISE:
                    print(pp.show())
        else:
            print("There are no NOISE points")








point_array = []
for p in test_array.tablica:
    pt = Point(p[0], p[1])

    point_array.append(pt)

db = DBscan(point_array)

db.start(point_array, 4, 8)

print("-----------------------------")
for p in point_array:
    print("clusterID="+str(p.get_clusterID())+" point: " + str(p.show()))


# tab = [ [2,3], [4,5]]
# print(len(tab))

#
# parr = PointArray(test_array.tablica)
# clustmap = ClusterMap()
# db = DBscan(parr, 0, clustmap, 2, 7)
# temp_list = db.start(CLUSTER_INDEX)
# print("temp_list", temp_list)
#
#
# for x in range(0, len(temp_list)):
#     print("Cluster %d contains points:" % x)
#     for ii in range(len(parr)-1):
#         p = parr.get_point(ii)
#         if p.get_cluster() == "G"+str(x):
#             p.show_point()
#
# print("")

#print(db.calculate_dis(parr.get_point(0),parr.get_point(3)))





