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
    #count[1][10] = 2
    #count[2][10] = 2
    #count[4][10] = 2
    ydif = y2 - y1 + 1
    width = 0.5
    r = np.arange(12)
    fig = plt.figure()
    for y in range(y1, y2+1):
        plt.bar(r*ydif+(y-y1)*width, count[y-y1], label=str(y), width=width)
    plt.xticks(r*ydif+width*ydif/2, range(1,13))
    plt.legend()
    fig.savefig('./test.png')
    return fig
