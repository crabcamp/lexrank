import math

import numpy as np
from scipy.linalg import block_diag

from lexrank.algorithms.power_method import (
    connected_nodes, stationary_distribution,
)


def test_connected_nodes():
    t_matrix = np.array([[1]])
    expected_result = [[0]]

    assert connected_nodes(t_matrix) == expected_result

    t_matrix = np.array([[.6, .1, .3], [.1, .7, .2], [.2, .2, .6]])

    expected_result = [[0, 1, 2]]
    assert connected_nodes(t_matrix) == expected_result

    t_matrix = np.array([[.5, 0, .5], [0, 1, 0], [.5, 0, .5]])

    expected_result = [[0, 2], [1]]
    assert connected_nodes(t_matrix) == expected_result

    mat_1 = np.array([[.5, 0, .5], [0, 1, 0], [.5, 0, .5]])
    mat_2 = np.array([[1]])
    mat_3 = np.array([[0, 1], [1, 0]])
    mat_4 = np.array([[.6, .1, .3], [.1, .7, .2], [.2, .2, .6]])
    t_matrix = block_diag(mat_1, mat_2, mat_3, mat_4)

    expected_result = [[0, 2], [1], [3], [4, 5], [6, 7, 8]]
    assert connected_nodes(t_matrix) == expected_result


def test_stationary_distribution():
    transition_matrices = []

    t_matrix = np.array([[1.]])

    assert np.array_equal(stationary_distribution(t_matrix), [1.])
    transition_matrices.append(t_matrix)

    t_matrix = np.array([
        [.6, .1, .3],
        [.1, .7, .2],
        [.2, .2, .6],
    ])

    expected_result = [.2759, .3448, .3793]
    actual_result_1 = stationary_distribution(t_matrix, increase_power=True)
    actual_result_2 = stationary_distribution(t_matrix, increase_power=False)

    assert np.array_equal(np.round(actual_result_1, 4), expected_result)
    assert np.array_equal(np.round(actual_result_2, 4), expected_result)
    transition_matrices.append(t_matrix)

    t_matrix = np.zeros([5, 5])
    t_matrix[np.ix_([0, 3], [2, 4])] = .5
    t_matrix[np.ix_([2], [0, 1, 3, 4])] = .25
    t_matrix[1, 2], t_matrix[4, 4] = 1, 1

    expected_result = [0, 0, 0, 0, 1]
    actual_result_1 = stationary_distribution(t_matrix, increase_power=True)
    actual_result_2 = stationary_distribution(t_matrix, increase_power=False)

    assert np.allclose(actual_result_1, expected_result)
    assert np.allclose(actual_result_2, expected_result)
    transition_matrices.append(t_matrix)

    t_matrix = np.zeros([4, 4])
    t_matrix[0, 1] = 1
    t_matrix[1, 1], t_matrix[1, 2] = 1 / 3, 2 / 3
    t_matrix[2, 3] = 1
    t_matrix[3, 0], t_matrix[3, 3] = 3 / 5, 2 / 5

    expected_result = [6 / 31, 9 / 31, 6 / 31, 10 / 31]
    actual_result_1 = stationary_distribution(t_matrix, increase_power=True)
    actual_result_2 = stationary_distribution(t_matrix, increase_power=False)

    assert np.allclose(actual_result_1, expected_result)
    assert np.allclose(actual_result_2, expected_result)
    transition_matrices.append(t_matrix)

    t_matrix = np.zeros([7, 7])
    t_matrix[0, 0], t_matrix[0, 1] = .5, .5
    t_matrix[1, 0], t_matrix[1, 1], t_matrix[1, 2] = .5, .4, .1
    t_matrix[2, 1], t_matrix[2, 2] = .6, .4
    t_matrix[3, 2], t_matrix[3, 3] = .2, .4
    t_matrix[3, 4], t_matrix[3, 5] = .2, .2
    t_matrix[4, 3], t_matrix[4, 6] = .7, .3
    t_matrix[5, 6] = 1.
    t_matrix[6, 5], t_matrix[6, 6] = .95, .05

    expected_result = [0.2465, 0.2465, 0.0411, 0., 0., 0.2269, 0.2389]
    actual_result_1 = stationary_distribution(t_matrix, increase_power=True)
    actual_result_2 = stationary_distribution(t_matrix, increase_power=False)

    assert np.array_equal(np.round(actual_result_1, 4), expected_result)
    assert np.array_equal(np.round(actual_result_2, 4), expected_result)
    transition_matrices.append(t_matrix)

    t_matrix = np.array([[1 / 2, 0, 1 / 2], [0, 1, 0], [1 / 2, 0, 1 / 2]])

    expected_result = [1 / 3] * 3
    actual_result_1 = stationary_distribution(t_matrix, increase_power=True)
    actual_result_2 = stationary_distribution(t_matrix, increase_power=False)

    assert np.allclose(actual_result_1, expected_result)
    assert np.allclose(actual_result_2, expected_result)
    transition_matrices.append(t_matrix)

    # crash test
    repeat_num = 20
    big_t_mat = block_diag(*transition_matrices * repeat_num)
    distribution_1 = stationary_distribution(big_t_mat, increase_power=True)
    distribution_2 = stationary_distribution(big_t_mat, increase_power=False)

    assert math.isclose(sum(distribution_1), 1)
    assert math.isclose(sum(distribution_2), 1)
    assert np.allclose(distribution_1, distribution_2)

    data = np.split(np.array(distribution_1), repeat_num)
    test_row = data[0]

    for row in data[1:]:
        assert np.array_equal(row, test_row)
