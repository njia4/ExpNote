import sys
from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, Signal)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, 
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
from Experiment import Experiment
from PySide2 import QtGui
from utilities import *

class PlotSignal(QObject):
	plot = Signal()

class Parameter(QWidget):
	def __init__(self, exp, parent):
		super(Parameter, self).__init__()
		self.exp = exp
		self.parent = parent
		self.signals = PlotSignal()
		self.setWindowTitle('Parameters')
		self.do_layout()

	def do_layout(self):
		layout = QVBoxLayout()
		var_layout = QGridLayout()
		var_layout.setHorizontalSpacing(20)
		var_layout.setVerticalSpacing(1)

		param_dict = self.exp.get_parameters()
		for ii, _key in enumerate(param_dict.keys()):
			_label = QLabel()
			_label.setText(_key)
			var_layout.addWidget(_label, ii, 0)
			
			if type(param_dict[_key])==list:
				_val = QComboBox()
				_val.setObjectName(_key)
				for _item in param_dict[_key]:
					_val.addItem(_item)
				# _val.activated[str].connect(self.OnChangeSelection)
				_val.currentTextChanged.connect(self.OnChangeSelection)
			else:
				_val = QLineEdit()
				_val.setObjectName(_key)
				_val.setText(str(param_dict[_key]))
				_val.editingFinished.connect(self.OnChangeParameter)
			var_layout.addWidget(_val, ii, 1)

		verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

		layout.addItem(var_layout)
		layout.addItem(verticalSpacer)
		self.setLayout(layout)
		self.show()

	def set_parameters(self, param_dict):
		for _widget in self.findChildren(QComboBox):
			try:
				_items = [_widget.itemText(ii) for ii in range(_widget.count())]
				_widget.setCurrentIndex(_items.index(param_dict[_widget.objectName()]))
			except:
				console_print('Parameter', 'Failed to set the value of parameter "{}"'.format(_widget.objectName()))
				continue

		for _widget in self.findChildren(QLineEdit):
			try:
				_widget.setText(str(param_dict[_widget.objectName()]))
			except:
				console_print('Parameter', 'Failed to set the value of parameter "{}"'.format(_widget.objectName()))
				continue

		# The code above only change the values on the GUI. It doesn't trigger the change event. 
		# The value in the Experiment class which is used to do the analysis hasn't been changed yet. 
		# Have to manually assign the value by the following line. 
		# self.exp.set_parameters(_param_dict)

	def OnChangeParameter(self):
		_param_dict = {self.sender().objectName(): self.sender().text()}
		self.exp.set_parameters(_param_dict)
		# self.exp.update_figure()
		# self.parent.update_figures()
		self.signals.plot.emit()

	def OnChangeSelection(self, text):
		_param_dict = {self.sender().objectName(): text}
		self.exp.set_parameters(_param_dict)
		# self.exp.update_figure()
		# self.parent.update_figures()
		self.signals.plot.emit()
