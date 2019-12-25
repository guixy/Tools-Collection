from PyQt5.QtWidgets import  *
import sys

import shutil

import PaintMAPGUI
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import  os
import  re
import subprocess
import time



class basePage(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(basePage, self).__init__()
        self.setupUi(self)



if __name__ == '__main__':
    cmd1 = ""
    NUM=0
    VAL=0
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('./Compile/mainwindowIcon.png'))

    a=basePage()

    a.ChooseProDir()



    a.show()

    #进入程序的主循环，并通过exit函数确保主循环安全结束
    sys.exit(app.exec_())
