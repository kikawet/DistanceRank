import abc

import numpy as np
from numpy.core.multiarray import ndarray


class AbstractRankAlgorithm(metaclass=abc.ABCMeta):

    @classmethod
    def calculateRank(cls, matrix=ndarray, epsilon=1, gamma=1, betta=1):
        """ Devuelve un ranking asignando en base a la matriz de incidencias"""

    def normalize(self, v):
        norm = np.linalg.norm(v, ord=1)
        print(norm)
        if norm == 0:
            norm = np.finfo(v.dtype).eps
        return v / norm
