from PyQt5.QtWidgets import  *
import sys

import shutil
from DramMap import *
from PaintMAPGUI import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import  os
import  re

import time
import traceback
from threading import Thread

class EmittingStr(QObject):
    textWritten = pyqtSignal(str) #定义一个发送str的信号
    def write(self, text):
      self.textWritten.emit(str(text))

class basePage(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(basePage, self).__init__()


        self.setWindowTitle('Icon')

        self.setWindowIcon(QIcon(os.getcwd()+'/windowsicon.png'))

        #self.setWindowIcon(QIcon('./windowsicon.PNG'))
        self.setupUi(self)
        self.ChooseFileFlag = False
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        self.actionOpen_excel.triggered.connect(self.OpenExcel)
        self.paint1.clicked.connect(self.PaintMap1)
        self.paint2.clicked.connect(self.PaintMap2)
        self.paint3.clicked.connect(self.PaintMap3)
        self.paint4.clicked.connect(self.PaintMap4)
        self.barlabel = QLabel()
        self.statusbara.addPermanentWidget(self.barlabel)
        self.barlabel.setText('未选择Excel')


    def OpenExcel(self):
        '''选择Excel文件'''
        dir,file = QFileDialog.getOpenFileName()
        self.dir=dir
        if dir!="":
            self.ChooseFileFlag=True
            self.paint1.setEnabled(False)
            self.paint2.setEnabled(False)
            self.paint3.setEnabled(False)
            self.paint4.setEnabled(False)

            print("reading excel..... wait seceonds please")

            self.barlabel.setText('选择的Excel是：' + dir)

            t = Thread(target=self.ReadExcelAndAnalyse)
            t.start()



    def ReadExcelAndAnalyse(self):
        try:
            self.DrawMap = oringin(self.dir)

            self.DrawMap.readExcel()
            self.paint1.setEnabled(True)
            self.paint2.setEnabled(True)
            self.paint3.setEnabled(True)
            self.paint4.setEnabled(True)
        except:
            print(traceback.print_exc())
            self.paint1.setEnabled(True)
            self.paint2.setEnabled(True)
            self.paint3.setEnabled(True)
            self.paint4.setEnabled(True)


    def PaintMap1(self):
        '''画外特性图'''
        if self.ChooseFileFlag:
            self.DrawMap.PaintMAP()
        else:
            QMessageBox.about(self, "消息", "请先选择Excel文件！")



    def PaintMap2(self):
        '''画原始MAP图'''
        if self.ChooseFileFlag:

            if self.lineEdit_2.text()=="":
                QMessageBox.about(self, "消息", "请先设置上下限以及步长！")
            else:
                if '；' in self.lineEdit_2.text() or "：" in self.lineEdit_2.text() or "，"in self.lineEdit_2.text() or ';' in self.lineEdit_2.text():
                    QMessageBox.about(self, "消息", "输入有非法字符！")
                else:
                    try:

                        self.DrawMap.ChooseMAP1(self.lineEdit.text(),self.lineEdit_2.text())
                    except Exception as e:
                        print(str(e))
        else:
            QMessageBox.about(self, "消息", "请先选择Excel文件！")




    def PaintMap3(self):
        '''画优化MAP图'''
        if self.ChooseFileFlag:
            if self.lineEdit_2.text()=="":
                QMessageBox.about(self, "消息", "请先设置上下限以及步长！")
            else:
                if '；' in self.lineEdit_2.text() or "：" in self.lineEdit_2.text() or "，"in self.lineEdit_2.text() or ';' in self.lineEdit_2.text():
                    QMessageBox.about(self, "消息", "输入有非法字符！")
                else:
                    try:
                        self.DrawMap.OptmizeMapData(self.lineEdit.text(),self.lineEdit_2.text())
                    except Exception as e:
                        print(traceback.print_exc())
        else:
            QMessageBox.about(self, "消息", "请先选择Excel文件！")
    def PaintMap4(self):
        '''画温度图'''
        if self.ChooseFileFlag:
            #if self.lineEdit_2.text()=="":
                #QMessageBox.about(self, "消息", "请先设置上下限以及步长！")
            #else:
                #if '；' in self.lineEdit_2.text() or "：" in self.lineEdit_2.text() or "，"in self.lineEdit_2.text() or ';' in self.lineEdit_2.text():
                    #QMessageBox.about(self, "消息", "输入有非法字符！")
                #else:
                    try:
                        self.DrawMap.PaintTempMap()
                    except Exception as e:
                        print(str(e))
        else:
            QMessageBox.about(self, "消息", "请先选择Excel文件！")

    def outputWritten(self, text):
        '''打印消息到控制台里'''
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    a=basePage()
    a.show()
    a.setWindowIcon(QIcon(os.getcwd()+'/windowsicon.png'))
    a.setFixedSize(a.width(), a.height())#禁止窗口大小变化

    #进入程序的主循环，并通过exit函数确保主循环安全结束
    sys.exit(app.exec_())
