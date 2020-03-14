import json

import numpy

from src.algorithms.DistanceRank import DistanceRank

if __name__ == '__main__':
    with open('../urls.json', 'r') as f:
        net = json.load(f)

    urls = list(net.keys())
    print('Hay {} urls'.format(len(urls)))
    dict_urls = {u: i for i, u in enumerate(urls)}
    matrix = numpy.zeros((len(urls), len(urls)))

    for i, url in enumerate(urls):
        for link in net[url]:
            matrix[i, dict_urls[link]] = 1

    ara = DistanceRank()

    v = ara.calculateRank(matrix)

    print(v)
