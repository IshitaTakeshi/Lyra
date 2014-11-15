#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 This is the modified version of 
 https://github.com/yusugomori/DeepLearning/blob/master/python/dA.py

 References :
   - P. Vincent, H. Larochelle, Y. Bengio, P.A. Manzagol: Extracting and
   Composing Robust Features with Denoising Autoencoders, ICML'08, 1096-1103,
   2008

   - DeepLearningTutorials
   https://github.com/lisa-lab/DeepLearningTutorials

   - Yusuke Sugomori: Stochastic Gradient Descent for Denoising Autoencoders,
   http://yusugomori.com/docs/SGD_DA.pdf

"""


import sys
import numpy as np
from .utils import sigmoid, softmax


class Autoencoder(object):
    def __init__(self, input=None, n_visible=2, n_hidden=3, 
                 learning_rate=0.1, corruption_level=0.3, 
                 W=None, hbias=None, vbias=None, np_rng=None):
        self.n_visible = n_visible  # num of units in visible (input) layer
        self.n_hidden = n_hidden    # num of units in hidden layer
        
        self.learning_rate = learning_rate
        assert corruption_level < 1
        self.corruption_level = corruption_level

        if np_rng is None:
            np_rng = np.random.RandomState(1234)

        if W is None:
            a = 1. / n_visible
            W = np_rng.uniform(low=-a, high=a, size=(n_visible, n_hidden))

        if hbias is None:
            hbias = np.zeros(n_hidden)  # initialize h bias 0

        if vbias is None:
            vbias = np.zeros(n_visible)  # initialize v bias 0

        #self.np_rng = np_rng
        self.x = input
        self.W = W
        self.W_prime = self.W.T
        self.hbias = hbias
        self.vbias = vbias

        # self.params = [self.W, self.hbias, self.vbias]

    #def get_corrupted_input(self, input):
    #    return self.np_rng.binomial(size=input.shape, n=1,
    #                                p=1-self.corruption_level) * input

    # Encode
    def get_hidden_values(self, input):
        return sigmoid(np.dot(input, self.W) + self.hbias)

    # Decode
    def get_reconstructed_input(self, hidden):
        return sigmoid(np.dot(hidden, self.W.T) + self.vbias)

    def train(self, input=None):
        if input is not None:
            self.x = input

        x = self.x
        #tilde_x = self.get_corrupted_input(x)
        y = self.get_hidden_values(x)
        z = self.get_reconstructed_input(y)

        L_vbias = x - z
        L_hbias = np.dot(L_vbias, self.W) * y * (1 - y)

        L_W =  np.dot(x.T, L_hbias) + np.dot(L_vbias.T, y)

        self.W += self.learning_rate * L_W
        self.hbias += self.learning_rate * np.mean(L_hbias, axis=0)
        self.vbias += self.learning_rate * np.mean(L_vbias, axis=0)

    def negative_log_likelihood(self):
        #tilde_x = self.get_corrupted_input(self.x)
        y = self.get_hidden_values(self.x)
        z = self.get_reconstructed_input(y)

        cross_entropy = -np.mean(np.sum(self.x*np.log(z) + (1-self.x)*np.log(1-z),
                                 axis=1))

        return cross_entropy

    def reconstruct(self, x):
        y = self.get_hidden_values(x)
        z = self.get_reconstructed_input(y)
        return z
