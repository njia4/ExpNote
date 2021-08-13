#!/usr/bin/env python

import sys, time, glob, shutil, math, pickle
import threading
from PySide2.QtWidgets import QPushButton, QApplication, QMainWindow, QWidget, QMdiSubWindow, QTextEdit, QShortcut, QFileDialog
from PySide2.QtWidgets import QStyleFactory
from PySide2.QtCore import QFile, Slot, Qt, QObject, Signal, QPoint, QRect
from PySide2.QtCore import QThread, QThreadPool, QRunnable
from PySide2.QtGui import QKeySequence, QIcon

# UI components
from ui_MainWindow import Ui_MainWindow
from Components.DataTable import DataTable
from Components.AnalysisParameter import Parameter
from Components.MPLCanvas import MplCanvas
from Components.NewExpDialog import NewExpDialog
from Components.ExpNotes import Notes
from Experiment.Experiment import Experiment, load_exp
from config import *
from utilities import *

sys.path.append(JPAC_DIR)

# Signal class to call the add_run function in the main thread. 
# Direct calling in the thread loop will trigger cellChanged signal and do strange stuff. 
# Since the singal and add_run() are ran in different thread. 
class NewRunSignal(QObject):
    result = Signal(object)
class FileThread(QThread):
    def __init__(self, exp, gui):
        QThread.__init__(self)
        self.exp = exp
        self.gui = gui
        self.run_flg = True
        self.save_flg = False

        self.signals = NewRunSignal()

    def __del__(self):
        self.wait()

    def set_experiment(self, exp):
        self.exp = exp
    def set_save(self, save):
        self.save_flg = save
        console_print('File Thread', "Record {}".format(self.save_flg))

    def abort(self):
        console_print('File Thread', "Stopping!")
        self.run_flg = False

    def run(self):
        data_input_dir = DATA_INPUT_FOLDER_NAME
        while self.run_flg: 
            if not os.path.exists(data_input_dir):
              continue

            file_format = os.path.join(data_input_dir, "*") # TODO: DECLARE FILE FORMAT TO LOOK FOR
            files = glob.glob(file_format)
            # files = sorted(files, key=lambda x: os.path.split) # TODO: SORT

            if len(files) > 0:
              for f in files:
                  # Move file
                  file_name = os.path.split(f)[-1]
                  src = f
                  dst_dir = os.path.join(generate_dir(self.exp.name, self.exp.dt), "Data")
                  dst = os.path.join(dst_dir, file_name)
                  if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                  
                  if not os.access(src, os.W_OK): # Check if other software has finish writing the file
                    continue
                  shutil.move(src, dst)

                  if not self.save_flg:
                    os.remove(dst)
                    continue

                  # Run analysis script
                  console_print('File Thread', "New data file: {}".format(file_name))
                  data_id = self.exp.do_analyze(dst)
                  if data_id >= 0:
                    self.signals.result.emit(data_id)

            time.sleep(FILECHECK_FREQUENCY)

class RefreshPlotSignal(QObject):
    refresh = Signal()
class PlotThread(QThread):
    def __init__(self, gui):
        QThread.__init__(self)
        self.run_flg = True
        self.replot_flg = False
        self.gui = gui
        self.signals = RefreshPlotSignal()

    def replot(self):
        self.replot_flg = True

    def abort(self):
        self.run_flg = False

    def run(self):
        while self.run_flg:
            try:
                if self.replot_flg:
                    self.gui.exp.update_figure()
                    self.signals.refresh.emit()
                    self.replot_flg = False
                    self.gui.update_figures()
            except:
                continue
            time.sleep(0.25)

class MainWindow(QMainWindow):
    def __init__(self, exp):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowIcon(QIcon('icons/main.ico'))

        # Setup status bar. Cannot do this in the Designer. 
        self.btn_idle = QPushButton("Record", self)
        self.btn_idle.setStyleSheet("background-color : red")
        self.btn_idle.setCheckable(True)
        self.ui.statusbar.addWidget(self.btn_idle)

        self.exp = exp
        self.threadpool = QThreadPool()

        # Setup the GUI windows
        self.showMaximized()
        self.set_windows()
        self.OnTileWindows()

        # Menu bar function binding
        self.ui.actionNew.triggered.connect(self.OnNewExperiment)
        self.ui.actionOpen.triggered.connect(self.OnOpenExperiment)
        self.ui.actionSave.triggered.connect(self.OnSaveExperiment)
        self.ui.actionTileWindows.triggered.connect(self.OnTileWindows)
        self.ui.actionOpenWindows.triggered.connect(self.OnShowWindows)
        self.ui.actionLoadScript.triggered.connect(self.OnLoadScript)
        self.ui.actionReloadScript.triggered.connect(self.OnReloadScript)
        # Status bar
        self.btn_idle.clicked.connect(self.OnRecord)
        # Keyboard shortcuts
        self.full_screen = False
        self.shortcut_full_screen = QShortcut(QKeySequence('F11'), self)
        self.shortcut_full_screen.activated.connect(self.OnFullScreen)

        # Start looking for data files
        self.start_file_thread()
        self.start_plot_thread()

        # self.showMaximized()
        self.show()

    def set_table_win(self):
        # Add data table sub-window
        self.data_table = DataTable(self.exp, self)
        self.data_table.signals.plot.connect(self.replot)
        self.DataTableWindow = QMdiSubWindow()
        self.DataTableWindow.setWidget(self.data_table)
        self.ui.mdiArea.addSubWindow(self.DataTableWindow)
        self.DataTableWindow.show()
    def set_param_win(self):
        # Add analysis parameters
        self.analysis_parameters = Parameter(self.exp, self)
        self.analysis_parameters.signals.plot.connect(self.replot)
        self.ParameterWindow = QMdiSubWindow()
        self.ParameterWindow.setWidget(self.analysis_parameters)
        self.ui.mdiArea.addSubWindow(self.ParameterWindow)
        self.ParameterWindow.show()
        # Add note window
        self.exp_notes = Notes(self.exp, self)
        self.NotesWindow = QMdiSubWindow()
        self.NotesWindow.setWidget(self.exp_notes)
        self.ui.mdiArea.addSubWindow(self.NotesWindow)
        self.NotesWindow.show()
    def set_figs_win(self):
        # Add plots
        self.FigureWindows = {}
        self.figs = {}
        _figs = self.exp.get_figures()
        for _name in _figs.keys():
            self.figs[_name] = MplCanvas(_figs[_name])
            self.FigureWindows[_name] = QMdiSubWindow()
            self.FigureWindows[_name].setWidget(self.figs[_name])
            self.FigureWindows[_name].resize(500, 400)
            self.ui.mdiArea.addSubWindow(self.FigureWindows[_name])
            self.FigureWindows[_name].show()
    def set_windows(self):
        self.set_table_win()
        self.set_param_win()
        self.set_figs_win()
        self.OnTileWindows()
    def clear_windows(self, subwindows='all'):
        if subwindows == 'all':
            subwindows = self.ui.mdiArea.subWindowList()
        for _win in subwindows:
            self.ui.mdiArea.removeSubWindow(_win)
    def refresh_windows(self):
        self.clear_windows()
        self.set_windows()

    def start_file_thread(self):
        # Start file thread
        self.file_thread = FileThread(self.exp, self)
        self.file_thread.signals.result.connect(self.add_result)
        self.file_thread.start()
    def stop_file_thread(self):
        self.file_thread.abort()

    def start_plot_thread(self):
        self.plot_thread = PlotThread(self)
        self.plot_thread.start()
    def stop_plot_thread(self):
        self.plot_thread.abort()
    @Slot()
    def replot(self):
        self.plot_thread.replot()

    @Slot()
    def OnFullScreen(self):
        if self.full_screen:
            self.showMaximized()
        else:
            self.showFullScreen()
        self.full_screen = not self.full_screen
    
    @Slot()
    def OnTileWindows(self):
        top_row_height = 400
        # Position table window
        _ract = QRect(0., 0., 1200, top_row_height)
        self.DataTableWindow.setGeometry(_ract)
        self.DataTableWindow.move(0, 0)
        # Positon parameter window
        _ract = QRect(0., 0., 250, top_row_height)
        self.ParameterWindow.setGeometry(_ract)
        self.ParameterWindow.move(1200, 0)
        # Position Note window
        _ract = QRect(0., 0., 400, top_row_height)
        self.NotesWindow.setGeometry(_ract)
        self.NotesWindow.move(1450, 0)
        # Tile figure windwos
        _win_size = self.ui.mdiArea.width()/4.
        for ii, _name in enumerate(self.FigureWindows.keys()):
            x_shift = ii%4
            y_shift = math.floor(ii/4)
            _rect = QRect(0., 0., _win_size, _win_size)
            self.FigureWindows[_name].setGeometry(_rect)
            self.FigureWindows[_name].move(_win_size*x_shift, _win_size*y_shift+top_row_height)
    @Slot()
    def OnShowWindows(self):
        self.refresh_windows()

    @Slot()
    def OnNewExperiment(self):
        self.OnSaveExperiment()
        _info = self.exp.get_exp_info()
        _name = _info['name']
        _script = os.path.join(_info['script_dir'], _info['script'])

        dlg = NewExpDialog(name=_name, script=_script)

        if dlg.exec_():
            _name = dlg.get_name()
            _script = dlg.get_script()
            self.exp = Experiment(name=_name, script=_script)
            self.file_thread.set_experiment(self.exp)
            self.clear_windows()
            self.set_windows()
    @Slot()
    def OnOpenExperiment(self):
        dlg = QFileDialog()
        if dlg.exec_():
            dirname = dlg.selectedFiles()[0]
            exp = load_exp(dirname)
            self.exp = exp
            self.file_thread.set_experiment(self.exp)
            self.clear_windows()
            self.set_windows()
    @Slot()
    def OnSaveExperiment(self):
        self.exp.save()

    @Slot()
    def OnLoadScript(self):
        dlg = QFileDialog()
        if dlg.exec_():
            _script = dlg.selectedFiles()[0]
            self.exp.set_analysis_script(_script)
            self.clear_windows()
            self.set_windows()
    @Slot()
    def OnReloadScript(self):
        # Load from data folder instead of script folder
        _script = os.path.join(self.exp.script_dir, self.exp.script_filename)
        _params = self.exp.get_parameters() # Preserve the parameters when reload
        self.exp.set_analysis_script(_script)
        self.exp.set_parameters(_params) # Set to current parameters
        self.clear_windows()
        self.set_windows()

    @Slot()
    def OnRecord(self):
        _status = self.btn_idle.isChecked()
        if self.file_thread == None: # Restart the file thread if it crashed
            self.start_file_thread()
        self.file_thread.set_save(_status)
        if _status:
            self.btn_idle.setStyleSheet("background-color : green")
        else:
            self.btn_idle.setStyleSheet("background-color : red")
        return 1

    @Slot(int)
    def add_result(self, data_id):
        self.data_table.add_run(data_id)
        self.replot()

    @Slot()
    def update_figures(self): # Refresh the GUI for new figures. 
        for _name in self.figs.keys():
            self.figs[_name].draw()
        return 1

    def load_analysis_script(self, filename):
        self.exp.set_analysis_script(filename)
        # self.ui.mdiArea.removeSubWindow(self.ParameterWindow)
        self.analysis_parameters = Parameter(self.exp, self)
        self.ParameterWindow.setWidget(self.analysis_parameters)
        # self.ui.mdiArea.addSubWindow(self.ParameterWindow)

if __name__ == "__main__":
    if os.name == 'nt':
        from os import system
        system("title "+"Experiment Note Atom Cloud")
    else:
        print('\33]0;Experiment Note\a', end='', flush=True)

    # These are few lines of magic code to not let the windows group the task bar icons
    if os.name == 'nt':
        import ctypes
        myappid = u'fermi2.ExperimentControl.ExperimentNote.1.0.AtomCloud' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow(Experiment())
    window.show()
    sys.exit(app.exec_())
    
