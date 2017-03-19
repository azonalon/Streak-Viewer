# -*- coding: utf-8 -*-
"""
Demonstrates a way to put multiple axes around a single plot. 

(This will eventually become a built-in feature of PlotItem)

"""
#import initExample ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

pg.mkQApp()

pw = pg.PlotWidget()
pw.show()
pw.setWindowTitle('pyqtgraph example: MultiplePlotAxes')
pi = pw.plotItem
#pi.setLabels(left='axis 1')
#pi.setXLink(pi)
pi.addLegend()
## create a new ViewBox, link the right axis to its coordinate system
lg = pg.LegendItem()
lg.setParentItem(pi)
vb1 = pg.ViewBox()
ax1 = pg.AxisItem('right')
pi.scene().addItem(vb1)
pi.layout.addItem(ax1, 2, 1)
pi.layout.addItem(lg, 2, 3)
#pi.layout.addItem(vb1, 2, 3)
ax1.linkToView(vb1)
vb1.setXLink(pi)

vb2 = pg.ViewBox()
ax2 = pg.AxisItem('right')
pi.scene().addItem(vb2)
pi.layout.addItem(ax2, 2, 2)
ax2.linkToView(vb2)
vb2.setXLink(pi)

## create third ViewBox. 
## this time we need to create a new axis as well.
#p3 = pg.ViewBox()
#p1.layout.addItem(ax3, 2, 3)
#p1.scene().addItem(p3)
#ax3.linkToView(p3)
#p3.setXLink(p1)
#ax3.setZValue(-10000)
#ax3.setLabel('axis 3', color='#ff0000')


## Handle view resizing 
def updateViews():
    ## view has resized; update auxiliary views to match
    global pi, vb1, vb2
    vb1.setGeometry(pi.vb.sceneBoundingRect())
    vb2.setGeometry(pi.vb.sceneBoundingRect())
    
    ## need to re-update linked axes since this was called
    ## incorrectly while views had different shapes.
    ## (probably this should be handled in ViewBox.resizeEvent)
#    vb1.linkedViewChanged(pi.vb, vb1.XAxis)
#    vb2.linkedViewChanged(pi.vb, vb1.XAxis)

updateViews()
pi.vb.sigResized.connect(updateViews)
it1 = pg.PlotCurveItem([3200,1600,800,400,200,100], pen='b')
it2 = pg.PlotCurveItem([10,20,40,80,40,20], pen='r')
it3 = pg.PlotCurveItem(np.array([10,20,40,80,40,20])/2, pen='g')

#p1.plot([1,2,4,8,16,32])
vb1.addItem(it1)
vb2.addItem(it2)
#p3.addItem(it3)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()