import sys
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout,QListWidget, \
QDockWidget, QTextEdit, QApplication
import PyQt5 as pq
from PyQt5.QtCore import Qt

class dockdemo(QMainWindow):
   def __init__(self, parent = None):
      super(dockdemo, self).__init__(parent)
		
      layout = QHBoxLayout()
      bar = self.menuBar()
      file = bar.addMenu("File")
      file.addAction("New")
      file.addAction("save")
      file.addAction("quit")
		
      self.items = QDockWidget("Dockable", self)
      self.listWidget = QListWidget()
      self.listWidget.addItem("item1")
      self.listWidget.addItem("item2")
      self.listWidget.addItem("item3")
      self.items.setWidget(self.listWidget)
      self.items.setFloating(False)
      
      self.items2 = QDockWidget("Dockable", self)
      self.listWidget2 = QListWidget()
      self.listWidget2.addItem("item1")
      self.listWidget2.addItem("item2")
      self.listWidget2.addItem("item3")
      self.items2.setWidget(self.listWidget2)
      self.items2.setFloating(False)

      self.setCentralWidget(QTextEdit())
      self.addDockWidget(Qt.RightDockWidgetArea, self.items)
      self.setLayout(layout)
      self.setWindowTitle("Dock demo")
		
def main():
   app = QApplication(sys.argv)
   ex = dockdemo()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()