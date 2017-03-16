# -*- coding: utf-8 -*-
#import sys
import numpy as np
from PyQt5 import QtCore, QtWidgets
#from pyqtgraph import QtCore
import pyqtgraph as pg
#import excepthook
import subprocess as sp
from .uidesign.loggerWidget  import Ui_Form
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

class LoggerCurve(pg.PlotCurveItem):
    def __init__(self, function, interval, color):
#        self.function = function
        self.interval = interval
        self.timer = QtCore.QTimer()
        self.color = color
#        self.thread = thread
        
        self.thread = FunctionEvaluateThread(function)
        self.thread.resultReady.connect(self.addEntry)
        super().__init__(pen=color)
        
    def start(self):
        self.timer.start(self.interval)
        
    def requestEntry(self):
        if self.thread.isRunning():
            return
        self.thread.start()
    
    def updatePlot(self):
        x = self.timeStamps
        y = self.values
        if self.n < self.numberOfEntries:
            self.setData(x=x[-self.n:], y=y[-self.n:])
        else:
            self.setData(x=x, y=y)
        

        
        
class LoggerWidget(QtWidgets.QWidget):
    def __init__(self, logFile, interval, valueGenerator, plotEntries=1000,
                 parent=None):
        super().__init__(parent=parent)
        self.logFile = logFile
#        QtCore.
        self.interval = interval
        
        self.numberOfEntries = plotEntries
        self.timeStamps = np.zeros(self.numberOfEntries, dtype=np.float64)
        self.values = np.zeros(self.numberOfEntries, dtype=np.float64)
#        self.shouldStop = False
        self.n = 0
        self.form = Ui_Form()
        self.form.setupUi(self)
        self.plotWidget = pg.PlotWidget(
                title='Timed data',
                axisItems={'bottom': TimeAxisItem(orientation='bottom')}
                )
        self.form.layoutPlotWidget.addWidget(self.plotWidget)
        self.form.buttonStop.clicked.connect(self.finish)
        self.form.buttonStart.clicked.connect(self.start)
        self.colors = ['r', 'g', 'b']
        self.plotItems = []
        self.views = [self.plotWidget]
        self.curves = []
        self.timer.timeout.connect(self.requestEntry)

        n = 0
        if callable(valueGenerator):
            self.valueGenerator = [valueGenerator]
        elif type(valueGenerator) is list:
            for i, g in enumerate(valueGenerator[1:]):
                p2 = pg.ViewBox()
                self.plotWidget.showAxis('right')
                self.plotWidget.scene().addItem(p2)
                self.plotWidget.getAxis('right').linkToView(p2)
                p2.setXLink(self.plotWidget)
                self.plotWidget.getAxis('right').setLabel('axis2', color='#0000ff')
                self.views.append(p2)
                if type(g) is not list:
                    g = [g]
                for j, c in g:
#                    curveItem = pg.PlotCurveItem(pen=self.colors[n])
                    self.curves.append(
                            LoggerCurve(
                                    FunctionEvaluateThread(c['function']),
                                    c['rate'],
                                    self.colors[n])
                                    )
                    p2.addItem(self.curves[n])
                    n += 1
                    
                
            
        

        self.curve = self.plotWidget.plot()
        self.start()

        

        
    def closeEvent(self, event):
        self.finish()
        print('closing logger widget')
        event.accept()
        

        
    def formatTime(self, epochTime):
        return time.strftime('%Y %m %d %H %M %S',
                             time.localtime(epochTime))


    def finish(self):
        self.timer.stop()
        while self.evaluateThread.isRunning():
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
#        print('adding entry')
        self.values = np.roll(self.values, -1)
        self.timeStamps = np.roll(self.timeStamps, -1)
        self.values[-1] = value
        self.timeStamps[-1] = time.time() #- 1488622099.3514423
        self.n += 1
        self.updatePlot()
        if self.n % self.numberOfEntries == 0:
            with open(self.logFile, 'a') as f:
                for j in range(self.numberOfEntries):
                    f.write(
                            '%s %f\n' % (self.formatTime(self.timeStamps[j]),
                                       self.values[j])
                    )
            


x=0
if __name__ == '__main__':
    sp.run('pyuic5 uidesign/loggerWidget.ui -o uidesign/loggerWidget.py', shell=True)
    #QtGui.QApplication.setGraphicsSystem('raster')
    from yahoo_finance import Share
    app = QtWidgets.QApplication([])
    mw = QtWidgets.QMainWindow()
    yahoo = Share('YHOO')
    def f():
        global x
        x += 1 - 2*np.random.random()
        time.sleep(.5)
        return x
    
    cw = LoggerWidget('yhoo.log', 100, [{'function':f}, {'function': f}], plotEntries=1000,
                      parent=mw)
    
    
    mw.setCentralWidget(cw)
    mw.show()
    app.exec_()
