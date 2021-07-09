import json
import requests
import sys, re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5 import QtCore as qtc
from dateutil import parser as date_parser
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)


uifile_1 = 'UIfiles/menu.ui'
form_1, base_1 = uic.loadUiType(uifile_1)

uifile_2 = 'UIfiles/grafico_por_mes.ui'
form_2, base_2 = uic.loadUiType(uifile_2)

class Menu(base_1, form_1):
    def __init__(self,*args, **kwargs):
        super(base_1, self).__init__(*args, **kwargs)
        self.setupUi(self)  

        #Eventos 
        self.clientesMes.clicked.connect(self.ClientesMes)
        self.clientesRegion.clicked.connect(self.ClientesRegion)

    
    def ClientesMes(self):
        self.cm= Clientes_mes()
        self.cm.show()
    
    def ClientesRegion(self):
        self.cr = Clientes_region()
        self.cr.show()

class Clientes_mes(base_2, form_2):
    def __init__(self,*args, **kwargs):
        super(base_2, self).__init__(*args, **kwargs)
        self.setupUi(self)

        
        #Example
        self.MplWidget.canvas.ax.bar(x=range(12), height=[20, 10, 5, 3, 2, 1, 2, 3, 4, 5, 6, 2], width=0.8, bottom=0, align='center', color=None, edgecolor=None, linewidth=None, xerr=None, yerr=None)
        self.MplWidget.canvas.ax.set_ylabel('N° de clientes por mes')
        self.MplWidget.canvas.ax.set_xticks(range(12))
        self.MplWidget.canvas.ax.set_xticklabels(['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'])

        #self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

        #Eventos
        self.agno.valueChanged.connect(self.FiltrarPorAgno)
   
    def FiltrarPorAgno(self):
        agno = self.agno.value()

        #Consulta filtrar po año

class Clientes_region(FigureCanvas):
    def __init__(self):

        fig, self.ax = plt.subplots(figsize=(12 , 6), tight_layout=True, facecolor='w')
        super().__init__(fig)

        #Example
        self.ax.bar(x=range(15), height=[20, 10, 5, 3, 4, 2, 6, 2, 1, 2, 6, 3, 8, 2, 1], width=0.8, bottom=0, align='center', color=None, edgecolor=None, linewidth=None, xerr=None, yerr=None)
        self.ax.set_ylabel('Clientes por región')
        self.ax.set_xticks(range(15))
        self.ax.set_xticklabels(['I', 'II', 'III','IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV'])

        #Consulta clientes por region

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.exit(app.exec_())   






