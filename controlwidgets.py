# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
import matplotlib.pyplot as plt
import numpy as np

#def f(setter, sb):
#    setter(sb.value())
def verticalSpacer():
    return QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
def horizontalSpacer():
    return QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
class PIDSpinboxes(QtWidgets.QWidget):
    def __init__(self, setP, setI, setD, setPoint, p0=0, i0=0, d0=0, sp0=0, **kwargs):
        super().__init__()
        self.boxes = [QtWidgets.QDoubleSpinBox(value=0, **kwargs, parent=self) for _ in range(4)]
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        for i in range(4):
            x0 = [p0, i0, d0, sp0][i]
            setter = [setP, setI, setD, setPoint][i]
            title = ['Prop', 'Int', 'Dev', 'Set'][i]
            box = self.boxes[i]
            setter(x0)
            self.boxes[i].setValue(x0)
            self.layout.addWidget(QtWidgets.QLabel(title), 0, i)
            self.layout.addWidget(self.boxes[i], 1, i)
            self.layout.addItem(verticalSpacer(), 2, i)
            box.valueChanged.connect(setter)
    def sizeHint(self):
        return QtCore.QSize(10, 10)
    
class ControlWidget(QtWidgets.QGroupBox):
    def __init__(self, descriptor, title):
        super().__init__(title)
        self.setLayout(QtWidgets.QGridLayout())
        if type(descriptor) is tuple:
            descriptor = [descriptor]
        i=0
        c=0
        for row in descriptor:
            if type(row) is tuple:
                row = [row]
            j=0
            for item in row:
                if item[0] == 'float set':
                    self.layout().addLayout(self.floatSetter(*item[1:]), i, j)
                else:
                    raise Exception('Unknown Descriptor: ' + item[0])
                j += 1
                c=max(j, c)
            self.layout().addItem(horizontalSpacer(), i, j)
            i += 1
        for k in range(c):
            print(k)
            self.layout().addItem(verticalSpacer(), i, k)
    def floatSetter(self, f, title, bounds=None, f0=0, decimals=2):
        layout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel(title)
        layout.addWidget(self.label, 0)
        sb = QtWidgets.QDoubleSpinBox(parent=self)
        if type(bounds) is tuple:
            sb.setRange(*bounds)
#        if f0 is not None:
        sb.setValue(f0)
        sb.setDecimals(decimals)
            
        sb.valueChanged.connect(f)
        layout.addWidget(sb)
        return layout
                
        
            
if __name__ == '__main__':
    import excepthook
    pg.mkQApp()
#    fs = [lambda x, i=i: print('f' + str(i) + ' ' + str(x)) for i in range(1, 5)]
#    boxes = PIDSpinboxes(*fs, p0=1, i0=2, d0=3, sp0=4)
#    boxes.show()
#    
    cw = ControlWidget([[('float set', lambda x: print(x), 'Print!', (0, 10), 4),
                        ('float set', lambda x: print(x), 'Print!', (0, 10), 4),
                        ('float set', lambda x: print(x), 'Print!', (0, 10), 4)],
    [('float set', lambda x: print(x), 'Print!', (0, 10), 4),
                        ('float set', lambda x: print(x), 'Print!', (0, 10), 4),
                        ('float set', lambda x: print(x), 'Print!', (0, 10), 4)]], 'Control It Man!')
    cw.show()
    


