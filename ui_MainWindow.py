# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionDataTable = QAction(MainWindow)
        self.actionDataTable.setObjectName(u"actionDataTable")
        self.actionDataTable.setCheckable(True)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionTileWindows = QAction(MainWindow)
        self.actionTileWindows.setObjectName(u"actionTileWindows")
        self.actionWindows = QAction(MainWindow)
        self.actionWindows.setObjectName(u"actionWindows")
        self.actionTile_Figures = QAction(MainWindow)
        self.actionTile_Figures.setObjectName(u"actionTile_Figures")
        self.actionFull_Screen_F11 = QAction(MainWindow)
        self.actionFull_Screen_F11.setObjectName(u"actionFull_Screen_F11")
        self.actionReloadScript = QAction(MainWindow)
        self.actionReloadScript.setObjectName(u"actionReloadScript")
        self.actionLoadScript = QAction(MainWindow)
        self.actionLoadScript.setObjectName(u"actionLoadScript")
        self.actionParameters = QAction(MainWindow)
        self.actionParameters.setObjectName(u"actionParameters")
        self.actionParameters.setCheckable(True)
        self.actionFigure = QAction(MainWindow)
        self.actionFigure.setObjectName(u"actionFigure")
        self.actionOpenWindows = QAction(MainWindow)
        self.actionOpenWindows.setObjectName(u"actionOpenWindows")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.mdiArea = QMdiArea(self.centralwidget)
        self.mdiArea.setObjectName(u"mdiArea")
        sizePolicy.setHeightForWidth(self.mdiArea.sizePolicy().hasHeightForWidth())
        self.mdiArea.setSizePolicy(sizePolicy)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.mdiArea.setViewMode(QMdiArea.SubWindowView)
        self.mdiArea.setTabsClosable(False)
        self.mdiArea.setTabShape(QTabWidget.Triangular)
        self.mdiArea.setTabPosition(QTabWidget.South)

        self.verticalLayout.addWidget(self.mdiArea)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuAnalysis = QMenu(self.menubar)
        self.menuAnalysis.setObjectName(u"menuAnalysis")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuAnalysis.menuAction())
        self.menuView.addAction(self.actionTileWindows)
        self.menuView.addAction(self.actionOpenWindows)
        self.menuAnalysis.addAction(self.actionLoadScript)
        self.menuAnalysis.addAction(self.actionReloadScript)
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionDataTable.setText(QCoreApplication.translate("MainWindow", u"Data Table", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
#if QT_CONFIG(shortcut)
        self.actionNew.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionTileWindows.setText(QCoreApplication.translate("MainWindow", u"Tile Windows", None))
#if QT_CONFIG(shortcut)
        self.actionTileWindows.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+T", None))
#endif // QT_CONFIG(shortcut)
        self.actionWindows.setText(QCoreApplication.translate("MainWindow", u"Windows", None))
        self.actionTile_Figures.setText(QCoreApplication.translate("MainWindow", u"Tile Figures", None))
        self.actionFull_Screen_F11.setText(QCoreApplication.translate("MainWindow", u"Full Screen (F11)", None))
        self.actionReloadScript.setText(QCoreApplication.translate("MainWindow", u"Reload Script", None))
#if QT_CONFIG(shortcut)
        self.actionReloadScript.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.actionLoadScript.setText(QCoreApplication.translate("MainWindow", u"Load Script", None))
#if QT_CONFIG(shortcut)
        self.actionLoadScript.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+L", None))
#endif // QT_CONFIG(shortcut)
        self.actionParameters.setText(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.actionFigure.setText(QCoreApplication.translate("MainWindow", u"Figures", None))
        self.actionOpenWindows.setText(QCoreApplication.translate("MainWindow", u"Open Windows", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuAnalysis.setTitle(QCoreApplication.translate("MainWindow", u"Analysis", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

