import numpy as np


def _power_method(transition_matrix, increase_power=True):
    probabilities = np.ones(len(transition_matrix))

    if len(probabilities) == 1:
        return probabilities

    transition = transition_matrix.transpose()

    while True:
        probabilities_next = np.dot(transition, probabilities)

        if np.allclose(probabilities_next, probabilities):
            return probabilities_next

        probabilities = probabilities_next

        if increase_power:
            transition = np.dot(transition, transition)
