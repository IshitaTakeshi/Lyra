import numpy as np

from .signalserver import SignalServer
from .mfcc import MFCC


#np.set_printoptions(threshold=np.nan, linewidth=np.inf)


class FeatureExtractor(object):
    def __init__(self, n_frames, n_blocks,
                 n_cepstrum=40, n_filters=26):
        """
        n_frames: The number of frames consisted in one block.
        n_frames consecutive frames form one block
        n_blocks: The number of blocks.
        """
        self.mfcc = MFCC(n_cepstrum, n_filters)
        self.n_frames = n_frames
        self.n_blocks = n_blocks

    def extract(self, filepath):
        # TODO explain the extraction algorithm
        """
        filepath: The path to an input file.
        """

        signal = SignalServer(filepath)

        last = signal.get_last_start_point(self.n_frames)
        start_points = np.random.randint(low=0, high=last, size=self.n_frames)

        features = []
        for start_point in start_points:
            frame = signal.get_frame(start_point)
            mfcc = self.mfcc.calc(frame)
            features.append(mfcc)
        features = np.array(features)
        return features
