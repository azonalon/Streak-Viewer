# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
import matplotlib.pyplot as plt
import numpy as np

class PIDSpinboxes(QtWidgets.QWidget):
    def __init__(self, setP, setI, setD, setPoint, p0=0, i0=0, d0=0, sp0=0, **kwargs):
        super().__init__()
        self.boxes = [pg.SpinBox(value=0, **kwargs) for _ in range(4)]
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.lambdas= []
        for i in range(4):
            x0 = [p0, i0, d0, sp0][i]
            setter = [setP, setI, setD, setPoint][i]
            title = ['Prop', 'Int', 'Dev', 'Set'][i]
#            box = self.boxes[i]
            self.lambdas.append(lambda sb: setter(sb.value()))
            self.boxes[i].sigValueChanged.connect(self.lambdas[i])
            setter(x0)
            self.boxes[i].setValue(x0)
            self.layout.addWidget(QtWidgets.QLabel(title), 0, i)
            self.layout.addWidget(self.boxes[i], 1, i)
            
            
            
            
if __name__ == '__main__':
    pg.mkQApp()
    f = lambda x: x
    boxes = PIDSpinboxes(f, f, f, f)
    boxes.show()
    


