import sys, time
from PySide2.QtWidgets import QDialog, QFileDialog
from PySide2.QtCore import QFile, Slot, Qt
from PySide2.QtGui import QCursor
from .ui_NewExpDialog import Ui_Dialog
from utilities import *

EMPTY_ROWS = 10

class NewExpDialog(QDialog):
	def __init__(self, name=None, script=''):
		super(NewExpDialog, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		if script != '':
			self.filename = script
			self.ui.label_ExpScriptFile.setText(os.path.split(script)[-1])

		if name != None:
			self.ui.lineEdit.setText(name)
		self.ui.label_ExpScriptFile.mousePressEvent = self.OnLoadScript

	def get_name(self):
		return self.ui.lineEdit.text()
	def get_script(self):
		return self.filename

	def OnLoadScript(self, event):
		dlg = QFileDialog()

		if dlg.exec_():
			self.filename = dlg.selectedFiles()[0]
			self.ui.label_ExpScriptFile.setText(os.path.split(self.filename)[-1])
			