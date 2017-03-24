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
#fnames = QtWidgets.QFileDialog.getOpenFileNames(
#        filter='HDF5 Image (*.hdf5)')
#print(fnames)
fs = []
a = np.fromfile('sampletemperature.log')
for i, T in enumerate(range(4, 48, 4)):
    f = h5py.File(('images/typeiipolarization/22_03_%2.2fk_tempdep.hdf5' % (T)).replace('.', ',', 1), 'r')
    fs.append(f)

    
#plt.plot()