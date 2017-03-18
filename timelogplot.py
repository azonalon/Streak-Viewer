# -*- coding: utf-8 -*-
#import sys
import numpy as np
from PyQt5 import QtCore, QtWidgets
#from pyqtgraph import QtCore
import pyqtgraph as pg
#import excepthook
import subprocess as sp
from uidesign.loggerWidget  import Ui_Form
#from PyQt5.QtCore import QTime, QTimer
#from collections import deque
#import time
#import multiprocessing as mp
import time
import random
#class DataGenerator():
#    def __init__(self, ):
#        self.inUse = False
#    def canGet()
class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        # PySide's QTime() initialiser fails miserably and dismisses args/kwargs
#        return [QTime().addMSecs(value).toString('mm:ss') for value in values]
        return [time.strftime('%H:%M:%S', time.localtime(value)) 
                for value in values]

# from multiprocessing import Process
class FunctionEvaluateThread(QtCore.QThread, QtCore.QObject):
    resultReady = QtCore.pyqtSignal(float)
    def __init__(self, f):
        super().__init__()
        self.f = f

    def run(self):
        result = self.f()
        self.resultReady.emit(result)

class Logger(QtCore.QObject):
    updated = QtCore.pyqtSignal(object)
    def __init__(self, logFile, function, interval, bufferLength):
        """ interval in ms """
        super().__init__()
        self.n = 0
        self.logFile = logFile
        self.interval = interval
        self.timer = QtCore.QTimer()
        self.numberOfEntries = bufferLength
        self.timeStamps = np.zeros(self.numberOfEntries, dtype=np.float64)
        self.values = np.zeros(self.numberOfEntries, dtype=np.float64)
        self.thread = FunctionEvaluateThread(function)
        
        self.timer.timeout.connect(self.requestEntry)
        self.thread.resultReady.connect(self.addEntry)

    def start(self):
        self.timer.start(self.interval)
        
    def requestEntry(self):
#        print('requesting...')
        if self.thread.isRunning():
            print('thread still running')
            return
        self.thread.start()
    

    def finish(self):
        self.timer.stop()
        while self.thread.isRunning():
            time.sleep(.01)
        f = open(self.logFile, 'a')
        remainingEntries = self.n % self.numberOfEntries
        for j in range(self.numberOfEntries - remainingEntries, self.numberOfEntries):
            f.write('%s %f\n' % (
                    self.formatTime(self.timeStamps[j]),
                    self.values[j])
                )
        f.close()
        
    def addEntry(self, value):
#        print('adding entry %d' % self.n)
        self.values = np.roll(self.values, -1)
        self.timeStamps = np.roll(self.timeStamps, -1)
        self.values[-1] = value
        self.timeStamps[-1] = time.time() #- 1488622099.3514423
        self.n += 1
        if self.n % self.numberOfEntries == 0:
            with open(self.logFile, 'a') as f:
                for j in range(self.numberOfEntries):
                    f.write(
                            '%s %f\n' % (self.formatTime(self.timeStamps[j]),
                                       self.values[j])
                    )
        self.updated.emit(self)
    def formatTime(self, epochTime):
        return time.strftime('%Y %m %d %H %M %S',
                             time.localtime(epochTime))



        
        
class LoggerPlotWidget(QtWidgets.QWidget):
    def __init__(self, axesDescriptor, parent=None):
        super().__init__(parent=parent)
        self.form = Ui_Form()
        self.form.setupUi(self)
        self.plotWidget = pg.PlotWidget(
                title='Timed data',
                axisItems={'bottom': TimeAxisItem(orientation='bottom')}
                )
        self.plotItem = self.plotWidget.plotItem
        self.form.layoutPlotWidget.addWidget(self.plotWidget)
        self.nAxis = 0

        if type(axesDescriptor) is not list:
            axesDescriptor = [axesDescriptor]
        for curves in axesDescriptor:
            self.attachAxis(curves)
    
    def updateViews(self, viewBox):
        viewBox.setGeometry(self.plotItem.vb.sceneBoundingRect())
        viewBox.linkedViewChanged(self.plotItem.vb, viewBox.XAxis)
    
    def attachAxis(self, axisDescriptor): 
        if self.nAxis == 0:
            viewBox = self.plotItem
            axis = viewBox.getAxis('left')
        else:
            viewBox = pg.ViewBox()
            axis = pg.AxisItem('right')
            self.plotItem.scene().addItem(viewBox)
            self.plotItem.layout.addItem(axis, 2, self.nAxis + 2)
            axis.linkToView(viewBox)
            viewBox.setXLink(self.plotItem)
            self.updateViews(viewBox)
            self.plotItem.vb.sigResized.connect(lambda: self.updateViews(viewBox))
        self.nAxis += 1
#        self.viewBoxes.append(viewBox)
        if type(axisDescriptor) is not dict:
            axisDescriptor = {'curves': axisDescriptor}
        elif 'source' in axisDescriptor:
            self.attachCurve(axisDescriptor, viewBox)
            return
        if type(axisDescriptor['curves']) is not list:
            axisDescriptor['curves'] = [axisDescriptor['curves']]
        for curve in axisDescriptor['curves']:
            self.attachCurve(curve, viewBox)
        
    def attachCurve(self, curve, viewBox):
        """ curve is a logger type object or a dict containing
        a logger type object and additional arguments forwarded to 
        plotcurveitem """
        if type(curve) is not dict:
            curve = {'source': curve}
        it = pg.PlotCurveItem(**curve)
        viewBox.addItem(it)
        curve['source'].updated.connect(lambda l: self.updatePlot(it, l))
    
#
    def updatePlot(self, plotCurveItem, logger):
        x = logger.timeStamps
        y = logger.values
        if logger.n < logger.numberOfEntries:
            plotCurveItem.setData(x=x[-logger.n:], y=y[-logger.n:])
        else:
            plotCurveItem.setData(x=x, y=y)
            
    def closeEvent(self, event):
        self.finish()
        for l in self.loggers:
            print('finishing logger...')
            l.finish()
        print('closing logger widget')
        event.accept()
        


v = [0, 0, 0]
if __name__ == '__main__':
    sp.run('pyuic5 uidesign/loggerWidget.ui -o uidesign/loggerWidget.py', shell=True)
    #QtGui.QApplication.setGraphicsSystem('raster')
#    import excepthook
    global x, y, z
    x=0; y=0; z=0
    def f(i):
        global v
        v[i] += 1 - 2*np.random.random()
        return v[i]

    app = QtWidgets.QApplication([])
    mw = QtWidgets.QMainWindow()
    cw = QtWidgets.QWidget(mw)
    mw.setCentralWidget(cw)
    layout = QtWidgets.QGridLayout(cw)
    
    
    loggerx = Logger('x.log', lambda: f(0), 100, 100)
    loggerx.start()
    loggery = Logger('y.log', lambda: f(1), 100, 100)
    loggery.start()
    loggerz = Logger('z.log', lambda: f(2), 100, 100)
    loggerz.start()
    
    lwg = LoggerPlotWidget([{'source': loggerx, 'pen': 'r'},
                            {'source': loggery, 'pen': 'g'},
                            {'source': loggerz, 'pen': 'b'}])
    layout.addWidget(lwg)
    mw.show()

    app.exec_()
#    loggerx.finish()


    
#    cw = LoggerPlotWidget('yhoo.log', 100, [{'function':f}, {'function': f}], plotEntries=1000,
#                      parent=mw)
#    
#    
#    mw.setCentralWidget(cw)
#    mw.show()

