import sys

import numpy as np
from matplotlib import pyplot

from extractor import GridSearch 

music_dirs = sys.argv[1:]
for music_root in music_dirs:
    print("target: {}".format(music_root))
    candidate_params = np.arange(0.00004, 0.00006, 0.000001)[1:]
    
    gridsearch = GridSearch(music_root, n_frames=40, n_blocks=1, 
                            n_trials=10, verbose=True)

    errors, argmin, min_error = gridsearch.search(candidate_params)

    print("target:{}".format(music_root)) 
    print("learning rate:{:.10f} min error:{:.10f}".format(argmin, min_error))
    pyplot.plot(candidate_params, errors, 'g^')
    pyplot.show()
