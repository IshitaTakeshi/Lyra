from __future__ import division

import wave
import json

import numpy as np


def read(filename, nchannels):
    """
    Parameters
        filename: The path to an input file.
        nchannels: The number of channels of wave.
    Returns
        A tuple of wave data and sample rate.
    """

    wavefile = wave.open(filename, 'r')
    framerate = wavefile.getframerate()
    nframes = wavefile.getnframes()
    data = wavefile.readframes(nframes)
    wavefile.close()

    data = np.frombuffer(data, dtype='int16', count=-1)
    data = data / 32768

    if(nchannels == 1):
        #stereo to monoral
        if(wavefile.getnchannels() == 2):
            L, R = data.reshape((nframes, 2)).T
            data = (L+R) / 2
        return data, framerate
    elif(nchannels == 2):
        if(wavefile.getnchannels() == 1):
            L = data
            R = data
        else:
            L, R = data.reshape((nframes, 2)).T
        return (L, R), framerate

    m = "Invalid numbef of channels {} specified.".format(nchannels)
    raise ValueError(m)
