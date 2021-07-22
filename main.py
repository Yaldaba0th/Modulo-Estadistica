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
from matplotlib.ticker import MaxNLocator
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
        
        self.graph = self.tipo_graph.currentText()
        self.months = ['Enero', 'Febrero', 'Marzo', 'Abril',
                    'Mayo', 'Junio', 'Julio', 'Agosto',
                    'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        self.regiones = ["Tarapaca", "Antofagasta", "Atacama",
                    "Coquimbo", "Valparaiso", "OHiggins",
                    "Maule", "Biobio", "Araucania", "Lagos",
                    "Campo", "Magallanes", "Metropolitana",
                    "Rios", "Arica"]

        #Imprime como primer grafico, reservas por mes por defecto.
        agno = self.agno.value()
        y1 = agno
        y2 = agno
        r = requests.get('{}/reservas_mes/{}/{}'.format(host, y1, y2))
        r = r.json()['data']
        count = [[0 for x in range(1, 13)] for i in range(y1, y2+1)]
        for d in r:
            count[d['year']-y1][d['month']-1] = d['count']

        self.MplWidget.canvas.ax.bar(x=range(12),
                                    height=count[0],
                                    color="orange")
        self.MplWidget.canvas.ax.set_ylabel('N° de clientes por mes')
        self.MplWidget.canvas.ax.set_xticks(range(12))
        self.MplWidget.canvas.ax.set_xticklabels(self.months)
        self.MplWidget.canvas.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.MplWidget.canvas.draw()
        #print(count[0])

        """
        data = count[0]
        #Datos estadisticos(N° de arriendos por mes)
        
            #Arriendos por mes 
        prom = np.mean(data)
        print(prom)

            #mes mas visitado por año
        mesmax = self.months[np.argmax(data)]
        print(mesmax)
            #3 meses mas visitados por el año seleccionado
        argsmax = []
        for i in range(3):
            argmax = np.argmax(data)
            argsmax.append(argmax)
            data = np.delete(data, argmax)
        print(self.months[argsmax[0]])
        print(self.months[argsmax[1]])
        print(self.months[argsmax[2]])

        #Datos esatdisticos(N° personas por región)
        
        argmax = np.argmax(data)
        month =  self.region[argmax] # Region que se recibe mas visitas
        print(month)
        """

        # Eventos
        self.agno.valueChanged.connect(self.FiltrarPorAgno)
        self.tipo_graph.currentIndexChanged.connect(self.selectionChange)
    
    def selectionChange(self):
        self.graph = self.tipo_graph.currentText()
        if(self.graph == 'N° Arriendos/mes'):
            agno = self.agno.value()
            y1 = agno
            y2 = agno

            r = requests.get('{}/reservas_mes/{}/{}'.format(host, y1, y2))
            r = r.json()['data']
            count = [[0 for x in range(1, 13)] for i in range(y1, y2+1)]
            for d in r:
                count[d['year']-y1][d['month']-1] = d['count']

            self.MplWidget.canvas.ax.clear()
            self.MplWidget.canvas.ax.bar(x=range(12),
                                        height=count[0],
                                        color="orange")
            self.MplWidget.canvas.ax.set_ylabel('N° de clientes por mes')
            self.MplWidget.canvas.ax.set_xticks(range(12))
            self.MplWidget.canvas.ax.set_xticklabels(self.months)
            self.MplWidget.canvas.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            self.MplWidget.canvas.draw()
        else:
            resreg = [0] * 15            
            #Realizar la consulta por año.
            #----------------------------
            r = requests.get('{}/reservas_region'.format(host))
            r = r.json()['data']

            for d in r:
                try:
                    resreg[self.regiones.index(d["Procedencia"])] = d["count"]
                except ValueError:
                    pass
            self.MplWidget.canvas.ax.clear()
            self.MplWidget.canvas.ax.bar(x=range(15), height=resreg, width=0.8,
                        bottom=0, align='center', color=None, linewidth=None, xerr=None, yerr=None)
            self.MplWidget.canvas.ax.set_ylabel('Clientes por región')
            self.MplWidget.canvas.ax.set_xticks(range(15))
            self.MplWidget.canvas.ax.set_xticklabels(['I', 'II', 'III', 'IV', 'V', 'VI',
                                    'VII', 'VIII', 'IX', 'X', 'XI',
                                    'XII', 'XIII', 'XIV', 'XV'])
            self.MplWidget.canvas.draw()
            
    def FiltrarPorAgno(self):
        self.graph = self.tipo_graph.currentText()
        if(self.graph == 'N° Arriendos/mes'):
            agno = self.agno.value()
            y1 = agno
            y2 = agno

            r = requests.get('{}/reservas_mes/{}/{}'.format(host, y1, y2))
            r = r.json()['data']
            count = [[0 for x in range(1, 13)] for i in range(y1, y2+1)]
            for d in r:
                count[d['year']-y1][d['month']-1] = d['count']

            self.MplWidget.canvas.ax.clear()
            self.MplWidget.canvas.ax.bar(x=range(12),
                                        height=count[0],
                                        color="orange")
            self.MplWidget.canvas.ax.set_ylabel('N° de clientes por mes')
            self.MplWidget.canvas.ax.set_xticks(range(12))
            self.MplWidget.canvas.ax.set_xticklabels(self.months)
            self.MplWidget.canvas.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            self.MplWidget.canvas.draw()
        else:
            resreg = [0] * 15            
            #Realizar la consulta por año.
            #----------------------------
            r = requests.get('{}/reservas_region'.format(host))
            r = r.json()['data']

            for d in r:
                try:
                    resreg[self.regiones.index(d["Procedencia"])] = d["count"]
                except ValueError:
                    pass
            
            self.MplWidget.canvas.ax.clear()
            self.MplWidget.canvas.ax.bar(x=range(15), height=resreg, width=0.8,
                        bottom=0, align='center', color=None, linewidth=None, xerr=None, yerr=None)
            self.MplWidget.canvas.ax.set_ylabel('Clientes por región')
            self.MplWidget.canvas.ax.set_xticks(range(15))
            self.MplWidget.canvas.ax.set_xticklabels(['I', 'II', 'III', 'IV', 'V', 'VI',
                                    'VII', 'VIII', 'IX', 'X', 'XI',
                                    'XII', 'XIII', 'XIV', 'XV'])
            self.MplWidget.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.exit(app.exec_())
    