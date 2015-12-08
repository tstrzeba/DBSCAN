import math

from point import Point
import test_array


class DBscan(object):
    """
        DBscan class for point clustering algorithm
    """

    # DBscan class object constructor
    def __init__(self):
        print("DBscan instance has been created successfully :-)")

    # get_region function find point pairs with max distance between in radius of eps.
    def get_region(self, points, pt, eps):
        region = []

        for i in range(len(points)):
            distSquared = Point.distance_squared(pt, points[i])
            if distSquared < eps:
                region.append(points[i])
        return region

    # expand_cluster function add point which fulfill requirements in proper cluster. Returns TRUE if done, FALSE if point does not fulfill required distance radius.
    def expand_cluster(self, points, pt, clusterID, eps, minPts):
        seeds = self.get_region(points, pt, eps)

        if (len(seeds)) < minPts:
            pt.set_clusterID(Point.NOISE)
            return False

        else:
            for i in range(len(seeds)):
                seeds[i].set_clusterID(clusterID)
            seeds.remove(pt)

            while (len(seeds)) > 0:
                currentP = seeds[0]
                result = self.get_region(points, currentP, eps)
                if (len(result)) >= minPts:
                    for i in range(len(result)):
                        resultP = result[i]
                        if resultP.get_clusterID() == Point.UNCLASSIFIED or resultP.get_clusterID() == Point.NOISE:
                            if resultP.get_clusterID() == Point.UNCLASSIFIED:
                                seeds.append(resultP)
                            resultP.set_clusterID(clusterID)
                seeds.remove(currentP)
            return True

    # get_cluster function return list of available clusters.
    def get_cluster(self, points, eps, minPts):
        if points is None:
            return None

        clusters = list()
        eps = eps**2
        clusterID = 1

        for i in range(len(points)):
            p = points[i]
            if p.get_clusterID() == Point.UNCLASSIFIED:
                if self.expand_cluster(points, p, clusterID, eps, minPts):
                    clusterID += 1

        # sort to find out max ClusterId value
        temp_pt_lst = sorted(points, key=lambda x: x.ClusterId)

        # maxClusterId = temp_pt_lst[-1].get_clusterID()
        # if maxClusterId<1:
        #     return clusters
        # for i in range(maxClusterId):
        #     clusters.append([None])

        for p in points:
            if p.get_clusterID() > 0:
                if len(clusters) < p.get_clusterID():
                    clusters.append([p])
                else:
                    clusters[p.get_clusterID()-1].append(p)
        return clusters

    # start function starts work of DBscan algorithm.
    def start(self, points, eps, minPts):
        points = sorted(points, key=lambda x: x.get_x())
        clusters = self.get_cluster(points, eps, minPts)
        return clusters



