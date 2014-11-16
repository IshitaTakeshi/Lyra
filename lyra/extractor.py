from subprocess import call
from multiprocessing import Pool, cpu_count
from copy import copy

import numpy as np

from features import FeatureExtractor
import utils
from path import get_wave_paths
from autoencoder import Autoencoder


n_iter = 40
n_components = 30


def compress_(path_feature_map, learning_rate):
    path_feature_map = copy(path_feature_map)

    feature_vectors = np.array(list(path_feature_map.values()))
    vector_size = feature_vectors.shape[2]
    feature_vectors = feature_vectors.reshape(-1, vector_size)

    feature_vectors /= np.sum(feature_vectors)
    #feature_vectors /= np.mean(feature_vectors)
    #feature_vectors = np.std(feature_vectors, axis=0)
    #print(np.std(feature_vectors, axis=0))
    #print(np.sum(feature_vectors, axis=0))
    #print(feature_vectors)

    autoencoder = Autoencoder(
        feature_vectors, 
        n_visible=feature_vectors.shape[1], 
        n_hidden=n_components,
        learning_rate=learning_rate
    )

    for epoch in range(n_iter):
        autoencoder.train() 

    for path, vector in path_feature_map.items():
        v = autoencoder.get_hidden_values(vector)
        path_feature_map[path] = v
    
    error = autoencoder.negative_log_likelihood()
    error = abs(error)
    return path_feature_map, error


def extraction_process_(paths, n_frames, n_blocks):
    """
    An single process of feature extraction.
    """

    extractor = FeatureExtractor(n_frames, n_blocks) 

    path_feature_map = {}
    for i, filepath in enumerate(paths):
        feature_vector = extractor.extract(filepath)
        path_feature_map[filepath] = feature_vector
    return path_feature_map


def extract_(args):
    return extraction_process_(*args)


#TODO Rename this or features.Featureextractor
class Extractor(object):
    def __init__(self, n_frames, n_blocks, learning_rate=0.1, 
                 n_cores=None, verbose=False):
        """
        All cores used if n_cores is None
        """
        self.n_frames = n_frames
        self.n_blocks = n_blocks
        
        if(n_cores is None):
            n_cores = cpu_count()

        self.n_cores = n_cores
        self.learning_rate = learning_rate
    
    def extract_(self, music_root):
        paths = get_wave_paths(music_root)

        paths_ = np.array_split(paths, self.n_cores)
        paths_ = [paths.tolist() for paths in paths_]

        args = []
        for paths in paths_:
            args.append([paths, self.n_frames, self.n_blocks])

        pool = Pool(self.n_cores)
        dicts = pool.map(extract_, args)

        path_feature_map = utils.merge_multiple_dicts(dicts)
        return path_feature_map

    def compress_(self, path_feature_map):
        path_feature_map, error = compress_(path_feature_map, 
                                            self.learning_rate)
        return path_feature_map, error

    def extract(self, music_root):
        """
        Extract features with multiprocessing
        """

        path_feature_map = self.extract_(music_root)
        path_feature_map, error = self.compress_(path_feature_map)
        return path_feature_map, error


class GridSearch(object):
    """
    Evaluates parameters 
    """
    def __init__(self, music_root, n_frames, n_blocks, 
                 n_trials=1, verbose=False):
        paths = get_wave_paths(music_root)
        extractor = Extractor(n_frames, n_blocks)
        self.path_feature_map = extractor.extract_(music_root)
        #self.path_feature_map = extraction_process_(paths, n_frames, n_blocks)
        self.n_trials = n_trials
        self.verbose = verbose

    def try_(self, learning_rate):
        total_error = 0
        for i in range(self.n_trials):
            path_feature_map, error = compress_(self.path_feature_map, 
                                                learning_rate)
            total_error += error
        return total_error

    def search(self, candidate_params):
        assert (candidate_params > 0).all()

        min_error = float('inf')
        argmin = 0
        errors = []
        for learning_rate in candidate_params:
            error = self.try_(learning_rate)
            errors.append(error)
            if(error < min_error):
                min_error = error 
                argmin = learning_rate
            
            if(self.verbose):
                print("learning rate:{:.5f}"
                      " error:{:5.3f}".format(learning_rate, error))

        return errors, argmin, min_error
