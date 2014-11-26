from __future__ import division

import numpy as np
from numpy.fft import fft, ifft, rfft
from scipy.fftpack import dct
from scipy.cluster.vq import kmeans, whiten
from scipy.signal import lfilter, hamming



MEL_SCALE = 1127.010480


def hz_to_mel(frequency):
    return MEL_SCALE * np.log10(frequency/700.0 + 1)


def mel_to_hz(frequency):
    return 700 * (np.power(10, frequency/MEL_SCALE) - 1)


def pre_emphasis_filter(sound, p=0.97):
# Copyright (c) 2008 Cournapeau David
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
    return lfilter([1., -p], 1, sound)


class MFCC(object):
    def __init__(self, n_cepstrum=8, n_filters=26):
        self.n_cepstrum = n_cepstrum
        self.n_filters = n_filters
        #for dct3 transform
        self.dct_matrix = self.generate_dct_matrix()

    def generate_melfilterbank(self, sound_length,
                               lower_frequency=133.3333,
                               upper_frequency=6855.4976):
        """
        Parameters:
            sound_length - int
                Length of audio data.
            lower_frequency - float
                Lower frequency.
            upper_frequency - float
                Upper frequency.
        Returns:
            Mel filter bank.
        """

        if(float(sound_length)/2 < upper_frequency):
            upper_frequency = float(sound_length)/2

        filters = np.zeros((self.n_filters, sound_length), dtype='d')

        melmax = hz_to_mel(upper_frequency)
        melmin = hz_to_mel(lower_frequency)
        filter_edges = mel_to_hz(np.linspace(melmin, melmax, self.n_filters+2))
        for whichfilter in range(self.n_filters):
            left = round(filter_edges[whichfilter])
            center = round(filter_edges[whichfilter+1])
            right = round(filter_edges[whichfilter+2])

            height = 2.0 / (right - left)
            left_slope = height / (center-left)
            right_slope = height / (center-right)

            for frequency in np.arange(left+1.0, center, 1.0):
                left = (frequency-left) * left_slope
                filters[whichfilter, int(frequency)] = left

            for frequency in np.arange(center, right, 1.0):
                right = (right-frequency) * right_slope
                filters[whichfilter, int(frequency)] = right
        return filters

    def generate_dct_matrix(self):
        matrix = np.empty((self.n_cepstrum, self.n_filters))
        for k in range(self.n_cepstrum):
            c = k * np.pi / self.n_filters
            matrix[k] = np.cos(c * np.arange(0.5, self.n_filters+0.5, 1.0))
        matrix[:, 0] = matrix[:, 0] * 0.5
        return matrix
    
    #TODO Rename
    def calc(self, sound_segment):
        segment_length = len(sound_segment)
        available_range = int(segment_length/2)

        #sound_segment = pre_emphasis_filter(sound_segment)

        # windowing
        window = np.hamming(segment_length)
        sound_segment = sound_segment * window.T

        spectrum = fft(sound_segment)
        spectrum = spectrum[:available_range]

        power = np.power(np.abs(spectrum), 2)

        melfilterbank = self.generate_melfilterbank(available_range)
        spectrum = np.dot(power, melfilterbank.T).clip(1e-5, np.inf)
        log_spectrum = np.log(spectrum)
        mfcc = np.dot(log_spectrum, self.dct_matrix.T) / self.n_filters
        return mfcc
