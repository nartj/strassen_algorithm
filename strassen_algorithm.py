"""
Strassen Algorithm implementation
Jeremy TRAN - Corentin DIEVAL
"""

import numpy as np
from math import sqrt
import time

counter = 0
level = -1
start_time = 0
elapsed_time = 0


def strassen(a, b):
    """
    strassen(a, b) multiply two square matrix a and b of the same size
    and return the result matrix
    Each integer multiplication done is counted by the global variable counter
    :arg a matrix n x n, n > 0
    :arg b matrix n x n, n > 0
    :return c the result matrix
    """
    global counter, level, start_time, elapsed_time

    # Track level of recursion for timer start and stop
    level += 1
    if not level:
        start_time = time.time()

    # Storing size of matrices
    a_size = a.size
    b_size = b.size

    # Error handling
    if a_size != b_size:
        return "Error: matrices to multiply must have the same size."

    # If matrices size = 1 just do multiply and increment counter
    if a_size == 1:
        counter += 1
        level -= 1
        return a * b

    # Odd dimension handling
    if (a_size % 2) != 0:
        a, b = complete_with_zeros(a, b)

    # If matrices size > 1
    else:
        # Compute Aij, Bij, matrices n/2 x n/2, n > 0
        a11, a12, a21, a22 = split(a)
        b11, b12, b21, b22 = split(b)
        # Compute qk recursively
        q1 = strassen(a11 - a12, b22)
        q2 = strassen(a21 - a22, b11)
        q3 = strassen(a22, b11 + b21)
        q4 = strassen(a11, b12 + b22)
        q5 = strassen(a11 + a22, b22 - b11)
        q6 = strassen(a11 + a21, b11 + b12)
        q7 = strassen(a12 + a22, b21 + b22)
        # Compute Cij thanks to Strassen formulas
        c11 = q1 - q3 - q5 + q7
        c12 = q4 - q1
        c21 = q2 + q3
        c22 = - q2 - q4 + q5 + q6
        # Create an array of matrices n/2 x n/2
        matrix = np.array([[c11, c12], [c21, c22]])
        if matrix.size == 4:
            result = matrix
        else:
            result = np.concatenate(
                (np.concatenate((matrix[0][0], matrix[0][1]), axis=1),
                 np.concatenate((matrix[1][0], matrix[1][1]), axis=1))
                , axis=0)
        if not level:
            elapsed_time = time.time() - start_time

        level -= 1
        return result


def split(matrix):
    """
    Split matrix into four sub-matrices.
    """
    size = matrix.size
    if size == 4:
        return matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
    else:
        matrix_array = split_matrix_in_four(matrix, int(sqrt(sqrt(size))))
        return matrix_array[0], matrix_array[1], matrix_array[2], matrix_array[3]


def split_matrix_in_four(matrix, dim):
    """
     Split a matrix into sub-matrices.
     source: https://stackoverflow.com/questions/16856788/slice-2d-array-into-smaller-2d-arrays
    """
    h, w = matrix.shape
    return (matrix.reshape(h // dim, dim, -1, dim)
            .swapaxes(1, 2)
            .reshape(-1, dim, dim))


def complete_with_zeros(m1, m2):
    """
    Complete matrices having odd size into even size
    by adding to each of them a line and a column of zeros

    :param m1: a matrix (2n + 1) x (2n + 1), n > 1
    :param m2: another matrix (2n + 1) x (2n + 1), n > 1
    :return: matrices m1 and m2 completed
    """
    return add_zeros_row_and_column_to_matrix(m1), add_zeros_row_and_column_to_matrix(m2)


def add_zeros_row_and_column_to_matrix(matrix):
    """
    Add a row and a column of zeros to a matrix
    :param matrix: the matrix to be modified
    :return: the matrix with a row and a column of zeros supplementary
    """
    size = int(sqrt(matrix.size))
    zeros_line = np.array([np.zeros((size,), dtype=int)])
    zeros_column = np.zeros((size + 1, 1), dtype=int)
    completed = np.concatenate((matrix, zeros_line), axis=0)
    return np.concatenate((completed, zeros_column), axis=1)


# Testing
matrix_a = np.array([
    [1, 2, 0, 1],
    [3, 4, -1, 1],
    [1, 0, 1, 2],
    [0, 1, 3, 4]
])
matrix_b = np.array([
    [1, -1, 0, 1],
    [2,  0, 1, 1],
    [0, 1, 1, 0],
    [1, 0, 0, -1]
])
print strassen(matrix_a, matrix_b), '\n',\
    'Number of multiplications done: ', counter, '\n',\
    'Compute time: ', elapsed_time
