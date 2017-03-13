# -*- coding: utf-8 -*-
import time, traceback

#from StringIO import cStringIO
import io
from PyQt5 import QtCore, QtWidgets
import sys
def PrettyPrintException(excType, excValue, tracebackobj):
    separator = '-' * 80
    timeString = time.strftime("%Y-%m-%d, %H:%M:%S")
    
    
    tbinfofile = io.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = '%s: \n%s' % (str(excType), str(excValue))
    sections = [separator, timeString, separator, errmsg, separator, tbinfo]
    msg = '\n'.join(sections)
    return msg
    
def excepthook(excType, excValue, tracebackobj):
    """
    Global function to catch unhandled exceptions.
    
    @param excType exception type
    @param excValue exception value
    @param tracebackobj traceback object
    """
    notice = 'Exception Occured: '
    app = QtWidgets.QApplication([])
    msg = PrettyPrintException(excType, excValue, tracebackobj)
    errorbox = QtWidgets.QMessageBox()
    errorbox.setText(str(notice)+str(msg))
    errorbox.exec_()


sys.excepthook = excepthook