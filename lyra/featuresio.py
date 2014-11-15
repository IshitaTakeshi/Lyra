import json


def to_list(path_feature_map):
    for path, vector in path_feature_map.items():
        path_feature_map[path] = vector.tolist()
    return path_feature_map


def to_ndarray(path_feature_map):
    for path, vector in path_feature_map.items():
        path_feature_map[path] = np.array(vector)
    return path_feature_map


def load_json(filepath):
    path_feature_map = json.dump(open(filepath, 'w'))
    path_feature_map = to_ndarray(path_feature_map)
    return path_feature_map


def dump_json(path_feature_map, filepath):
    path_feature_map = to_list(path_feature_map)
    json.dump(path_feature_map, open(filepath, 'w'))
