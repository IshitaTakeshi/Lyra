import numpy as np


def merge_multiple_dicts(dicts):
    items = []
    for d in dicts:
        items += list(d.items())
    dicts = dict(items)
    return dicts


def to_list(path_feature_map):
    for path, vector in path_feature_map.items():
        path_feature_map[path] = vector.tolist()
    return path_feature_map


def to_ndarray(path_feature_map):
    for path, vector in path_feature_map.items():
        path_feature_map[path] = np.array(vector)
    return path_feature_map
