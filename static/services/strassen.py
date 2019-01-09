"""
Strassen Algorithm implementation
Jeremy TRAN - Corentin DIEVAL
"""

import numpy as np
from math import sqrt
from math import log
import time


class Strassen:
    # multiplication counter
    counter = 0
    # level of recursion
    level = -1
    # start of computing instant
    start_time = 0
    # end of computing instant
    elapsed_time = 0
    # result matrix
    result = []

    def __init__(self, matrix_a, matrix_b):
        self.result = self.compute(matrix_a, matrix_b)

    def get_result(self):
        return self.result, self.elapsed_time, self.counter

    def compute(self, a, b):
        """
        compute(a, b) multiply two square matrix a and b of the same size
        and return the result matrix
        Each integer multiplication done is counted by the global variable counter
        :param a matrix n x n, n > 0
        :param b matrix n x n, n > 0
        :return c the result matrix
        """

        # Storing size of matrices
        a_size = int(sqrt(a.size))
        b_size = int(sqrt(b.size))
        new_size = 0
        previous_size = a_size

        # Error handling
        if (a_size != b_size) or (not a_size or not b_size):
            return "Error: matrices to multiply must have the same size, and must not be empty."

        # Track level of recursion for timer start and stop
        self.level += 1
        # Beginning detection
        if not self.level:
            print 'Request for computing', a_size, 'x', b_size, 'matrices multiplication.'
            self.start_time = time.time()

        # If input are integers just multiply them
        # and increment global multiplication counter
        if a_size == 1:
            self.counter += 1
            self.level -= 1
            return int(a) * int(b)

        # If matrices size > 1
        else:
            # Odd dimension matrices handling
            if log(a_size)/log(2) % 1 != 0:
                a, b, new_size = self.complete_with_zeros(a, b, a_size)
                a_size = previous_size
                a_size, b_size = new_size, new_size

            # Compute Aij, Bij, matrices n/2 x n/2, n > 2
            a11, a12, a21, a22 = self.split(a, a_size)
            b11, b12, b21, b22 = self.split(b, b_size)

            # Compute qk recursively
            q1 = self.compute(a11 - a12, b22)
            q2 = self.compute(a21 - a22, b11)
            q3 = self.compute(a22, b11 + b21)
            q4 = self.compute(a11, b12 + b22)
            q5 = self.compute(a11 + a22, b22 - b11)
            q6 = self.compute(a11 + a21, b11 + b12)
            q7 = self.compute(a12 + a22, b21 + b22)

            # Compute Cij thanks to Strassen formulas
            c11 = q1 - q3 - q5 + q7
            c12 = q4 - q1
            c21 = q2 + q3
            c22 = - q2 - q4 + q5 + q6

            # Create an array of matrices n/2 x n/2
            matrix = np.array([[c11, c12], [c21, c22]])

            # if matrix is not 2 x 2 then rebuild the matrix properly
            # TODO: Might be refactorable by using concatenate instead of array above
            if matrix.size != 4:
                matrix = np.concatenate(
                    (np.concatenate((matrix[0][0], matrix[0][1]), axis=1),
                     np.concatenate((matrix[1][0], matrix[1][1]), axis=1))
                    , axis=0)

            # End detection
            if not self.level:
                self.elapsed_time = time.time() - self.start_time
                print 'Computation realised in', self.elapsed_time, 'seconds.'
                # Remove added zeros rows and columns before returning
                if new_size != 0:
                    matrix = self.remove_added_zeros(matrix, new_size, new_size - previous_size)

            self.level -= 1
            return matrix

    def split(self, matrix, size):
        """
        Split matrix into four sub-matrices.
        :param matrix: the matrix of size 2n x 2n to split
         :param size: this size of matrix
        :return 4 matrices of size n x n
        """
        if size == 2:
            return matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
        else:
            matrix_array = self.split_matrix_in_four(matrix, size / 2)
            return matrix_array[0], matrix_array[1], matrix_array[2], matrix_array[3]

    @staticmethod
    def split_matrix_in_four(matrix, dim):
        """
         Split a matrix into sub-matrices.
         source: https://stackoverflow.com/questions/16856788/slice-2d-array-into-smaller-2d-arrays
         :param matrix the matrix of size 2n x 2n to split
         :param dim the dimension of the matrix (2n)
         :return an array 4 matrices of size n x n
        """
        h, w = matrix.shape
        return (matrix.reshape(h // dim, dim, -1, dim)
                .swapaxes(1, 2)
                .reshape(-1, dim, dim))

    def complete_with_zeros(self, m1, m2, size):
        """
        Complete matrices having odd size into even size
        by adding to each of them a line and a column of zeros

        :param m1: a matrix (2n + 1) x (2n + 1), n > 1
        :param m2: another matrix (2n + 1) x (2n + 1), n > 1
        :param size: the size of m1 and m2
        :return: matrices m1 and m2 completed
        """
        new_size = size
        while log(new_size) / log(2) % 1 != 0:
            new_size += 1
        return self.add_zeros_rows_and_columns(m1, size, new_size), self.add_zeros_rows_and_columns(m2, size, new_size), new_size

    @staticmethod
    def add_zeros_rows_and_columns(matrix, size, new_size):
        """
        Add a row and a column of zeros to a matrix
        :param matrix: the matrix to be modified
        :param size: the matrix size
        :param new_size: the completed matrix size
        :return: the matrix with a row and a column of zeros added
        """
        for i in range(0, new_size - size):
            zeros_line = np.array([np.zeros((size + i,), dtype=int)])
            zeros_column = np.zeros((size + i + 1, 1), dtype=int)
            # Add zeros line to the bottom of the matrix
            completed = np.concatenate((matrix, zeros_line), axis=0)
            # Add zeros column to the bottom of the matrix and return it
            new_matrix = np.concatenate((completed, zeros_column), axis=1)
            matrix = new_matrix

        return matrix

    @staticmethod
    def remove_added_zeros(matrix, actual_size, nb_rows_to_remove):
        """
        Add a row and a column of zeros to a matrix
        :param matrix: the matrix to be modified
        :param actual_size: the size of the matrix to be modified
        :param nb_rows_to_remove: the number of rows and columns to remove
        :return: the matrix with a row and a column of zeros added
        """
        for i in range(actual_size - 1, actual_size - nb_rows_to_remove - 1, -1):
            matrix = np.delete(matrix, i, axis=0)
            matrix = np.delete(matrix, i, axis=1)

        return matrix


# if __name__ == '__main__':
#   matrix_a = np.array([
#       [1, 2, 0, 1],
#       [3, 4, -1, 1],
#       [1, 0, 1, 2],
#       [0, 1, 3, 4]
#   ])
#   matrix_b = np.array([
#       [1, -1, 0, 1],
#       [2,  0, 1, 1],
#       [0, 1, 1, 0],
#       [1, 0, 0, -1]
#   ])
#   strassen = Strassen(matrix_a, matrix_b)
#   print strassen.get_result(), '\n',\
#       'Number of multiplications done: ', strassen.counter, '\n',\
#       'Compute time: ', strassen.elapsed_time
