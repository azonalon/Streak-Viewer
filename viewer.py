# -*- coding: utf-8 -*-

#import os
import sys
#import numpy as np
from PyQt5 import QtWidgets, QtGui
import pyqtgraph as pg
import matplotlib.pyplot as plt
import numpy as np
from pyqtgraph import QtCore
Qt = QtCore.Qt
import h5py
from pathlib import Path
import importlib
#from pyqtgraph.Qt import QtWidgets

#from scipy.optimize import curve_fit
#from PyQt5.QtWidgets import QMessageBox

from .uidesign.mainWindow import Ui_MainWindow
def makeColorMap():
    pos = np.array([0., 1., 0.5, 0.25, 0.75])
    color = np.array([[0,255,255,255], [255,255,0,255], [0,0,0,255], (0, 0, 255, 255), (255, 0, 0, 255)], dtype=np.ubyte)
    return pg.ColorMap(pos, color)
cmap = makeColorMap()
sourceDataFlags = Qt.ItemIsSelectable | Qt.ItemIsUserCheckable \
    | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled #| Qt.ItemIsDropEnabled
import time
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#%%
def unrecurseDictionary(sourceDict, targetDict={}, parentKey=''):
    for key, value in sourceDict.items():
        key = parentKey + key
        if type(value) != dict:
            targetDict[key] = value
        else:
            unrecurseDictionary(value, targetDict, key + '.')
    return targetDict

#def recurseDictionary()

print('hi')     
        
#%%
class PIDSpinboxes(QtWidgets.QWidget):
    def __init__(self, setP, setI, setD, p0=0, i0=0, d0=0, **kwargs):
        super().__init__()
        self.p, self.i, self.d = [pg.SpinBox(value=0, **kwargs) for _ in range(3)]
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.p)
        self.layout.addWidget(self.i)
        self.layout.addWidget(self.d)
        self.p.setValue(p0)
        self.i.setValue(i0)
        self.d.setValue(d0)
        setP(p0)
        setI(i0)
        setD(d0)
        
        self.p.sigValueChanged.connect(lambda sb: setP(sb.value()))
        self.i.sigValueChanged.connect(lambda sb: setI(sb.value()))
        self.d.sigValueChanged.connect(lambda sb: setD(sb.value()))
#%%
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class CalcTreeWidget(QtWidgets.QTreeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setDragEnabled(True)
        self.setDragDropOverwriteMode(False)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)
        self.setItemsExpandable(True)
        self.setAnimated(True)
        self.setObjectName("tree_images")
        self.treeHeaderItem = CalcTreeWidgetItem(['Filename', 'Time'], kind='folder')
        self.setHeaderItem(self.treeHeaderItem)
    def addFunctionNode(self, function, description, argumentCount=-1,
                        parentNode=None):
        if parentNode is None:
            parentNode = self.treeHeaderItem
        CalcTreeWidgetItem(self, ['Operation', description],
                                kind='function', function=function)
    def recalc(self):
        for i in range(self.topLevelItemCount()):
            self.topLevelItem(i).recalc()
        
    
bytesInImage = 1024*1024*4   

class CalcTreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, *args, kind='data', img=None, info={}, 
                 function=None, fromfile=None, **kwargs):
        self.kind = kind
        self.img = img 
        self.info = info
        self.function = function
        if fromfile is not None:
            self.loadImageFromFile(fromfile)
        super().__init__(*args, **kwargs)
        
        
    def recalc(self):
        if self.kind == 'data':
            return self.img
        elif self.kind == 'folder':
            for i in range(self.childCount()):
                self.child(i).recalc()
        elif self.kind == 'function':
            arg = [self.child(i).recalc() for i in range(self.childCount())]
            arg = [x for x in arg if x is not None]
            self.img = self.function(arg)
#            print(self.img)
            return self.img
        
    [].index
    def saveImageToFile(self, fname):
        fname = Path(fname).with_suffix('.hdf5').as_posix()
        f = h5py.File(fname, 'w')
        f.create_dataset('img', data=self.img)
        for key, value in self.info.items():
            f.attrs[key] = value
        f.close()
        
    def loadImageFromFile(self, fname):
        f = h5py.File(fname, 'r')
        self.img = f['img'][...]
        self.info = dict(f.attrs)
        f.close()
        
    
def polarization(imgs):
    n = int(np.floor(len(imgs)/2.))
    print('polarization n', n)
    if n >= 1:
        a = np.sum(imgs[0:2*n:2], 0) - np.sum(imgs[1:2*n:2], 0)
        b = np.sum(imgs, 0)
#        print(a/b)
        return a/b

class Console(QtWidgets.QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setFont(QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont))
    def write(self, msg):
        self.insertPlainText('>>> ')
        msg = msg.split('\n')
        self.insertPlainText(msg[0] + '\n')
        
        for l in msg[1:]:
            self.insertPlainText('    ' + l + '\n')
    
def imgSum(imgs):
    return np.sum(imgs, axis=0)/len(imgs)
        
class ImageViewer(QtWidgets.QMainWindow):
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        super().__init__()
        self.setupUi()
        
        
    def setupUi(self):
        self.dockWidgets = []
        self.dtw = pg.DataTreeWidget()
        
        self.form = Ui_MainWindow()
        self.form.setupUi(self)
        self.form.layoutImageInfo.addWidget(self.dtw)
        self.imgview = pg.ImageView()
        self.form.tabWidget.addTab(self.imgview, "Image")
#        self.form.tabWidget.addTab(self.imgview, "Monitor")

        self.treeImages = CalcTreeWidget()
        self.tabWidgets = [self.imgview]
        self.measurementObject = None
        self.form.layoutCalcTreeWidget.addWidget(self.treeImages)
        self.newItems = CalcTreeWidgetItem(
                self.treeImages, ['New', ''], kind='folder')
        
        self.fromFileItems = CalcTreeWidgetItem(
                self.treeImages, ['From File', 'f'], kind='folder')
        self.treeImages.currentItemChanged.connect(self.changeActiveImage)
        self.form.actionRecalc.triggered.connect(
                self.treeImages.recalc
        )
        self.form.actionAddSumNode.triggered.connect(
                lambda: self.treeImages.addFunctionNode(
                        lambda a: np.sum(a, 0)/len(a), 'sum')
                )
        self.form.actionAddPolarizationNode.triggered.connect(
        lambda: self.treeImages.addFunctionNode(
                polarization, 'polarization')
        )
        self.form.actionAutoLevel.triggered.connect(
                self.autoLevel
                )
        def sleepAndRaise():
            time.sleep(5)
            raise Exception
        
        self.form.actionSleep.triggered.connect(
                sleepAndRaise
        )
        self.form.actionAdd_File.triggered.connect(self.loadImageFromFile)
        self.form.actionSave.triggered.connect(self.saveImageToFile)
        self.imgview.setColorMap(cmap)
        
        self.console = Console()
        self.addTabWidget(self.console, 'Measurement')
   
    def addImage(self, data, info, name='New', autoLevel = False):
        it = CalcTreeWidgetItem(self.newItems,
                                [name, info['time']],
                                img=data, info=info,
                                kind = 'data'
                                       )
        it.setFlags(sourceDataFlags)
#        if autoLevel:
#            self.autoLevel(it)
        self.changeActiveImage(it, None)
    def startMeasurement(self):
        if self.measurementObject != None and self.measurementObject.isRunning():
            print('measurement is running')
            return
        try:
            self.measurementObject = self.measurementObjectCreator()
        except Exception as e:
            print('Could not create measurement object:\n', e)
            return
        self.form.actionStartMeasurement.setEnabled(False)
        self.form.actionStartMeasurement.setText('Running...')

        self.measurementObject.finished.connect(
                lambda: self.form.actionStartMeasurement.setEnabled(True))
        self.measurementObject.finished.connect(
                lambda: self.form.actionStartMeasurement.setText('Start'))
        self.measurementObject.finished.connect(lambda: self.console.write('~' * 80 + "\nMeasurement exit!\n" + '~' *80 ))
        self.measurementObject.signalMessage.connect(self.console.write)
        
            
        self.console.write('~' * 80 + '\nStarting new measurement...\n' + '~' * 80)
        self.measurementObject.start()
        
    def connectMeasurement(self, measurementObjectCreator):
        self.measurementObjectCreator = measurementObjectCreator
        self.form.actionStartMeasurement.triggered.connect(self.startMeasurement)
        self.form.actionStartMeasurement.setEnabled(True)

    def addTabWidget(self, widget, name):
        self.form.tabWidget.addTab(widget, name)
        self.tabWidgets.append(widget)
        
    def addMovableWidget(self, widget):
        dw = QtWidgets.QDockWidget(self)
        self.dockWidgets.append(dw)
        dw.setWidget(widget)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), dw)
        
    def loadImageFromFile(self):
        fname = QtWidgets.QFileDialog.getOpenFileName()[0]
        if fname == "":
            return
        if Path(fname).suffix != '.hdf5':
            print(fname + ' is not a hdf5 file')
            return
        CalcTreeWidgetItem(
                self.fromFileItems,
                [Path(fname).stem], 
                fromfile = fname, kind='data')
    def saveImageToFile(self, fname=None):
        item = self.treeImages.currentItem()
#        print(f)
        print('fname :', fname)
        if item == None:
            return
#        if fname == None:
        fname = QtWidgets.QFileDialog.getSaveFileName()[0]
 
        
        item.saveImageToFile(fname)
    def autoLevel(self):
        item = self.treeImages.currentItem()
        print(item)
        if item is None or item.img == None:
            return
        data = item.img
        hist, bins = np.histogram(data, bins=2**16)
        bins = bins[:-1]
        hist = (hist * np.roll(hist, 10) * np.roll(hist, 60))**1/3
    #    m = np.max(hist)/1000
        print(hist)
        minmax = np.argwhere(hist>0).flatten()[[0, -1]]
        print(minmax)
        minmax = bins[minmax].flatten()
        print(minmax)
        self.imgview.setLevels(*minmax)
    
        
    def changeActiveImage(self, newItem, lastItem):
#        print('item ' +  newItem.data(1, 0) + ' activated')
        if newItem is not None and newItem.img is not None:
            (data, info) = newItem.img, newItem.info
            self.dtw.setData(info)
            self.imgview.setImage(data, autoLevels=False)
#        print('Item Count', newItem.childCount())
    def closeEvent(self, event):
        print('closing main window')
        for child in self.tabWidgets:
            child.closeEvent(event)
        event.accept()
        
    def exec(self):
        self.show()
        self.app.exec_()


        

fit = lambda x, a, b, x0: a*np.exp(b*(x-x0)**2)
# from aqt.qt import debug; debug()
#%%
if __name__=='__main__':
    import subprocess as sp
    import excepthook
    from pathlib import Path
    sp.run('pyuic5 uidesign/mainWindow.ui -o uidesign/mainWindow.py', shell=True)
    from hamamatsu import HamamatsuFile
    imv  = ImageViewer()
    i=0
    imgs = []
#    win = pg.GraphicsWindow()
#    p = win.addPlot()
    for f in [p.as_posix() for p in Path('.').glob('sample_images/*.img')]:
        sample = HamamatsuFile(f)
        sample.header['time'] = sample.header['Application']['Time']
        sample.header['exposure'] = sample.header['Acquisition']['ExposureTime']
        sample.header['optical orientation'] = '+' if i % 2 == 0 else '-' 
        sample.header = unrecurseDictionary(sample.header)
        imv.addImage(sample.data, sample.header, name = f)
        imgs.append(sample.data)
        i += 1
#    print(unrecurseDictionary(sample.header))
    imv.newItems.child(0).saveImageToFile('testimg')
    node = CalcTreeWidgetItem(imv.fromFileItems, ['testimg'], fromfile = 'testimg.hdf5')
#    print(polarization(imgs))
    imv.exec()