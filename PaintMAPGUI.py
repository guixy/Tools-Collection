# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PaintMAPGUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1041, 382)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.paint1 = QtWidgets.QPushButton(self.centralwidget)
        self.paint1.setGeometry(QtCore.QRect(10, 30, 121, 23))
        self.paint1.setObjectName("paint1")
        self.paint2 = QtWidgets.QPushButton(self.centralwidget)
        self.paint2.setGeometry(QtCore.QRect(10, 70, 121, 23))
        self.paint2.setObjectName("paint2")
        self.paint3 = QtWidgets.QPushButton(self.centralwidget)
        self.paint3.setGeometry(QtCore.QRect(10, 110, 121, 23))
        self.paint3.setObjectName("paint3")
        self.save = QtWidgets.QPushButton(self.centralwidget)
        self.save.setGeometry(QtCore.QRect(10, 150, 121, 23))
        self.save.setObjectName("save")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(140, 160, 881, 161))
        self.groupBox.setObjectName("groupBox")
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser.setGeometry(QtCore.QRect(0, 30, 881, 131))
        self.textBrowser.setObjectName("textBrowser")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(140, 20, 881, 131))
        self.groupBox_2.setObjectName("groupBox_2")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(20, 20, 61, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit.setGeometry(QtCore.QRect(90, 20, 771, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(150, 50, 711, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(20, 52, 121, 20))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1041, 23))
        self.menubar.setObjectName("menubar")
        self.menua = QtWidgets.QMenu(self.menubar)
        self.menua.setObjectName("menua")
        MainWindow.setMenuBar(self.menubar)
        self.statusbara = QtWidgets.QStatusBar(MainWindow)
        self.statusbara.setObjectName("statusbara")
        MainWindow.setStatusBar(self.statusbara)
        self.actionOpen_excel = QtWidgets.QAction(MainWindow)
        self.actionOpen_excel.setObjectName("actionOpen_excel")
        self.menua.addAction(self.actionOpen_excel)
        self.menubar.addAction(self.menua.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MAPDrawing"))
        self.paint1.setText(_translate("MainWindow", "绘制外特性图"))
        self.paint2.setText(_translate("MainWindow", "绘制原始MAP图"))
        self.paint3.setText(_translate("MainWindow", "优化MAP图"))
        self.save.setText(_translate("MainWindow", "保存图"))
        self.groupBox.setTitle(_translate("MainWindow", "控制台"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.groupBox_2.setTitle(_translate("MainWindow", "MAP图参数设置"))
        self.label.setText(_translate("MainWindow", "图形名称："))
        self.label_2.setText(_translate("MainWindow", "设置上下限以及步长："))
        self.menua.setTitle(_translate("MainWindow", "打开文件"))
        self.actionOpen_excel.setText(_translate("MainWindow", "Open excel"))
