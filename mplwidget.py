# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import*
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class MplWidget(QWidget):

    def __init__(self, parent=None):

        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())
        self.canvas.ax = self.canvas.figure.add_subplot(111)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.ax.bar(x=range(12), height=[20, 10, 5, 3, 2, 1, 2,
                                                3, 4, 5, 6, 2],
                           width=0.8, bottom=0, align='center',
                           color=None, edgecolor=None, linewidth=None,
                           xerr=None, yerr=None)
        self.canvas.ax.set_ylabel('Infectados totales a la fecha')
        self.canvas.ax.set_xticks(range(12))
        self.canvas.ax.set_xticklabels(['Enero', 'Febrero', 'Marzo',
                                        'Abril', 'Mayo', 'Junio',
                                        'Julio', 'Agosto', 'Septiembre',
                                        'Octubre', 'Noviembre',
                                        'Diciembre'])

        self.setLayout(vertical_layout)
