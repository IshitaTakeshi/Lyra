from numpy.linalg import norm
import numpy as np


def calc_distance(vector1, vector2):
    """Calc L1 norm of vector2-vector1"""
    return np.sum(np.power(vector2-vector1, 2))
    #return norm(vector2-vector1, ord=-1)
