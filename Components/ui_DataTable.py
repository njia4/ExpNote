# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DataTable.ui'
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


class Ui_DataTable(object):
    def setupUi(self, DataTable):
        if not DataTable.objectName():
            DataTable.setObjectName(u"DataTable")
        DataTable.resize(400, 300)
        self.gridLayout = QGridLayout(DataTable)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tb_DataFrame = QTableWidget(DataTable)
        if (self.tb_DataFrame.columnCount() < 5):
            self.tb_DataFrame.setColumnCount(5)
        if (self.tb_DataFrame.rowCount() < 5):
            self.tb_DataFrame.setRowCount(5)
        self.tb_DataFrame.setObjectName(u"tb_DataFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_DataFrame.sizePolicy().hasHeightForWidth())
        self.tb_DataFrame.setSizePolicy(sizePolicy)
        self.tb_DataFrame.setRowCount(5)
        self.tb_DataFrame.setColumnCount(5)
        self.tb_DataFrame.verticalHeader().setMinimumSectionSize(21)
        self.tb_DataFrame.verticalHeader().setDefaultSectionSize(20)

        self.verticalLayout.addWidget(self.tb_DataFrame)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(DataTable)

        QMetaObject.connectSlotsByName(DataTable)
    # setupUi

    def retranslateUi(self, DataTable):
        DataTable.setWindowTitle(QCoreApplication.translate("DataTable", u"Form", None))
    # retranslateUi

