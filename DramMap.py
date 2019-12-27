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
import re
class oringin:
    def __init__(self,path):
        self.path=path
        plt.rcParams['font.sans-serif'] = ['SimHei']
    def readExcel(self):
        '''读Excel，提取需要的各列数据'''
        workbook1 = xlrd.open_workbook(filename=self.path)
        if self.path != "":

            sheet = workbook1.sheet_by_name('DD')
            #sheet = workbook1.sheets()[]

            # sheet = workbook1.sheet_by_name(name)
            #TODO这里是1的原因是因为这是修改后的表，实际的表这里应该是0
            row = sheet.row_values(0)

            needkk=2

            for i in range(0,len(row)):

                if row[i] == "N_dem_E":#speed指令
                    self.N_dem_E_col = sheet.col_values(i)[needkk:]
                if row[i] == "N_dem_D":#实际转速
                    self.N_dem_D_col = sheet.col_values(i)[needkk:]

                if row[i] == "T_dem_E":#扭矩指令
                    self.T_dem_E_col = sheet.col_values(i)[needkk:]

                if row[i] =="DC_ACT_I":
                    self.DC_col1=sheet.col_values(i)[needkk:]
                if row[i] =="DC_ACT_U":
                    self.DC_col2 = sheet.col_values(i)[needkk:]
                if row[i] =="EFF_CON":#控制器效率
                    self.EFF_CON_col=sheet.col_values(i)[needkk:]
                if row[i] =="EFF_MOT":#电机效率
                    self.EFF_MOT_col = sheet.col_values(i)[needkk:]
                if row[i] == "EFF_SYS":#系统效率
                    self.EFF_SYS_col = sheet.col_values(i)[needkk:]

                if row[i] == "IGBT_TEMP_U":
                    #self.IGBT_col=[]
                    self.IGBT_TEMP_U_col = sheet.col_values(i)[needkk:]

                    self.IGBT_TEMP_V_col = sheet.col_values(i+1)[needkk:]
                    self.IGBT_TEMP_W_col = sheet.col_values(i+2)[needkk:]
                    '''for j in range(0,len(IGBT_col1)):
                        if IGBT_col1[j]>=IGBT_col2[j] and IGBT_col1[j]>=IGBT_col3[j]:
                            self.IGBT_col.append(IGBT_col1[j])
                        elif IGBT_col2[j]>=IGBT_col3[j]:
                            self.IGBT_col.append(IGBT_col2[j])
                        else:
                            self.IGBT_col.append(IGBT_col3[j])'''

                if row[i] == "IrmsA":
                    self.IrmsA_col = sheet.col_values(i)[needkk:]

                if row[i] == "P":#功率
                    self.P_col = sheet.col_values(i)[needkk:]
                if row[i] == "TM_TEMP":
                    #self.TM_TEMP_col = []

                    self.TM_TEMP = sheet.col_values(i)[needkk:]

                    self.TM_TEMP2 = sheet.col_values(i+1)[needkk:]
                    '''for jj in range(0,len(TM_TEMP_col1)):
                        if TM_TEMP_col1[j]>=TM_TEMP_col2[j]:

                            self.TM_TEMP_col.append(TM_TEMP_col1[j])
                        else:
                            self.TM_TEMP_col.append(TM_TEMP_col2[j])'''

                if row[i] == "TORQUE":#实际扭矩
                    self.TORQUE_col = sheet.col_values(i)[needkk:]

                if row[i] == "UrmsA":
                    self.UrmsA_col = sheet.col_values(i)[needkk:]
            self.Num = 0


            self.AnalyseData()


    def ChooseMAP1(self,title,T):
        self.title = title
        '''与绘制外特性图的按钮连接'''
        self.MAPFLAG=0
        T0 = []

        # T1=re.split("\[",T)[0]
        # T1=re.split("\]",T1)[0]
        T1 = re.split(",", T)
        for i in T1:
            if i == "":
                pass
            if ":" in i:
                T2 = re.split(':', i)
                # for j in T2:
                # a=np.linspace(float(T2[0]),float(T2[2]),float(T2[1]))
                j = float(T2[0])
                while j <= float(T2[2]):
                    T0.append(j)
                    j = j + float(T2[1])

                '''for k in a:
                    T0.append(k)'''
            else:
                T0.append(float(i))

        self.T0 = T0
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
        '''外特性图绘制'''
        #figure1
        fig, ax = plt.subplots(num=None,  facecolor='w', edgecolor='k')

        l1 = ax.plot(self.speed_maxs, self.torque_maxs, 'bs-', label='扭矩')
        plt.xlabel("转速(rpm)")

        # 共享x轴，生成次坐标轴
        ax_sub = ax.twinx()
        l2 = ax_sub.plot(self.speed_maxs, self.power_maxs, 'rs-', label='功率')
        fig.legend(loc=1, bbox_to_anchor=(1, 1), bbox_transform=ax.transAxes)
        ax.set_ylabel('扭矩(Nm)')
        ax_sub.set_ylabel('功率(kw)')
        torque_y = 280
        torque_step = 20
        power_y = 170

        for  i in range(0,len(self.speed_maxs)):
            ax.text(self.speed_maxs[i] - 50, self.torque_maxs[i] + 0.03 * torque_y, str(self.torque_maxs[i]), fontsize=12,fontweight='bold', color='b')
            ax_sub.text(self.speed_maxs[i] + 50, self.power_maxs[i] + 0.01 * torque_y,
                 str(round(self.power_maxs[i] * 100) / 100), fontsize=12,fontweight='bold', color='r')





        plt.show()


    def PaintMAP1(self):
        '''MAP图绘制'''
        if self.MAPFLAG==0:
            strname="原始图"
        else:
            strname="优化图"
        # figure2  控制器效率

        fig2 = plt.figure()
        plt.ylabel('扭矩(Nm)')
        plt.xlabel("转速(rpm)")



        contour = plt.contour(self.X, self.Y, self.zz1, self.T1)
        plt.clabel(contour, inline=True, fontsize=12, fmt='%1.1f')
        plt.plot(self.speed300, self.trq_max_serial, 'r-', linewidth=1.5)
        plt.title('%s控制器效率%s\n 效率大于80占比：%.2f%s  效率大于85占比：%.2f%s 效率大于90占比：%.2f%s' %(self.title,strname,self.eff80_TMI,'%',self.eff85_TMI,'%',self.eff90_TMI,'%'))

        # figure3 电机效率
        fig3 = plt.figure()
        plt.ylabel('扭矩(Nm)')
        plt.xlabel("转速(rpm)")



        contour = plt.contour(self.X, self.Y, self.zz2, self.T1)
        plt.clabel(contour, inline=True, fontsize=12, fmt='%1.1f')
        plt.plot(self.speed300, self.trq_max_serial, 'r-', linewidth=1.5)
        plt.title('%s电机效率%s\n 效率大于80占比：%.2f%s  效率大于85占比：%.2f%s 效率大于90占比：%.2f%s'%(self.title,strname,self.eff80_TM,'%',self.eff85_TM,'%',self.eff85_TM,'%'))

        # figure4 系统效率
        fig4 = plt.figure()
        plt.ylabel('扭矩(Nm)')
        plt.xlabel("转速(rpm)")



        contour = plt.contour(self.X, self.Y, self.zz3, self.T1)
        plt.clabel(contour, inline=True, fontsize=12, fmt='%1.1f')
        plt.plot(self.speed300, self.trq_max_serial, 'r-', linewidth=1.5)
        plt.title('%s系统效率%s\n 效率大于80占比：%.2f%s  效率大于85占比：%.2f%s 效率大于90占比：%.2f%s'%(self.title,strname,self.eff80,'%',self.eff85,'%',self.eff90,'%'))

        plt.show()

    def OptmizeMapData(self,title,T):
        self.title=title
        T0=[]
        self.MAPFLAG=1

        #T1=re.split("\[",T)[0]
        #T1=re.split("\]",T1)[0]
        T1=re.split(",",T)
        for i in T1:
            if i=="":
                pass
            if ":"in i:
                T2=re.split(':',i)
                #for j in T2:
                #a=np.linspace(float(T2[0]),float(T2[2]),float(T2[1]))
                j=float(T2[0])
                while j<=float(T2[2]):
                    T0.append(j)
                    j=j+float(T2[1])
                


                '''for k in a:
                    T0.append(k)'''
            else:
                T0.append(float(i))

        self.T0=T0





        efficient_sys=[]

        efficient_tm=[]
        efficient_tmi=[]

        for ii in range(0,len(self.speed_matrix)):
            if ii==0:
                length=0
                maxsys = self.efficient_sys[ii]
                maxtm = self.efficient_tm[ii]
                maxtmi = self.efficient_tmi[ii]
            else:
                length=length+len(self.speed_matrix[ii-1])
                maxsys = self.efficient_sys[length]

                maxtm = self.efficient_tm[length]
                maxtmi = self.efficient_tmi[length]

            for j in range(1,len(self.speed_matrix[ii])):


                #for i in range(1, len(self.efficient_sys)):
                    if self.efficient_sys[length+j] > maxsys:
                        maxsys = self.efficient_sys[length+j]
                        maxsysN = j
                    if self.efficient_tm[length+j] > maxtm:
                        maxtm = self.efficient_tm[length+j]
                        maxtmN = j
                    if self.efficient_tmi[length+j] > maxtmi:
                        maxtmi = self.efficient_tmi[length+j]
                        maxtmiN = j
            #sysNow = self.efficient_sys[length]
            #tmNow = self.efficient_tm[length]
            #tmiNow = self.efficient_tmi[length]
            efficient_sys.append(self.efficient_sys[length])
            efficient_tm.append(self.efficient_tm[length])
            efficient_tmi.append(self.efficient_tmi[length])


            for i in range(1, len(self.speed_matrix[ii])):

                    if i < maxsysN:
                        if self.efficient_sys[length+i] < efficient_sys[i +length- 1]:
                            efficient_sys.append( self.efficient_sys[length+i - 1] + (maxsys - efficient_sys[length+i - 1]) / (
                            maxsysN - i))
                        else:
                            efficient_sys.append(self.efficient_sys[length + i])
                    elif i > maxsysN:
                        if self.efficient_sys[length+i] > efficient_sys[length+i - 1]:
                            efficient_sys.append(efficient_sys[length+i - 1] - (maxsys - efficient_sys[length+i - 1]) / (
                            i - maxsysN))
                        else:
                            efficient_sys.append(self.efficient_sys[length + i])
                    else:
                        efficient_sys.append(self.efficient_sys[length+i])
                    if i<maxtmN:
                        if self.efficient_tm[length+i] < self.efficient_tm[length+i - 1]:
                            efficient_tm.append(self.efficient_tm[length+i - 1] + (maxtm - self.efficient_tm[length+i - 1]) / (
                                maxtmN - i))
                        else:
                            efficient_tm.append(self.efficient_tm[length + i])
                    elif i > maxtmN:
                        if self.efficient_tm[length+i] > self.efficient_tm[length+i - 1]:
                            efficient_tm.append( self.efficient_tm[length+i - 1] - (maxtm - self.efficient_tm[length+i - 1]) / (
                                i - maxtmN))
                        else:
                            efficient_tm.append(self.efficient_tm[length + i])
                    else:
                        efficient_tm.append(self.efficient_tm[length+i])
                    if i<maxtmiN:
                        if self.efficient_tmi[length+i] < self.efficient_tmi[length+i - 1]:
                            efficient_tmi.append( self.efficient_tmi[length+i - 1] + (maxtmi - self.efficient_tmi[length+i - 1]) / (
                                maxtmiN - i))
                        else:
                            efficient_tmi.append(self.efficient_tmi[length + i])
                    elif i>maxtmiN:
                        if self.efficient_tmi[length+i] > self.efficient_tmi[length+i - 1]:
                            efficient_tmi.append( self.efficient_tmi[length+i - 1] - (maxtmi - self.efficient_tmi[length+i - 1]) / (
                                i - maxtmiN))
                        else:
                            efficient_tmi.append(self.efficient_tmi[length + i])
                    else:
                        efficient_tmi.append(self.efficient_tmi[length + i])

        #print(self.efficient_sys)

        #print(len(efficient_sys),len(self.efficient_sys))
        #print(efficient_sys)
        for i in range(0,len(efficient_sys)):
                a=1
                #if efficient_sys[i]!=self.efficient_sys[i]:
                #print(efficient_sys[i],self.efficient_sys[i])
                #print(efficient_sys[i],self.efficient_sys[i])


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
        num_90 = 0
        num_90_TM = 0
        num_90_TMI = 0


        for i in range(0, num_all):
            if zz33[i] > 80:
                num_80 = num_80 + 1

            if zz33[i] > 85:
                num_85 = num_85 + 1

            if zz33[i] > 90:
                num_90 = num_90 + 1

            if zz22[i] > 80:
                num_80_TM = num_80_TM + 1

            if zz22[i] > 85:
                num_85_TM = num_85_TM + 1

            if zz22[i] > 90:
                num_90_TM = num_90_TM + 1

            if zz11[i] > 80:
                num_80_TMI = num_80_TMI + 1

            if zz11[i] > 85:
                num_85_TMI = num_85_TMI + 1

            if zz11[i] > 90:
                num_90_TMI = num_90_TMI + 1



        self.zz1 = zz1
        self.zz2 = zz2
        self.zz3 = zz3

        # 这里的T待定
        T1=[]
        T2=[]
        T3=[]
        for i in self.T0:

            T1.append(i)
            T2.append(i)
            T3.append(i)


        T1.append(max_tmi)
        self.T1 = T1
        self.T2 = T2.append( max_tm)
        self.T2 = T2
        self.T3 = T3.append(max_sys)
        self.T3 = T3

        self.T1.sort()
        self.T2.sort()
        self.T3.sort()

        self.eff80=num_80/num_all*100
        self.eff85=num_85/num_all*100
        self.eff90=num_90/num_all*100
        self.eff80_TM=num_80_TM/num_all*100
        self.eff85_TM=num_85_TM/num_all*100
        self.eff90_TMI=num_90_TM/num_all*100
        self.eff80_TMI=num_80_TMI/num_all*100
        self.eff85_TMI=num_85_TMI/num_all*100
        self.eff90_TMI=num_90_TMI/num_all*100

    def PaintTempMap(self):
        #figure
        plt.figure()
        plt.plot(self.temp,'b-', label='电机温度1')
        plt.plot(self.temp2,'r-',label='电机温度2')
        plt.legend(loc=1, bbox_to_anchor=(1, 1))
        plt.ylabel('温度（℃）')
        plt.figure()
        plt.plot(self.igbtu,'g-',label='IGBT-U向温度')
        plt.plot(self.igbtv,'c-',label='IGBT-V向温度')
        plt.plot(self.igbtw,'y-',label='IGBT-W向温度')
        plt.legend(loc=1, bbox_to_anchor=(1, 1))
        plt.ylabel('温度（℃）')

        plt.show()


    def AnalyseData(self):
        '''处理数据'''

        speed = list(map(abs,self.N_dem_D_col))
        speed_order=list(map(abs,self.N_dem_E_col))
        torque=list(map(abs,self.TORQUE_col))
        power=list(map(abs,self.P_col))
        efficient_sys=list(map(abs,self.EFF_SYS_col))
        efficient_tm=list(map(abs,self.EFF_MOT_col))
        efficient_tmi=list(map(abs,self.EFF_CON_col))
        igbtu = list(map(abs, self.IGBT_TEMP_U_col))
        igbtv = list(map(abs, self.IGBT_TEMP_V_col))
        igbtw = list(map(abs, self.IGBT_TEMP_W_col))
        temp = list(map(abs, self.TM_TEMP))
        temp2 = list(map(abs, self.TM_TEMP2))






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
        torqueFact=[]
        speedFact=[]
        efficient_sysFact=[]
        efficient_tmFact=[]
        efficient_tmiFact=[]
        igbtuFact=[]
        igbtvFact=[]
        igbtwFact=[]
        tempFact=[]
        temp2Fact=[]


        speed_matrix = []
        speed_matrix.append([speed[0]])
        efficient_sysFact.append(efficient_sys[0])
        efficient_tmFact.append(efficient_tm[0])
        efficient_tmiFact.append(efficient_tmi[0])
        igbtuFact.append(igbtu[0])
        igbtvFact.append(igbtv[0])
        igbtwFact.append(igbtw[0])
        tempFact.append(temp[0])
        temp2Fact.append(temp2[0])
        torqueFact.append(torque[0])
        speedFact.append(speed[0])

        j = 0
        for i in range(1,len(speed_order)):
            if speed_order[i]==speed_order[i-1] and torque_matrix[speed_num][len(torque_matrix[speed_num])-1]<=torque[i] and speed_matrix[speed_num][len(speed_matrix[speed_num])-1]<=speed[i]:
                speed_kinds.append(speed_order[i])
                torque_matrix[speed_num].append(torque[i])
                power_matrix[speed_num].append(power[i])
                speed_matrix[speed_num] .append(speed[i])
                efficient_sysFact.append(efficient_sys[i])
                efficient_tmFact.append(efficient_tm[i])
                efficient_tmiFact.append(efficient_tmi[i])
                igbtuFact.append(igbtu[i])
                igbtvFact.append(igbtv[i])
                igbtwFact.append(igbtw[i])
                tempFact.append(temp[i])
                temp2Fact.append(temp2[i])
                torqueFact.append(torque[i])
                speedFact.append(speed[i])




            if speed_order[i]>speed_order[i-1]:
                torque_matrix.append([torque[i]])
                power_matrix.append([power[i]])
                speed_matrix.append([speed[i]])
                speed_num = speed_num + 1
                efficient_sysFact.append(efficient_sys[i])
                efficient_tmFact.append(efficient_tm[i])
                efficient_tmiFact.append(efficient_tmi[i])
                igbtuFact.append(igbtu[i])
                igbtvFact.append(igbtv[i])
                igbtwFact.append(igbtw[i])
                tempFact.append(temp[i])
                temp2Fact.append(temp2[i])
                torqueFact.append(torque[i])
                speedFact.append(speed[i])

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
        self.efficient_sys = efficient_sysFact
        self.efficient_tm = efficient_tmFact
        self.efficient_tmi = efficient_tmiFact
        self.speed = speedFact
        self.torque = torqueFact
        self.temp=tempFact
        self.temp2=temp2Fact
        self.igbtu=igbtuFact
        self.igbtv=igbtvFact
        self.igbtw=igbtwFact




