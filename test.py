# -*- coding: utf-8 -*-
"""
Demonstrates a way to put multiple axes around a single plot. 

(This will eventually become a built-in feature of PlotItem)

"""
#import initExample ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from pathlib import Path
pg.mkQApp()
import os
import h5py
import time
#fnames = QtWidgets.QFileDialog.getOpenFileNames(
#        filter='HDF5 Image (*.hdf5)')
#print(fnames)

class A(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        
    def run(self):
        while True:
            print('im sleeping')
            time.sleep(100)
            
a = A()
a.start()
time.sleep(1)
a.terminate()