import json
import os
import glob

import numpy as np

import utils
from extractor import extract
from mds import calculate_positions
from plot import plot_with_labels


def to_ndarray(path_feature_map):
    for path, vector in path_feature_map.items():
        path_feature_map[path] = np.array(vector)
    return path_feature_map


def to_list(path_feature_map):
    for path, vector in path_feature_map.items():
        path_feature_map[path] = vector.tolist()
    return path_feature_map


categories = [
    'KiminoShiranaiMonogatari', 'ReMIKUS', 'Haruhi', 'Reading', 'supercell'
] 

for category in categories:
    wavpath = '../dataset/Music/{}'.format(category)
    jsonpath = './jsonfiles/{}.json'.format(category)

    path_feature_map = extract(wavpath, n_frames=40, n_blocks=10)    
    path_feature_map = to_list(path_feature_map)

    json.dump(path_feature_map, open(jsonpath, 'w'))


dicts = []
for path in glob.glob('./jsonfiles/*.json'):  
    dicts.append(json.load(open(path, 'r')))
path_feature_map = utils.merge_multiple_dicts(dicts)
path_feature_map = to_ndarray(path_feature_map) 

features = []
filenames = []
for path, feature in path_feature_map.items():
    feature = feature * 10e7
    features.append(feature)
    filename = os.path.basename(path)
    filenames.append(filename)
features = np.array(features)

positions = calculate_positions(features)
plot_with_labels(positions, filenames)

#keys = list(path_feature_map.keys())
#i = np.random.randint(0, len(keys))
#key = keys[i]
#key = '../dataset/Music/supercell/02 ハートブレイカー.wav'
#print("key:{}".format(key))
#query = path_feature_map[key]
#k_nearest = search_k_nearest(path_feature_map, query)
#for filepath, distance in k_nearest:
#    print("{}\n{:>3e}\n".format(os.path.basename(filepath), distance))
