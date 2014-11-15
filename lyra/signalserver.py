from __future__ import division

import numpy as np

import waveio


#TODO separate to core and interface
class SignalServer(object):
    """Serves frames of a music signal"""
    def __init__(self, filepath, frame_size_msec=64, overlap_msec=32):
        """
        Parameters:
            filpath: The path to a music file.
            msec: The frame size in milliseconds.
            overlap: The overlap size of frames.
        """
        if(overlap_msec > frame_size_msec):
            raise ValueError("The overlap must be less than the frame size")
        signal, framerate = waveio.read(filepath, 1)
        #signal in numpy array
        self.signal = signal
        self.signal_size = len(signal)

        self.msec_to_size = lambda msec: int(framerate*msec / 1000)
        self.size_to_msec = lambda size: int(size*1000 / framerate)
        self.overlap = self.msec_to_size(overlap_msec)
        self.frame_size = self.msec_to_size(frame_size_msec)
        self.current = 0

    def get_last_start_point(self, n_frames):
        if(n_frames < 0):
            raise ValueError(
                "The number of frames must be greater than or equal to zero.")
        required_size = n_frames*self.frame_size + (n_frames-1)*self.overlap  
        return len(self.signal)-required_size

    def get_consecutive_frames(self, n_frames, start_point):
        last = self.get_last_start_point(n_frames)

        if(n_frames < 0):
            raise ValueError(
                "The number of frames must be greater than or equal to zero.")
        if(start_point > last):
            raise ValueError("The start point is too late.")
        if(start_point < 0):
            raise ValueError(
                "The start point must be greater than or equal to 0.")

        frames = []
        for i in range(n_frames):
            frame = self.signal[start_point:start_point+self.frame_size]
            frames.append(frame)
            start_point += self.frame_size - self.overlap
        return np.array(frames)

    def get_frame(self, start_point):
        last = self.get_last_start_point(1)
        if(start_point > last):
            raise ValueError("The start point is too late.")
        if(start_point < 0):
            raise ValueError(
                "The start point must be greater than or equal to 0.")
        return self.signal[start_point:start_point+self.frame_size]

    def seek(self, point):
        if(point > self.signal_size):
            raise ValueError("The point is too late.")
        if(point < 0):
            raise ValueError("The point must be greater than or equal to 0.")
        self.current = point

    def next(self):
        if(self.current+self.frame_size > self.signal_size):
            return np.array([])
        frame = self.signal[self.current:self.current+self.frame_size]
        self.current += self.frame_size - self.overlap
        return frame
