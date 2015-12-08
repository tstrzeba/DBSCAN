import sys
import timeit
from random import randint
from random import uniform
# sklearn
from sklearn.cluster import DBSCAN

# our version
sys.path.append("../db_scan")
sys.path.append("../tests")
from dbscan import DBscan
from point import Point
from random_data_generator import RandomDataGenerator


class ScikitTest(object):
    """
        Compares times of computing our algorithm and scikit algorithm
    """
    def __init__(self):
        self.scikit_average = list()
        self.our_average = list()
        self.db = DBscan()

    def start_test(self):

        db = DBscan()
        table = [100, 1000, 3000, 5000, 10000]
        for i in range(0, len(table)):
            number_of_centers = randint(2, 5)
            range1 = randint(1, 10)
            scikit_average = 0.0
            our_average = 0.0
            random_generator = RandomDataGenerator(number_of_samples=table[i],
                                                   number_of_centers=number_of_centers, range=range1)

            for _ in range(0, 3):
                EPS = uniform(0.09, range1/10)
                MIN_SAMPLES = randint(5, 10)

                #################################################################################
                # Generate sample data
                #################################################################################
                X, labels = random_generator.generate_data()

                xx = X.tolist()
                point_array = []
                for x in xx:
                    pt = Point(x[0], x[1])
                    point_array.append(pt)

                #################################################################################
                # sklearn
                #################################################################################

                start = timeit.default_timer()
                DBSCAN(eps=EPS, min_samples=MIN_SAMPLES).fit(X)
                end = timeit.default_timer()
                scikit_average += end - start

                start =timeit.default_timer()
                clusters = db.start(points=point_array, eps=EPS, minPts=MIN_SAMPLES)
                end = timeit.default_timer()
                our_average += end - start


            print("Number of samples: %d" % table[i])
            print("Scikit average time of computing = %0.5f" % (scikit_average / 3))
            print("Our version average time of computing = %0.5f" % (our_average / 3))
            print("Our algorithm is %0.2f slower than algorithm from scikit" % (our_average/scikit_average))

        return True


ScikitTest().start_test()