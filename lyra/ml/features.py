import numpy as np

from lyra.util.config import Config

from .signalserver import SignalServer
from .mfcc import MFCC


#np.set_printoptions(threshold=np.nan, linewidth=np.inf)


class MFCCExtractor(object):
    def __init__(self, config_path):
        config = Config(config_path, 'MFCC')
        self.mfcc = MFCC(config.n_cepstrum, config.n_filters)
        self.n_frames = config.n_frames  #the number of frames in a block
        self.n_blocks = config.n_blocks  #the number of blocks

    def extract(self, filepath):
        # TODO explain the extraction algorithm
        """
        filepath: The path to an input file.
        """

        signal = SignalServer(filepath)

        last = signal.get_last_start_point(self.n_frames)
        start_points = np.random.normal(loc=last/2, scale=last/6,
                                        size=self.n_frames).astype(np.int32)

        features = []
        for start_point in start_points:
            if(start_point < 0):
                start_point = 0
            if(start_point > last):
                start_point = last

            frame = signal.get_frame(start_point)
            mfcc = self.mfcc.calc(frame)
            features.append(mfcc)
        features = np.mean(features, axis=0)
        return features
