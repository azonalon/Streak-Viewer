# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui
pyqtSignal = QtCore.pyqtSignal
import time
#import random
import sys
#import random
import StreakViewer.excepthook as exc

        
class Measurement(QtCore.QThread, QtCore.QObject):
    signalNumberGenerated = pyqtSignal(int)
    signalMessage = pyqtSignal(str)

    def __init__(self, **kwargs):
        print('hi')
        """ kwargs: instruments """
#        super(QtCore.QThread).__init__()
#        super(QtCore.QObject).__init__()
        super().__init__()
        self.random = kwargs['random']
        print('hu')
        
    def message(self, msg):
        self.signalMessage.emit(msg)
        
    def procedure(self):
        for i in range(3):
            time.sleep(1)
#            asdfsdf
            self.message('lala measure')
            self.signalNumberGenerated.emit(30)

    def run(self):
        try:
            self.procedure()
        except Exception:
            msg = exc.PrettyPrintException(*sys.exc_info())
            self.message(msg)
            

