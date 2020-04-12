from math import exp, log

import numpy as np


class DistanceRank:
    __O = None
    __matrix = None

    def __init__(self, matrix):
        # Pre calculamos todas las sumas
        self.__O = matrix.sum(axis=1).transpose().tolist()[0]
        self.__matrix = matrix.transpose()

    def calculateRank(self, epsilon=0.0001, gamma=1, betta=0.1):
        size = len(self.__O)
        B = lambda j: self.__matrix.getrowview(j).rows[0]

        Dn = np.full(shape=size, fill_value=size + 1, dtype=float)
        itr = 0
        delta = epsilon + 1

        while delta > epsilon:
            alpha = exp(-betta * itr)
            itr = itr + 1
            Dn1 = np.copy(Dn)
            for j in range(size):
                Dn[j] = (1 - alpha) * Dn1[j] + alpha * (min([gamma * Dn1[i] + log(self.__O[i]) for i in B(j)])
                                                        if len(B(j)) != 0 else log(size))
            delta = np.linalg.norm(Dn1 - Dn)

        Xmin = min(Dn)
        Xmax = max(Dn)
        norm = lambda x: (x - Xmin) / (Xmax - Xmin)
        Dn = norm(Dn)
        return Dn
