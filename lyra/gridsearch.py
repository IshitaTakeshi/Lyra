import sys

import numpy as np
from matplotlib import pyplot

from extractor import extraction_process


def calc_mean_error(music_root, learning_rate, n_trials):
    total_error = 0
    for i in range(n_trials):
        path_feature_map, error = extraction_process(
            music_root, n_frames=40, n_blocks=4, learning_rate=learning_rate
        )
        total_error += error
    return total_error


def gridsearch(music_root, candidate_params, verbose=False):
    min_error = float('inf')
    argmin = 0
    errors = []
    for learning_rate in candidate_params:
        error = calc_mean_error(music_root, learning_rate, 10)
        errors.append(error)

        if(error < min_error):
            min_error = error 
            argmin = learning_rate
        
        if(verbose):
            print("learning rate:{:.5f}"
                  " error:{:5.3f}".format(learning_rate, error))

    errors = np.array(errors)
    return errors, argmin, min_error


music_dirs = sys.argv[1:]
for music_root in music_dirs:
    print("target: {}".format(music_root))
    candidate_params = np.arange(0.0, 0.05, 0.001)[1:]

    errors, argmin, min_error = gridsearch(
        music_root, candidate_params, verbose=True)

    print("target:{}".format(music_root)) 
    print("learning rate:{:.5f} min error:{:5.3f}".format(argmin, min_error))

    pyplot.plot(candidate_params, errors, 'g^')
    pyplot.show()
