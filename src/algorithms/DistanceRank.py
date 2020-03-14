from math import exp, log

import numpy as np
from numpy.core.multiarray import ndarray

from src.AbstractRankAlgorithm import AbstractRankAlgorithm


class DistanceRank(AbstractRankAlgorithm):

    def calculateRank(self, matrix=ndarray, epsilon=100, gamma=1, betta=0.1):
        size = matrix.shape[0]

        Dn = np.full(size, size + 1)
        itr = 0
        delta = epsilon + 1

        while itr < 30:  # delta > epsilon:
            alpha = exp(-betta * itr)
            itr = itr + 1
            Dn1 = np.copy(Dn)
            for j in range(size):
                Dn[j] = (1 - alpha) * Dn1[j] + alpha * self.__mini(j, Dn1, gamma, matrix)
            delta = np.linalg.norm(Dn1 - Dn)

        return Dn  # self.normalize(Dn)

    def __mini(self, j, Dn1, gamma, matrix=ndarray):
        mini = np.iinfo(Dn1[0].dtype).max
        for i in range(matrix.shape[0]):
            if matrix[i, j] == 1:
                mini = min(mini, gamma * Dn1[i] + log(self.__O(i, matrix)))

        return mini

    def __O(self, i, matrix=ndarray):
        """
        O(i) denotes the number of outgoing links from page i
        :param i: page index
        :param matrix: incidence matrix
        :return: O(i) function
        """
        sum = 0
        for j in range(matrix.shape[0]):
            sum += matrix[i, j]

        return sum
