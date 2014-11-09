import numpy as np
from sklearn.decomposition import PCA
from sklearn.neural_network import BernoulliRBM

from signal import SignalServer
from mfcc import calc_mfcc


def extract_mfcc_vectors(filename, n_vectors):
    signal = SignalServer(filename)

    last = signal.get_last_start_point_msec(n_vectors) 
    start_point = np.random.randint(low=0, high=last)
    frames = signal.get_consecutive_frames(n_vectors, start_point)
    
    vectors = [calc_mfcc(frame, n_cepstrum=40) for frame in frames]
    return np.array(vectors)


filename = '../dataset/wavfiles/jazz/Candali-One_Masquerade.wav'
n_vectors = 40
vectors = extract_mfcc_vectors(filename, n_vectors)
vectors = np.array(vectors)
vectors /= np.sum(vectors)

rbm = BernoulliRBM(n_components=40, learning_rate=10e-3, n_iter=1000, 
                   verbose=True)
rbm.fit(vectors)
components = rbm.components_
components /= np.sum(components)
