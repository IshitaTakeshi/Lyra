from numpy.linalg import norm


def calc_distance(vector1, vector2):
    """Calc L1 norm of vector2-vector1"""
    return norm(vector2-vector1, ord=-1)
