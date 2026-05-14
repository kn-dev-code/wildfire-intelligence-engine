from sklearn.cluster import DBSCAN
import numpy as np


data = np.array([[34.05, -118.24], [34.06, -118.25], [40.71, -74.00]])
clustering = DBSCAN(eps=0.1, min_samples=2).fit(data)

print(f"Clusters found: {clustering.labels_}")