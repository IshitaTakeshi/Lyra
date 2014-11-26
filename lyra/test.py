import sys
import os
import json

from ml.extractor import Extractor
from ml.search  import search_k_nearest
from ml.featuresio import dump_json, load_json
from ml import MLInterface

jsonpath = os.path.join('jsonfiles', 'test.json')


def test_extraction(music_root):
    print("Test Extractor")
    print("extracting from {}".format(music_root))

    extractor = Extractor(n_frames=40, n_blocks=100, learning_rate=0.00053,
                          verbose=True)
    path_feature_map, error = extractor.extract(music_root)

    print("Error:{}".format(error))
    dump_json(path_feature_map, jsonpath)
    print("Saved as {}".format(jsonpath))
    print("\n")


def test_similarity(query):
    print("Test search_k_nearest")
    path_feature_map = load_json(jsonpath)
    n_results = len(path_feature_map)
    k_nearest = search_k_nearest(path_feature_map, query, n_results)
    for filepath, distance in k_nearest:
        print("{}\n{:>3e}\n".format(filepath, distance))
    print("\n")
    return k_nearest


def test_interface(music_root, query):
    print("Test MLInterface")
    ml = MLInterface()
    ml.set_music_root(music_root)
    ml.extract_features()
    ml.save(jsonpath)
    ml.load(jsonpath)
    k_nearest = ml.search(query)
    for filepath, distance in k_nearest:
        print("{}\n{:>3e}\n".format(filepath, distance))
    print("\n")
    return ml

    
if(__name__ == '__main__'):
    if(len(sys.argv) < 3):
        print("How to test")
        print("\t$python3 test.py <music root> <path to query>")
        exit(-1)

    music_root = sys.argv[1]
    query = sys.argv[2]
    #test_extraction(music_root)
    #test_similarity(query)
    test_interface(music_root, query)
