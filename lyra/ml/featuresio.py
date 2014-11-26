import json

from .utils import to_ndarray, to_list


def load_json(filepath):
    path_feature_map = json.load(open(filepath, 'r'))
    path_feature_map = to_ndarray(path_feature_map)
    return path_feature_map


def dump_json(path_feature_map, filepath):
    path_feature_map = to_list(path_feature_map)
    json.dump(path_feature_map, open(filepath, 'w'))
