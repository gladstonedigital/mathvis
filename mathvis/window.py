#!/usr/bin/env python3

import random
import sys
from time import sleep
from numpy import linspace

from polynomials import Binomial
from polynomials import Trinomial

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'mathvis'
        self.left=10
        self.top=10
        self.width=800
        self.height=420
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowFlags(Qt.Dialog)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.plotcanvas = PlotCanvas(self, width=5, height=4)
        self.plotcanvas.move(0,0)

        self.text_a = QLineEdit(self)
        self.text_a.move(520,50)
        self.text_a.resize(40,20)

        self.text_b = QLineEdit(self)
        self.text_b.move(600,50)
        self.text_b.resize(40,20)

        self.text_c = QLineEdit(self)
        self.text_c.move(680,50)
        self.text_c.resize(40,20)

        button_update = QPushButton('Update', self)
        button_update.setToolTip('example buttonboi')
        button_update.move(700,360)
        button_update.resize(80,30)
        button_update.clicked.connect(self.update)

        self.show()

    @pyqtSlot()
    def update(self):
        a = self.text_a.text()
        b = self.text_b.text()
        c = self.text_c.text()
        f = Trinomial(a, b, c)
        x = linspace(-8, 8, (8 - -8) * 10)
        y = f.evaluate(x)
        self.plotcanvas.axes.clear()
        self.plotcanvas.plot(x, y, 'f(x) = ' + str(f))
        print(f)

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width,height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot([i for i in range(25)], [random.random() for i in range(25)])

    def plot(self, x_data, y_data, title='Plot'):
        ax = self.figure.add_subplot(111)
        ax.plot(x_data, y_data)
        ax.set_title(title)
        self.draw()

def main():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

