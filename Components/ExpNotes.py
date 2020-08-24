import sys
from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, 
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
from Experiment import Experiment
from PySide2 import QtGui

class Notes(QWidget):
	def __init__(self, exp, parent):
		super(Notes, self).__init__()
		self.exp = exp
		self.parent = parent
		self.setWindowTitle('Notes')
		self.do_layout()

	def do_layout(self):
		layout = QVBoxLayout()
		
		note = self.exp.get_exp_info()['description']
		txt_edit = QTextEdit()
		txt_edit.setText(note)
		txt_edit.textChanged.connect(self.OnChangeNote)
		
		layout.addWidget(txt_edit)
		self.setLayout(layout)
		self.show()

	def OnChangeNote(self):
		note = self.sender().toPlainText()
		self.exp.set_exp_info({'name': self.exp.name, 'description': note})
