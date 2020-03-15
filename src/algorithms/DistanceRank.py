from math import exp, log

import numpy as np


class DistanceRank:
    __O = None
    __matrix = None

    def __init__(self, matrix):
        # Pre calculamos todas las sumas
        self.__O = matrix.sum(axis=1).transpose().tolist()[0]
        self.__matrix = matrix.transpose()

    def calculateRank(self, epsilon=10, gamma=1, betta=0.1):
        size = len(self.__O)

        Dn = np.full(size, size + 1)
        itr = 0
        delta = epsilon + 1

        while delta > epsilon:
            alpha = exp(-betta * itr)
            itr = itr + 1
            Dn1 = np.copy(Dn)
            for j in range(size):
                Dn[j] = (1 - alpha) * Dn1[j] + alpha * min([gamma * Dn1[i] + log(self.__O[i]) for i in self.__matrix.getrowview(j).rows[0]] + [np.iinfo(Dn1[0].dtype).max])
            delta = np.linalg.norm(Dn1 - Dn)
        return Dn - min(Dn)  # self.normalize(Dn)