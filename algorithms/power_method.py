import numpy as np


def split_transition_matrix(matrix):
    """Split symmetric transition matrix into a list of smaller ones."""
    adjacencies = []

    for i in range(len(matrix)):
        adjacent = np.where(matrix[i])
        adjacencies.append(adjacent)[0]

    connected_nodes = []
