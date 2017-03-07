# -*- coding: utf-8 -*-
#import sys
import numpy as np
from PyQt5 import QtCore, QtWidgets
#from pyqtgraph import QtCore
import pyqtgraph as pg
#import excepthook
import subprocess as sp
from .uidesign.loggerWidget import Ui_Form
#from PyQt5.QtCore import QTime, QTimer
#from collections import deque
#import time
#import multiprocessing as mp
import time

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

#from multiprocessing import Process
class LoggerWidget(QtWidgets.QWidget):
    def __init__(self, logFile, interval, valueGenerator, plotEntries=1000,
                 parent=None):
        super().__init__(parent=parent)
        self.logFile = logFile
#        QtCore.
        self.interval = interval
        self.valueGenerator = valueGenerator
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
        
#        self.thread = Process(target=self.addEntry)
        self.curve = self.plotWidget.plot()
        self.timer = QtCore.QTimer(parent=parent)
        self.timer.timeout.connect(self.addEntry)
        self.start()
        
    def start(self):
        self.timer.start(self.interval)
        
    def closeEvent(self, event):
        print('closing...')
        event.accept()
        
    def updatePlot(self):
        x = self.timeStamps
        y = self.values
#        print(x, y)
        if self.n < self.numberOfEntries:
            self.curve.setData(x=x[-self.n:], y=y[-self.n:])
        else:
            self.curve.setData(x=x, y=y)
        
        
    def formatTime(self, epochTime):
        return time.strftime('%Y %m %d %H %M %S',
                             time.localtime(epochTime))

    def finish(self):
        self.timer.stop()
        f = open(self.logFile, 'a')
        remainingEntries = self.n % self.numberOfEntries
        for j in range(self.numberOfEntries - remainingEntries, self.numberOfEntries):
            f.write('%s %f' % (
                    self.formatTime(self.timeStamps[j]),
                    self.values[j])
                )
        f.close()
        
    def addEntry(self):
        
#        if self.n == 2*self.numberOfEntries:
#            self.finish()
#            return
        print('adding entry')
        if self.n % self.numberOfEntries == 0:
            with open(self.logFile, 'a') as f:
                for j in range(self.numberOfEntries):
                    f.write(
                            '%s %f\n' % (self.formatTime(self.timeStamps[j]),
                                       self.values[j])
                    )
            

        
        self.values = np.roll(self.values, -1)
        self.timeStamps = np.roll(self.timeStamps, -1)
        self.values[-1] = self.valueGenerator()
        self.timeStamps[-1] = time.time() #- 1488622099.3514423
#        print(self.values, self.timeStamps)
        self.updatePlot()
        self.n += 1
        

#class AsynchronousLoggerWidget(LoggerWidget):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.qthread = QtCore.QThread()


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
    
    cw = LoggerWidget('yhoo.log', 100, f, plotEntries=1000,
                      parent=mw)
    
    
    mw.setCentralWidget(cw)
    mw.show()
    app.exec_()
