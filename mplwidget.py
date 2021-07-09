# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import*

from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure
import matplotlib.pyplot as plt

    
class MplWidget(QWidget):
    
    def __init__(self, parent = None):

        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())
        self.canvas.ax = self.canvas.figure.add_subplot(111)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)        
        self.setLayout(vertical_layout)

