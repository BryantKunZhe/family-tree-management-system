from PyQt4.QtGui import * 
from PyQt4.QtCore import *
class MyLabel(QLabel):
	#signal_test = pyqtSignal()
	def __init__(self,parent=None):
		super(MyLabel,self).__init__(parent)

	def mouseDoubleClickEvent(self,e):
		self.emit(SIGNAL("mouseDoubleClicked()"))