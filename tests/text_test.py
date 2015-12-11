#################################################################################
# generate data settings
#################################################################################
CENTERS = [[-1, -1], [1, -1], [5, 5]]
N_SAMPLES = 100
CLUSTER_STD = 0.7
RANDOM_STATE = 0

#################################################################################
# db_scan settings
#################################################################################
EPS = 15
MIN_SAMPLES = 3

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
# X, labels_true = make_blobs(n_samples=N_SAMPLES, centers=CENTERS, cluster_std=CLUSTER_STD,
#                             random_state=RANDOM_STATE)

import sys

sys.path.append("../db_scan")
from text2vector import getTextData

# test_data, X = getTextData()
#
# print( "\nRaw blobs: " , X[:5] )
# X = StandardScaler().fit_transform(X)
# test_data = StandardScaler().fit_transform(test_data)
# print( "\nAfter standarization:", X[:5])
# #################################################################################
# # Compute DBSCAN
# #################################################################################
# db = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES).fit(X)
# core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
# core_samples_mask[db.core_sample_indices_] = True
# labels = db.labels_
#
# # Number of clusters in labels, ignoring noise if present.
# n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
#
# # print('Estimated number of clusters: %d' % n_clusters_)
# # print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
# # print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
# # print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
# # print("Adjusted Rand Index: %0.3f"
# #       % metrics.adjusted_rand_score(labels_true, labels))
# # print("Adjusted Mutual Information: %0.3f"
# #       % metrics.adjusted_mutual_info_score(labels_true, labels))
# # print("Silhouette Coefficient: %0.3f"
# #       % metrics.silhouette_score(X, labels))
#
# #################################################################################
# # Plot result
# #################################################################################
# import matplotlib.pyplot as plt
#
# # Black removed and is used for noise instead.
# unique_labels = set(labels)
# colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
# plt.subplot(211)
# for k, col in zip(unique_labels, colors):
#     if k == -1:
#         # Black used for noise.
#         col = 'k'
#
#     class_member_mask = (labels == k)
#
#     xy = X[class_member_mask & core_samples_mask]
#     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
#              markeredgecolor='k', markersize=10)
#
#     xy = X[class_member_mask & ~core_samples_mask]
#     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
#              markeredgecolor='k', markersize=10)
#
#
# #plt.plot( [x[0] for x in test_data], [x[1] for x in test_data], 'go')
#
# plt.title('Sklearn - estimated number of clusters: %d' % n_clusters_)
# plt.grid()

# #################################################################################
# # our version
# #################################################################################
import sys

sys.path.append("../db_scan")
from dbscan import DBscan
from point import Point
from text2vector import getTextData
import matplotlib.pyplot as plt
#################################################################################
# Compute DBSCAN
#################################################################################
##xx = X.tolist()
##print( "\nxx= \n", xx)
xx, test_tab = getTextData()
#xx = StandardScaler().fit_transform(xxx).tolist()
#print( xx )
point_array = []

for x in xx:
    pt = Point(x[0], x[1])
    point_array.append(pt)
# db = DBscan(point_array=parr, start_point_index= 0, cluster_map=clustmap, epsilon=EPS, min_neighbour=MIN_SAMPLES)
db = DBscan()
clusters = db.start(points=point_array, eps=EPS, minPts=MIN_SAMPLES)

#################################################################################
# Plot result
#################################################################################
plt.subplot(212)
colors = plt.cm.Spectral(np.linspace(0, 1, len(clusters)))

for p in point_array:
    if p.get_clusterID() == Point.NOISE:
        col = 'k'
    elif p.get_clusterID == Point.UNCLASSIFIED:
        col = 'g'
    else:
        col = colors[p.get_clusterID() - 1]

    plt.plot(p.get_x(), p.get_y(), 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=10)

plt.title('Our algorithm - estimated number of clusters: %d' % len(clusters))
plt.grid()

plt.plot( [x[0] for x in test_tab], [x[1] for x in test_tab], 'go', markersize=10)
plt.show()
