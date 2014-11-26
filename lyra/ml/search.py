# -*- coding: utf-8 -*-
import os 

import numpy as np

from .distance import calc_distance


def search_k_nearest(path_feature_map, query_filepath, k=None):
    """
    Returns filepaths and similarities in similarity order
    Returns tuple (filepath, distance)
    """

    query_filepath = os.path.abspath(query_filepath)

    if not(query_filepath in path_feature_map.keys()):
        raise ValueError(
            "{} is not in the extracted music list".format(query_filepath))

    query_vector = path_feature_map[query_filepath]

    distances = []
    for filepath, vector in path_feature_map.items():
        distance = calc_distance(vector, query_vector)
        distances.append((filepath, distance))
    #sort by distance
    distances = sorted(distances, key=lambda x: x[1])
    return distances[:k]
