import json
import glob
import os
import sys

import numpy as np

import utils
from plot import plot
from mds import calculate_positions


jsonpaths = sys.argv[1:]

dicts = []
for path in jsonpaths:
    dicts.append(json.load(open(path, 'r')))
path_feature_map = utils.merge_multiple_dicts(dicts)

plot(path_feature_map)
