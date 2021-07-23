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
from scipy.stats import linregress


uifile_1 = 'UIfiles/menu.ui'
form_1, base_1 = uic.loadUiType(uifile_1)

uifile_2 = 'UIfiles/grafico_por_mes.ui'
form_2, base_2 = uic.loadUiType(uifile_2)

uifile_3 = 'UIfiles/grafico_por_region.ui'
form_3, base_3 = uic.loadUiType(uifile_3)

uifile_4 = 'UIfiles/sugerencias.ui'
form_4, base_4 = uic.loadUiType(uifile_4)

global host
host = "http://127.0.0.1:8007"


class Menu(base_1, form_1):
    def __init__(self, *args, **kwargs):
        super(base_1, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Eventos
        self.clientesMes.clicked.connect(self.ClientesMes)
        self.clientesRegion.clicked.connect(self.ClientesRegion)
        self.suger.clicked.connect(self.SugerenciasCliente)

    def ClientesMes(self):
        self.cm = Clientes_mes()
        self.cm.show()

    def ClientesRegion(self):
        self.cr = Clientes_region()
        self.cr.show()

    def SugerenciasCliente(self):
        self.sgr = Sugrencias()
        self.sgr.show()

class Clientes_mes(base_2, form_2):
    def __init__(self, *args, **kwargs):
        super(base_2, self).__init__(*args, **kwargs)
        self.setupUi(self)
        
        self.months = ['Enero', 'Febrero', 'Marzo', 'Abril',
                    'Mayo', 'Junio', 'Julio', 'Agosto',
                    'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

        #Imprime como primer grafico, reservas por mes por defecto.
        agno = self.agno.value()
        y1 = agno
        y2 = agno
        r = requests.get('{}/reservas_mes/{}/{}'.format(host, y1, y2))
        r = r.json()['data']
        count = [[0 for x in range(1, 13)] for i in range(y1, y2+1)]
        for d in r:
            count[d['year']-y1][d['month']-1] = d['count']

        self.MplWidget.canvas.ax.set_title('Arrendatarios por mes')
        self.MplWidget.canvas.ax.bar(x=range(12),
                                    height=count[0])
        self.MplWidget.canvas.ax.set_ylabel('N° de arrendatarios por mes')
        self.MplWidget.canvas.ax.set_xticks(range(12))
        self.MplWidget.canvas.ax.set_xticklabels(self.months, rotation=25)
        self.MplWidget.canvas.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.MplWidget.canvas.ax.set_ylim(0)
        self.MplWidget.canvas.ax.grid(color="green", which="major", axis='both', linestyle=':', linewidth=0.5)
        #Linea de tendencia
        x = np.array([0,1,2,3,4,5,6,7,8,9,10,11])
        y = count[0]
        self.slope, self.intercept, r_value, p_value, std_err = linregress(x, y)
        self.MplWidget.canvas.ax.plot(x, self.intercept + self.slope*x, '--', label='Linea de tendencia', color='orange')
        self.MplWidget.canvas.ax.legend(loc=1, ncol=3, bbox_to_anchor=(0.75, 1))
        
        self.MplWidget.canvas.draw()

        self.cargarEstadisticos(count[0])

        #== EVENTOS == #
        self.agn.valueChanged.connect(self.AgnoExtrapolar)
        self.agno.valueChanged.connect(self.FiltrarPorAgno)
    
    def AgnoExtrapolar(self):
        monthE = self.agn.value()*12
        est = self.intercept + self.slope*monthE
        self.number.setText(str(est))

    def cargarEstadisticos(self, data):
        #Arriendos por mes 
        prom = np.mean(data)
        self.a.setText(str(prom) + ' arriendos por mes')

        #Meses mas visitado por año
        mesmax = self.months[np.argmax(data)]
        self.b.setText(mesmax)
        
        #Porcentaje del mes mas visitado respecto a los demás.
        total = np.sum(data)
        mesP = np.max(data)
        perc = mesP/total * 100
        self.d.setText(str(perc) + '%')

        #3 meses mas visitados por el año seleccionado
        argsmax = []
        for i in range(3):
            argmax = np.argmax(data)
            argsmax.append(argmax)
            data = np.delete(data, argmax)
        text = self.months[argsmax[0]] + ', ' + self.months[argsmax[1]] + ' y ' + self.months[argsmax[2]]
        self.c.setText(text)



    def FiltrarPorAgno(self):
        self.agn.setValue(0)
        self.number.setText('')

        agno = self.agno.value()
        y1 = agno
        y2 = agno

        r = requests.get('{}/reservas_mes/{}/{}'.format(host, y1, y2))
        r = r.json()['data']
        count = [[0 for x in range(1, 13)] for i in range(y1, y2+1)]
        for d in r:
            count[d['year']-y1][d['month']-1] = d['count']

        self.MplWidget.canvas.ax.clear()
        self.MplWidget.canvas.ax.set_title('Arrendatarios por mes')
        self.MplWidget.canvas.ax.bar(x=range(12),
                                    height=count[0])
        self.MplWidget.canvas.ax.set_ylabel('N° de arrendatarios por mes')
        self.MplWidget.canvas.ax.set_xticks(range(12))
        self.MplWidget.canvas.ax.set_xticklabels(self.months, rotation=25)
        self.MplWidget.canvas.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.MplWidget.canvas.ax.set_ylim(0)
        
        #Linea de tendencia
        x = np.array([0,1,2,3,4,5,6,7,8,9,10,11])
        y = count[0]
        self.slope, self.intercept, r_value, p_value, std_err = linregress(x, y)
        self.MplWidget.canvas.ax.plot(x, self.intercept + self.slope*x, '--', label='Linea de tendencia',  color='orange')
        self.MplWidget.canvas.ax.legend(loc=1, ncol=3, bbox_to_anchor=(0.75, 1))
        self.MplWidget.canvas.ax.grid(color="green", which="major", axis='both', linestyle=':', linewidth=0.5)
        self.MplWidget.canvas.draw()


        self.cargarEstadisticos(count[0])

class Clientes_region(base_3, form_3):
    def __init__(self, *args, **kwargs):
        super(base_3, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.regiones = ["Tarapaca", "Antofagasta", "Atacama",
                "Coquimbo", "Valparaiso", "OHiggins",
                "Maule", "Biobio", "Araucania", "Lagos",
                "Campo", "Magallanes", "Metropolitana",
                "Rios", "Arica"]
        
        resreg = [0] * 15            
        r = requests.get('{}/reservas_region'.format(host))
        r = r.json()['data']

        for d in r:
            try:
                resreg[self.regiones.index(d["Procedencia"])] = d["count"]
            except ValueError:
                pass
            
        self.MplRegion.canvas.ax.clear()
        self.MplRegion.canvas.ax.set_title('Arrendatarios por región')
        self.MplRegion.canvas.ax.bar(x=range(15), height=resreg, width=0.8,
                    bottom=0, align='center', color=None, linewidth=None, xerr=None, yerr=None)
        self.MplRegion.canvas.ax.set_ylabel('Clientes por región')
        self.MplRegion.canvas.ax.set_xticks(range(15))
        self.MplRegion.canvas.ax.set_xticklabels(['I', 'II', 'III', 'IV', 'V', 'VI',
                                    'VII', 'VIII', 'IX', 'X', 'XI',
                                    'XII', 'XIII', 'XIV', 'XV'])
        self.MplRegion.canvas.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.MplRegion.canvas.ax.set_ylim(0)

        #Linea de tendencia
        x = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
        y = resreg
        self.slope, self.intercept, r_value, p_value, std_err = linregress(x, y)
        self.MplRegion.canvas.ax.plot(x, self.intercept + self.slope*x, '--', label='Linea de tendencia', color='orange')
        self.MplRegion.canvas.ax.legend(loc=1, ncol=3, bbox_to_anchor=(0.75, 1))

        self.MplRegion.canvas.ax.grid(color="green", which="major", axis='both', linestyle=':', linewidth=0.5)
        self.MplRegion.canvas.draw()

        self.cargarEstadisticos(resreg)
        
        #== EVENTOS == #
        self.agno.valueChanged.connect(self.FiltrarPorAgno)

    def cargarEstadisticos(self, data):
        
        # Region que se recibe mas visitas
        argmax = np.argmax(data)
        region =  self.regiones[argmax]
        self.a.setText(region)

        # Porcentaje de la region que mas nos visitan conrespecto a las demás
        total = np.sum(data)
        regionP = np.max(data)
        perc = regionP/total * 100
        self.c.setText(str(perc) + '%')

        # Las 3 regiones mas visitadas       
        argsmax = []
        for i in range(3):
            argmax = np.argmax(data)
            argsmax.append(argmax)
            data = np.delete(data, argmax)
        text = self.regiones[argsmax[0]] + ', ' + self.regiones[argsmax[1]] + ' y ' + self.regiones[argsmax[2]]
        self.b.setText(text)
    
    def FiltrarPorAgno(self):

        agno = self.agno.value()
        y1 = agno
        y2 = agno
        resreg = [0] * 15
        r = requests.get('{}/reservas_region_agno/{}/{}'.format(host, y1, y2))
        r = r.json()['data']
        for d in r:
            try:
                resreg[self.regiones.index(d["Procedencia"])] = d["count"]
            except ValueError:
                pass
        
        self.MplRegion.canvas.ax.clear()
        self.MplRegion.canvas.ax.set_title('Arrendatarios por region')
        self.MplRegion.canvas.ax.bar(x=range(15), height=resreg, width=0.8,
                    bottom=0, align='center', color=None, linewidth=None, xerr=None, yerr=None)
        self.MplRegion.canvas.ax.set_ylabel('Clientes por región')
        self.MplRegion.canvas.ax.set_xticks(range(15))
        self.MplRegion.canvas.ax.set_xticklabels(['I', 'II', 'III', 'IV', 'V', 'VI',
                                    'VII', 'VIII', 'IX', 'X', 'XI',
                                    'XII', 'XIII', 'XIV', 'XV'])
        self.MplRegion.canvas.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.MplRegion.canvas.ax.set_ylim(0)

        x = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
        y = resreg
        self.slope, self.intercept, r_value, p_value, std_err = linregress(x, y)
        self.MplRegion.canvas.ax.plot(x, self.intercept + self.slope*x, '--', label='Linea de tendencia', color='orange')
        self.MplRegion.canvas.ax.legend(loc=1, ncol=3, bbox_to_anchor=(0.75, 1))

        self.MplRegion.canvas.ax.grid(color="green", which="major", axis='both', linestyle=':', linewidth=0.5)
        self.MplRegion.canvas.draw()

        self.cargarEstadisticos(resreg)

class Sugrencias(base_4, form_4):
    def __init__(self, *args, **kwargs):
        super(base_4, self).__init__(*args, **kwargs)
        self.setupUi(self)
        r = requests.get('{}/sugerencias'.format(host))
        r = r.json()['data']
        sugs = [d["Sugerencia"] for d in r]
        #sugs tiene las sugerencias como lista de strings  
        self.tableSuger.setRowCount(0)
        for row, sug in enumerate(sugs):   
            self.tableSuger.insertRow(row)
            self.tableSuger.setItem(row, 0, QTableWidgetItem(sug))
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.exit(app.exec_())
    