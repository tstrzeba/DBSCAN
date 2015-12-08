import numpy as np
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
from random import randint
from random import uniform


class RandomDataGenerator(object):
    """
        Generates random data for dbscan
    """

    def __init__(self, number_of_samples, number_of_centers, range):
        self.centers = [[0, 0]]
        self.cluster_std = 0
        self.random_state = 0
        self.n_samples = number_of_samples
        self.number_of_centers = number_of_centers
        self.range = range

    def generate_data(self):
        self.centers.clear()
        for _ in range(0, self.number_of_centers):
            self.centers.append([randint(-int(self.range), self.range), randint(-int(self.range), self.range)])

        self.cluster_std = uniform(0.3, 0.4)

        X, labels = make_blobs(n_samples=self.n_samples, centers=self.centers, cluster_std=self.cluster_std,
                       random_state=self.random_state)

        X = StandardScaler().fit_transform(X)
        return X, labels