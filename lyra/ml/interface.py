import os


from .extractor import Extractor
from .search import search_k_nearest
from .featuresio import dump_json, load_json


class MLInterface(object):
    def __init__(self, n_frames=40, n_blocks=100, learning_rate=0.00053):
        self.extractor = Extractor(n_frames, n_blocks, learning_rate, 
                                   verbose=True)
        self.music_root = os.getcwd() 
        self.query_filepath = None
        self.path_feature_map = {}
   
    def set_music_root(self, music_root):
        print("The music root is set: {}".format(music_root))
        self.music_root = music_root
        
    def extract_features(self):
        if(self.music_root is None):
            print("Set the music root first.")
            return

        path_feature_map, error = self.extractor.extract(self.music_root)
        self.path_feature_map = path_feature_map
        return self

    def save(self, filepath):
        dump_json(self.path_feature_map, filepath)

    def load(self, filepath):        
        if not(os.path.exists(filepath)):
            raise IOError("{} does not exist.".format(filename))

        self.path_feature_map = load_json(filepath)
    
    def set_query(self, query_filepath):
        self.query_filepath = query_filepath

    def search(self, n_results=None):
        """
        self.query_filepath: path to query
        k: number of results
        """
        if(self.query_filepath is None):
            print("Set a query first.")
            return

        if(n_results is None):
            n_results = len(self.path_feature_map)

        k_nearest = search_k_nearest(self.path_feature_map, self.query_filepath, 
                                     n_results)
        return k_nearest
