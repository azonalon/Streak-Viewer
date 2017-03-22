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
#fnames = QtWidgets.QFileDialog.getOpenFileNames(
#        filter='HDF5 Image (*.hdf5)')
#print(fnames)
fname = 'images/testfolder/test.bla'
fname = fname.lower()
fname = Path(fname).with_suffix('.hdf5').as_posix()
directory = os.path.dirname(fname)
if not os.path.exists(directory):
    os.makedirs(directory)
    
def testprint(*args):
    print(' '.join([str(arg) for arg in args]))
testprint('haha', 'lulu')