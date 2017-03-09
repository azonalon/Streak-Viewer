# -*- coding: utf-8 -*-

#import os
import sys
#import numpy as np
from PyQt5 import QtWidgets
import pyqtgraph as pg
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from pyqtgraph import QtCore
Qt = QtCore.Qt
#from pyqtgraph.Qt import QtWidgets

#from scipy.optimize import curve_fit
#from PyQt5.QtWidgets import QMessageBox

from uidesign.mainWindow import Ui_MainWindow
def makeColorMap():
    pos = np.array([0., 1., 0.5, 0.25, 0.75])
    color = np.array([[0,255,255,255], [255,255,0,255], [0,0,0,255], (0, 0, 255, 255), (255, 0, 0, 255)], dtype=np.ubyte)
    return pg.ColorMap(pos, color)
cmap = makeColorMap()
sourceDataFlags = Qt.ItemIsSelectable | Qt.ItemIsUserCheckable \
    | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled #| Qt.ItemIsDropEnabled
import time
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
        
    
bytesInImage = 1024*1024*2   

class CalcTreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, *args, kind='data', img=None, info=None, 
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
        f = open(fname, 'wb')
        if f.write(self.img.tobytes()) == bytesInImage:
            print("Wrote whole image...")
        else:
            print("warning, data has inappropriate dimensions")
        f.write(bytes(str(self.info), 'utf-8'))
        
        
    def loadImageFromFile(self, fname):
        f = open(fname, 'rb')
        tab = f.read(bytesInImage)
        if len(tab) == bytesInImage:
            self.img = np.fromstring(tab, dtype='<u2')
            self.img.shape = (1024, 1024)
            try:
                self.info = eval(str(f.read()))
            except:
                print(fname + ': could not parse metadata')
#                pass
        
    
def polarization(imgs):
    n = int(np.floor(len(imgs)/2.))
    print('polarization n', n)
    if n >= 1:
        a = np.sum(imgs[0:2*n:2], 0) - np.sum(imgs[1:2*n:2], 0)
        b = np.sum(imgs, 0)
#        print(a/b)
        return a/b

def imgSum(imgs):
    return np.sum(imgs, axis=0)/len(imgs)
        
class ImageViewer(QtWidgets.QMainWindow):
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        super().__init__()
        self.setupUi()
        
    def setupUi(self):
        self.dtw = pg.DataTreeWidget()
        
        self.form = Ui_MainWindow()
        self.form.setupUi(self)
        self.form.area_info.setWidget(self.dtw)
        self.imgview = pg.ImageView()
        self.form.tabWidget.addTab(self.imgview, "Image")
#        self.form.tabWidget.addTab(self.imgview, "Monitor")

        self.treeImages = CalcTreeWidget()
        self.tabWidgets = [self.imgview]
        self.form.areaCalcTreeWidget.setWidget(self.treeImages)
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
                self.imgview.autoLevels
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
        
    def addImage(self, data, info, filename='New'):
        it = CalcTreeWidgetItem(self.newItems,
                                [filename, info['time']],
                                img=data, info=info,
                                kind = 'data'
                                       )
        it.setFlags(sourceDataFlags)
        self.changeActiveImage(it, None)
        
    def addTabWidget(self, widget, name):
        self.form.tabWidget.addTab(widget, name)
        self.tabWidgets.append(widget)
        
    def loadImageFromFile(self):
        fname = QtWidgets.QFileDialog.getOpenFileName()[0]
        if fname == "":
            return
        CalcTreeWidgetItem(self.fromFileItems, fromfile = fname, kind='data')
    def saveImageToFile(self, fname=None):
        item = self.treeImages.currentItem()
#        print(f)
        print('fname :', fname)
        if item == None:
            return
#        if fname == None:
        fname = QtWidgets.QFileDialog.getSaveFileName()[0]
 
        
        item.saveImageToFile(fname)
        
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
            print('hi')
            child.closeEvent(event)
        event.accept()
        
    def exec(self):
        self.show()
        self.app.exec_()

def AutoLevel(data):
    data = np.clip(data, 1000, 10000)
    hist, bins = np.histogram(data, bins=np.arange(0, 2**15))
    bins = bins[:-1]
    hist = np.sqrt(hist * np.roll(hist, 10))
    m = np.max(hist)/10
    print(np.argmin(hist[hist>m]), np.argmax(hist))
    plt.plot(bins, hist)
    
        

fit = lambda x, a, b, x0: a*np.exp(b*(x-x0)**2)
# from aqt.qt import debug; debug()
#%%
if __name__=='__main__':
    import subprocess as sp
    import excepthook
    sp.run('pyuic5 uidesign/mainWindow.ui -o uidesign/mainWindow.py', shell=True)
    from hamamatsu import HamamatsuFile
    imv  = ImageViewer()
    imv.setupUi()
    i=0
    imgs = []
    for f in [p.as_posix() for p in Path('.').glob('sample_images/*.img')]:
        sample = HamamatsuFile(f)
        sample.header['time'] = sample.header['Application']['Time']
        sample.header['exposure'] = sample.header['Acquisition']['ExposureTime']
        sample.header['optical orientation'] = '+' if i % 2 == 0 else '-' 
        imv.addImage(sample.data, sample.header, filename = f)
        imgs.append(sample.data)
        i += 1
    imv.newItems.child(0).saveImageToFile('testimg.img')
    node = CalcTreeWidgetItem(imv.fromFileItems, fromfile = 'testimg.img')
#    print(polarization(imgs))
    imv.exec()