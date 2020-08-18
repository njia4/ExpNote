import sys
from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, 
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
from Experiment import Experiment
from PySide2 import QtGui

class Parameter(QWidget):
	def __init__(self, exp, parent):
		super(Parameter, self).__init__()
		self.exp = exp
		self.parent = parent
		self.setWindowTitle('Parameters')
		self.do_layout()

	def do_layout(self):
		layout = QVBoxLayout()
		var_layout = QGridLayout()

		param_dict = self.exp.get_parameters()
		for ii, _key in enumerate(param_dict.keys()):
			_label = QLabel()
			_label.setText(_key)
			var_layout.addWidget(_label, ii, 0)
			
			_val = QLineEdit()
			_val.setObjectName(_key)
			_val.setText(str(param_dict[_key]))
			var_layout.addWidget(_val, ii, 1)
			_val.editingFinished.connect(self.OnChangeParameter)

		verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

		layout.addItem(var_layout)
		layout.addItem(verticalSpacer)
		self.setLayout(layout)
		self.show()

	def OnChangeParameter(self):
		_param_dict = {self.sender().objectName(): self.sender().text()}
		self.exp.set_parameters(_param_dict)
		self.exp.update_figure()
		self.parent.update_figures()
