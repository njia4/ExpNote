import sys, time
from PySide2.QtWidgets import QAction, QMenu, QApplication, QMainWindow, QWidget, QTableWidgetItem, QMessageBox, QInputDialog
from PySide2.QtCore import QFile, Slot, Qt
from PySide2.QtGui import QCursor
from ui_DataTable import Ui_DataTable
from utilities import *

EMPTY_ROWS = 10

class DataTable(QWidget):
	def __init__(self, exp):
		super(DataTable, self).__init__()
		self.ui = Ui_DataTable()
		self.ui.setupUi(self)

		self.exp = exp
		self.col_header = list(self.exp.df.columns)

		self.backend_writing = False
		
		self.populate_tabel(self.exp.df)

		self.ui.tb_DataFrame.cellChanged.connect(self.OnCellChanged)
		self.ui.tb_DataFrame.cellActivated.connect(self.OnCellSelected)
		self.ui.tb_DataFrame.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
		self.ui.tb_DataFrame.horizontalHeader().customContextMenuRequested.connect(self.hoizontalMenu)
       
	def _insert_row(self, row_index):
		return
	def _insert_col(self, col_index):
		return
	def _add_row(self):
		self.ui.tb_DataFrame.insertRow(self.ui.tb_DataFrame.rowCount())
		return self.ui.tb_DataFrame.rowCount()
	def _add_col(self):
		self.ui.tb_DataFrame.insertColumn(self.ui.tb_DataFrame.columnCount())
		return self.ui.tb_DataFrame.columnCount()

	def _edit_cell(self, row, col, val):
		col = self.get_col_header_labels()[col]
		self.exp.set_cell(row, col, val)
		return 1

	def get_col_header_labels(self):
		_labels = []
		for ii in range(self.ui.tb_DataFrame.columnCount()):
			_labels.append(self.ui.tb_DataFrame.horizontalHeaderItem(ii).text())
		return _labels

	def hoizontalMenu(self, event):
		menu = QMenu(self)
		actionAddColRight = QAction("Add column to the right", self)
		actionAddColLeft  = QAction("Add column to the left ", self)
		menu.addAction(actionAddColRight)
		menu.addAction(actionAddColLeft )
		menu.popup(QCursor.pos())
		_col = self.ui.tb_DataFrame.horizontalHeader().logicalIndexAt(event)
		action = menu.exec_()
		# action = menu.exec_()
		if action == actionAddColRight:
			self.OnNewVar(_col+1)
			return
		if action == actionAddColLeft:
			self.OnNewVar(_col)
			return

	
	def add_run(self, data_id):
		self.ui.tb_DataFrame.blockSignals(True)
		data = self.exp.get_row(data_id)
		for _key in data.keys():
			if _key == 'id':
				continue
			if not _key in self.col_header:
				_col_header_labels = self.get_col_header_labels()
				_col_header_labels.append(_key) # Add new variable 
				self._add_col()
				self.ui.tb_DataFrame.setHorizontalHeaderLabels(_col_header_labels)
				self.col_header = _col_header_labels

			_row = data_id-1
			_col = self.col_header.index(_key)

			self.ui.tb_DataFrame.setItem(_row, _col, QTableWidgetItem(str(data[_key])))

		self.ui.tb_DataFrame.blockSignals(False)

		_empty_rows = self.ui.tb_DataFrame.rowCount() - data_id
		if _empty_rows < EMPTY_ROWS:
			for ii in range(EMPTY_ROWS-_empty_rows+1):
				self._add_row()
		return
	def populate_tabel(self, df):
		# Resize the grid
		n_row, n_col = df.shape
		self.ui.tb_DataFrame.setColumnCount(n_col)
		self.ui.tb_DataFrame.setRowCount(n_row+EMPTY_ROWS)

		# Update headers
		self.ui.tb_DataFrame.setHorizontalHeaderLabels(list(df.columns))

		# Populate grid row by row
		for ii in range(len(df)):
			self.add_run(ii+1)
		return

	@Slot()
	def OnCellChanged(self, row, col):
		_val = self.ui.tb_DataFrame.item(row, col).text()
		self._edit_cell(row, col, _val)

		_empty_rows = self.ui.tb_DataFrame.rowCount() - row
		if _empty_rows < EMPTY_ROWS:
			for ii in range(EMPTY_ROWS-_empty_rows+1):
				self._add_row()

		self.ui.tb_DataFrame.setCurrentCell(row+1, col) # Move the cursor to the next row
		return
	@Slot()
	def OnCellSelected(self, row, col):
		_item = self.ui.tb_DataFrame.item(row, col)
		if col == 1:
			_item.setFlags(Qt.ItemIsEditable)
			_item.setFlags(Qt.ItemIsSelectable)
			print('=')
		return
	@Slot()
	def OnNewVar(self, col):
		text, ok = QInputDialog.getText(self, 'New variable', 'Variable name:')
		if ok:
			_col_header_labels = self.get_col_header_labels()
			if text in _col_header_labels:
				print("Columne already exists!")
				return
			self.ui.tb_DataFrame.insertColumn(col)
			_col_header_labels.insert(col, text) # Add new variable 
			self.ui.tb_DataFrame.setHorizontalHeaderLabels(_col_header_labels)
			self.col_header = _col_header_labels
		return
	@Slot()
	def OnReanalyze(self):
		return
