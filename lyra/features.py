import numpy as np
from sklearn.decomposition import PCA
from sklearn.neural_network import BernoulliRBM

from signalserver import SignalServer
from mfcc import calc_mfcc


#FIXME sometimes pseudo-likelihood holds 
#an unreasonable value like -20917.83 
n_cepstrum = 40
learning_rate = 10e-4
n_iter = 100
latent_vector_size = 40

#DEBUG
vecbose_rbm = False

def infer_latent(vectors, n_components):
    # BernoulliRBM allows vectors which the input is binary values or 
    # values between 0 and 1
    
    # divide by its sum so that 
    # each element becomes less than or equal to 1
    vectors /= np.sum(vectors)
    rbm = BernoulliRBM(n_components=n_components, learning_rate=learning_rate,
                       n_iter=n_iter, verbose=vecbose_rbm)
    rbm.fit(vectors)
    components = rbm.components_
    #normalize so that this sums to 1
    rbm.components_ / np.sum(rbm.components_)
    return components


def extract_features(filename, n_frames, n_blocks):
    #TODO explain the extraction algorithm 
    """
    filename: The input file name.
    n_frames: The number of frames consisted in one block.
    n_frames consecutive frames form one block
    n_blocks: The number of blocks. 
    """
    signal = SignalServer(filename)

    last = signal.get_last_start_point_msec(n_frames)
    start_points = np.random.randint(low=0, high=last, size=n_blocks)

    feature_vector = np.zeros(latent_vector_size) 
    for i in range(n_blocks):
        frames = signal.get_consecutive_frames(n_frames, start_points[i])
        block = [calc_mfcc(frame, n_cepstrum=n_cepstrum) for frame in frames]
        block = np.array(block)
        latent_vectors = infer_latent(block, latent_vector_size)
        #sum latent vectors
        vector = np.sum(latent_vectors, axis=0)
        feature_vector += vector
    #normalize
    feature_vector /= np.sum(feature_vector)
    return feature_vector
