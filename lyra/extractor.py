from subprocess import call
from multiprocessing import Pool, cpu_count

import numpy as np

from features import extract_features
import utils
from path import get_wave_paths


def extract_(args):
    def process(paths, n_frames, n_blocks):
        path_feature_map = {}
        for i, filepath in enumerate(paths):
            feature_vector = extract_features(filepath, 
                                              n_frames=n_frames, 
                                              n_blocks=n_blocks)
            path_feature_map[filepath] = feature_vector
        return path_feature_map
    return process(*args)


def extract(music_root, n_frames, n_blocks):
    paths = get_wave_paths(music_root)

    n_cores = cpu_count()    
    paths_ = np.array_split(paths, n_cores)
    paths_ = [paths.tolist() for paths in paths_]
    
    args = []
    for paths in paths_:
        args.append([paths, n_frames, n_blocks])
     
    pool = Pool()
    dicts = pool.map(extract_, args) 
    path_feature_map = utils.merge_multiple_dicts(dicts)
    return path_feature_map
