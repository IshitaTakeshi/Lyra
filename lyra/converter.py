from subprocess import call
import os
import time
from multiprocessing import Pool, cpu_count
import itertools

import numpy as np

from progressbar import ProgressBar
from features import extract_features
import utils


def get_wave_paths(music_root):
    paths = []
    for dirpath, dirname, filenames in os.walk(music_root):
        for filename in filenames:
            if not(filename.endswith('.wav')):
                continue
            filepath = os.path.join(dirpath, filename)
            paths.append(filepath)
    return paths


def extract_(args):
    def process(paths, n_frames, n_blocks):
        vectors = {}
        for i, filepath in enumerate(paths):
            feature_vector = extract_features(filepath, 
                                              n_frames=n_frames, 
                                              n_blocks=n_blocks)
            vectors[filepath] = feature_vector
        return vectors
    return process(*args)


def extract(music_root, n_frames, n_blocks):
    paths = get_wave_paths(music_root)
    paths = paths[:40]

    n_cores = cpu_count()    
    paths_ = np.array_split(paths, n_cores)
    paths_ = [paths.tolist() for paths in paths_]
    
    args = []
    for paths in paths_:
        args.append([paths, n_frames, n_blocks])
     
    pool = Pool()
    vectors = pool.map(extract_, args)
    
    vectors = utils.merge_multiple_dicts(vectors)
    return vectors


categories = [
    'KiminoShiranaiMonogatari', 'ReMIKUS', 'ElectricLoveCollection', 
    'Haruhi', 'Reading'
] 

for category in categories:
    wavpath = '../dataset/Music/{}'.format(category)
    jsonpath = './jsonfiles/{}.json'.format(category)

    vectors = extract(wavpath, n_frames=40, n_blocks=400)

    for key, vector in vectors.items():
        vectors[key] = vector.tolist()

    import json
    json.dump(vectors, open(jsonpath, 'w'))
