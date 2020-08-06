# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NewExpDialog.ui'
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


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 98)
        self.horizontalLayout = QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_ExpName = QLabel(Dialog)
        self.label_ExpName.setObjectName(u"label_ExpName")

        self.gridLayout.addWidget(self.label_ExpName, 0, 0, 1, 2)

        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 0, 2, 1, 1)

        self.label_ExpScript = QLabel(Dialog)
        self.label_ExpScript.setObjectName(u"label_ExpScript")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ExpScript.sizePolicy().hasHeightForWidth())
        self.label_ExpScript.setSizePolicy(sizePolicy)
        self.label_ExpScript.setMaximumSize(QSize(150, 16777215))

        self.gridLayout.addWidget(self.label_ExpScript, 1, 0, 1, 1)

        self.label_ExpScriptFile = QLabel(Dialog)
        self.label_ExpScriptFile.setObjectName(u"label_ExpScriptFile")
        font = QFont()
        font.setUnderline(True)
        self.label_ExpScriptFile.setFont(font)
        self.label_ExpScriptFile.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridLayout.addWidget(self.label_ExpScriptFile, 1, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_ExpName.setText(QCoreApplication.translate("Dialog", u"Experiment Name: ", None))
        self.label_ExpScript.setText(QCoreApplication.translate("Dialog", u"Script: ", None))
        self.label_ExpScriptFile.setText(QCoreApplication.translate("Dialog", u"None", None))
    # retranslateUi

