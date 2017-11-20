import numpy as np
from scipy.sparse.csgraph import connected_components


def _power_method(transition_matrix, increase_power=True):
    eigenvector = np.ones(len(transition_matrix))

    if len(eigenvector) == 1:
        return eigenvector

    transition = transition_matrix.transpose()

    while True:
        eigenvector_next = np.dot(transition, eigenvector)

        if np.allclose(eigenvector_next, eigenvector):
            return eigenvector_next

        eigenvector = eigenvector_next

        if increase_power:
            transition = np.dot(transition, transition)


def connected_nodes(matrix):
    _, labels = connected_components(matrix)
    groups = dict()

    for ix, label in enumerate(labels):
        if label in groups:
            groups[label].append(ix)
            continue

        groups[label] = [ix]

    return list(groups.values())


def stationary_distribution(transition_matrix, increase_power=True):
    num_nodes = len(transition_matrix)
    grouped_indices = connected_nodes(transition_matrix)

    eigenvector = []
    indices = []

    for group in grouped_indices:
        t_matrix = transition_matrix[np.ix_(group, group)]
        eigenvector.extend(
            _power_method(t_matrix, increase_power=increase_power),
        )
        indices.extend(group)

    return [float(eigenvector[ix]) / num_nodes for ix in indices]
