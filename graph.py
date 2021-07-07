import requests
import numpy as np
import matplotlib.pyplot as plt

host = 'http://127.0.0.1:8000'

def reservas_mes(y1, y2):
    r = requests.get('{}/reservas_mes/{}/{}'.format(host, y1, y2))
    r = r.json()['data']
    count = [[0 for x in range(1,13)] for i in range(y1, y2+1)]
    for d in r:
        count[d['year']-y1][d['month']-1] = d['count']
    #count[1][1] = 2
    #count[1][11] = 2
    #count[2][11] = 2
    r = np.arange(12)
    fig = plt.figure()
    for y in range(y1, y2+1):
        plt.bar(r, count[y-y1], label=str(y))
    plt.xticks(r, range(1,13))
    plt.legend()
    #fig.savefig('./test.png')
    return fig
