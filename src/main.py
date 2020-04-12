import time
from idlelib.iomenu import encoding

import scipy
from scipy.sparse import lil_matrix

from algorithms.DistanceRank import DistanceRank
import json

if __name__ == '__main__':
    inicio_carga = time.time()

    matrix = scipy.sparse.load_npz('../matrix.npz')

    sizeUrls = matrix.shape[0]
    print('Hay {} urls'.format(sizeUrls))

    matrix = matrix.tolil()

    fin_carga = time.time()
    dRank = DistanceRank(matrix)

    inicio_calculo = time.time()
    v = dRank.calculateRank()
    #
    fin_calculo = time.time()

    print('tiempo carga: ', fin_carga - inicio_carga)
    print('tiempo preprocesamiento: ', inicio_calculo - fin_carga)
    print('tiempo calculo: ', fin_calculo - inicio_calculo)

    with open('../urls.json', 'r') as f:
        urls = json.load(f, encoding='utf8')

    ranking = sorted(zip(urls, v), key=lambda x: x[1], reverse=True)

    print(ranking[:100])
