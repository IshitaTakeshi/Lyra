import glob
import json
import sys
import os

import numpy as np

import utils
from similarity import search_k_nearest
from mds import calculate_positions
from plot import plot_with_labels


dicts = []
for path in glob.glob('./jsonfiles/*.json'):
    dicts.append(json.load(open(path, 'r')))
path_feature_map = utils.merge_multiple_dicts(dicts)
path_feature_map = utils.to_ndarray(path_feature_map)

#TODO Show error messages
key = sys.argv[1]
keys = path_feature_map.keys()
print(keys)
query = path_feature_map[key]
k_nearest = search_k_nearest(path_feature_map, query)
for filepath, distance in k_nearest:
    print("{}\n{:>3e}\n".format(filepath.encode('utf-8'), distance))
