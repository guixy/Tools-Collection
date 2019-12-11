#-*- coding:utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QMessageBox, QVBoxLayout, QSizePolicy, QWidget

from PyQt5.QtGui import QIcon
import xlrd
import matplotlib.pyplot as plt
class oringin:
    def __init__(self,path):
        self.path=path
    def readExcel(self):
        workbook1 = xlrd.open_workbook(filename=self.path)
        if self.path != "":
            sheet = workbook1.sheet_by_name('DD')
            #sheet = workbook1.sheets()[]

            # sheet = workbook1.sheet_by_name(name)
            #TODO这里是1的原因是因为这是修改后的表，实际的表这里应该是0
            row = sheet.row_values(1)

            needkk=3

            for i in range(0,len(row)):

                if row[i] == "N_dem_E":
                    N_dem_E_col = sheet.col_values(i)[needkk:]
                if row[i] == "T_dem_E":
                    T_dem_E_col = sheet.col_values(i)[needkk:]



                if row[i] =="DC_ACT_I":
                    DC_col1=sheet.col_values(i)[needkk:]
                if row[i] =="DC_ACT_U":
                    DC_col2 = sheet.col_values(i)[needkk:]
                if row[i] =="EFF_CON":
                    EFF_CON_col=sheet.col_values(i)[needkk:]
                if row[i] =="EFF_MOT":
                    EFF_MOT_col = sheet.col_values(i)[needkk:]
                if row[i] == "EFF_SYS":
                    EFF_SYS_col = sheet.col_values(i)[needkk:]
                if row[i] == "IGBT_TEMP_U":
                    IGBT_col=[]
                    IGBT_col1 = sheet.col_values(i)[needkk:]
                    IGBT_col2 = sheet.col_values(i+1)[needkk:]
                    IGBT_col3 = sheet.col_values(i+2)[needkk:]
                    for j in range(0,len(IGBT_col1)):
                        if IGBT_col1[j]>=IGBT_col2[j] and IGBT_col1[j]>=IGBT_col3[j]:
                            IGBT_col.append(IGBT_col1[j])
                        elif IGBT_col2[j]>=IGBT_col3[j]:
                            IGBT_col.append(IGBT_col2[j])
                        else:
                            IGBT_col.append(IGBT_col3[j])
                if row[i] == "IrmsA":

                    IrmsA_col = sheet.col_values(i)[needkk:]

                if row[i] == "P":
                    P_col = sheet.col_values(i)[needkk:]
                if row[i] == "TM_TEMP":
                    TM_TEMP_col = []

                    TM_TEMP_col1 = sheet.col_values(i)[needkk:]

                    TM_TEMP_col2 = sheet.col_values(i+1)[needkk:]
                    for jj in range(0,len(TM_TEMP_col1)):
                        if TM_TEMP_col1[j]>=TM_TEMP_col2[j]:

                            TM_TEMP_col.append(TM_TEMP_col1[j])
                        else:
                            TM_TEMP_col.append(TM_TEMP_col2[j])

                if row[i] == "TORQUE":
                    TORQUE_col = sheet.col_values(i)[needkk:]
                if row[i] == "UrmsA":
                    UrmsA_col = sheet.col_values(i)[needkk:]
            self.N_dem_E=[N_dem_E_col[0]]
            self.T_dem_E=[T_dem_E_col[0]]
            self.DC1=[DC_col1[0]]
            self.DC2=[DC_col2[0]]
            self.EFF_CON=[EFF_CON_col[00]]
            self.EFF_MOT=[EFF_MOT_col[0]]
            self.EFF_SYS=[EFF_SYS_col[0]]
            self.IGBT=[N_dem_E_col[0]]
            self.IrmsA=[IrmsA_col[0]]
            self.P=[P_col[0]]
            self.TM_TEMP=[TM_TEMP_col[0]]
            self.TORQUE=[TORQUE_col[0]]
            self.UrmsA=[UrmsA_col[0]]
            max1 = T_dem_E_col[1]
            for ii in range(1,len(N_dem_E_col)):

                #if N_dem_E_col[ii]<N_dem_E_col[ii-1] or T_dem_E_col[ii]<T_dem_E_col[ii-1] or TORQUE_col[ii]<TORQUE_col[ii-1]:
                if T_dem_E_col[ii]<max1:
                    pass
                else:
                    max1=T_dem_E_col[ii]
                    self.N_dem_E.append(N_dem_E_col[ii])
                    self.T_dem_E .append(T_dem_E_col[ii])
                    self.DC1.append(DC_col1[ii])
                    self.DC2 .append(DC_col2[ii])
                    self.EFF_CON .append(EFF_CON_col[ii])
                    self.EFF_MOT .append(EFF_MOT_col[ii])
                    self.EFF_SYS .append(EFF_SYS_col[ii])
                    self.IGBT .append(IGBT_col[ii])
                    self.IrmsA .append(IrmsA_col[ii])
                    self.P .append(P_col[ii])
                    self.TM_TEMP .append(TM_TEMP_col[ii])
                    self.TORQUE .append(TORQUE_col[ii])
                    self.UrmsA.append(UrmsA_col[ii])

            #row1 = sheet.row_values(0)

            #self.singalesDIC = {}

    def PaintMAP(self):
        sp_step=30;     #%%%转速细分
        tor_step=2;   #%%%转矩细分
        print(self.T_dem_E)
        plt.plot(self.N_dem_E,self.TORQUE)

        plt.show()
        
a=oringin("EI09_B_MAP_350V_DD_20191011_WT.xls")
a.readExcel()
a.PaintMAP()
