import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PySide2 import QtCore, QtWidgets
from PySide2.QtWidgets import QWidget

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class Canvas(FigureCanvas):
	def __init__(self, figure, parent=None):
		self.name = figure.name
		self.fig = figure.fig
		self.axes = figure.ax
		super(Canvas, self).__init__(self.fig)

class MplCanvas(QWidget):
	def __init__(self, figure):
		super(MplCanvas, self).__init__()

		self.canvas  = Canvas(figure)
		self.toolbar = NavigationToolbar(self.canvas, self)

		layout = QtWidgets.QVBoxLayout()
		layout.addWidget(self.toolbar)
		layout.addWidget(self.canvas)
		self.setLayout(layout)
		self.setWindowTitle("Fig: "+self.canvas.name)
		self.show()

	def draw(self):
		self.canvas.draw()