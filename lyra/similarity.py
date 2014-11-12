# -*- coding: utf-8 -*-
import numpy as np

from scale import calc_distance
from plot import plot_with_labels


def search_k_nearest(path_feature_map, query, k=None):
    if(k is None):
        k = len(path_feature_map)

    distances = []
    for filepath, vector in path_feature_map.items():
        distance = calc_distance(vector, query)
        distances.append((filepath, distance))
    #sort by distance
    distances = sorted(distances, key=lambda x: x[1])
    return distances[:k]
