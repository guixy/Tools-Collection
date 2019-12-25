#-*- coding:utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QMessageBox, QVBoxLayout, QSizePolicy, QWidget

from PyQt5.QtGui import QIcon
import xlrd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.interpolate import *
import  math
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

                if row[i] == "N_dem_E":#speed
                    self.N_dem_E_col = sheet.col_values(i)[needkk:]
                if row[i] == "N_dem_D":
                    self.N_dem_D_col = sheet.col_values(i)[needkk:]

                if row[i] == "T_dem_E":
                    self.T_dem_E_col = sheet.col_values(i)[needkk:]



                if row[i] =="DC_ACT_I":
                    self.DC_col1=sheet.col_values(i)[needkk:]
                if row[i] =="DC_ACT_U":
                    self.DC_col2 = sheet.col_values(i)[needkk:]
                if row[i] =="EFF_CON":
                    self.EFF_CON_col=sheet.col_values(i)[needkk:]
                if row[i] =="EFF_MOT":
                    self.EFF_MOT_col = sheet.col_values(i)[needkk:]
                if row[i] == "EFF_SYS":
                    self.EFF_SYS_col = sheet.col_values(i)[needkk:]

                if row[i] == "IGBT_TEMP_U":
                    self.IGBT_col=[]
                    IGBT_col1 = sheet.col_values(i)[needkk:]

                    IGBT_col2 = sheet.col_values(i+1)[needkk:]
                    IGBT_col3 = sheet.col_values(i+2)[needkk:]
                    for j in range(0,len(IGBT_col1)):
                        if IGBT_col1[j]>=IGBT_col2[j] and IGBT_col1[j]>=IGBT_col3[j]:
                            self.IGBT_col.append(IGBT_col1[j])
                        elif IGBT_col2[j]>=IGBT_col3[j]:
                            self.IGBT_col.append(IGBT_col2[j])
                        else:
                            self.IGBT_col.append(IGBT_col3[j])
                if row[i] == "IrmsA":
                    self.IrmsA_col = sheet.col_values(i)[needkk:]

                if row[i] == "P":
                    self.P_col = sheet.col_values(i)[needkk:]
                if row[i] == "TM_TEMP":
                    self.TM_TEMP_col = []

                    TM_TEMP_col1 = sheet.col_values(i)[needkk:]

                    TM_TEMP_col2 = sheet.col_values(i+1)[needkk:]
                    for jj in range(0,len(TM_TEMP_col1)):
                        if TM_TEMP_col1[j]>=TM_TEMP_col2[j]:

                            self.TM_TEMP_col.append(TM_TEMP_col1[j])
                        else:
                            self.TM_TEMP_col.append(TM_TEMP_col2[j])

                if row[i] == "TORQUE":
                    self.TORQUE_col = sheet.col_values(i)[needkk:]

                if row[i] == "UrmsA":
                    self.UrmsA_col = sheet.col_values(i)[needkk:]
            self.Num = 0
            self.list = locals()
            self.CreateList()
            self.AnalyseData()




            '''max1 = N_dem_E_col[0]
            max2 = T_dem_E_col[0]
            max3 = TORQUE_col[0]
            self.N_dem_E = []
            self.N_dem_E.append(N_dem_E_col[0])
            for ii in range(0,len(N_dem_E_col)):

                #if N_dem_E_col[ii]<N_dem_E_col[ii-1] or T_dem_E_col[ii]<T_dem_E_col[ii-1] or TORQUE_col[ii]<TORQUE_col[ii-1]:
                if N_dem_E_col[ii]<max1 :
                    pass
                else:

                    if max1 == N_dem_E_col[ii]:

                        if T_dem_E_col[ii]<max2 or TORQUE_col[ii]<max3:

                            pass
                        else:

                            #self.list["N_dem_E" + str(self.Num)].append(N_dem_E_col[ii])
                            self.list["T_dem_E" + str(self.Num)].append(T_dem_E_col[ii])

                            self.list["DC1" + str(self.Num)].append(DC_col1[ii])
                            self.list["DC2" + str(self.Num)].append(DC_col2[ii])
                            self.list["EFF_CON" + str(self.Num)].append(EFF_CON_col[ii])
                            self.list["EFF_MOT" + str(self.Num)].append(EFF_MOT_col[ii])
                            self.list["EFF_SYS" + str(self.Num)].append(EFF_SYS_col[ii])
                            self.list["IGBT" + str(self.Num)].append(IGBT_col[ii])
                            self.list["IrmsA" + str(self.Num)].append(IrmsA_col[ii])
                            self.list["P" + str(self.Num)].append(P_col[ii])
                            self.list["TM_TEMP" + str(self.Num)].append(TM_TEMP_col[ii])
                            self.list["TORQUE" + str(self.Num)].append(TORQUE_col[ii])
                            self.list["UrmsA" + str(self.Num)].append(UrmsA_col[ii])

                    else:

                        max1 = N_dem_E_col[ii]
                        self.Num=self.Num+1
                        self.N_dem_E.append(N_dem_E_col[ii])
                        self.CreateList()
                        #self.list["N_dem_E" + str(self.Num)].append(N_dem_E_col[ii])
                        self.list["T_dem_E" + str(self.Num)].append(T_dem_E_col[ii])
                        self.list["DC1" + str(self.Num)].append(DC_col1[ii])
                        self.list["DC2" + str(self.Num)].append(DC_col2[ii])
                        self.list["EFF_CON" + str(self.Num)].append(EFF_CON_col[ii])
                        self.list["EFF_MOT" + str(self.Num)].append(EFF_MOT_col[ii])
                        self.list["EFF_SYS" + str(self.Num)].append(EFF_SYS_col[ii])
                        self.list["IGBT" + str(self.Num)].append(IGBT_col[ii])
                        self.list["IrmsA" + str(self.Num)].append(IrmsA_col[ii])
                        self.list["P" + str(self.Num)].append(P_col[ii])
                        self.list["TM_TEMP" + str(self.Num)].append(TM_TEMP_col[ii])
                        self.list["TORQUE" + str(self.Num)].append(TORQUE_col[ii])
                        self.list["UrmsA" + str(self.Num)].append(UrmsA_col[ii])
                        '''






    def CreateList(self):
        self.list["N_dem_E"+str(self.Num)]=[]
        self.list["T_dem_E" + str(self.Num)] = []
        self.list["DC1" + str(self.Num)] = []
        self.list["DC2" + str(self.Num)] = []
        self.list["EFF_CON" + str(self.Num)] = []
        self.list["EFF_MOT" + str(self.Num)] = []
        self.list["EFF_SYS" + str(self.Num)] = []
        self.list["IGBT" + str(self.Num)] = []
        self.list["IrmsA" + str(self.Num)] = []
        self.list["P"+str(self.Num)]=[]
        self.list["TM_TEMP" + str(self.Num)] = []
        self.list["TORQUE" + str(self.Num)] = []
        self.list["UrmsA" + str(self.Num)] = []
    def ChooseMAP1(self):
        maxsys = self.efficient_sys[0]
        maxtm = self.efficient_tm[0]
        maxtmi = self.efficient_tmi[0]
        for i in range(1, len(self.efficient_sys)):
            if self.efficient_sys[i] > maxsys:
                maxsys = self.efficient_sys[i]
                maxsysN = i
            if self.efficient_tm[i] > maxtm:
                maxtm = self.efficient_tm[i]
                maxtmN = i
            if self.efficient_tmi[i] > maxtmi:
                maxtmi = self.efficient_tmi[i]
                maxtmiN = i
        self.InterData(self.efficient_tmi,self.efficient_tm,self.efficient_sys,maxsys,maxtm,maxtmi)
        self.PaintMAP1()

    def PaintMAP(self):

        #figure1
        fig, ax = plt.subplots(num=None, figsize=(13, 8), dpi=60, facecolor='w', edgecolor='k')

        l1 = ax.plot(self.speed_maxs, self.torque_maxs, 'bs-', label='扭矩')
        plt.xlabel("转速(rpm)")
        # 共享x轴，生成次坐标轴
        ax_sub = ax.twinx()
        l2 = ax_sub.plot(self.speed_maxs, self.power_maxs, 'rs-', label='功率')
        fig.legend(loc=1, bbox_to_anchor=(1, 1), bbox_transform=ax.transAxes)
        ax.set_ylabel('扭矩(Nm)')
        ax_sub.set_ylabel('功率(kw)')
        '''for a, b in zip(self.speed_base, self.torque_ec):
            ax.text(a-50, b + 0.02*300, '1' % b, ha='center', va='bottom', fontsize=8,fontweight='bold',color='b')

        for a, b in zip(self.speed_base, self.power_ec):
            ax_sub.text(a+50, b+3, '%s' % b, ha='center', va='bottom', fontsize=8.8,color='r')'''
        torque_y = 280
        torque_step = 20
        power_y = 170

        for  i in range(0,len(self.speed_maxs)):
            ax.text(self.speed_maxs[i] - 50, self.torque_maxs[i] + 0.03 * torque_y, str(self.torque_maxs[i]), fontsize=12,fontweight='bold', color='b')
            ax_sub.text(self.speed_maxs[i] + 50, self.power_maxs[i] + 0.01 * torque_y,
                 str(round(self.power_maxs[i] * 100) / 100), fontsize=12,fontweight='bold', color='r')





        plt.show()


    def PaintMAP1(self):

        # figure2
        fig2 = plt.figure()
        plt.ylabel('扭矩(Nm)')
        plt.xlabel("转速(rpm)")

        # ax2 = fig2.add_subplot(111, projection='3d')
        # surf= ax.plot_surface(self.X,self.Y,self.zz1)

        contour = plt.contour(self.X, self.Y, self.zz1, self.T1)
        plt.clabel(contour, inline=True, fontsize=12, fmt='%1.1f')
        plt.plot(self.speed300, self.trq_max_serial, 'r-', linewidth=1.5)
        plt.title('控制器效率')

        # figure3
        fig3 = plt.figure()
        plt.ylabel('扭矩(Nm)')
        plt.xlabel("转速(rpm)")

        # ax2 = fig2.add_subplot(111, projection='3d')
        # surf= ax.plot_surface(self.X,self.Y,self.zz1)

        contour = plt.contour(self.X, self.Y, self.zz2, self.T1)
        plt.clabel(contour, inline=True, fontsize=12, fmt='%1.1f')
        plt.plot(self.speed300, self.trq_max_serial, 'r-', linewidth=1.5)
        plt.title('电机效率')

        # figure4
        fig4 = plt.figure()
        plt.ylabel('扭矩(Nm)')
        plt.xlabel("转速(rpm)")

        # ax2 = fig2.add_subplot(111, projection='3d')
        # surf= ax.plot_surface(self.X,self.Y,self.zz1)

        contour = plt.contour(self.X, self.Y, self.zz3, self.T1)
        plt.clabel(contour, inline=True, fontsize=12, fmt='%1.1f')
        plt.plot(self.speed300, self.trq_max_serial, 'r-', linewidth=1.5)
        plt.title('系统效率')
        plt.show()

    def OptmizeMapData(self):
        efficient_sys=self.efficient_sys
        efficient_tm=self.efficient_tm
        efficient_tmi=self.efficient_tmi
        for ii in range(0,len(self.speed_matrix)):
            if ii==0:
                length=0
                maxsys = self.efficient_sys[ii]
                maxtm = self.efficient_tm[ii]
                maxtmi = self.efficient_tmi[ii]
            else:
                length=ii*len(self.speed_matrix[ii])-1
                maxsys = self.efficient_sys[ii*len(self.speed_matrix[ii])-1]
                maxtm = self.efficient_tm[ii*len(self.speed_matrix[ii])-1]
                maxtmi = self.efficient_tmi[ii*len(self.speed_matrix[ii])-1]

            for j in range(1,len(self.speed_matrix[ii])):


                #for i in range(1, len(self.efficient_sys)):
                    if self.efficient_sys[length+j] > maxsys:
                        maxsys = self.efficient_sys[length+j]
                        maxsysN = j
                    if self.efficient_tm[length+j] > maxtm:
                        maxtm = efficient_tm[length+j]
                        maxtmN = j
                    if efficient_tmi[length+j] > maxtmi:
                        maxtmi = efficient_tmi[length+j]
                        maxtmiN = j
            sysNow = self.efficient_sys[length]
            tmNow = self.efficient_tm[length]
            tmiNow = self.efficient_tmi[length]
            for i in range(1, len(self.speed_matrix[ii])):
                    if i < maxsysN:
                        if efficient_sys[length+i] < efficient_sys[i +length- 1]:
                            efficient_sys[length+i] = efficient_sys[length+i - 1] + (maxsys - efficient_sys[length+i - 1]) / (
                            maxsysN - i)
                    elif i > maxsysN:
                        if efficient_sys[length+i] > efficient_sys[length+i - 1]:
                            efficient_sys[length+i] = efficient_sys[length+i - 1] - (maxsys - efficient_sys[length+i - 1]) / (
                            i - maxsysN)
                    if i<maxtmN:
                        if efficient_tm[length+i] < efficient_tm[length+i - 1]:
                            efficient_tm[length+i] = efficient_tm[length+i - 1] + (maxtm - efficient_tm[length+i - 1]) / (
                                maxtmN - i)
                    elif i > maxtmN:
                        if efficient_tm[length+i] > efficient_tm[length+i - 1]:
                            efficient_tm[length+i] = efficient_tm[length+i - 1] - (maxtm - efficient_tm[length+i - 1]) / (
                                i - maxtmN)
                    if i<maxtmiN:
                        if efficient_tmi[length+i] < efficient_tmi[length+i - 1]:
                            efficient_tmi[length+i] = efficient_tmi[length+i - 1] + (maxtmi - efficient_tmi[length+i - 1]) / (
                                maxtmiN - i)
                    elif i>maxtmiN:
                        if efficient_tmi[length+i] > efficient_tmi[length+i - 1]:
                            efficient_tmi[length+i] = efficient_tmi[length+i - 1] - (maxtmi - efficient_tmi[length+i - 1]) / (
                                i - maxtmiN)

        print(efficient_sys)
        self.InterData(efficient_tmi,efficient_tm,efficient_sys,maxsys,maxtm,maxtmi)
        self.PaintMAP1()



    def InterData(self,efficient_tmi,efficient_tm,efficient_sys,maxsys,maxtm,maxtmi):
        zz1 = griddata((self.speed, self.torque), efficient_tmi, (self.X, self.Y), 'cubic')
        zz2 = griddata((self.speed, self.torque), efficient_tm, (self.X, self.Y), 'cubic')
        zz3 = griddata((self.speed, self.torque), efficient_sys, (self.X, self.Y), 'cubic')

        trq_max_coord = []

        for ii in range(0, len(self.Y[1])):
            trq_max_coord.append(1)
        trq_max_serial1 = interp1d(self.speed_maxs, self.torque_maxs, bounds_error=False)

        c = []
        for i in range(0, int((max(self.speed) + 300) / 30) + 1):
            c.append(i * self.sp_step)
        self.speed300 = c
        trq_max_serial = trq_max_serial1(c)
        self.trq_max_serial = trq_max_serial
        for i in range(0, len(self.X[0])):
            for n in range(0, len(self.X)):

                if trq_max_serial[i] <= self.Y[n][i]:
                    trq_max_coord[i] = n
                    break

        for i in range(0, len(trq_max_coord)):
            if trq_max_coord[i] == 0:
                trq_max_coord[i] = 1

        for i in range(0, len(self.X[1])):
            for j in range(trq_max_coord[i], len(zz1)):
                # 把值设置为Nan
                zz1[j][i] = float('nan')
                zz2[j][i] = float('nan')
                zz3[j][i] = float('nan')
        # print(zz1)

        #print(len(xx[1]), len(trq_max_coord))

        '''zz33=zz3(:)
        zz33(isnan(zz33))=[]
        zz22=zz2(:)
        zz22(isnan(zz22))=[]
        zz11=zz1(:)
        zz11(isnan(zz11))=[]'''
        zz11 = []
        zz22 = []
        zz33 = []
        for i in range(0, len(zz1)):
            for j in range(0, len(zz1[0])):
                if math.isnan(zz1[i][j]):
                    pass
                else:
                    zz11.append(zz1[i][j])

        # zz33 = zz3

        for i in range(0, len(zz2)):
            for j in range(0, len(zz2[0])):
                if math.isnan(zz2[i][j]):
                    pass
                else:
                    zz22.append(zz2[i][j])

        for i in range(0, len(zz3)):
            for j in range(0, len(zz3[0])):
                if math.isnan(zz3[i][j]):
                    pass
                else:
                    zz33.append(zz3[i][j])

        # zz33(isnan(zz33)) = []

        # zz22(isnan(zz22)) = []

        # zz11(isnan(zz11)) = []


        max_sys = int(maxsys * 10) / 10
        max_tm = int(maxtm * 10) / 10
        max_tmi = int(maxtmi * 10) / 10
        num_all = len(zz33)
        num_80 = 0
        num_85 = 0
        num_80_TM = 0
        num_85_TM = 0
        num_80_TMI = 0
        num_85_TMI = 0

        for i in range(0, num_all):
            if zz33[i] > 80:
                num_80 = num_80 + 1

            if zz33[i] > 85:
                num_85 = num_85 + 1

            if zz22[i] > 80:
                num_80_TM = num_80_TM + 1

            if zz22[i] > 85:
                num_85_TM = num_85_TM + 1

            if zz11[i] > 80:
                num_80_TMI = num_80_TMI + 1

            if zz11[i] > 85:
                num_85_TMI = num_85_TMI + 1


        self.zz1 = zz1
        self.zz2 = zz2
        self.zz3 = zz3

        # 这里的T待定
        self.T1 = [72, 74, 76, 78, 80, 81, 82, 83, 84, 85, 85.5, 86, 86.5, 87, 87.5, 88, 88.5, 89, 89.5, 90, 90.5, 91,
                   91.5, 92, 92.5, 93, 93.5, 94, 94.5, 95, 95.5, 96, 96.5, 97, 97.5, 98, 98.5, 99, 99.5, 100, max_tmi]
        self.T2 = [10, 25, 40, 55, 60, 65, 70, 72, 74, 76, 78, 80, 81, 82, 83, 84, 85, 85.5, 86, 86.5, 87, 87.5, 88,
                   88.5, 89, 89.5, 90, 90.5, 91, 91.5, 92, 92.5, 93, 93.5, 94, 94.5, 95, 95.5, 96, 96.5, 97, 97.5, 98,
                   98.5, 99, 99.5, 100, max_tm]
        self.T3 = [10, 25, 40, 55, 60, 65, 70, 72, 74, 76, 78, 80, 81, 82, 83, 84, 85, 85.5, 86, 86.5, 87, 87.5, 88,
                   88.5, 89, 89.5, 90, 90.5, 91, 91.5, 92, 92.5, 93, 93.5, 94, 94.5, 95, 95.5, 96, 96.5, 97, 97.5, 98,
                   98.5, 99, 99.5, 100, max_sys]
        self.T1.sort()
        self.T2.sort()
        self.T3.sort()




    def AnalyseData(self):
        speed = list(map(abs,self.N_dem_D_col))
        speed_order=list(map(abs,self.N_dem_E_col))
        torque=list(map(abs,self.TORQUE_col))
        power=list(map(abs,self.P_col))
        efficient_sys=list(map(abs,self.EFF_SYS_col))
        efficient_tm=list(map(abs,self.EFF_MOT_col))
        efficient_tmi=list(map(abs,self.EFF_CON_col))


        self.efficient_sys=efficient_sys
        self.efficient_tm=efficient_tm
        self.efficient_tmi=efficient_tmi

        #self.OptmizeMap(efficient_sys,efficient_tm,efficient_tmi)
        self.speed=speed
        self.torque=torque


        sp_step=30
        tor_step=2
        self.sp_step=sp_step
        a=[]
        b=[]
        k1=0
        k2=0
        while (k1<=max(speed)+300):

            a.append(k1)
            k1 = k1 + sp_step
        while (k2 <= 330):

            b.append(k2)
            k2 = k2 + tor_step

        xx, yy = np.meshgrid(a, b)




        speed_base=[]
        for i in range(0,int(max(speed)/30)):

            speed_base.append(i*sp_step)

        torque_y=330
        torque_step=20
        power_y=170
        power_step=15
        compare=1
        torque_max=305
        power_max=150



        str1='EI09'
        str2='Y01'
        str3='350V'
        str4='aaa'




        speed_num=0

        speed_kinds=[]
        speed_kinds.append(speed_order[0])




        torque_matrix=[]
        torque_matrix.append([torque[0]])
        power_matrix=[]
        power_matrix.append([power[0]])



        speed_matrix = []
        speed_matrix.append([speed[0]])
        j = 0
        for i in range(1,len(speed_order)):
            if speed_order[i]==speed_order[i-1]:
                #speed_num = speed_num + 1
                speed_kinds.append(speed_order[i])

                torque_matrix[speed_num].append(torque[i])
                power_matrix[speed_num].append(power[i])
                speed_matrix[speed_num] .append(speed[i])
                #print(torque_matrix)


            if speed_order[i]!=speed_order[i-1]:
                torque_matrix.append([torque[i]])
                power_matrix.append([power[i]])
                speed_matrix.append([speed[i]])
                speed_num = speed_num + 1

        self.speed_matrix=speed_matrix
        torque_maxs=[]
        power_maxs = []
        speed_maxs = []
        for i in range(0,speed_num+1):

            torque_maxs.append( max(torque_matrix[i]))
            power_maxs.append( max(power_matrix[i]))
            speed_maxs.append( max(speed_matrix[i]))


        torque_ec1=interp1d(speed_maxs,torque_maxs,kind='cubic',bounds_error=False)#如果不为false，就会报A value in x_new is below the interpolation range.

        torque_ec=torque_ec1(speed_base)


        power_ec1=interp1d(speed_maxs,power_maxs,kind='cubic',bounds_error=False)
        power_ec = power_ec1(speed_base)





        speed_turn = power_max * 9550 / torque_max
        torque_perfet = [0]*len(speed_base)
        speed_perfet = [0]*len(speed_base)
        torque_perfect=[]
        power_perfect=[]

        for i in range(0,len(speed_base)):
            if speed_base[i]< speed_turn:
                torque_perfect.append(torque_max)
                power_perfect.append(speed_base[i] * torque_max / 9550)

            if speed_base[i] >= speed_turn:
                torque_perfect.append( power_max * 9550 / speed_base[i])
                power_perfect.append(power_max)



        self.speed_base = speed_base
        self.torque_ec = torque_ec
        self.power_ec = power_ec
        self.speed_maxs = speed_maxs
        self.torque_maxs = torque_maxs
        self.power_maxs = power_maxs
        self.X = xx
        self.Y = yy



plt.rcParams['font.sans-serif'] = ['SimHei']
a=oringin("EI09_B_MAP_350V_DD_20191011_WT.xls")
a.readExcel()
a.PaintMAP()
#a.OptmizeMapData()
a.ChooseMAP1()
