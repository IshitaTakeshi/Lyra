import sys
import os
import json

from extractor import Extractor
from path import get_wave_paths
from featuresio import dump_json


def test_extraction(music_root):
    filename = os.path.basename(music_root)
    jsonpath = './jsonfiles/{}.json'.format(filename)

    print("extracting from {}".format(music_root))

    extractor = Extractor(n_frames=40, n_blocks=100, learning_rate=0.00050,
                          verbose=True)
    path_feature_map, error = extractor.extract(music_root)

    print("Error:{}".format(error))
    print("Saving as {}".format(jsonpath))
    dump_json(path_feature_map, jsonpath)


for music_root in sys.argv[1:]:
    test_extraction(music_root)
