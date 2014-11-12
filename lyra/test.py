import json
import os
import utils
import glob

from extractor import extract
import mds

categories = [
    'KiminoShiranaiMonogatari', 'ReMIKUS', 'Haruhi', 'Reading', 'supercell'
] 

for category in categories:
    wavpath = '../dataset/Music/{}'.format(category)
    jsonpath = './jsonfiles/{}.json'.format(category)

    path_feature_map = extract(wavpath, n_frames=40, n_blocks=40)

    for key, vector in path_feature_map.items():
        path_feature_map[key] = vector.tolist()

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

positions = mds.calculate_positions(features)
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
