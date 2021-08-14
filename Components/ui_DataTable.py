# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DataTable.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_DataTable(object):
    def setupUi(self, DataTable):
        DataTable.setObjectName("DataTable")
        DataTable.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(DataTable)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tb_DataFrame = QtWidgets.QTableWidget(DataTable)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_DataFrame.sizePolicy().hasHeightForWidth())
        self.tb_DataFrame.setSizePolicy(sizePolicy)
        self.tb_DataFrame.setRowCount(5)
        self.tb_DataFrame.setColumnCount(5)
        self.tb_DataFrame.setObjectName("tb_DataFrame")
        self.tb_DataFrame.horizontalHeader().setVisible(True)
        self.tb_DataFrame.horizontalHeader().setDefaultSectionSize(80)
        self.tb_DataFrame.horizontalHeader().setHighlightSections(True)
        self.tb_DataFrame.verticalHeader().setDefaultSectionSize(20)
        self.tb_DataFrame.verticalHeader().setMinimumSectionSize(21)
        self.verticalLayout.addWidget(self.tb_DataFrame)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(DataTable)
        QtCore.QMetaObject.connectSlotsByName(DataTable)

    def retranslateUi(self, DataTable):
        _translate = QtCore.QCoreApplication.translate
        DataTable.setWindowTitle(_translate("DataTable", "Form"))

