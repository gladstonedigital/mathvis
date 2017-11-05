#!/usr/bin/env python3

import numpy
import random
import sys
from fractions import Fraction
from time import sleep
from numpy import linspace

from polynomials import Binomial
from polynomials import Trinomial

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QIcon, QFont
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
        self.text_a.move(510,50)
        self.text_a.resize(40,20)
        self.text_a.setText("1")
        self.label_a = QLabel(self)
        self.label_a.move(555,45)
        self.label_a.setText("x² +")
        self.label_a.setFont(QFont("Roboto", 16))

        self.text_b = QLineEdit(self)
        self.text_b.move(600,50)
        self.text_b.resize(40,20)
        self.text_b.setText("0")
        self.label_b = QLabel(self)
        self.label_b.move(645,45)
        self.label_b.setText("x +")
        self.label_b.setFont(QFont("Roboto", 16))

        self.text_c = QLineEdit(self)
        self.text_c.move(680,50)
        self.text_c.resize(40,20)
        self.text_c.setText("0")

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

        for p in numpy.arange(Fraction(-10), Fraction(11), Fraction(1)):
            f.factor(p)

        self.plotcanvas.axes.clear()

        low = -10
        high = 10
        x = linspace(low, high, (high - low) * 10)

        self.plotcanvas.plot(x, f.evaluate(x), 'f(x) = ' + str(f))
        for pair in f.factor_pairs.values():
            for line in pair.binomials:
                self.plotcanvas.plot(x, line.evaluate(x), linewidth=0.4)

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width,height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.plot([i - 12 for i in range(25)], [0 for i in range(25)], linewidth=0.5, color='black')
        self.axes.plot([0 for i in range(25)], [i - 12 for i in range(25)], linewidth=0.5, color='black')

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, x_data, y_data, title=None, linewidth=1.0):
        self.axes.plot(x_data, y_data, linewidth=linewidth)
        if title != None:
            self.axes.set_title(title)
        self.draw()

def main():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

