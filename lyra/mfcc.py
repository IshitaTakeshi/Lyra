from __future__ import division

import numpy as np
from numpy.fft import fft, ifft, rfft
from scipy.fftpack import dct
from scipy.cluster.vq import kmeans, whiten


MEL_SCALE = 1127.010480


def hz_to_mel(frequency):
    return MEL_SCALE * np.log10(frequency/700.0 + 1)


def mel_to_hz(frequency):
    return 700 * (np.power(10, frequency/MEL_SCALE) - 1)


def pre_emphasis_filter(sound, p=0.97):
    filtered_sound = np.empty(len(sound))
    for i in range(1, len(sound)):
        filtered_sound[i] = sound[i] - p*sound[i-1]
    return filtered_sound


def generate_melfilterbank(sound_length, n_filters=26,
                           lower_frequency=133.3333, upper_frequency=6855.4976):
    """
    Parameters:
        sound_length - int 
            Length of audio data.
        n_filters - int
            Number of filters.
        lower_frequency - float
            Lower frequency.
        upper_frequency - float
            Upper frequency.
    Returns:
        Mel filter bank.
    """

    if(float(sound_length)/2 < upper_frequency):
        upper_frequency = float(sound_length)/2
          
    filters = np.zeros((n_filters, sound_length), dtype='d')

    melmax = hz_to_mel(upper_frequency)
    melmin = hz_to_mel(lower_frequency)
    filter_edges = mel_to_hz(np.linspace(melmin, melmax, n_filters+2))
    for whichfilter in range(n_filters):
        left   = np.round(filter_edges[whichfilter])
        center = np.round(filter_edges[whichfilter+1])
        right  = np.round(filter_edges[whichfilter+2])

        height = 2.0 / (right - left)
        leftslope  = height / (center-left)
        rightslope = height / (center-right)
        
        for frequency in np.arange(left+1.0, center, 1.0):
            filters[whichfilter, np.int(frequency)] = (frequency-left) * leftslope
        
        for frequency in np.arange(center, right, 1.0):
            filters[whichfilter, np.int(frequency)] = (right-frequency) * leftslope
    
    return filters


def generate_dct_matrix(n_filters, n_cepstrum):
    matrix = np.empty((n_cepstrum, n_filters))
    for k in range(n_cepstrum):
        c = k * np.pi / n_filters
        matrix[k] = np.cos(c * np.arange(0.5, n_filters+0.5, 1.0))
    matrix[:, 0] = matrix[:, 0] * 0.5
    return matrix


def calc_mfcc(sound_segment, n_cepstrum=8, n_filters=26):
    segment_length = len(sound_segment)
    available_range = int(segment_length/2)

    #windowing
    window = np.hamming(segment_length)
    sound_segment = pre_emphasis_filter(sound_segment) * window.T

    spectrum = fft(sound_segment)
    spectrum = spectrum[:available_range]

    power = np.power(np.abs(spectrum), 2)
    melfilterbank = generate_melfilterbank(available_range, n_filters)

    log_spectrum = np.log(np.dot(power, melfilterbank.T).clip(1e-5, np.inf)) 
    dct_matrix = generate_dct_matrix(n_filters, n_cepstrum)
    #apply dct3 transform
    mfcc = np.dot(log_spectrum, dct_matrix.T) / n_filters
    return mfcc
