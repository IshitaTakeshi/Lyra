import sys
import os
import json

from lyra.ml.extractor import Extractor
from lyra.ml.search  import search_k_nearest
from lyra.ml.featuresio import dump_json, load_json
from lyra.ml import MLInterface

jsonpath = os.path.join('jsonfiles', 'test.json')
config_path = './lyra/config'


def test_extraction(music_root):
    print("Test Extractor")
    print("extracting from {}".format(music_root))

    extractor = Extractor(config_path=config_path, verbose=True)
    path_feature_map = extractor.extract(music_root)

    dump_json(path_feature_map, jsonpath)
    print("Saved as {}\n".format(jsonpath))


def test_similarity(query):
    print("Test search_k_nearest")
    path_feature_map = load_json(jsonpath)
    n_results = len(path_feature_map)
    k_nearest = search_k_nearest(path_feature_map, query, n_results)
    for filepath, distance in k_nearest:
        print("{}\n{:>3e}\n".format(filepath, distance))
    print("\n")
    return k_nearest


def test_interface(music_root, query, config_path=config_path):
    print("Test MLInterface")
    ml = MLInterface(config_path)
    ml.set_music_root(music_root)
    ml.extract_features()
    ml.save(jsonpath)
    ml.load(jsonpath)
    ml.set_query(query)
    k_nearest = ml.search(n_results=10)
    for filepath, similarity in k_nearest:
        print("{}\n{:>3e}\n".format(filepath, similarity))
    print("\n")
    return k_nearest


if(__name__ == '__main__'):
    if(len(sys.argv) < 3):
        print("How to test")
        print("\t$python3 test.py <music root> <path to query>")
        exit(-1)

    music_root = sys.argv[1]
    query = sys.argv[2]
    k_nearest = test_interface(music_root, query)
    from subprocess import call
    import os

    for filepath, similarity in k_nearest:
        print("title: {}  similarity: {}".format(
              os.path.basename(filepath), similarity))
    for filepath, similarity in k_nearest[:3]:
        call('mplayer {}'.format(filepath).split(' '))

    test_similarity(query)
    test_extraction(music_root)
