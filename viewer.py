# -*- coding: utf-8 -*-
#__package__ = 'StreakViewer'
import os
import sys
#import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
import matplotlib.pyplot as plt
import numpy as np
import StreakViewer.excepthook as exc
#from pyqtgraph import QtCore
Qt = QtCore.Qt
import h5py
from pathlib import Path
if __name__ != '__main__':
    from .uidesign.mainWindow import Ui_MainWindow
    from .hamamatsu import HamamatsuFile
else:
    from uidesign.mainWindow import Ui_MainWindow
    from hamamatsu import HamamatsuFile
    

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
#        fname = fname.lower()
        fname = Path(fname).with_suffix('.hdf5').as_posix()
        directory = os.path.dirname(fname)
        if not os.path.exists(directory):
            print('creating new directory:', directory)
            os.makedirs(directory)
        try:
            f = h5py.File(fname, 'w')
            f.create_dataset('img', data=self.img)
            for key, value in self.info.items():
                print(key, value)
                f.attrs[key] = value
            f.close()
        except Exception as e:
            print('error saving file')
        
    def loadImageFromFile(self, fname):
        fname = Path(fname).with_suffix('.hdf5').as_posix()
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
        return a.astype('f8')/b.astype('f8')

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
        self.addMovableWidget(self.dtw, 'Image Info')
        self.imgview = pg.ImageView()
        self.form.tabWidget.addTab(self.imgview, "Image")
#        self.form.tabWidget.addTab(self.imgview, "Monitor")

        self.treeImages = CalcTreeWidget()
        self.tabWidgets = [self.imgview]
        self.measurementObject = None
        self.addMovableWidget(self.treeImages, 'Images')
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
        
    def timedTask(self, intervall, function):
        self.timers = []
        timer = QtCore.QTimer()
        timer.timeout.connect(function)
        timer.start(intervall)
        self.timers.append(timer)
    
    def addImage(self, data, info, name='New', autoLevel = False):
        it = CalcTreeWidgetItem(self.newItems,
                                [name],
                                img=data, info=info,
                                kind = 'data'
                                       )
        it.setFlags(sourceDataFlags)
#        if autoLevel:
#            self.autoLevel(it)
        self.changeActiveImage(it, None)
        return it
    def startMeasurement(self):
        if self.measurementObject != None and self.measurementObject.isRunning():
            print('measurement is running')
            return
        try:
            self.measurementObject = self.measurementObjectCreator()
        except Exception as e:
#            print('Could not create measurement object:\n', e)
            self.errorBox('Failed to start measurement:' + exc.PrettyPrintException(*sys.exc_info()))
            return
        
        self.form.actionStartMeasurement.setText('Terminate')
        self.form.actionStartMeasurement.triggered.connect(self.killMeasurement)
        

        self.measurementObject.finished.connect(self.onMeasurementEnd)
        self.measurementObject.finished.connect(lambda: self.console.write('~' * 80 + "\nMeasurement exit!\n" + '~' * 80 ))
        self.measurementObject.signalMessage.connect(self.console.write)
        
            
        self.console.write('~' * 80 + '\nStarting new measurement...\n' + '~' * 80)
        self.measurementObject.start()
        
    def onMeasurementEnd(self):
        self.measurementObject.terminate()
        self.form.actionStartMeasurement.setText('Start')
        self.form.actionStartMeasurement.triggered.disconnect()
        self.form.actionStartMeasurement.triggered.connect(self.startMeasurement)
        
    def connectMeasurement(self, measurementObjectCreator):
        try:
            self.measurementObjectCreator = measurementObjectCreator
        except Exception as e:
            self.errorBox('Could not create measurement:' + str(e))
            return
        self.form.actionStartMeasurement.triggered.connect(self.startMeasurement)
        self.form.actionStartMeasurement.setEnabled(True)
    
    def killMeasurement(self):
        self.measurementObject.shouldExit = True
        self.measurementObject.wait()
        

    def addTabWidget(self, widget, name):
        self.form.tabWidget.addTab(widget, name)
        self.tabWidgets.append(widget)
        
    def addMovableWidget(self, widget, title):
        dw = QtWidgets.QDockWidget(title, parent=self)
        self.dockWidgets.append(dw)
        dw.setWidget(widget)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), dw)
        visibleAction = QtWidgets.QAction(title, self)
        visibleAction.setCheckable(True)
        visibleAction.toggled['bool'].connect(dw.setVisible)
        dw.visibilityChanged.connect(visibleAction.setChecked)
        self.form.menuView.addAction(visibleAction)
    def errorBox(self, text):
        QtWidgets.QMessageBox.warning(self, 'Error', text)
    def loadImageFromFile(self):
        fnames = QtWidgets.QFileDialog.getOpenFileNames(
                self, filter='HDF5 Image (*.hdf5)')[0]

        for fname in fnames:
            try:
                CalcTreeWidgetItem(
                        self.fromFileItems,
                        [Path(fname).stem], 
                        fromfile = fname, kind='data')
            except Exception as e:
                self.errorBox(fname + ': ' + str(e))
                
    def saveImageToFile(self, fname=None):
        item = self.treeImages.currentItem()
#        print(f)
        print('fname :', fname)
        if item == None or item.img == None:
            return
#        if fname == None:
        fname = QtWidgets.QFileDialog.getSaveFileName()[0]
 
        
        item.saveImageToFile(fname)
    def autoLevel(self):
        item = self.treeImages.currentItem()
        print(item)
        if item is None or item.img is None:
            return
        data = item.img
        hist, bins = np.histogram(data, bins=2**15)
        bins = bins[:-1]
        hist = (hist * np.roll(hist, 10) * np.roll(hist, 60))**1/3
    #    m = np.max(hist)/1000
        print(hist)
        a = np.argwhere(hist>0)
        if len(a) >= 2:
            minmax = np.argwhere(hist>0).flatten()[[0, -1]]
            print(minmax)
            minmax = bins[minmax].flatten()
            self.imgview.setLevels(*minmax)
        else:
            print("Could not auto level")
    
        
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
        quit()
        
    def exec(self):
        self.show()
        self.app.exec_()


def makeTestViewer():
    p = os.path.dirname(__file__)
    imv  = ImageViewer()
    i=0
    imgs = []
    print(p)
    for f in os.listdir(p + '/sample_images'):
        sample = HamamatsuFile(p + '/sample_images/' + f)
        sample.header['time'] = sample.header['Application']['Time']
        sample.header['exposure'] = sample.header['Acquisition']['ExposureTime']
        sample.header['optical orientation'] = '+' if i % 2 == 0 else '-' 
        sample.header = unrecurseDictionary(sample.header)
        imv.addImage(sample.data, sample.header, name = f)
        imgs.append(sample.data)
        i += 1
    return imv

def testSaveAndLoadImage():
    a = CalcTreeWidgetItem(['some item'], img=np.zeros((1024, 1024)))
    a.saveImageToFile('Images/Somefile')
    b = CalcTreeWidgetItem(fromfile='Images/Somefile')
    return b

# from aqt.qt import debug; debug()
#%%
if __name__=='__main__':
#    sp.run('pyuic5 uidesign/mainWindow.ui -o uidesign/mainWindow.py', shell=True)
#    import subprocess as sp
#    import excepthook
    imv = makeTestViewer()
    b = testSaveAndLoadImage()
#    print(polarization(imgs))
    imv.exec()