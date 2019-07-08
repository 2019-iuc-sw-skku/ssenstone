# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FE1.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import pickle

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(614, 493)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(90, 120, 401, 191))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.la_Model = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.la_Model.setFont(font)
        self.la_Model.setAlignment(QtCore.Qt.AlignCenter)
        self.la_Model.setObjectName("la_Model")
        self.gridLayout.addWidget(self.la_Model, 0, 0, 1, 1)
        self.la_RSEED = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.la_RSEED.setFont(font)
        self.la_RSEED.setAlignment(QtCore.Qt.AlignCenter)
        self.la_RSEED.setObjectName("la_RSEED")
        self.gridLayout.addWidget(self.la_RSEED, 1, 0, 1, 1)
        self.line_RSEED = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.line_RSEED.setObjectName("line_RSEED")
        self.gridLayout.addWidget(self.line_RSEED, 1, 2, 1, 1)
        self.line_Model = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.line_Model.setObjectName("line_Model")
        self.gridLayout.addWidget(self.line_Model, 0, 2, 1, 1)
        self.la_TESTP = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.la_TESTP.setFont(font)
        self.la_TESTP.setAlignment(QtCore.Qt.AlignCenter)
        self.la_TESTP.setObjectName("la_TESTP")
        self.gridLayout.addWidget(self.la_TESTP, 2, 0, 1, 1)
        self.la_FNAME = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.la_FNAME.setFont(font)
        self.la_FNAME.setAlignment(QtCore.Qt.AlignCenter)
        self.la_FNAME.setObjectName("la_FNAME")
        self.gridLayout.addWidget(self.la_FNAME, 3, 0, 1, 1)
        self.line_TESTP = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.line_TESTP.setObjectName("line_TESTP")
        self.gridLayout.addWidget(self.line_TESTP, 2, 2, 1, 1)
        self.line_FNAME = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.line_FNAME.setObjectName("line_FNAME")
        self.gridLayout.addWidget(self.line_FNAME, 3, 2, 1, 1)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(190, 370, 195, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.OKButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.OKButton.setObjectName("OKButton")
        self.horizontalLayout.addWidget(self.OKButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.retranslateUi(Dialog)
        self.OKButton.clicked.connect(self.OKbutton_click)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.la_Model.setText(_translate("Dialog", "Model"))
        self.la_RSEED.setText(_translate("Dialog", "R_Seed"))
        self.la_TESTP.setText(_translate("Dialog", "Test_Per"))
        self.la_FNAME.setText(_translate("Dialog", "File Name"))
        self.OKButton.setText(_translate("Dialog", "OK"))
        self.pushButton_2.setText(_translate("Dialog", "Exit"))

    def OKbutton_click(self):
        modelNumber=self.line_Model.text()
        randomSeed=self.line_RSEED.text()
        testPer=self.line_TESTP.text()
        fileName=self.line_FNAME.text()
        # self.la_FNAME.setText(fileName) #test
        list={'modelNumber','randomSeed', 'testPer','fileName'}
        with open('list.txt','wb') as f:
            pickle.dump(list, f)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
