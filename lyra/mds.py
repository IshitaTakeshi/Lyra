from sklearn import manifold
import numpy as np

from scale import calc_distance


def calculate_positions(vectors):
    def calc_distance_matrix(vectors):
        n_vectors = len(vectors)
        matrix = np.zeros((n_vectors, n_vectors))
        for i in range(n_vectors):
            for j in range(n_vectors):
                matrix[i][j] = calc_distance(vectors[i], vectors[j])
        return matrix

    distance_matrix = calc_distance_matrix(vectors)

    #TODO tune params
    mds = manifold.MDS(n_components=2, max_iter=300, eps=1e-9,
                       dissimilarity="precomputed", n_jobs=1)
    mds.fit(distance_matrix)
    positions = mds.embedding_
    return positions
