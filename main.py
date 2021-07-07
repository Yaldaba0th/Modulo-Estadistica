import json
import requests
import sys
import re

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5 import QtCore as qtc
from dateutil import parser as date_parser
from datetime import datetime, timedelta

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg \
    import FigureCanvasQTAgg as FigureCanvas


uifile_1 = 'UIfiles/menu.ui'
form_1, base_1 = uic.loadUiType(uifile_1)

uifile_2 = 'UIfiles/grafico_por_mes.ui'
form_2, base_2 = uic.loadUiType(uifile_2)

global host
host = "http://127.0.0.1:8007"


class Menu(base_1, form_1):
    def __init__(self, *args, **kwargs):
        super(base_1, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Eventos
        self.clientesMes.clicked.connect(self.ClientesMes)
        self.clientesRegion.clicked.connect(self.ClientesRegion)

    def ClientesMes(self):
        self.cm = Clientes_mes()
        self.cm.show()

    def ClientesRegion(self):
        self.cr = Clientes_region()
        self.cr.show()


class Clientes_mes(base_2, form_2):
    def __init__(self, *args, **kwargs):
        super(base_2, self).__init__(*args, **kwargs)
        self.setupUi(self)

        months = ['Enero', 'Febrero', 'Marzo', 'Abril',
                  'Mayo', 'Junio', 'Julio', 'Agosto',
                  'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        # Example
        agno = self.agno.value()
        y1 = agno
        y2 = agno
        r = requests.get('{}/reservas_mes/{}/{}'.format(host, y1, y2))
        r = r.json()['data']
        count = [[0 for x in range(1, 13)] for i in range(y1, y2+1)]
        for d in r:
            count[d['year']-y1][d['month']-1] = d['count']
        # print(count[0])
        self.MplWidget.canvas.ax.bar(x=range(12),
                                     height=[0]*12,
                                     width=0.8, bottom=0,
                                     align='center',
                                     color="orange",
                                     dgecolor=None,
                                     linewidth=None,
                                     err=None, yerr=None)
        self.MplWidget.canvas.ax.set_ylabel('N° de clientes por mes')
        self.MplWidget.canvas.ax.set_xticks(range(12))
        self.MplWidget.canvas.ax.set_xticklabels(months)
        self.MplWidget.canvas.ax.clear()

        self.MplWidget.canvas.ax.bar(x=range(12),
                                     height=count[0],
                                     color="orange")
        self.MplWidget.canvas.draw()

        # Eventos
        self.agno.valueChanged.connect(self.FiltrarPorAgno)

    def FiltrarPorAgno(self):
        agno = self.agno.value()
        y1 = agno
        y2 = agno
        # print(agno)
        # print()
        r = requests.get('{}/reservas_mes/{}/{}'.format(host, y1, y2))
        r = r.json()['data']
        count = [[0 for x in range(1, 13)] for i in range(y1, y2+1)]
        for d in r:
            count[d['year']-y1][d['month']-1] = d['count']
        # print(count[0])
        self.MplWidget.canvas.ax.clear()
        self.MplWidget.canvas.ax.bar(x=range(12),
                                     height=count[0],
                                     color="orange")
        self.MplWidget.canvas.draw()

        # Consulta filtrar po año


class Clientes_region(FigureCanvas):
    def __init__(self):

        fig, self.ax = plt.subplots(figsize=(12, 6),
                                    tight_layout=True,
                                    facecolor='w')
        super().__init__(fig)

        regiones = ["Tarapaca", "Antofagasta", "Atacama",
                    "Coquimbo", "Valparaiso", "OHiggins",
                    "Maule", "Biobio", "Araucania", "Lagos",
                    "Campo", "Magallanes", "Metropolitana",
                    "Rios", "Arica"]
        resreg = [0] * 15
        r = requests.get('{}/reservas_region'.format(host))
        r = r.json()['data']

        for d in r:
            try:
                resreg[regiones.index(d["Procedencia"])] = d["count"]
            except ValueError:
                pass

        # Example
        self.ax.bar(x=range(15), height=resreg, width=0.8,
                    bottom=0, align='center', color=None,
                    edgecolor=None, linewidth=None, xerr=None, yerr=None)
        self.ax.set_ylabel('Clientes por región')
        self.ax.set_xticks(range(15))
        self.ax.set_xticklabels(['I', 'II', 'III', 'IV', 'V', 'VI',
                                 'VII', 'VIII', 'IX', 'X', 'XI',
                                 'XII', 'XIII', 'XIV', 'XV'])

        # Consulta clientes por region


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.exit(app.exec_())
