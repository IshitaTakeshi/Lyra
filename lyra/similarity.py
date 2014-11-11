# -*- coding: utf-8 -*-
import numpy as np
from numpy.linalg import norm


def search_k_nearest(vectors, query, k=None):
    if(k is None):
        k = len(vectors)

    distances = []
    for filepath, vector in vectors.items():
        distance = norm(vector-query, ord=-1)
        distances.append((filepath, distance))
    #sort by distance
    distances = sorted(distances, key=lambda x: x[1])
    return distances[:k]


if(__name__ == '__main__'):
    import json
    import os
    import utils

    dicts = []
    dicts.append(json.load(open('./jsonfiles/supercell.json', 'r')))
    dicts.append(json.load(open('./jsonfiles/Haruhi.json', 'r')))
    dicts.append(json.load(open('./jsonfiles/Reading.json', 'r')))
    vectors = utils.merge_multiple_dicts(dicts)

    for key, vector in vectors.items():
        vectors[key] = np.array(vector)
    
    keys = list(vectors.keys())
    i = np.random.randint(0, len(keys))
    key = keys[i]
    key = '../dataset/Music/supercell/02 ハートブレイカー.wav'
    print("key:{}".format(key))
    query = vectors[key]
    k_nearest = search_k_nearest(vectors, query)
    for filepath, distance in k_nearest:
        print("{}\n{:>3e}\n".format(os.path.basename(filepath), distance))
