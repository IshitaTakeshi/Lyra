import glob
import json
import sys
import os

import numpy as np

import utils
from similarity import search_k_nearest
from mds import calculate_positions
from plot import plot_with_labels


def to_ndarray(path_feature_map):
    for path, vector in path_feature_map.items():
        path_feature_map[path] = np.array(vector)
    return path_feature_map


def plot(features, magnification=10e7):
    features = []
    filenames = []
    for path, feature in path_feature_map.items():
        feature *= magnification
        features.append(feature)

        filename = os.path.basename(path)
        filenames.append(filename)

    features = np.array(features)

    positions = calculate_positions(features)
    plot_with_labels(positions, filenames)


dicts = []
for path in glob.glob('./jsonfiles/*.json'):
    dicts.append(json.load(open(path, 'r')))
path_feature_map = utils.merge_multiple_dicts(dicts)
path_feature_map = to_ndarray(path_feature_map)

key = sys.argv[1]
query = path_feature_map[key]
path_feature_map = to_ndarray(path_feature_map)
k_nearest = search_k_nearest(path_feature_map, query)
for filepath, distance in k_nearest:
    print("{}\n{:>3e}\n".format(filepath, distance))

plot(path_feature_map)
