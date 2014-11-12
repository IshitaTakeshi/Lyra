from numpy.linalg import norm


def calc_distance(vector1, vector2):
    return norm(vector2-vector1, ord=-1)
