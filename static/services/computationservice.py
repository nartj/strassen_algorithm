"""
Strassen Algorithm implementation
Jeremy TRAN - Corentin DIEVAL
"""

import numpy as np
from math import sqrt
from math import log
import time


class ComputationService:
    # multiplication counter using strassen algorithm
    classical_mult_cnt = 0
    # multiplication counter using classical algorithm
    strassen_mult_cnt = 0
    # start of computing instant
    classical_comp_time = 0
    # computation time using strassen algorithm
    strassen_comp_time = 0
    # result matrix
    result = []

    def __init__(self, matrix_a, matrix_b):
        self.result = self.compute(matrix_a, matrix_b)

    def get_result(self):
        return self.result, self.strassen_comp_time, self.strassen_mult_cnt, self.classical_comp_time, self.classical_mult_cnt

    def compute(self, a, b):
        """
        compute(a, b) multiply two square matrix a and b of the same size
        and return the result matrix
        The computations are done following Strassen algorithm, then following classical matrices multiplication
        algorithm (Sum(AikBkj)).

        :param a matrix n x n, n > 0
        :param b matrix n x n, n > 0
        :return c the result matrix
        """
        # Storing size of matrices
        a_size = int(sqrt(a.size))
        b_size = int(sqrt(b.size))

        # Error handling
        if (a_size != b_size) or (not a_size or not b_size):
            return "Error: matrices to multiply must have the same size, and must not be empty."

        new_size = 0
        previous_size = a_size

        # Odd dimension matrices handling for Strassen algorithm
        if log(a_size) / log(2) % 1 != 0:
            a, b, new_size = self.complete_with_zeros(a, b, a_size)
            a_size = new_size

        print 'Request for computing', a_size, 'x', a_size, 'matrices multiplication.'

        # Compute result matrix using strassen algorithm implementation
        start_time = time.time()
        result = self.compute_using_strassen(a, b)

        self.strassen_comp_time = time.time() - start_time
        print 'Strassen computation realised in', self.strassen_comp_time, 'seconds.'

        # Remove added zeros rows and columns before starting classical algorithm
        if new_size != 0:
            self.result = self.remove_added_zeros(result, new_size, new_size - previous_size)
            a = self.remove_added_zeros(a, new_size, new_size - previous_size)
            b = self.remove_added_zeros(b, new_size, new_size - previous_size)
        else:
            self.result = result

        # Compute result matrix using classical algorithm implementation
        start_time = time.time()
        result = self.classical_compute(a, b)

        self.classical_comp_time = time.time() - start_time
        print 'Classical computation realised in', self.classical_comp_time, 'seconds.'

        # Result verification
        if not (result == self.result).all():
            return "Error: classical and strassen algorithm returned different results."

        return result

    def compute_using_strassen(self, a, b):
        """
        Compute matrices multiplication using strassen algorithm
        Each integer multiplication done is counted by the global variable counter

        :param a: a square matrix of size n^2k
        :param b: a square matrix of size n^2k
        :return: the matrix result of size n^2k
        """

        size = int(sqrt(a.size))

        # If input are integers just multiply them
        # and increment global multiplication counter
        if size == 1:
            self.strassen_mult_cnt += 1
            return int(a) * int(b)

        # If matrices size > 1, call recursively compute_using_strassen
        # to compute q1, q2 ..., q7 following strassen formulas
        # until a11, a12 ... , b21, b22 are integers
        # then just multiply them and increment multiplication counter
        else:

            # Compute Aij, Bij, matrices n/2 x n/2, n > 2
            a11, a12, a21, a22 = self.split(a, size)
            b11, b12, b21, b22 = self.split(b, size)

            # Compute qk recursively
            q1 = self.compute_using_strassen(a11 - a12, b22)
            q2 = self.compute_using_strassen(a21 - a22, b11)
            q3 = self.compute_using_strassen(a22, b11 + b21)
            q4 = self.compute_using_strassen(a11, b12 + b22)
            q5 = self.compute_using_strassen(a11 + a22, b22 - b11)
            q6 = self.compute_using_strassen(a11 + a21, b11 + b12)
            q7 = self.compute_using_strassen(a12 + a22, b21 + b22)

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

            return matrix

    def classical_compute(self, a, b):
        """
        Compute matrices multiplication using classical algorithm (AikBkj)
        Each integer multiplication done is counted by the global variable counter

        :param a: a square matrix of size n
        :param b: another square matrix of size n
        :return: the matrix result of size n
        """
        n = np.shape(a)[0]
        c = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                s = 0
                for k in range(n):
                    s += a[i][k] * b[k][j]
                    self.classical_mult_cnt += 1
                    c[i][j] = s
        return c

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
         Split a matrix into four sub-matrices
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
        Complete matrices which sizes are not 2^k form, k natural integer
        by adding to each of them a line and a column of zeros

        :param m1: a matrix (2n + 1) x (2n + 1), n > 1
        :param m2: another matrix (2n + 1) x (2n + 1), n > 1
        :param size: the size of m1 and m2
        :return: matrices m1 and m2 completed until their size are 2^k form
        """
        new_size = size
        while log(new_size) / log(2) % 1 != 0:
            new_size += 1
        return self.add_zeros_rows_and_columns(m1, size, new_size), self.add_zeros_rows_and_columns(m2, size, new_size), new_size

    @staticmethod
    def add_zeros_rows_and_columns(matrix, size, new_size):
        """
        Add (new_size - size) rows and columns of zeros to a matrix beginning by right bottom sides
        :param matrix: the matrix to be completed of zeros
        :param size: the matrix size
        :param new_size: the completed matrix size
        :return: the matrix with (new_size - size) rows and columns of zeros added
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
        Remove nb_rows_to_remove rows and a columns of zeros to a matrix beginning by right and bottom sides
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
