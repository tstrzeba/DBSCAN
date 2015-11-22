#################################################################################
# generate data settings
#################################################################################
CENTERS = [[1, 1], [-1, -1], [1, -1]]
N_SAMPLES = 150
CLUSTER_STD = 0.7
RANDOM_STATE = 0

#################################################################################
# db_scan settings
#################################################################################
EPS = 0.4
MIN_SAMPLES = 10

#################################################################################
# sklearn
#################################################################################
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

#################################################################################
# Generate sample data
#################################################################################
X, labels_true = make_blobs(n_samples=N_SAMPLES, centers=CENTERS, cluster_std=CLUSTER_STD,
                            random_state=RANDOM_STATE)

X = StandardScaler().fit_transform(X)

#################################################################################
# Compute DBSCAN
#################################################################################
db = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

print('Estimated number of clusters: %d' % n_clusters_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(labels_true, labels))
print("Adjusted Mutual Information: %0.3f"
      % metrics.adjusted_mutual_info_score(labels_true, labels))
# print("Silhouette Coefficient: %0.3f"
#       % metrics.silhouette_score(X, labels))

#################################################################################
# Plot result
#################################################################################
import matplotlib.pyplot as plt

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
plt.subplot(211)
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = 'k'

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=14)

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=6)

plt.title('Sklearn - estimated number of clusters: %d' % n_clusters_)
plt.grid()


#################################################################################
# our version
#################################################################################
import sys
sys.path.append( "../db_scan" )
from cluster_class import ClusterMap
from point_class import PointArray
from dbscan import DBscan


#################################################################################
# Compute DBSCAN
#################################################################################
xx = X.tolist()
parr = PointArray(xx)
clustmap = ClusterMap()
db = DBscan(point_array=parr, start_point_index= 0, cluster_map=clustmap, epsilon=EPS, min_neighbour=MIN_SAMPLES)
temp_list = db.start(0)

#################################################################################
# Plot result
#################################################################################
plt.subplot(212)
colors = plt.cm.Spectral(np.linspace(0, 1, len(temp_list)))
for x in range(0, len(temp_list)):
    for ii in range(len(parr) - 1):
        p = parr.get_point(ii)
        if p.get_cluster() == "G" + str(x):
            col = colors[x]
            if p.is_edge() == True:
                plt.plot(p.get_x(), p.get_y(), 'o',  markerfacecolor=col,
                            markeredgecolor='k', markersize=6)
            else:
                 plt.plot(p.get_x(), p.get_y(), 'o',  markerfacecolor=col,
                            markeredgecolor='k', markersize=14)
        if p.get_cluster() == None:
            col = 'k'
            plt.plot(p.get_x(), p.get_y(), 'o',  markerfacecolor=col,
                            markeredgecolor='k', markersize=6)

plt.title('Our algorithm - estimated number of clusters: %d' % len(temp_list))
plt.grid()
plt.show()

