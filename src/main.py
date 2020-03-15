import time

import numpy as np
from scipy.sparse import dok_matrix
from tinydb import TinyDB, Query
from tqdm import tqdm

from src.algorithms.DistanceRank import DistanceRank

if __name__ == '__main__':
    inicio = time.time()
    db = TinyDB('../urls.json', default_table='links')
    url = Query()
    sizeUrls = len(db)
    print('Hay {} urls'.format(sizeUrls))
    # dict_urls = {u: i for i, u in enumerate(urls)}
    matrix = dok_matrix((sizeUrls, sizeUrls), dtype=np.bool)

    # for i, url in enumerate(urls):
    #     for link in net[url]:
    #         matrix[i, dict_urls[link]] = 1
    inicio_leer = time.time()
    rows = []
    cols = []
    for i in tqdm(range(sizeUrls)):
        for link in db.get(doc_id=i + 1)['links']:
            j = db.get(url.domain == link)
            if j:
                matrix[i, j.doc_id - 1] = 1

    matrix = matrix.tolil()
    fin_matriz = time.time()
    dRank = DistanceRank(matrix)

    # print(matrix.toarray())

    # print(matrix.getrowview(1))

    # cx = matrix.tocsc()
    # # for i, j, v in izip(cx.row, cx.col, cx.data):
    # #     print(i, j, v)
    # a = matrix.transpose().getrowview(2)
    #
    # for x in a.rows[0]:
    #     print(x)
    # v = np.full(3, 3)
    # for x in matrix:
    #     print(x[0,])
    inicio_calculo = time.time()
    v = dRank.calculateRank()
    #
    fin_programa = time.time()

    print('tiempo de carga: ', inicio_leer - inicio)
    print('tiempo lectura: ', fin_matriz - inicio_leer)
    print('tiempo preprocesamiento: ', inicio_calculo - fin_matriz)
    print('tiempo calculo: ', fin_programa - inicio_calculo)

    print(v)
