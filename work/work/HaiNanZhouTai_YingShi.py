import datetime
import os
import re
#确定文件长度
def checkFileLenth(filePath):
    with open(filePath, encoding='GBK') as file1:
        lenthOfFile = len(file1.readlines())
        return lenthOfFile
#定位站点所在行数
def numCheck(filePath, lenthOfFile, stationNum):
    with open(filePath, encoding='GBK') as file1:
        for i in range(lenthOfFile):
            result = file1.readline().split(' ')
            if result[0] == stationNum:
                return i
#挑出该站点资料
def pickOut(filePath, lineNum, timeStep):
    with open(filePath, encoding='GBK') as file1:
        a = file1.readlines()
        b = a[lineNum + timeStep]
        c = b.split(' ')
        list2 = []
        list3 = []
        for j in c:
            if j != '':
                list2.append(j)
        list3.append(list2[0])
        list3.append(list2[11])
        list3.append(list2[12])
        list3.append(list2[-3])
        list3.append(list2[-2])
        list3.append(list2[-1])
    return list3
#获取当天时间及设置00或12时次资料
def getTime():
    Now = datetime.datetime.now()
    now2Str = int(datetime.datetime.strftime(Now,"%H%M"))
    today1 = datetime.date.today()
    if now2Str >= 530 and now2Str < 1530:
        dateToday = datetime.datetime.strftime(today1, "%Y%m%d") + "00"
    elif now2Str >= 1530:
        dateToday = datetime.datetime.strftime(today1, "%Y%m%d") + "12"
    return dateToday
#遍历文件目录下所有文件，并正则配对所需文件
def checkFile(filePath, dateToday):
    fileList = os.listdir(filePath)
    p1 = r"((Z_SEVP_C_BFGH_).*?(P_RFFC-SPCC-)"+dateToday+".*?)"
    pattern1 = re.compile(p1)
    for singleFile in fileList:
        match1 = re.match(pattern1, singleFile)
        if match1 != None:
            return singleFile
#温度转换
def TempCalculation(Temp):
    if Temp > -10 and Temp < 0:
        Ta = 5
        TempShow = str(Ta) + str(abs(int(Temp)))
    elif Temp > -20 and Temp <= -10:
        Ta = 6
        TempShow = str(Ta) + str(abs(int(Temp + 10)))
    elif Temp > -30 and Temp <= -20:
        Ta = 7
        TempShow = str(Ta) + str(abs(int(Temp + 20)))
    elif Temp > -40 and Temp <= -30:
        Ta = 8
        TempShow = str(Ta) + str(abs(int(Temp + 30)))
    elif Temp >= 0 and Temp < 10:
        TempShow = "0" + str(abs(int(Temp)))
    else:
        TempShow = str(abs(int(Temp)))
    return TempShow
#风向风速转换
def windCal(WindD12,WindD24,WindS12,WindS24):
    if WindS12 == 0 and WindS24 == 0:
        Wa = 0
        WindD12Show = WindD24Show = 8
        WindS12Show = WindS24Show = 0
    else:
        Wa = 1
        WindD12Show = WindD12
        WindD24Show = WindD24
        WindS12Show = WindS12
        WindS24Show = WindS24
    WindShowFinal = str(Wa)+"%01d"%WindD12Show+"%01d"%WindD24Show+"%01d"%WindS12Show+"%01d"%WindS24Show
    return WindShowFinal
#主程序
if __name__ == "__main__":

    filePath = "D:\\shengxun\\baowen\\"
    dateToday = getTime()
    fileName = checkFile(filePath,dateToday)
    print(fileName)
    fileInputPath = filePath + fileName
    lenthOfFile = checkFileLenth(fileInputPath)
    stationNum = ['52856','52868','52943','52955','52957']
    listOfStep = [1, 2]
    #写国家站数据到文件
    fileExist = os.path.exists("E:\\data\\" + "temp.txt")
    if fileExist == True:
        os.remove("E:\\data\\" + "temp.txt")
    for i in stationNum:
        lineNum = numCheck(fileInputPath, lenthOfFile, i)
        for j in listOfStep:
            eleOfSingleStation = pickOut(fileInputPath,lineNum,1) + pickOut(fileInputPath,lineNum,2)
        print(eleOfSingleStation)
        Weather12 = int(float(eleOfSingleStation[3]))
        Weather24 = int(float(eleOfSingleStation[-3]))
        WindD12 = int(float(eleOfSingleStation[4]))
        WindD24 = int(float(eleOfSingleStation[-2]))
        WindS12 = int(float(eleOfSingleStation[5].split('\n')[0]))
        WindS24 = int(float(eleOfSingleStation[-1].split('\n')[0]))
        TMax = float(eleOfSingleStation[-5])
        TMin = float(eleOfSingleStation[-4])
        TMinShow = TempCalculation(TMin)
        TMaxShow = TempCalculation(TMax)
        WindCalShow = windCal(WindD12,WindD24,WindS12,WindS24)
        #生成共和相关站信息
        if i == "52856":
            TMaxLongYangXia = TMax + 1.0
            TMinLongYangXia = TMin + 1.0
            TMaxGaRang = TMax + 1.0
            TMinGaRang = TMin + 1.0
            TMaxQiaBuQia = TMax
            TMinQiaBuQia = TMin
            WindS12LongYangXia=WindS12DaoTangHe=WindS12RiYueShan=WindS12QingHaiHu=WindS12QiaBuQia = WindS12
            WindS24LongYangXia=WindS24DaoTangHe=WindS24RiYueShan=WindS24QingHaiHu=WindS24QiaBuQia = WindS24
            WindD12LongYangXia=WindD12DaoTangHe=WindD12RiYueShan=WindD12QingHaiHu=WindD12QiaBuQia = WindD12
            WindD24LongYangXia=WindD24DaoTangHe=WindD24RiYueShan=WindD24QingHaiHu=WindD24QiaBuQia = WindD24
            Weather12LongYangXia=Weather12DaoTangHe=Weather12RiYueShan=Weather12QingHaiHu=Weather12QiaBuQia = Weather12
            Weather24LongYangXia=Weather24DaoTangHe=Weather24RiYueShan=Weather24QingHaiHu=Weather24QiaBuQia = Weather24
        # 生成兴海相关站信息
        if i == "52943":
            TMaxDaoTangHe = TMax + 1.0
            TMinDaoTangHe = TMin + 1.0
            TMaxHeKa = TMax - 1.0
            TMinHeKa = TMin - 1.0
            TMaxRiYueShan = TMaxDaoTangHe - 3.0
            TMinRiYueShan = TMinDaoTangHe - 3.0
            TMaxQingHaiHu = TMaxDaoTangHe - 1.0
            TMinQingHaiHu = TMinDaoTangHe - 1.0
            WindS12HeKa = WindS12
            WindS24HeKa = WindS24
            WindD12HeKa = WindD12
            WindD24HeKa = WindD24
            Weather12HeKa = Weather12
            Weather24HeKa = Weather24
        # 生成贵南相关站信息
        if i == "52955":
            WindS12GuoMaYing = WindS12
            WindS24GuoMaYing = WindS24
            WindD12GuoMaYing = WindD12
            WindD24GuoMaYing = WindD24
            Weather12GuoMaYing = Weather12
            Weather24GuoMaYing = Weather24
            TMinGuoMaYing = TMin
            TMaxGuoMaYing = TMax
        # 生成贵德相关站信息
        if i == "52868":
            WindS12GaRang = WindS12
            WindS24GaRang = WindS24
            WindD12GaRang = WindD12
            WindD24GaRang = WindD24
            Weather12GaRang = Weather12
            Weather24GaRang = Weather24
        FinalWrite = "0"+"%02d"%Weather12+"%02d"%Weather24+" "+WindCalShow+" 0"+TMinShow+TMaxShow+"\n"

        with open("E:\\data\\"+"temp.txt","a") as file1:
            file1.write(FinalWrite)
    #写区域站数据到文件
    with open("E:\\data\\"+"temp.txt","a") as file2:
        WindCalShowLongYangXia = windCal(WindD12LongYangXia, WindD24LongYangXia, WindS12LongYangXia, WindS24LongYangXia)
        WindCalShowDaoTangHe = windCal(WindD12DaoTangHe, WindD24DaoTangHe, WindS12DaoTangHe, WindS24DaoTangHe)
        WindCalShowHeKa = windCal(WindD12HeKa, WindD24HeKa, WindS12HeKa, WindS24HeKa)
        WindCalShowGuoMaYing = windCal(WindD12GuoMaYing, WindD24GuoMaYing, WindS12GuoMaYing, WindS24GuoMaYing)
        WindCalShowGaRang = windCal(WindD12GaRang, WindD24GaRang, WindS12GaRang, WindS24GaRang)
        WindCalShowRiYueShan = windCal(WindD12RiYueShan, WindD24RiYueShan, WindS12RiYueShan, WindS24RiYueShan)
        WindCalShowQingHaiHu = windCal(WindD12QingHaiHu, WindD24QingHaiHu, WindS12QingHaiHu, WindS24QingHaiHu)
        WindCalShowQiaBuQia = windCal(WindD12QiaBuQia, WindD24QiaBuQia, WindS12QiaBuQia, WindS24QiaBuQia)
        TMinShowLongYangXia = TempCalculation(TMinLongYangXia)
        TMaxShowLongYangXia = TempCalculation(TMaxLongYangXia)
        TMinShowDaoTangHe = TempCalculation(TMinDaoTangHe)
        TMaxShowDaoTangHe = TempCalculation(TMaxDaoTangHe)
        TMinShowHeKa = TempCalculation(TMinHeKa)
        TMaxShowHeKa = TempCalculation(TMaxHeKa)
        TMinShowGuoMaYing = TempCalculation(TMinGuoMaYing)
        TMaxShowGuoMaYing = TempCalculation(TMaxGuoMaYing)
        TMinShowGaRang = TempCalculation(TMinGaRang)
        TMaxShowGaRang = TempCalculation(TMaxGaRang)
        TMinShowRiYueShan = TempCalculation(TMinRiYueShan)
        TMaxShowRiYueShan = TempCalculation(TMaxRiYueShan)
        TMinShowQingHaiHu = TempCalculation(TMinQingHaiHu)
        TMaxShowQingHaiHu = TempCalculation(TMaxQingHaiHu)
        TMinShowQiaBuQia = TempCalculation(TMinQiaBuQia)
        TMaxShowQiaBuQia = TempCalculation(TMaxQiaBuQia)
        FinalWrite1 = "0" + "%02d" % Weather12LongYangXia + "%02d" % Weather24LongYangXia + " " + WindCalShowLongYangXia + " 0" + TMinShowLongYangXia + TMaxShowLongYangXia + "\n"
        FinalWrite2 = "0" + "%02d" % Weather12DaoTangHe + "%02d" % Weather24DaoTangHe + " " + WindCalShowDaoTangHe + " 0" + TMinShowDaoTangHe + TMaxShowDaoTangHe + "\n"
        FinalWrite3 = "0" + "%02d" % Weather12HeKa + "%02d" % Weather24HeKa + " " + WindCalShowHeKa + " 0" + TMinShowHeKa + TMaxShowHeKa + "\n"
        FinalWrite4 = "0" + "%02d" % Weather12GuoMaYing + "%02d" % Weather24GuoMaYing + " " + WindCalShowGuoMaYing + " 0" + TMinShowGuoMaYing + TMaxShowGuoMaYing + "\n"
        FinalWrite5 = "0" + "%02d" % Weather12GaRang + "%02d" % Weather24GaRang + " " + WindCalShowGaRang + " 0" + TMinShowGaRang + TMaxShowGaRang + "\n"
        FinalWrite6 = "0" + "%02d" % Weather12QiaBuQia + "%02d" % Weather24QiaBuQia + " " + WindCalShowQiaBuQia + " 0" + TMinShowQiaBuQia + TMaxShowQiaBuQia + "\n"
        FinalWrite7 = "0" + "%02d" % Weather12DaoTangHe + "%02d" % Weather24DaoTangHe + " " + WindCalShowDaoTangHe + " 0" + TMinShowDaoTangHe + TMaxShowDaoTangHe + "\n"
        FinalWrite8 = "0" + "%02d" % Weather12RiYueShan + "%02d" % Weather24RiYueShan + " " + WindCalShowRiYueShan + " 0" + TMinShowRiYueShan + TMaxShowRiYueShan + "\n"
        FinalWrite9 = "0" + "%02d" % Weather12LongYangXia + "%02d" % Weather24LongYangXia + " " + WindCalShowLongYangXia + " 0" + TMinShowLongYangXia + TMaxShowLongYangXia + "\n"
        FinalWrite0 = "0" + "%02d" % Weather12QingHaiHu + "%02d" % Weather24QingHaiHu + " " + WindCalShowQingHaiHu + " 0" + TMinShowQingHaiHu + TMaxShowQingHaiHu + "\n"
        file2.write(FinalWrite1)
        file2.write(FinalWrite2)
        file2.write(FinalWrite3)
        file2.write(FinalWrite4)
        file2.write(FinalWrite5)
        file2.write(FinalWrite6)
        file2.write(FinalWrite7)
        file2.write(FinalWrite8)
        file2.write(FinalWrite9)
        file2.write(FinalWrite0)

with open("E:\\data\\" + "temp.txt") as file0:
    originData = file0.readlines()
    HanQiaBuQia = "00000 " + originData[0].strip("\n") + " 恰卜恰 汉州01.rec hnd003.wav"
    HanHeYin = "00001 " + originData[1].strip("\n") + " 河阴 汉州02.rec hnd005.wav"
    HanZiKeTan = "00002 " + originData[2].strip("\n") + " 子科滩 汉州03.rec hnd007.wav"
    HanMangQu = "00003 " + originData[3].strip("\n") + " 茫曲 汉州04.rec hnd009.wav"
    HanGaBaSongDuo = "00004 " + originData[4].strip("\n") + " 尕巴松多 汉州05.rec hnd011.wav"
    HanLongYangXia = "00005 " + originData[5].strip("\n") + " 龙羊峡 汉州06.rec hnd028.wav"
    HanDaoTangHe = "00006 " + originData[6].strip("\n") + " 倒淌河镇 汉州07.rec hnd014.wav"
    HanHeKa = "00007 " + originData[7].strip("\n") + " 河卡镇 汉州08.rec hnd013.wav"
    HanGuoMaYing = "00008 " + originData[8].strip("\n") + " 过马营镇 汉州09.rec hnd016.wav"
    HanGaRang = "00009 " + originData[9].strip("\n") + " 尕让 汉州10.rec hnd074.wav"
    HanGongHeQiaBuQia = "00010 " + originData[10].strip("\n") + " 共和恰卜恰 汉县01.rec hnd003.wav"
    HanGongHeDaoTangHe = "00011 " + originData[11].strip("\n") + " 共和倒淌河 汉县02.rec hnd017.wav"
    HanGongHeRiYueShan = "00012 " + originData[12].strip("\n") + " 共和日月山 汉县03.rec hnd029.wav"
    HanGongHeLongYangXia = "00013 " + originData[13].strip("\n") + " 共和龙羊峡 汉县04.rec hnd028.wav"
    HanGongHeQingHaHu = "00014 " + originData[14].strip("\n") + " 共和青海湖 汉县05.rec hnd031.wav"

    print(HanQiaBuQia)
    print(HanHeYin)
    print(HanZiKeTan)
    print(HanMangQu)
    print(HanGaBaSongDuo)
    print(HanLongYangXia)
    print(HanDaoTangHe)
    print(HanHeKa)
    print(HanGuoMaYing)
    print(HanGaRang)
    print(HanGongHeQiaBuQia)
    print(HanGongHeDaoTangHe)
    print(HanGongHeRiYueShan)
    print(HanGongHeLongYangXia)
    print(HanGongHeQingHaHu)
    print("#####")
with open("C:\\qx00\\dat\\" + "汉语24小时.dat","w") as file1:
    file1.write(HanQiaBuQia+"\n")
    file1.write(HanHeYin+"\n")
    file1.write(HanZiKeTan+"\n")
    file1.write(HanMangQu+"\n")
    file1.write(HanGaBaSongDuo+"\n")
    file1.write(HanLongYangXia+"\n")
    file1.write(HanDaoTangHe+"\n")
    file1.write(HanHeKa+"\n")
    file1.write(HanGuoMaYing+"\n")
    file1.write(HanGaRang+"\n")
    file1.write(HanGongHeQiaBuQia+"\n")
    file1.write(HanGongHeDaoTangHe+"\n")
    file1.write(HanGongHeRiYueShan+"\n")
    file1.write(HanGongHeLongYangXia+"\n")
    file1.write(HanGongHeQingHaHu+"\n")
    file1.write("#####")


    filePath = "D:\\shengxun\\baowen\\"
    dateToday = getTime()
    fileName = checkFile(filePath,dateToday)
    print(fileName)
    fileInputPath = filePath + fileName
    lenthOfFile = checkFileLenth(fileInputPath)
    stationNum = ['52856','52868','52943','52955','52957']
    listOfStep = [1, 2]
    #写国家站数据到文件
    fileExist = os.path.exists("E:\\data\\" + "temp.txt")
    if fileExist == True:
        os.remove("E:\\data\\" + "temp.txt")
    for i in stationNum:
        lineNum = numCheck(fileInputPath, lenthOfFile, i)
        for j in listOfStep:
            eleOfSingleStation = pickOut(fileInputPath,lineNum,3) + pickOut(fileInputPath,lineNum,4)
        print(eleOfSingleStation)
        Weather12 = int(float(eleOfSingleStation[3]))
        Weather24 = int(float(eleOfSingleStation[-3]))
        WindD12 = int(float(eleOfSingleStation[4]))
        WindD24 = int(float(eleOfSingleStation[-2]))
        WindS12 = int(float(eleOfSingleStation[5].split('\n')[0]))
        WindS24 = int(float(eleOfSingleStation[-1].split('\n')[0]))
        TMax = float(eleOfSingleStation[-5])
        TMin = float(eleOfSingleStation[-4])
        TMinShow = TempCalculation(TMin)
        TMaxShow = TempCalculation(TMax)
        WindCalShow = windCal(WindD12,WindD24,WindS12,WindS24)
        #生成共和相关站信息
        if i == "52856":
            TMaxLongYangXia = TMax + 1.0
            TMinLongYangXia = TMin + 1.0
            TMaxGaRang = TMax + 1.0
            TMinGaRang = TMin + 1.0
            TMaxQiaBuQia = TMax
            TMinQiaBuQia = TMin
            WindS12LongYangXia=WindS12DaoTangHe=WindS12RiYueShan=WindS12QingHaiHu=WindS12QiaBuQia = WindS12
            WindS24LongYangXia=WindS24DaoTangHe=WindS24RiYueShan=WindS24QingHaiHu=WindS24QiaBuQia = WindS24
            WindD12LongYangXia=WindD12DaoTangHe=WindD12RiYueShan=WindD12QingHaiHu=WindD12QiaBuQia = WindD12
            WindD24LongYangXia=WindD24DaoTangHe=WindD24RiYueShan=WindD24QingHaiHu=WindD24QiaBuQia = WindD24
            Weather12LongYangXia=Weather12DaoTangHe=Weather12RiYueShan=Weather12QingHaiHu=Weather12QiaBuQia = Weather12
            Weather24LongYangXia=Weather24DaoTangHe=Weather24RiYueShan=Weather24QingHaiHu=Weather24QiaBuQia = Weather24
        # 生成兴海相关站信息
        if i == "52943":
            TMaxDaoTangHe = TMax + 1.0
            TMinDaoTangHe = TMin + 1.0
            TMaxHeKa = TMax - 1.0
            TMinHeKa = TMin - 1.0
            TMaxRiYueShan = TMaxDaoTangHe - 3.0
            TMinRiYueShan = TMinDaoTangHe - 3.0
            TMaxQingHaiHu = TMaxDaoTangHe - 1.0
            TMinQingHaiHu = TMinDaoTangHe - 1.0
            WindS12HeKa = WindS12
            WindS24HeKa = WindS24
            WindD12HeKa = WindD12
            WindD24HeKa = WindD24
            Weather12HeKa = Weather12
            Weather24HeKa = Weather24
        # 生成贵南相关站信息
        if i == "52955":
            WindS12GuoMaYing = WindS12
            WindS24GuoMaYing = WindS24
            WindD12GuoMaYing = WindD12
            WindD24GuoMaYing = WindD24
            Weather12GuoMaYing = Weather12
            Weather24GuoMaYing = Weather24
            TMinGuoMaYing = TMin
            TMaxGuoMaYing = TMax
        # 生成贵德相关站信息
        if i == "52868":
            WindS12GaRang = WindS12
            WindS24GaRang = WindS24
            WindD12GaRang = WindD12
            WindD24GaRang = WindD24
            Weather12GaRang = Weather12
            Weather24GaRang = Weather24
        FinalWrite = "0"+"%02d"%Weather12+"%02d"%Weather24+" "+WindCalShow+" 0"+TMinShow+TMaxShow+"\n"

        with open("E:\\data\\"+"temp.txt","a") as file1:
            file1.write(FinalWrite)
    #写区域站数据到文件
    with open("E:\\data\\"+"temp.txt","a") as file2:
        WindCalShowLongYangXia = windCal(WindD12LongYangXia, WindD24LongYangXia, WindS12LongYangXia, WindS24LongYangXia)
        WindCalShowDaoTangHe = windCal(WindD12DaoTangHe, WindD24DaoTangHe, WindS12DaoTangHe, WindS24DaoTangHe)
        WindCalShowHeKa = windCal(WindD12HeKa, WindD24HeKa, WindS12HeKa, WindS24HeKa)
        WindCalShowGuoMaYing = windCal(WindD12GuoMaYing, WindD24GuoMaYing, WindS12GuoMaYing, WindS24GuoMaYing)
        WindCalShowGaRang = windCal(WindD12GaRang, WindD24GaRang, WindS12GaRang, WindS24GaRang)
        WindCalShowRiYueShan = windCal(WindD12RiYueShan, WindD24RiYueShan, WindS12RiYueShan, WindS24RiYueShan)
        WindCalShowQingHaiHu = windCal(WindD12QingHaiHu, WindD24QingHaiHu, WindS12QingHaiHu, WindS24QingHaiHu)
        WindCalShowQiaBuQia = windCal(WindD12QiaBuQia, WindD24QiaBuQia, WindS12QiaBuQia, WindS24QiaBuQia)
        TMinShowLongYangXia = TempCalculation(TMinLongYangXia)
        TMaxShowLongYangXia = TempCalculation(TMaxLongYangXia)
        TMinShowDaoTangHe = TempCalculation(TMinDaoTangHe)
        TMaxShowDaoTangHe = TempCalculation(TMaxDaoTangHe)
        TMinShowHeKa = TempCalculation(TMinHeKa)
        TMaxShowHeKa = TempCalculation(TMaxHeKa)
        TMinShowGuoMaYing = TempCalculation(TMinGuoMaYing)
        TMaxShowGuoMaYing = TempCalculation(TMaxGuoMaYing)
        TMinShowGaRang = TempCalculation(TMinGaRang)
        TMaxShowGaRang = TempCalculation(TMaxGaRang)
        TMinShowRiYueShan = TempCalculation(TMinRiYueShan)
        TMaxShowRiYueShan = TempCalculation(TMaxRiYueShan)
        TMinShowQingHaiHu = TempCalculation(TMinQingHaiHu)
        TMaxShowQingHaiHu = TempCalculation(TMaxQingHaiHu)
        TMinShowQiaBuQia = TempCalculation(TMinQiaBuQia)
        TMaxShowQiaBuQia = TempCalculation(TMaxQiaBuQia)
        FinalWrite1 = "0" + "%02d" % Weather12LongYangXia + "%02d" % Weather24LongYangXia + " " + WindCalShowLongYangXia + " 0" + TMinShowLongYangXia + TMaxShowLongYangXia + "\n"
        FinalWrite2 = "0" + "%02d" % Weather12DaoTangHe + "%02d" % Weather24DaoTangHe + " " + WindCalShowDaoTangHe + " 0" + TMinShowDaoTangHe + TMaxShowDaoTangHe + "\n"
        FinalWrite3 = "0" + "%02d" % Weather12HeKa + "%02d" % Weather24HeKa + " " + WindCalShowHeKa + " 0" + TMinShowHeKa + TMaxShowHeKa + "\n"
        FinalWrite4 = "0" + "%02d" % Weather12GuoMaYing + "%02d" % Weather24GuoMaYing + " " + WindCalShowGuoMaYing + " 0" + TMinShowGuoMaYing + TMaxShowGuoMaYing + "\n"
        FinalWrite5 = "0" + "%02d" % Weather12GaRang + "%02d" % Weather24GaRang + " " + WindCalShowGaRang + " 0" + TMinShowGaRang + TMaxShowGaRang + "\n"
        FinalWrite6 = "0" + "%02d" % Weather12QiaBuQia + "%02d" % Weather24QiaBuQia + " " + WindCalShowQiaBuQia + " 0" + TMinShowQiaBuQia + TMaxShowQiaBuQia + "\n"
        FinalWrite7 = "0" + "%02d" % Weather12DaoTangHe + "%02d" % Weather24DaoTangHe + " " + WindCalShowDaoTangHe + " 0" + TMinShowDaoTangHe + TMaxShowDaoTangHe + "\n"
        FinalWrite8 = "0" + "%02d" % Weather12RiYueShan + "%02d" % Weather24RiYueShan + " " + WindCalShowRiYueShan + " 0" + TMinShowRiYueShan + TMaxShowRiYueShan + "\n"
        FinalWrite9 = "0" + "%02d" % Weather12LongYangXia + "%02d" % Weather24LongYangXia + " " + WindCalShowLongYangXia + " 0" + TMinShowLongYangXia + TMaxShowLongYangXia + "\n"
        FinalWrite0 = "0" + "%02d" % Weather12QingHaiHu + "%02d" % Weather24QingHaiHu + " " + WindCalShowQingHaiHu + " 0" + TMinShowQingHaiHu + TMaxShowQingHaiHu + "\n"
        file2.write(FinalWrite1)
        file2.write(FinalWrite2)
        file2.write(FinalWrite3)
        file2.write(FinalWrite4)
        file2.write(FinalWrite5)
        file2.write(FinalWrite6)
        file2.write(FinalWrite7)
        file2.write(FinalWrite8)
        file2.write(FinalWrite9)
        file2.write(FinalWrite0)

with open("E:\\data\\" + "temp.txt") as file0:
    originData = file0.readlines()
    HanQiaBuQia = "00000 " + originData[0].strip("\n") + " 恰卜恰 汉州01.rec hnd003.wav"
    HanHeYin = "00001 " + originData[1].strip("\n") + " 河阴 汉州02.rec hnd005.wav"
    HanZiKeTan = "00002 " + originData[2].strip("\n") + " 子科滩 汉州03.rec hnd007.wav"
    HanMangQu = "00003 " + originData[3].strip("\n") + " 茫曲 汉州04.rec hnd009.wav"
    HanGaBaSongDuo = "00004 " + originData[4].strip("\n") + " 尕巴松多 汉州05.rec hnd011.wav"
    HanLongYangXia = "00005 " + originData[5].strip("\n") + " 龙羊峡 汉州06.rec hnd028.wav"
    HanDaoTangHe = "00006 " + originData[6].strip("\n") + " 倒淌河镇 汉州07.rec hnd014.wav"
    HanHeKa = "00007 " + originData[7].strip("\n") + " 河卡镇 汉州08.rec hnd013.wav"
    HanGuoMaYing = "00008 " + originData[8].strip("\n") + " 过马营镇 汉州09.rec hnd016.wav"
    HanGaRang = "00009 " + originData[9].strip("\n") + " 尕让 汉州10.rec hnd074.wav"
    HanGongHeQiaBuQia = "00010 " + originData[10].strip("\n") + " 共和恰卜恰 汉县01.rec hnd003.wav"
    HanGongHeDaoTangHe = "00011 " + originData[11].strip("\n") + " 共和倒淌河 汉县02.rec hnd017.wav"
    HanGongHeRiYueShan = "00012 " + originData[12].strip("\n") + " 共和日月山 汉县03.rec hnd029.wav"
    HanGongHeLongYangXia = "00013 " + originData[13].strip("\n") + " 共和龙羊峡 汉县04.rec hnd028.wav"
    HanGongHeQingHaHu = "00014 " + originData[14].strip("\n") + " 共和青海湖 汉县05.rec hnd031.wav"

    print(HanQiaBuQia)
    print(HanHeYin)
    print(HanZiKeTan)
    print(HanMangQu)
    print(HanGaBaSongDuo)
    print(HanLongYangXia)
    print(HanDaoTangHe)
    print(HanHeKa)
    print(HanGuoMaYing)
    print(HanGaRang)
    print(HanGongHeQiaBuQia)
    print(HanGongHeDaoTangHe)
    print(HanGongHeRiYueShan)
    print(HanGongHeLongYangXia)
    print(HanGongHeQingHaHu)
    print("#####")
with open("C:\\qx00\\dat\\" + "汉语48小时.dat","w") as file1:
    file1.write(HanQiaBuQia+"\n")
    file1.write(HanHeYin+"\n")
    file1.write(HanZiKeTan+"\n")
    file1.write(HanMangQu+"\n")
    file1.write(HanGaBaSongDuo+"\n")
    file1.write(HanLongYangXia+"\n")
    file1.write(HanDaoTangHe+"\n")
    file1.write(HanHeKa+"\n")
    file1.write(HanGuoMaYing+"\n")
    file1.write(HanGaRang+"\n")
    file1.write(HanGongHeQiaBuQia+"\n")
    file1.write(HanGongHeDaoTangHe+"\n")
    file1.write(HanGongHeRiYueShan+"\n")
    file1.write(HanGongHeLongYangXia+"\n")
    file1.write(HanGongHeQingHaHu+"\n")
    file1.write("#####")

    filePath = "D:\\shengxun\\baowen\\"
    dateToday = getTime()
    fileName = checkFile(filePath,dateToday)
    print(fileName)
    fileInputPath = filePath + fileName
    lenthOfFile = checkFileLenth(fileInputPath)
    stationNum = ['52856','52868','52943','52955','52957']
    listOfStep = [1, 2]
    #写国家站数据到文件
    fileExist = os.path.exists("E:\\data\\" + "temp.txt")
    if fileExist == True:
        os.remove("E:\\data\\" + "temp.txt")
    for i in stationNum:
        lineNum = numCheck(fileInputPath, lenthOfFile, i)
        for j in listOfStep:
            eleOfSingleStation = pickOut(fileInputPath,lineNum,5) + pickOut(fileInputPath,lineNum,6)
        print(eleOfSingleStation)
        Weather12 = int(float(eleOfSingleStation[3]))
        Weather24 = int(float(eleOfSingleStation[-3]))
        WindD12 = int(float(eleOfSingleStation[4]))
        WindD24 = int(float(eleOfSingleStation[-2]))
        WindS12 = int(float(eleOfSingleStation[5].split('\n')[0]))
        WindS24 = int(float(eleOfSingleStation[-1].split('\n')[0]))
        TMax = float(eleOfSingleStation[-5])
        TMin = float(eleOfSingleStation[-4])
        TMinShow = TempCalculation(TMin)
        TMaxShow = TempCalculation(TMax)
        WindCalShow = windCal(WindD12,WindD24,WindS12,WindS24)
        #生成共和相关站信息
        if i == "52856":
            TMaxLongYangXia = TMax + 1.0
            TMinLongYangXia = TMin + 1.0
            TMaxGaRang = TMax + 1.0
            TMinGaRang = TMin + 1.0
            TMaxQiaBuQia = TMax
            TMinQiaBuQia = TMin
            WindS12LongYangXia=WindS12DaoTangHe=WindS12RiYueShan=WindS12QingHaiHu=WindS12QiaBuQia = WindS12
            WindS24LongYangXia=WindS24DaoTangHe=WindS24RiYueShan=WindS24QingHaiHu=WindS24QiaBuQia = WindS24
            WindD12LongYangXia=WindD12DaoTangHe=WindD12RiYueShan=WindD12QingHaiHu=WindD12QiaBuQia = WindD12
            WindD24LongYangXia=WindD24DaoTangHe=WindD24RiYueShan=WindD24QingHaiHu=WindD24QiaBuQia = WindD24
            Weather12LongYangXia=Weather12DaoTangHe=Weather12RiYueShan=Weather12QingHaiHu=Weather12QiaBuQia = Weather12
            Weather24LongYangXia=Weather24DaoTangHe=Weather24RiYueShan=Weather24QingHaiHu=Weather24QiaBuQia = Weather24
        # 生成兴海相关站信息
        if i == "52943":
            TMaxDaoTangHe = TMax + 1.0
            TMinDaoTangHe = TMin + 1.0
            TMaxHeKa = TMax - 1.0
            TMinHeKa = TMin - 1.0
            TMaxRiYueShan = TMaxDaoTangHe - 3.0
            TMinRiYueShan = TMinDaoTangHe - 3.0
            TMaxQingHaiHu = TMaxDaoTangHe - 1.0
            TMinQingHaiHu = TMinDaoTangHe - 1.0
            WindS12HeKa = WindS12
            WindS24HeKa = WindS24
            WindD12HeKa = WindD12
            WindD24HeKa = WindD24
            Weather12HeKa = Weather12
            Weather24HeKa = Weather24
        # 生成贵南相关站信息
        if i == "52955":
            WindS12GuoMaYing = WindS12
            WindS24GuoMaYing = WindS24
            WindD12GuoMaYing = WindD12
            WindD24GuoMaYing = WindD24
            Weather12GuoMaYing = Weather12
            Weather24GuoMaYing = Weather24
            TMinGuoMaYing = TMin
            TMaxGuoMaYing = TMax
        # 生成贵德相关站信息
        if i == "52868":
            WindS12GaRang = WindS12
            WindS24GaRang = WindS24
            WindD12GaRang = WindD12
            WindD24GaRang = WindD24
            Weather12GaRang = Weather12
            Weather24GaRang = Weather24
        FinalWrite = "0"+"%02d"%Weather12+"%02d"%Weather24+" "+WindCalShow+" 0"+TMinShow+TMaxShow+"\n"

        with open("E:\\data\\"+"temp.txt","a") as file1:
            file1.write(FinalWrite)
    #写区域站数据到文件
    with open("E:\\data\\"+"temp.txt","a") as file2:
        WindCalShowLongYangXia = windCal(WindD12LongYangXia, WindD24LongYangXia, WindS12LongYangXia, WindS24LongYangXia)
        WindCalShowDaoTangHe = windCal(WindD12DaoTangHe, WindD24DaoTangHe, WindS12DaoTangHe, WindS24DaoTangHe)
        WindCalShowHeKa = windCal(WindD12HeKa, WindD24HeKa, WindS12HeKa, WindS24HeKa)
        WindCalShowGuoMaYing = windCal(WindD12GuoMaYing, WindD24GuoMaYing, WindS12GuoMaYing, WindS24GuoMaYing)
        WindCalShowGaRang = windCal(WindD12GaRang, WindD24GaRang, WindS12GaRang, WindS24GaRang)
        WindCalShowRiYueShan = windCal(WindD12RiYueShan, WindD24RiYueShan, WindS12RiYueShan, WindS24RiYueShan)
        WindCalShowQingHaiHu = windCal(WindD12QingHaiHu, WindD24QingHaiHu, WindS12QingHaiHu, WindS24QingHaiHu)
        WindCalShowQiaBuQia = windCal(WindD12QiaBuQia, WindD24QiaBuQia, WindS12QiaBuQia, WindS24QiaBuQia)
        TMinShowLongYangXia = TempCalculation(TMinLongYangXia)
        TMaxShowLongYangXia = TempCalculation(TMaxLongYangXia)
        TMinShowDaoTangHe = TempCalculation(TMinDaoTangHe)
        TMaxShowDaoTangHe = TempCalculation(TMaxDaoTangHe)
        TMinShowHeKa = TempCalculation(TMinHeKa)
        TMaxShowHeKa = TempCalculation(TMaxHeKa)
        TMinShowGuoMaYing = TempCalculation(TMinGuoMaYing)
        TMaxShowGuoMaYing = TempCalculation(TMaxGuoMaYing)
        TMinShowGaRang = TempCalculation(TMinGaRang)
        TMaxShowGaRang = TempCalculation(TMaxGaRang)
        TMinShowRiYueShan = TempCalculation(TMinRiYueShan)
        TMaxShowRiYueShan = TempCalculation(TMaxRiYueShan)
        TMinShowQingHaiHu = TempCalculation(TMinQingHaiHu)
        TMaxShowQingHaiHu = TempCalculation(TMaxQingHaiHu)
        TMinShowQiaBuQia = TempCalculation(TMinQiaBuQia)
        TMaxShowQiaBuQia = TempCalculation(TMaxQiaBuQia)
        FinalWrite1 = "0" + "%02d" % Weather12LongYangXia + "%02d" % Weather24LongYangXia + " " + WindCalShowLongYangXia + " 0" + TMinShowLongYangXia + TMaxShowLongYangXia + "\n"
        FinalWrite2 = "0" + "%02d" % Weather12DaoTangHe + "%02d" % Weather24DaoTangHe + " " + WindCalShowDaoTangHe + " 0" + TMinShowDaoTangHe + TMaxShowDaoTangHe + "\n"
        FinalWrite3 = "0" + "%02d" % Weather12HeKa + "%02d" % Weather24HeKa + " " + WindCalShowHeKa + " 0" + TMinShowHeKa + TMaxShowHeKa + "\n"
        FinalWrite4 = "0" + "%02d" % Weather12GuoMaYing + "%02d" % Weather24GuoMaYing + " " + WindCalShowGuoMaYing + " 0" + TMinShowGuoMaYing + TMaxShowGuoMaYing + "\n"
        FinalWrite5 = "0" + "%02d" % Weather12GaRang + "%02d" % Weather24GaRang + " " + WindCalShowGaRang + " 0" + TMinShowGaRang + TMaxShowGaRang + "\n"
        FinalWrite6 = "0" + "%02d" % Weather12QiaBuQia + "%02d" % Weather24QiaBuQia + " " + WindCalShowQiaBuQia + " 0" + TMinShowQiaBuQia + TMaxShowQiaBuQia + "\n"
        FinalWrite7 = "0" + "%02d" % Weather12DaoTangHe + "%02d" % Weather24DaoTangHe + " " + WindCalShowDaoTangHe + " 0" + TMinShowDaoTangHe + TMaxShowDaoTangHe + "\n"
        FinalWrite8 = "0" + "%02d" % Weather12RiYueShan + "%02d" % Weather24RiYueShan + " " + WindCalShowRiYueShan + " 0" + TMinShowRiYueShan + TMaxShowRiYueShan + "\n"
        FinalWrite9 = "0" + "%02d" % Weather12LongYangXia + "%02d" % Weather24LongYangXia + " " + WindCalShowLongYangXia + " 0" + TMinShowLongYangXia + TMaxShowLongYangXia + "\n"
        FinalWrite0 = "0" + "%02d" % Weather12QingHaiHu + "%02d" % Weather24QingHaiHu + " " + WindCalShowQingHaiHu + " 0" + TMinShowQingHaiHu + TMaxShowQingHaiHu + "\n"
        file2.write(FinalWrite1)
        file2.write(FinalWrite2)
        file2.write(FinalWrite3)
        file2.write(FinalWrite4)
        file2.write(FinalWrite5)
        file2.write(FinalWrite6)
        file2.write(FinalWrite7)
        file2.write(FinalWrite8)
        file2.write(FinalWrite9)
        file2.write(FinalWrite0)

with open("E:\\data\\" + "temp.txt") as file0:
    originData = file0.readlines()
    HanQiaBuQia = "00000 " + originData[0].strip("\n") + " 恰卜恰 汉州01.rec hnd003.wav"
    HanHeYin = "00001 " + originData[1].strip("\n") + " 河阴 汉州02.rec hnd005.wav"
    HanZiKeTan = "00002 " + originData[2].strip("\n") + " 子科滩 汉州03.rec hnd007.wav"
    HanMangQu = "00003 " + originData[3].strip("\n") + " 茫曲 汉州04.rec hnd009.wav"
    HanGaBaSongDuo = "00004 " + originData[4].strip("\n") + " 尕巴松多 汉州05.rec hnd011.wav"
    HanLongYangXia = "00005 " + originData[5].strip("\n") + " 龙羊峡 汉州06.rec hnd028.wav"
    HanDaoTangHe = "00006 " + originData[6].strip("\n") + " 倒淌河镇 汉州07.rec hnd014.wav"
    HanHeKa = "00007 " + originData[7].strip("\n") + " 河卡镇 汉州08.rec hnd013.wav"
    HanGuoMaYing = "00008 " + originData[8].strip("\n") + " 过马营镇 汉州09.rec hnd016.wav"
    HanGaRang = "00009 " + originData[9].strip("\n") + " 尕让 汉州10.rec hnd074.wav"
    HanGongHeQiaBuQia = "00010 " + originData[10].strip("\n") + " 共和恰卜恰 汉县01.rec hnd003.wav"
    HanGongHeDaoTangHe = "00011 " + originData[11].strip("\n") + " 共和倒淌河 汉县02.rec hnd017.wav"
    HanGongHeRiYueShan = "00012 " + originData[12].strip("\n") + " 共和日月山 汉县03.rec hnd029.wav"
    HanGongHeLongYangXia = "00013 " + originData[13].strip("\n") + " 共和龙羊峡 汉县04.rec hnd028.wav"
    HanGongHeQingHaHu = "00014 " + originData[14].strip("\n") + " 共和青海湖 汉县05.rec hnd031.wav"

    print(HanQiaBuQia)
    print(HanHeYin)
    print(HanZiKeTan)
    print(HanMangQu)
    print(HanGaBaSongDuo)
    print(HanLongYangXia)
    print(HanDaoTangHe)
    print(HanHeKa)
    print(HanGuoMaYing)
    print(HanGaRang)
    print(HanGongHeQiaBuQia)
    print(HanGongHeDaoTangHe)
    print(HanGongHeRiYueShan)
    print(HanGongHeLongYangXia)
    print(HanGongHeQingHaHu)
    print("#####")
with open("C:\\qx00\\dat\\" + "汉语72小时.dat","w") as file1:
    file1.write(HanQiaBuQia+"\n")
    file1.write(HanHeYin+"\n")
    file1.write(HanZiKeTan+"\n")
    file1.write(HanMangQu+"\n")
    file1.write(HanGaBaSongDuo+"\n")
    file1.write(HanLongYangXia+"\n")
    file1.write(HanDaoTangHe+"\n")
    file1.write(HanHeKa+"\n")
    file1.write(HanGuoMaYing+"\n")
    file1.write(HanGaRang+"\n")
    file1.write(HanGongHeQiaBuQia+"\n")
    file1.write(HanGongHeDaoTangHe+"\n")
    file1.write(HanGongHeRiYueShan+"\n")
    file1.write(HanGongHeLongYangXia+"\n")
    file1.write(HanGongHeQingHaHu+"\n")
    file1.write("#####")

    filePath = "D:\\shengxun\\baowen\\"
    dateToday = getTime()
    fileName = checkFile(filePath, dateToday)
    print(fileName)
    fileInputPath = filePath + fileName
    lenthOfFile = checkFileLenth(fileInputPath)
    stationNum = ['52856', '52868', '52943', '52955', '52957']
    listOfStep = [1, 2]
    # 写国家站数据到文件
    fileExist = os.path.exists("E:\\data\\" + "temp.txt")
    if fileExist == True:
        os.remove("E:\\data\\" + "temp.txt")
    for i in stationNum:
        lineNum = numCheck(fileInputPath, lenthOfFile, i)
        for j in listOfStep:
            eleOfSingleStation = pickOut(fileInputPath, lineNum, 7) + pickOut(fileInputPath, lineNum, 8)
        print(eleOfSingleStation)
        Weather12 = int(float(eleOfSingleStation[3]))
        Weather24 = int(float(eleOfSingleStation[-3]))
        WindD12 = int(float(eleOfSingleStation[4]))
        WindD24 = int(float(eleOfSingleStation[-2]))
        WindS12 = int(float(eleOfSingleStation[5].split('\n')[0]))
        WindS24 = int(float(eleOfSingleStation[-1].split('\n')[0]))
        TMax = float(eleOfSingleStation[-5])
        TMin = float(eleOfSingleStation[-4])
        TMinShow = TempCalculation(TMin)
        TMaxShow = TempCalculation(TMax)
        WindCalShow = windCal(WindD12, WindD24, WindS12, WindS24)
        # 生成共和相关站信息
        if i == "52856":
            TMaxLongYangXia = TMax + 1.0
            TMinLongYangXia = TMin + 1.0
            TMaxGaRang = TMax + 1.0
            TMinGaRang = TMin + 1.0
            TMaxQiaBuQia = TMax
            TMinQiaBuQia = TMin
            WindS12LongYangXia = WindS12DaoTangHe = WindS12RiYueShan = WindS12QingHaiHu = WindS12QiaBuQia = WindS12
            WindS24LongYangXia = WindS24DaoTangHe = WindS24RiYueShan = WindS24QingHaiHu = WindS24QiaBuQia = WindS24
            WindD12LongYangXia = WindD12DaoTangHe = WindD12RiYueShan = WindD12QingHaiHu = WindD12QiaBuQia = WindD12
            WindD24LongYangXia = WindD24DaoTangHe = WindD24RiYueShan = WindD24QingHaiHu = WindD24QiaBuQia = WindD24
            Weather12LongYangXia = Weather12DaoTangHe = Weather12RiYueShan = Weather12QingHaiHu = Weather12QiaBuQia = Weather12
            Weather24LongYangXia = Weather24DaoTangHe = Weather24RiYueShan = Weather24QingHaiHu = Weather24QiaBuQia = Weather24
        # 生成兴海相关站信息
        if i == "52943":
            TMaxDaoTangHe = TMax + 1.0
            TMinDaoTangHe = TMin + 1.0
            TMaxHeKa = TMax - 1.0
            TMinHeKa = TMin - 1.0
            TMaxRiYueShan = TMaxDaoTangHe - 3.0
            TMinRiYueShan = TMinDaoTangHe - 3.0
            TMaxQingHaiHu = TMaxDaoTangHe - 1.0
            TMinQingHaiHu = TMinDaoTangHe - 1.0
            WindS12HeKa = WindS12
            WindS24HeKa = WindS24
            WindD12HeKa = WindD12
            WindD24HeKa = WindD24
            Weather12HeKa = Weather12
            Weather24HeKa = Weather24
        # 生成贵南相关站信息
        if i == "52955":
            WindS12GuoMaYing = WindS12
            WindS24GuoMaYing = WindS24
            WindD12GuoMaYing = WindD12
            WindD24GuoMaYing = WindD24
            Weather12GuoMaYing = Weather12
            Weather24GuoMaYing = Weather24
            TMinGuoMaYing = TMin
            TMaxGuoMaYing = TMax
        # 生成贵德相关站信息
        if i == "52868":
            WindS12GaRang = WindS12
            WindS24GaRang = WindS24
            WindD12GaRang = WindD12
            WindD24GaRang = WindD24
            Weather12GaRang = Weather12
            Weather24GaRang = Weather24
        FinalWrite = "0" + "%02d" % Weather12 + "%02d" % Weather24 + " " + WindCalShow + " 0" + TMinShow + TMaxShow + "\n"

        with open("E:\\data\\" + "temp.txt", "a") as file1:
            file1.write(FinalWrite)
    # 写区域站数据到文件
    with open("E:\\data\\" + "temp.txt", "a") as file2:
        WindCalShowLongYangXia = windCal(WindD12LongYangXia, WindD24LongYangXia, WindS12LongYangXia, WindS24LongYangXia)
        WindCalShowDaoTangHe = windCal(WindD12DaoTangHe, WindD24DaoTangHe, WindS12DaoTangHe, WindS24DaoTangHe)
        WindCalShowHeKa = windCal(WindD12HeKa, WindD24HeKa, WindS12HeKa, WindS24HeKa)
        WindCalShowGuoMaYing = windCal(WindD12GuoMaYing, WindD24GuoMaYing, WindS12GuoMaYing, WindS24GuoMaYing)
        WindCalShowGaRang = windCal(WindD12GaRang, WindD24GaRang, WindS12GaRang, WindS24GaRang)
        WindCalShowRiYueShan = windCal(WindD12RiYueShan, WindD24RiYueShan, WindS12RiYueShan, WindS24RiYueShan)
        WindCalShowQingHaiHu = windCal(WindD12QingHaiHu, WindD24QingHaiHu, WindS12QingHaiHu, WindS24QingHaiHu)
        WindCalShowQiaBuQia = windCal(WindD12QiaBuQia, WindD24QiaBuQia, WindS12QiaBuQia, WindS24QiaBuQia)
        TMinShowLongYangXia = TempCalculation(TMinLongYangXia)
        TMaxShowLongYangXia = TempCalculation(TMaxLongYangXia)
        TMinShowDaoTangHe = TempCalculation(TMinDaoTangHe)
        TMaxShowDaoTangHe = TempCalculation(TMaxDaoTangHe)
        TMinShowHeKa = TempCalculation(TMinHeKa)
        TMaxShowHeKa = TempCalculation(TMaxHeKa)
        TMinShowGuoMaYing = TempCalculation(TMinGuoMaYing)
        TMaxShowGuoMaYing = TempCalculation(TMaxGuoMaYing)
        TMinShowGaRang = TempCalculation(TMinGaRang)
        TMaxShowGaRang = TempCalculation(TMaxGaRang)
        TMinShowRiYueShan = TempCalculation(TMinRiYueShan)
        TMaxShowRiYueShan = TempCalculation(TMaxRiYueShan)
        TMinShowQingHaiHu = TempCalculation(TMinQingHaiHu)
        TMaxShowQingHaiHu = TempCalculation(TMaxQingHaiHu)
        TMinShowQiaBuQia = TempCalculation(TMinQiaBuQia)
        TMaxShowQiaBuQia = TempCalculation(TMaxQiaBuQia)
        FinalWrite1 = "0" + "%02d" % Weather12LongYangXia + "%02d" % Weather24LongYangXia + " " + WindCalShowLongYangXia + " 0" + TMinShowLongYangXia + TMaxShowLongYangXia + "\n"
        FinalWrite2 = "0" + "%02d" % Weather12DaoTangHe + "%02d" % Weather24DaoTangHe + " " + WindCalShowDaoTangHe + " 0" + TMinShowDaoTangHe + TMaxShowDaoTangHe + "\n"
        FinalWrite3 = "0" + "%02d" % Weather12HeKa + "%02d" % Weather24HeKa + " " + WindCalShowHeKa + " 0" + TMinShowHeKa + TMaxShowHeKa + "\n"
        FinalWrite4 = "0" + "%02d" % Weather12GuoMaYing + "%02d" % Weather24GuoMaYing + " " + WindCalShowGuoMaYing + " 0" + TMinShowGuoMaYing + TMaxShowGuoMaYing + "\n"
        FinalWrite5 = "0" + "%02d" % Weather12GaRang + "%02d" % Weather24GaRang + " " + WindCalShowGaRang + " 0" + TMinShowGaRang + TMaxShowGaRang + "\n"
        FinalWrite6 = "0" + "%02d" % Weather12QiaBuQia + "%02d" % Weather24QiaBuQia + " " + WindCalShowQiaBuQia + " 0" + TMinShowQiaBuQia + TMaxShowQiaBuQia + "\n"
        FinalWrite7 = "0" + "%02d" % Weather12DaoTangHe + "%02d" % Weather24DaoTangHe + " " + WindCalShowDaoTangHe + " 0" + TMinShowDaoTangHe + TMaxShowDaoTangHe + "\n"
        FinalWrite8 = "0" + "%02d" % Weather12RiYueShan + "%02d" % Weather24RiYueShan + " " + WindCalShowRiYueShan + " 0" + TMinShowRiYueShan + TMaxShowRiYueShan + "\n"
        FinalWrite9 = "0" + "%02d" % Weather12LongYangXia + "%02d" % Weather24LongYangXia + " " + WindCalShowLongYangXia + " 0" + TMinShowLongYangXia + TMaxShowLongYangXia + "\n"
        FinalWrite0 = "0" + "%02d" % Weather12QingHaiHu + "%02d" % Weather24QingHaiHu + " " + WindCalShowQingHaiHu + " 0" + TMinShowQingHaiHu + TMaxShowQingHaiHu + "\n"
        file2.write(FinalWrite1)
        file2.write(FinalWrite2)
        file2.write(FinalWrite3)
        file2.write(FinalWrite4)
        file2.write(FinalWrite5)
        file2.write(FinalWrite6)
        file2.write(FinalWrite7)
        file2.write(FinalWrite8)
        file2.write(FinalWrite9)
        file2.write(FinalWrite0)

with open("E:\\data\\" + "temp.txt") as file0:
    originData = file0.readlines()
    HanQiaBuQia = "00000 " + originData[0].strip("\n") + " 恰卜恰 汉州01.rec hnd003.wav"
    HanHeYin = "00001 " + originData[1].strip("\n") + " 河阴 汉州02.rec hnd005.wav"
    HanZiKeTan = "00002 " + originData[2].strip("\n") + " 子科滩 汉州03.rec hnd007.wav"
    HanMangQu = "00003 " + originData[3].strip("\n") + " 茫曲 汉州04.rec hnd009.wav"
    HanGaBaSongDuo = "00004 " + originData[4].strip("\n") + " 尕巴松多 汉州05.rec hnd011.wav"
    HanLongYangXia = "00005 " + originData[5].strip("\n") + " 龙羊峡 汉州06.rec hnd028.wav"
    HanDaoTangHe = "00006 " + originData[6].strip("\n") + " 倒淌河镇 汉州07.rec hnd014.wav"
    HanHeKa = "00007 " + originData[7].strip("\n") + " 河卡镇 汉州08.rec hnd013.wav"
    HanGuoMaYing = "00008 " + originData[8].strip("\n") + " 过马营镇 汉州09.rec hnd016.wav"
    HanGaRang = "00009 " + originData[9].strip("\n") + " 尕让 汉州10.rec hnd074.wav"
    HanGongHeQiaBuQia = "00010 " + originData[10].strip("\n") + " 共和恰卜恰 汉县01.rec hnd003.wav"
    HanGongHeDaoTangHe = "00011 " + originData[11].strip("\n") + " 共和倒淌河 汉县02.rec hnd017.wav"
    HanGongHeRiYueShan = "00012 " + originData[12].strip("\n") + " 共和日月山 汉县03.rec hnd029.wav"
    HanGongHeLongYangXia = "00013 " + originData[13].strip("\n") + " 共和龙羊峡 汉县04.rec hnd028.wav"
    HanGongHeQingHaHu = "00014 " + originData[14].strip("\n") + " 共和青海湖 汉县05.rec hnd031.wav"

    print(HanQiaBuQia)
    print(HanHeYin)
    print(HanZiKeTan)
    print(HanMangQu)
    print(HanGaBaSongDuo)
    print(HanLongYangXia)
    print(HanDaoTangHe)
    print(HanHeKa)
    print(HanGuoMaYing)
    print(HanGaRang)
    print(HanGongHeQiaBuQia)
    print(HanGongHeDaoTangHe)
    print(HanGongHeRiYueShan)
    print(HanGongHeLongYangXia)
    print(HanGongHeQingHaHu)
    print("#####")
with open("C:\\qx00\\dat\\" + "汉语96小时.dat", "w") as file1:
    file1.write(HanQiaBuQia + "\n")
    file1.write(HanHeYin + "\n")
    file1.write(HanZiKeTan + "\n")
    file1.write(HanMangQu + "\n")
    file1.write(HanGaBaSongDuo + "\n")
    file1.write(HanLongYangXia + "\n")
    file1.write(HanDaoTangHe + "\n")
    file1.write(HanHeKa + "\n")
    file1.write(HanGuoMaYing + "\n")
    file1.write(HanGaRang + "\n")
    file1.write(HanGongHeQiaBuQia + "\n")
    file1.write(HanGongHeDaoTangHe + "\n")
    file1.write(HanGongHeRiYueShan + "\n")
    file1.write(HanGongHeLongYangXia + "\n")
    file1.write(HanGongHeQingHaHu + "\n")
    file1.write("#####")

    filePath = "D:\\shengxun\\baowen\\"
    dateToday = getTime()
    fileName = checkFile(filePath, dateToday)
    print(fileName)
    fileInputPath = filePath + fileName
    lenthOfFile = checkFileLenth(fileInputPath)
    stationNum = ['52856', '52868', '52943', '52955', '52957']
    listOfStep = [1, 2]
    # 写国家站数据到文件
    fileExist = os.path.exists("E:\\data\\" + "temp.txt")
    if fileExist == True:
        os.remove("E:\\data\\" + "temp.txt")
    for i in stationNum:
        lineNum = numCheck(fileInputPath, lenthOfFile, i)
        for j in listOfStep:
            eleOfSingleStation = pickOut(fileInputPath, lineNum, 1) + pickOut(fileInputPath, lineNum, 2)
        print(eleOfSingleStation)
        Weather12 = int(float(eleOfSingleStation[3]))
        Weather24 = int(float(eleOfSingleStation[-3]))
        WindD12 = int(float(eleOfSingleStation[4]))
        WindD24 = int(float(eleOfSingleStation[-2]))
        WindS12 = int(float(eleOfSingleStation[5].split('\n')[0]))
        WindS24 = int(float(eleOfSingleStation[-1].split('\n')[0]))
        TMax = float(eleOfSingleStation[-5])
        TMin = float(eleOfSingleStation[-4])
        TMinShow = TempCalculation(TMin)
        TMaxShow = TempCalculation(TMax)
        WindCalShow = windCal(WindD12, WindD24, WindS12, WindS24)
        # 生成共和相关站信息
        if i == "52856":
            TMaxLongYangXia = TMax + 1.0
            TMinLongYangXia = TMin + 1.0
            TMaxGaRang = TMax + 1.0
            TMinGaRang = TMin + 1.0
            TMaxQiaBuQia = TMax
            TMinQiaBuQia = TMin
            WindS12LongYangXia = WindS12DaoTangHe = WindS12RiYueShan = WindS12QingHaiHu = WindS12QiaBuQia = WindS12
            WindS24LongYangXia = WindS24DaoTangHe = WindS24RiYueShan = WindS24QingHaiHu = WindS24QiaBuQia = WindS24
            WindD12LongYangXia = WindD12DaoTangHe = WindD12RiYueShan = WindD12QingHaiHu = WindD12QiaBuQia = WindD12
            WindD24LongYangXia = WindD24DaoTangHe = WindD24RiYueShan = WindD24QingHaiHu = WindD24QiaBuQia = WindD24
            Weather12LongYangXia = Weather12DaoTangHe = Weather12RiYueShan = Weather12QingHaiHu = Weather12QiaBuQia = Weather12
            Weather24LongYangXia = Weather24DaoTangHe = Weather24RiYueShan = Weather24QingHaiHu = Weather24QiaBuQia = Weather24
        # 生成兴海相关站信息
        if i == "52943":
            TMaxDaoTangHe = TMax + 1.0
            TMinDaoTangHe = TMin + 1.0
            TMaxHeKa = TMax - 1.0
            TMinHeKa = TMin - 1.0
            TMaxRiYueShan = TMaxDaoTangHe - 3.0
            TMinRiYueShan = TMinDaoTangHe - 3.0
            TMaxQingHaiHu = TMaxDaoTangHe - 1.0
            TMinQingHaiHu = TMinDaoTangHe - 1.0
            WindS12HeKa = WindS12
            WindS24HeKa = WindS24
            WindD12HeKa = WindD12
            WindD24HeKa = WindD24
            Weather12HeKa = Weather12
            Weather24HeKa = Weather24
        # 生成贵南相关站信息
        if i == "52955":
            WindS12GuoMaYing = WindS12
            WindS24GuoMaYing = WindS24
            WindD12GuoMaYing = WindD12
            WindD24GuoMaYing = WindD24
            Weather12GuoMaYing = Weather12
            Weather24GuoMaYing = Weather24
            TMinGuoMaYing = TMin
            TMaxGuoMaYing = TMax
        # 生成贵德相关站信息
        if i == "52868":
            WindS12GaRang = WindS12
            WindS24GaRang = WindS24
            WindD12GaRang = WindD12
            WindD24GaRang = WindD24
            Weather12GaRang = Weather12
            Weather24GaRang = Weather24
        FinalWrite = "2" + "%02d" % Weather12 + "%02d" % Weather24 + " " + WindCalShow + " 0" + TMinShow + TMaxShow + "\n"

        with open("E:\\data\\" + "temp.txt", "a") as file1:
            file1.write(FinalWrite)
    # 写区域站数据到文件
    with open("E:\\data\\" + "temp.txt", "a") as file2:
        WindCalShowLongYangXia = windCal(WindD12LongYangXia, WindD24LongYangXia, WindS12LongYangXia, WindS24LongYangXia)
        WindCalShowDaoTangHe = windCal(WindD12DaoTangHe, WindD24DaoTangHe, WindS12DaoTangHe, WindS24DaoTangHe)
        WindCalShowHeKa = windCal(WindD12HeKa, WindD24HeKa, WindS12HeKa, WindS24HeKa)
        WindCalShowGuoMaYing = windCal(WindD12GuoMaYing, WindD24GuoMaYing, WindS12GuoMaYing, WindS24GuoMaYing)
        WindCalShowGaRang = windCal(WindD12GaRang, WindD24GaRang, WindS12GaRang, WindS24GaRang)
        WindCalShowRiYueShan = windCal(WindD12RiYueShan, WindD24RiYueShan, WindS12RiYueShan, WindS24RiYueShan)
        WindCalShowQingHaiHu = windCal(WindD12QingHaiHu, WindD24QingHaiHu, WindS12QingHaiHu, WindS24QingHaiHu)
        WindCalShowQiaBuQia = windCal(WindD12QiaBuQia, WindD24QiaBuQia, WindS12QiaBuQia, WindS24QiaBuQia)
        TMinShowLongYangXia = TempCalculation(TMinLongYangXia)
        TMaxShowLongYangXia = TempCalculation(TMaxLongYangXia)
        TMinShowDaoTangHe = TempCalculation(TMinDaoTangHe)
        TMaxShowDaoTangHe = TempCalculation(TMaxDaoTangHe)
        TMinShowHeKa = TempCalculation(TMinHeKa)
        TMaxShowHeKa = TempCalculation(TMaxHeKa)
        TMinShowGuoMaYing = TempCalculation(TMinGuoMaYing)
        TMaxShowGuoMaYing = TempCalculation(TMaxGuoMaYing)
        TMinShowGaRang = TempCalculation(TMinGaRang)
        TMaxShowGaRang = TempCalculation(TMaxGaRang)
        TMinShowRiYueShan = TempCalculation(TMinRiYueShan)
        TMaxShowRiYueShan = TempCalculation(TMaxRiYueShan)
        TMinShowQingHaiHu = TempCalculation(TMinQingHaiHu)
        TMaxShowQingHaiHu = TempCalculation(TMaxQingHaiHu)
        TMinShowQiaBuQia = TempCalculation(TMinQiaBuQia)
        TMaxShowQiaBuQia = TempCalculation(TMaxQiaBuQia)
        FinalWrite1 = "2" + "%02d" % Weather12LongYangXia + "%02d" % Weather24LongYangXia + " " + WindCalShowLongYangXia + " 0" + TMinShowLongYangXia + TMaxShowLongYangXia + "\n"
        FinalWrite2 = "2" + "%02d" % Weather12DaoTangHe + "%02d" % Weather24DaoTangHe + " " + WindCalShowDaoTangHe + " 0" + TMinShowDaoTangHe + TMaxShowDaoTangHe + "\n"
        FinalWrite3 = "2" + "%02d" % Weather12HeKa + "%02d" % Weather24HeKa + " " + WindCalShowHeKa + " 0" + TMinShowHeKa + TMaxShowHeKa + "\n"
        FinalWrite4 = "2" + "%02d" % Weather12GuoMaYing + "%02d" % Weather24GuoMaYing + " " + WindCalShowGuoMaYing + " 0" + TMinShowGuoMaYing + TMaxShowGuoMaYing + "\n"
        FinalWrite5 = "2" + "%02d" % Weather12GaRang + "%02d" % Weather24GaRang + " " + WindCalShowGaRang + " 0" + TMinShowGaRang + TMaxShowGaRang + "\n"
        FinalWrite6 = "2" + "%02d" % Weather12QiaBuQia + "%02d" % Weather24QiaBuQia + " " + WindCalShowQiaBuQia + " 0" + TMinShowQiaBuQia + TMaxShowQiaBuQia + "\n"
        FinalWrite7 = "2" + "%02d" % Weather12DaoTangHe + "%02d" % Weather24DaoTangHe + " " + WindCalShowDaoTangHe + " 0" + TMinShowDaoTangHe + TMaxShowDaoTangHe + "\n"
        FinalWrite8 = "2" + "%02d" % Weather12RiYueShan + "%02d" % Weather24RiYueShan + " " + WindCalShowRiYueShan + " 0" + TMinShowRiYueShan + TMaxShowRiYueShan + "\n"
        FinalWrite9 = "2" + "%02d" % Weather12LongYangXia + "%02d" % Weather24LongYangXia + " " + WindCalShowLongYangXia + " 0" + TMinShowLongYangXia + TMaxShowLongYangXia + "\n"
        FinalWrite0 = "2" + "%02d" % Weather12QingHaiHu + "%02d" % Weather24QingHaiHu + " " + WindCalShowQingHaiHu + " 0" + TMinShowQingHaiHu + TMaxShowQingHaiHu + "\n"
        file2.write(FinalWrite1)
        file2.write(FinalWrite2)
        file2.write(FinalWrite3)
        file2.write(FinalWrite4)
        file2.write(FinalWrite5)
        file2.write(FinalWrite6)
        file2.write(FinalWrite7)
        file2.write(FinalWrite8)
        file2.write(FinalWrite9)
        file2.write(FinalWrite0)

with open("E:\\data\\" + "temp.txt") as file0:
    originData = file0.readlines()
    ZangQiaBuQia = "00000 " + originData[0].strip("\n") + " 恰卜恰 藏州01.rec hnd003.wav"
    ZangHeYin = "00001 " + originData[1].strip("\n") + " 河阴 藏州02.rec hnd005.wav"
    ZangZiKeTan = "00002 " + originData[2].strip("\n") + " 子科滩 藏州03.rec hnd007.wav"
    ZangMangQu = "00003 " + originData[3].strip("\n") + " 茫曲 藏州04.rec hnd009.wav"
    ZangGaBaSongDuo = "00004 " + originData[4].strip("\n") + " 尕巴松多 藏州05.rec hnd011.wav"
    ZangLongYangXia = "00005 " + originData[5].strip("\n") + " 龙羊峡 藏州06.rec hnd028.wav"
    ZangDaoTangHe = "00006 " + originData[6].strip("\n") + " 倒淌河镇 藏州07.rec hnd014.wav"
    ZangHeKa = "00007 " + originData[7].strip("\n") + " 河卡镇 藏州08.rec hnd013.wav"
    ZangGuoMaYing = "00008 " + originData[8].strip("\n") + " 过马营镇 藏州09.rec hnd016.wav"
    ZangGaRang = "00009 " + originData[9].strip("\n") + " 尕让 藏州10.rec hnd074.wav"
    ZangGongHeQiaBuQia = "00010 " + originData[10].strip("\n") + " 共和恰卜恰 藏县01.rec hnd003.wav"
    ZangGongHeDaoTangHe = "00011 " + originData[11].strip("\n") + " 共和倒淌河 藏县02.rec hnd017.wav"
    ZangGongHeRiYueShan = "00012 " + originData[12].strip("\n") + " 共和日月山 藏县03.rec hnd029.wav"
    ZangGongHeLongYangXia = "00013 " + originData[13].strip("\n") + " 共和龙羊峡 藏县04.rec hnd028.wav"
    ZangGongHeQingHaHu = "00014 " + originData[14].strip("\n") + " 共和青海湖 藏县05.rec hnd031.wav"

    print(ZangQiaBuQia)
    print(ZangHeYin)
    print(ZangZiKeTan)
    print(ZangMangQu)
    print(ZangGaBaSongDuo)
    print(ZangLongYangXia)
    print(ZangDaoTangHe)
    print(ZangHeKa)
    print(ZangGuoMaYing)
    print(ZangGaRang)
    print(ZangGongHeQiaBuQia)
    print(ZangGongHeDaoTangHe)
    print(ZangGongHeRiYueShan)
    print(ZangGongHeLongYangXia)
    print(ZangGongHeQingHaHu)
    print("#####")
with open("D:\qx00\\dat\\" + "藏语24小时.dat", "w") as file1:
    file1.write(ZangQiaBuQia + "\n")
    file1.write(ZangHeYin + "\n")
    file1.write(ZangZiKeTan + "\n")
    file1.write(ZangMangQu + "\n")
    file1.write(ZangGaBaSongDuo + "\n")
    file1.write(ZangLongYangXia + "\n")
    file1.write(ZangDaoTangHe + "\n")
    file1.write(ZangHeKa + "\n")
    file1.write(ZangGuoMaYing + "\n")
    file1.write(ZangGaRang + "\n")
    file1.write(ZangGongHeQiaBuQia + "\n")
    file1.write(ZangGongHeDaoTangHe + "\n")
    file1.write(ZangGongHeRiYueShan + "\n")
    file1.write(ZangGongHeLongYangXia + "\n")
    file1.write(ZangGongHeQingHaHu + "\n")
    file1.write("#####")

    filePath = "D:\\shengxun\\baowen\\"
    dateToday = getTime()
    fileName = checkFile(filePath, dateToday)
    print(fileName)
    fileInputPath = filePath + fileName
    lenthOfFile = checkFileLenth(fileInputPath)
    stationNum = ['52856', '52868', '52943', '52955', '52957']
    listOfStep = [1, 2]
    # 写国家站数据到文件
    fileExist = os.path.exists("E:\\data\\" + "temp.txt")
    if fileExist == True:
        os.remove("E:\\data\\" + "temp.txt")
    for i in stationNum:
        lineNum = numCheck(fileInputPath, lenthOfFile, i)
        for j in listOfStep:
            eleOfSingleStation = pickOut(fileInputPath, lineNum, 3) + pickOut(fileInputPath, lineNum, 4)
        print(eleOfSingleStation)
        Weather12 = int(float(eleOfSingleStation[3]))
        Weather24 = int(float(eleOfSingleStation[-3]))
        WindD12 = int(float(eleOfSingleStation[4]))
        WindD24 = int(float(eleOfSingleStation[-2]))
        WindS12 = int(float(eleOfSingleStation[5].split('\n')[0]))
        WindS24 = int(float(eleOfSingleStation[-1].split('\n')[0]))
        TMax = float(eleOfSingleStation[-5])
        TMin = float(eleOfSingleStation[-4])
        TMinShow = TempCalculation(TMin)
        TMaxShow = TempCalculation(TMax)
        WindCalShow = windCal(WindD12, WindD24, WindS12, WindS24)
        # 生成共和相关站信息
        if i == "52856":
            TMaxLongYangXia = TMax + 1.0
            TMinLongYangXia = TMin + 1.0
            TMaxGaRang = TMax + 1.0
            TMinGaRang = TMin + 1.0
            TMaxQiaBuQia = TMax
            TMinQiaBuQia = TMin
            WindS12LongYangXia = WindS12DaoTangHe = WindS12RiYueShan = WindS12QingHaiHu = WindS12QiaBuQia = WindS12
            WindS24LongYangXia = WindS24DaoTangHe = WindS24RiYueShan = WindS24QingHaiHu = WindS24QiaBuQia = WindS24
            WindD12LongYangXia = WindD12DaoTangHe = WindD12RiYueShan = WindD12QingHaiHu = WindD12QiaBuQia = WindD12
            WindD24LongYangXia = WindD24DaoTangHe = WindD24RiYueShan = WindD24QingHaiHu = WindD24QiaBuQia = WindD24
            Weather12LongYangXia = Weather12DaoTangHe = Weather12RiYueShan = Weather12QingHaiHu = Weather12QiaBuQia = Weather12
            Weather24LongYangXia = Weather24DaoTangHe = Weather24RiYueShan = Weather24QingHaiHu = Weather24QiaBuQia = Weather24
        # 生成兴海相关站信息
        if i == "52943":
            TMaxDaoTangHe = TMax + 1.0
            TMinDaoTangHe = TMin + 1.0
            TMaxHeKa = TMax - 1.0
            TMinHeKa = TMin - 1.0
            TMaxRiYueShan = TMaxDaoTangHe - 3.0
            TMinRiYueShan = TMinDaoTangHe - 3.0
            TMaxQingHaiHu = TMaxDaoTangHe - 1.0
            TMinQingHaiHu = TMinDaoTangHe - 1.0
            WindS12HeKa = WindS12
            WindS24HeKa = WindS24
            WindD12HeKa = WindD12
            WindD24HeKa = WindD24
            Weather12HeKa = Weather12
            Weather24HeKa = Weather24
        # 生成贵南相关站信息
        if i == "52955":
            WindS12GuoMaYing = WindS12
            WindS24GuoMaYing = WindS24
            WindD12GuoMaYing = WindD12
            WindD24GuoMaYing = WindD24
            Weather12GuoMaYing = Weather12
            Weather24GuoMaYing = Weather24
            TMinGuoMaYing = TMin
            TMaxGuoMaYing = TMax
        # 生成贵德相关站信息
        if i == "52868":
            WindS12GaRang = WindS12
            WindS24GaRang = WindS24
            WindD12GaRang = WindD12
            WindD24GaRang = WindD24
            Weather12GaRang = Weather12
            Weather24GaRang = Weather24
        FinalWrite = "2" + "%02d" % Weather12 + "%02d" % Weather24 + " " + WindCalShow + " 0" + TMinShow + TMaxShow + "\n"

        with open("E:\\data\\" + "temp.txt", "a") as file1:
            file1.write(FinalWrite)
    # 写区域站数据到文件
    with open("E:\\data\\" + "temp.txt", "a") as file2:
        WindCalShowLongYangXia = windCal(WindD12LongYangXia, WindD24LongYangXia, WindS12LongYangXia, WindS24LongYangXia)
        WindCalShowDaoTangHe = windCal(WindD12DaoTangHe, WindD24DaoTangHe, WindS12DaoTangHe, WindS24DaoTangHe)
        WindCalShowHeKa = windCal(WindD12HeKa, WindD24HeKa, WindS12HeKa, WindS24HeKa)
        WindCalShowGuoMaYing = windCal(WindD12GuoMaYing, WindD24GuoMaYing, WindS12GuoMaYing, WindS24GuoMaYing)
        WindCalShowGaRang = windCal(WindD12GaRang, WindD24GaRang, WindS12GaRang, WindS24GaRang)
        WindCalShowRiYueShan = windCal(WindD12RiYueShan, WindD24RiYueShan, WindS12RiYueShan, WindS24RiYueShan)
        WindCalShowQingHaiHu = windCal(WindD12QingHaiHu, WindD24QingHaiHu, WindS12QingHaiHu, WindS24QingHaiHu)
        WindCalShowQiaBuQia = windCal(WindD12QiaBuQia, WindD24QiaBuQia, WindS12QiaBuQia, WindS24QiaBuQia)
        TMinShowLongYangXia = TempCalculation(TMinLongYangXia)
        TMaxShowLongYangXia = TempCalculation(TMaxLongYangXia)
        TMinShowDaoTangHe = TempCalculation(TMinDaoTangHe)
        TMaxShowDaoTangHe = TempCalculation(TMaxDaoTangHe)
        TMinShowHeKa = TempCalculation(TMinHeKa)
        TMaxShowHeKa = TempCalculation(TMaxHeKa)
        TMinShowGuoMaYing = TempCalculation(TMinGuoMaYing)
        TMaxShowGuoMaYing = TempCalculation(TMaxGuoMaYing)
        TMinShowGaRang = TempCalculation(TMinGaRang)
        TMaxShowGaRang = TempCalculation(TMaxGaRang)
        TMinShowRiYueShan = TempCalculation(TMinRiYueShan)
        TMaxShowRiYueShan = TempCalculation(TMaxRiYueShan)
        TMinShowQingHaiHu = TempCalculation(TMinQingHaiHu)
        TMaxShowQingHaiHu = TempCalculation(TMaxQingHaiHu)
        TMinShowQiaBuQia = TempCalculation(TMinQiaBuQia)
        TMaxShowQiaBuQia = TempCalculation(TMaxQiaBuQia)
        FinalWrite1 = "2" + "%02d" % Weather12LongYangXia + "%02d" % Weather24LongYangXia + " " + WindCalShowLongYangXia + " 0" + TMinShowLongYangXia + TMaxShowLongYangXia + "\n"
        FinalWrite2 = "2" + "%02d" % Weather12DaoTangHe + "%02d" % Weather24DaoTangHe + " " + WindCalShowDaoTangHe + " 0" + TMinShowDaoTangHe + TMaxShowDaoTangHe + "\n"
        FinalWrite3 = "2" + "%02d" % Weather12HeKa + "%02d" % Weather24HeKa + " " + WindCalShowHeKa + " 0" + TMinShowHeKa + TMaxShowHeKa + "\n"
        FinalWrite4 = "2" + "%02d" % Weather12GuoMaYing + "%02d" % Weather24GuoMaYing + " " + WindCalShowGuoMaYing + " 0" + TMinShowGuoMaYing + TMaxShowGuoMaYing + "\n"
        FinalWrite5 = "2" + "%02d" % Weather12GaRang + "%02d" % Weather24GaRang + " " + WindCalShowGaRang + " 0" + TMinShowGaRang + TMaxShowGaRang + "\n"
        FinalWrite6 = "2" + "%02d" % Weather12QiaBuQia + "%02d" % Weather24QiaBuQia + " " + WindCalShowQiaBuQia + " 0" + TMinShowQiaBuQia + TMaxShowQiaBuQia + "\n"
        FinalWrite7 = "2" + "%02d" % Weather12DaoTangHe + "%02d" % Weather24DaoTangHe + " " + WindCalShowDaoTangHe + " 0" + TMinShowDaoTangHe + TMaxShowDaoTangHe + "\n"
        FinalWrite8 = "2" + "%02d" % Weather12RiYueShan + "%02d" % Weather24RiYueShan + " " + WindCalShowRiYueShan + " 0" + TMinShowRiYueShan + TMaxShowRiYueShan + "\n"
        FinalWrite9 = "2" + "%02d" % Weather12LongYangXia + "%02d" % Weather24LongYangXia + " " + WindCalShowLongYangXia + " 0" + TMinShowLongYangXia + TMaxShowLongYangXia + "\n"
        FinalWrite0 = "2" + "%02d" % Weather12QingHaiHu + "%02d" % Weather24QingHaiHu + " " + WindCalShowQingHaiHu + " 0" + TMinShowQingHaiHu + TMaxShowQingHaiHu + "\n"
        file2.write(FinalWrite1)
        file2.write(FinalWrite2)
        file2.write(FinalWrite3)
        file2.write(FinalWrite4)
        file2.write(FinalWrite5)
        file2.write(FinalWrite6)
        file2.write(FinalWrite7)
        file2.write(FinalWrite8)
        file2.write(FinalWrite9)
        file2.write(FinalWrite0)

with open("E:\\data\\" + "temp.txt") as file0:
    originData = file0.readlines()
    ZangQiaBuQia = "00000 " + originData[0].strip("\n") + " 恰卜恰 藏州01.rec hnd003.wav"
    ZangHeYin = "00001 " + originData[1].strip("\n") + " 河阴 藏州02.rec hnd005.wav"
    ZangZiKeTan = "00002 " + originData[2].strip("\n") + " 子科滩 藏州03.rec hnd007.wav"
    ZangMangQu = "00003 " + originData[3].strip("\n") + " 茫曲 藏州04.rec hnd009.wav"
    ZangGaBaSongDuo = "00004 " + originData[4].strip("\n") + " 尕巴松多 藏州05.rec hnd011.wav"
    ZangLongYangXia = "00005 " + originData[5].strip("\n") + " 龙羊峡 藏州06.rec hnd028.wav"
    ZangDaoTangHe = "00006 " + originData[6].strip("\n") + " 倒淌河镇 藏州07.rec hnd014.wav"
    ZangHeKa = "00007 " + originData[7].strip("\n") + " 河卡镇 藏州08.rec hnd013.wav"
    ZangGuoMaYing = "00008 " + originData[8].strip("\n") + " 过马营镇 藏州09.rec hnd016.wav"
    ZangGaRang = "00009 " + originData[9].strip("\n") + " 尕让 藏州10.rec hnd074.wav"
    ZangGongHeQiaBuQia = "00010 " + originData[10].strip("\n") + " 共和恰卜恰 藏县01.rec hnd003.wav"
    ZangGongHeDaoTangHe = "00011 " + originData[11].strip("\n") + " 共和倒淌河 藏县02.rec hnd017.wav"
    ZangGongHeRiYueShan = "00012 " + originData[12].strip("\n") + " 共和日月山 藏县03.rec hnd029.wav"
    ZangGongHeLongYangXia = "00013 " + originData[13].strip("\n") + " 共和龙羊峡 藏县04.rec hnd028.wav"
    ZangGongHeQingHaHu = "00014 " + originData[14].strip("\n") + " 共和青海湖 藏县05.rec hnd031.wav"

    print(ZangQiaBuQia)
    print(ZangHeYin)
    print(ZangZiKeTan)
    print(ZangMangQu)
    print(ZangGaBaSongDuo)
    print(ZangLongYangXia)
    print(ZangDaoTangHe)
    print(ZangHeKa)
    print(ZangGuoMaYing)
    print(ZangGaRang)
    print(ZangGongHeQiaBuQia)
    print(ZangGongHeDaoTangHe)
    print(ZangGongHeRiYueShan)
    print(ZangGongHeLongYangXia)
    print(ZangGongHeQingHaHu)
    print("#####")
with open("D:\qx00\\dat\\" + "藏语48小时.dat", "w") as file1:
    file1.write(ZangQiaBuQia + "\n")
    file1.write(ZangHeYin + "\n")
    file1.write(ZangZiKeTan + "\n")
    file1.write(ZangMangQu + "\n")
    file1.write(ZangGaBaSongDuo + "\n")
    file1.write(ZangLongYangXia + "\n")
    file1.write(ZangDaoTangHe + "\n")
    file1.write(ZangHeKa + "\n")
    file1.write(ZangGuoMaYing + "\n")
    file1.write(ZangGaRang + "\n")
    file1.write(ZangGongHeQiaBuQia + "\n")
    file1.write(ZangGongHeDaoTangHe + "\n")
    file1.write(ZangGongHeRiYueShan + "\n")
    file1.write(ZangGongHeLongYangXia + "\n")
    file1.write(ZangGongHeQingHaHu + "\n")
    file1.write("#####")

    filePath = "D:\\shengxun\\baowen\\"
    dateToday = getTime()
    fileName = checkFile(filePath, dateToday)
    print(fileName)
    fileInputPath = filePath + fileName
    lenthOfFile = checkFileLenth(fileInputPath)
    stationNum = ['52856', '52868', '52943', '52955', '52957']
    listOfStep = [1, 2]
    # 写国家站数据到文件
    fileExist = os.path.exists("E:\\data\\" + "temp.txt")
    if fileExist == True:
        os.remove("E:\\data\\" + "temp.txt")
    for i in stationNum:
        lineNum = numCheck(fileInputPath, lenthOfFile, i)
        for j in listOfStep:
            eleOfSingleStation = pickOut(fileInputPath, lineNum, 5) + pickOut(fileInputPath, lineNum, 6)
        print(eleOfSingleStation)
        Weather12 = int(float(eleOfSingleStation[3]))
        Weather24 = int(float(eleOfSingleStation[-3]))
        WindD12 = int(float(eleOfSingleStation[4]))
        WindD24 = int(float(eleOfSingleStation[-2]))
        WindS12 = int(float(eleOfSingleStation[5].split('\n')[0]))
        WindS24 = int(float(eleOfSingleStation[-1].split('\n')[0]))
        TMax = float(eleOfSingleStation[-5])
        TMin = float(eleOfSingleStation[-4])
        TMinShow = TempCalculation(TMin)
        TMaxShow = TempCalculation(TMax)
        WindCalShow = windCal(WindD12, WindD24, WindS12, WindS24)
        # 生成共和相关站信息
        if i == "52856":
            TMaxLongYangXia = TMax + 1.0
            TMinLongYangXia = TMin + 1.0
            TMaxGaRang = TMax + 1.0
            TMinGaRang = TMin + 1.0
            TMaxQiaBuQia = TMax
            TMinQiaBuQia = TMin
            WindS12LongYangXia = WindS12DaoTangHe = WindS12RiYueShan = WindS12QingHaiHu = WindS12QiaBuQia = WindS12
            WindS24LongYangXia = WindS24DaoTangHe = WindS24RiYueShan = WindS24QingHaiHu = WindS24QiaBuQia = WindS24
            WindD12LongYangXia = WindD12DaoTangHe = WindD12RiYueShan = WindD12QingHaiHu = WindD12QiaBuQia = WindD12
            WindD24LongYangXia = WindD24DaoTangHe = WindD24RiYueShan = WindD24QingHaiHu = WindD24QiaBuQia = WindD24
            Weather12LongYangXia = Weather12DaoTangHe = Weather12RiYueShan = Weather12QingHaiHu = Weather12QiaBuQia = Weather12
            Weather24LongYangXia = Weather24DaoTangHe = Weather24RiYueShan = Weather24QingHaiHu = Weather24QiaBuQia = Weather24
        # 生成兴海相关站信息
        if i == "52943":
            TMaxDaoTangHe = TMax + 1.0
            TMinDaoTangHe = TMin + 1.0
            TMaxHeKa = TMax - 1.0
            TMinHeKa = TMin - 1.0
            TMaxRiYueShan = TMaxDaoTangHe - 3.0
            TMinRiYueShan = TMinDaoTangHe - 3.0
            TMaxQingHaiHu = TMaxDaoTangHe - 1.0
            TMinQingHaiHu = TMinDaoTangHe - 1.0
            WindS12HeKa = WindS12
            WindS24HeKa = WindS24
            WindD12HeKa = WindD12
            WindD24HeKa = WindD24
            Weather12HeKa = Weather12
            Weather24HeKa = Weather24
        # 生成贵南相关站信息
        if i == "52955":
            WindS12GuoMaYing = WindS12
            WindS24GuoMaYing = WindS24
            WindD12GuoMaYing = WindD12
            WindD24GuoMaYing = WindD24
            Weather12GuoMaYing = Weather12
            Weather24GuoMaYing = Weather24
            TMinGuoMaYing = TMin
            TMaxGuoMaYing = TMax
        # 生成贵德相关站信息
        if i == "52868":
            WindS12GaRang = WindS12
            WindS24GaRang = WindS24
            WindD12GaRang = WindD12
            WindD24GaRang = WindD24
            Weather12GaRang = Weather12
            Weather24GaRang = Weather24
        FinalWrite = "2" + "%02d" % Weather12 + "%02d" % Weather24 + " " + WindCalShow + " 0" + TMinShow + TMaxShow + "\n"

        with open("E:\\data\\" + "temp.txt", "a") as file1:
            file1.write(FinalWrite)
    # 写区域站数据到文件
    with open("E:\\data\\" + "temp.txt", "a") as file2:
        WindCalShowLongYangXia = windCal(WindD12LongYangXia, WindD24LongYangXia, WindS12LongYangXia, WindS24LongYangXia)
        WindCalShowDaoTangHe = windCal(WindD12DaoTangHe, WindD24DaoTangHe, WindS12DaoTangHe, WindS24DaoTangHe)
        WindCalShowHeKa = windCal(WindD12HeKa, WindD24HeKa, WindS12HeKa, WindS24HeKa)
        WindCalShowGuoMaYing = windCal(WindD12GuoMaYing, WindD24GuoMaYing, WindS12GuoMaYing, WindS24GuoMaYing)
        WindCalShowGaRang = windCal(WindD12GaRang, WindD24GaRang, WindS12GaRang, WindS24GaRang)
        WindCalShowRiYueShan = windCal(WindD12RiYueShan, WindD24RiYueShan, WindS12RiYueShan, WindS24RiYueShan)
        WindCalShowQingHaiHu = windCal(WindD12QingHaiHu, WindD24QingHaiHu, WindS12QingHaiHu, WindS24QingHaiHu)
        WindCalShowQiaBuQia = windCal(WindD12QiaBuQia, WindD24QiaBuQia, WindS12QiaBuQia, WindS24QiaBuQia)
        TMinShowLongYangXia = TempCalculation(TMinLongYangXia)
        TMaxShowLongYangXia = TempCalculation(TMaxLongYangXia)
        TMinShowDaoTangHe = TempCalculation(TMinDaoTangHe)
        TMaxShowDaoTangHe = TempCalculation(TMaxDaoTangHe)
        TMinShowHeKa = TempCalculation(TMinHeKa)
        TMaxShowHeKa = TempCalculation(TMaxHeKa)
        TMinShowGuoMaYing = TempCalculation(TMinGuoMaYing)
        TMaxShowGuoMaYing = TempCalculation(TMaxGuoMaYing)
        TMinShowGaRang = TempCalculation(TMinGaRang)
        TMaxShowGaRang = TempCalculation(TMaxGaRang)
        TMinShowRiYueShan = TempCalculation(TMinRiYueShan)
        TMaxShowRiYueShan = TempCalculation(TMaxRiYueShan)
        TMinShowQingHaiHu = TempCalculation(TMinQingHaiHu)
        TMaxShowQingHaiHu = TempCalculation(TMaxQingHaiHu)
        TMinShowQiaBuQia = TempCalculation(TMinQiaBuQia)
        TMaxShowQiaBuQia = TempCalculation(TMaxQiaBuQia)
        FinalWrite1 = "2" + "%02d" % Weather12LongYangXia + "%02d" % Weather24LongYangXia + " " + WindCalShowLongYangXia + " 0" + TMinShowLongYangXia + TMaxShowLongYangXia + "\n"
        FinalWrite2 = "2" + "%02d" % Weather12DaoTangHe + "%02d" % Weather24DaoTangHe + " " + WindCalShowDaoTangHe + " 0" + TMinShowDaoTangHe + TMaxShowDaoTangHe + "\n"
        FinalWrite3 = "2" + "%02d" % Weather12HeKa + "%02d" % Weather24HeKa + " " + WindCalShowHeKa + " 0" + TMinShowHeKa + TMaxShowHeKa + "\n"
        FinalWrite4 = "2" + "%02d" % Weather12GuoMaYing + "%02d" % Weather24GuoMaYing + " " + WindCalShowGuoMaYing + " 0" + TMinShowGuoMaYing + TMaxShowGuoMaYing + "\n"
        FinalWrite5 = "2" + "%02d" % Weather12GaRang + "%02d" % Weather24GaRang + " " + WindCalShowGaRang + " 0" + TMinShowGaRang + TMaxShowGaRang + "\n"
        FinalWrite6 = "2" + "%02d" % Weather12QiaBuQia + "%02d" % Weather24QiaBuQia + " " + WindCalShowQiaBuQia + " 0" + TMinShowQiaBuQia + TMaxShowQiaBuQia + "\n"
        FinalWrite7 = "2" + "%02d" % Weather12DaoTangHe + "%02d" % Weather24DaoTangHe + " " + WindCalShowDaoTangHe + " 0" + TMinShowDaoTangHe + TMaxShowDaoTangHe + "\n"
        FinalWrite8 = "2" + "%02d" % Weather12RiYueShan + "%02d" % Weather24RiYueShan + " " + WindCalShowRiYueShan + " 0" + TMinShowRiYueShan + TMaxShowRiYueShan + "\n"
        FinalWrite9 = "2" + "%02d" % Weather12LongYangXia + "%02d" % Weather24LongYangXia + " " + WindCalShowLongYangXia + " 0" + TMinShowLongYangXia + TMaxShowLongYangXia + "\n"
        FinalWrite0 = "2" + "%02d" % Weather12QingHaiHu + "%02d" % Weather24QingHaiHu + " " + WindCalShowQingHaiHu + " 0" + TMinShowQingHaiHu + TMaxShowQingHaiHu + "\n"
        file2.write(FinalWrite1)
        file2.write(FinalWrite2)
        file2.write(FinalWrite3)
        file2.write(FinalWrite4)
        file2.write(FinalWrite5)
        file2.write(FinalWrite6)
        file2.write(FinalWrite7)
        file2.write(FinalWrite8)
        file2.write(FinalWrite9)
        file2.write(FinalWrite0)

with open("E:\\data\\" + "temp.txt") as file0:
    originData = file0.readlines()
    ZangQiaBuQia = "00000 " + originData[0].strip("\n") + " 恰卜恰 藏州01.rec hnd003.wav"
    ZangHeYin = "00001 " + originData[1].strip("\n") + " 河阴 藏州02.rec hnd005.wav"
    ZangZiKeTan = "00002 " + originData[2].strip("\n") + " 子科滩 藏州03.rec hnd007.wav"
    ZangMangQu = "00003 " + originData[3].strip("\n") + " 茫曲 藏州04.rec hnd009.wav"
    ZangGaBaSongDuo = "00004 " + originData[4].strip("\n") + " 尕巴松多 藏州05.rec hnd011.wav"
    ZangLongYangXia = "00005 " + originData[5].strip("\n") + " 龙羊峡 藏州06.rec hnd028.wav"
    ZangDaoTangHe = "00006 " + originData[6].strip("\n") + " 倒淌河镇 藏州07.rec hnd014.wav"
    ZangHeKa = "00007 " + originData[7].strip("\n") + " 河卡镇 藏州08.rec hnd013.wav"
    ZangGuoMaYing = "00008 " + originData[8].strip("\n") + " 过马营镇 藏州09.rec hnd016.wav"
    ZangGaRang = "00009 " + originData[9].strip("\n") + " 尕让 藏州10.rec hnd074.wav"
    ZangGongHeQiaBuQia = "00010 " + originData[10].strip("\n") + " 共和恰卜恰 藏县01.rec hnd003.wav"
    ZangGongHeDaoTangHe = "00011 " + originData[11].strip("\n") + " 共和倒淌河 藏县02.rec hnd017.wav"
    ZangGongHeRiYueShan = "00012 " + originData[12].strip("\n") + " 共和日月山 藏县03.rec hnd029.wav"
    ZangGongHeLongYangXia = "00013 " + originData[13].strip("\n") + " 共和龙羊峡 藏县04.rec hnd028.wav"
    ZangGongHeQingHaHu = "00014 " + originData[14].strip("\n") + " 共和青海湖 藏县05.rec hnd031.wav"

    print(ZangQiaBuQia)
    print(ZangHeYin)
    print(ZangZiKeTan)
    print(ZangMangQu)
    print(ZangGaBaSongDuo)
    print(ZangLongYangXia)
    print(ZangDaoTangHe)
    print(ZangHeKa)
    print(ZangGuoMaYing)
    print(ZangGaRang)
    print(ZangGongHeQiaBuQia)
    print(ZangGongHeDaoTangHe)
    print(ZangGongHeRiYueShan)
    print(ZangGongHeLongYangXia)
    print(ZangGongHeQingHaHu)
    print("#####")
with open("D:\qx00\\dat\\" + "藏语72小时.dat", "w") as file1:
    file1.write(ZangQiaBuQia + "\n")
    file1.write(ZangHeYin + "\n")
    file1.write(ZangZiKeTan + "\n")
    file1.write(ZangMangQu + "\n")
    file1.write(ZangGaBaSongDuo + "\n")
    file1.write(ZangLongYangXia + "\n")
    file1.write(ZangDaoTangHe + "\n")
    file1.write(ZangHeKa + "\n")
    file1.write(ZangGuoMaYing + "\n")
    file1.write(ZangGaRang + "\n")
    file1.write(ZangGongHeQiaBuQia + "\n")
    file1.write(ZangGongHeDaoTangHe + "\n")
    file1.write(ZangGongHeRiYueShan + "\n")
    file1.write(ZangGongHeLongYangXia + "\n")
    file1.write(ZangGongHeQingHaHu + "\n")
    file1.write("#####")

    filePath = "D:\\shengxun\\baowen\\"
    dateToday = getTime()
    fileName = checkFile(filePath, dateToday)
    print(fileName)
    fileInputPath = filePath + fileName
    lenthOfFile = checkFileLenth(fileInputPath)
    stationNum = ['52856', '52868', '52943', '52955', '52957']
    listOfStep = [1, 2]
    # 写国家站数据到文件
    fileExist = os.path.exists("E:\\data\\" + "temp.txt")
    if fileExist == True:
        os.remove("E:\\data\\" + "temp.txt")
    for i in stationNum:
        lineNum = numCheck(fileInputPath, lenthOfFile, i)
        for j in listOfStep:
            eleOfSingleStation = pickOut(fileInputPath, lineNum, 7) + pickOut(fileInputPath, lineNum, 8)
        print(eleOfSingleStation)
        Weather12 = int(float(eleOfSingleStation[3]))
        Weather24 = int(float(eleOfSingleStation[-3]))
        WindD12 = int(float(eleOfSingleStation[4]))
        WindD24 = int(float(eleOfSingleStation[-2]))
        WindS12 = int(float(eleOfSingleStation[5].split('\n')[0]))
        WindS24 = int(float(eleOfSingleStation[-1].split('\n')[0]))
        TMax = float(eleOfSingleStation[-5])
        TMin = float(eleOfSingleStation[-4])
        TMinShow = TempCalculation(TMin)
        TMaxShow = TempCalculation(TMax)
        WindCalShow = windCal(WindD12, WindD24, WindS12, WindS24)
        # 生成共和相关站信息
        if i == "52856":
            TMaxLongYangXia = TMax + 1.0
            TMinLongYangXia = TMin + 1.0
            TMaxGaRang = TMax + 1.0
            TMinGaRang = TMin + 1.0
            TMaxQiaBuQia = TMax
            TMinQiaBuQia = TMin
            WindS12LongYangXia = WindS12DaoTangHe = WindS12RiYueShan = WindS12QingHaiHu = WindS12QiaBuQia = WindS12
            WindS24LongYangXia = WindS24DaoTangHe = WindS24RiYueShan = WindS24QingHaiHu = WindS24QiaBuQia = WindS24
            WindD12LongYangXia = WindD12DaoTangHe = WindD12RiYueShan = WindD12QingHaiHu = WindD12QiaBuQia = WindD12
            WindD24LongYangXia = WindD24DaoTangHe = WindD24RiYueShan = WindD24QingHaiHu = WindD24QiaBuQia = WindD24
            Weather12LongYangXia = Weather12DaoTangHe = Weather12RiYueShan = Weather12QingHaiHu = Weather12QiaBuQia = Weather12
            Weather24LongYangXia = Weather24DaoTangHe = Weather24RiYueShan = Weather24QingHaiHu = Weather24QiaBuQia = Weather24
        # 生成兴海相关站信息
        if i == "52943":
            TMaxDaoTangHe = TMax + 1.0
            TMinDaoTangHe = TMin + 1.0
            TMaxHeKa = TMax - 1.0
            TMinHeKa = TMin - 1.0
            TMaxRiYueShan = TMaxDaoTangHe - 3.0
            TMinRiYueShan = TMinDaoTangHe - 3.0
            TMaxQingHaiHu = TMaxDaoTangHe - 1.0
            TMinQingHaiHu = TMinDaoTangHe - 1.0
            WindS12HeKa = WindS12
            WindS24HeKa = WindS24
            WindD12HeKa = WindD12
            WindD24HeKa = WindD24
            Weather12HeKa = Weather12
            Weather24HeKa = Weather24
        # 生成贵南相关站信息
        if i == "52955":
            WindS12GuoMaYing = WindS12
            WindS24GuoMaYing = WindS24
            WindD12GuoMaYing = WindD12
            WindD24GuoMaYing = WindD24
            Weather12GuoMaYing = Weather12
            Weather24GuoMaYing = Weather24
            TMinGuoMaYing = TMin
            TMaxGuoMaYing = TMax
        # 生成贵德相关站信息
        if i == "52868":
            WindS12GaRang = WindS12
            WindS24GaRang = WindS24
            WindD12GaRang = WindD12
            WindD24GaRang = WindD24
            Weather12GaRang = Weather12
            Weather24GaRang = Weather24
        FinalWrite = "2" + "%02d" % Weather12 + "%02d" % Weather24 + " " + WindCalShow + " 0" + TMinShow + TMaxShow + "\n"

        with open("E:\\data\\" + "temp.txt", "a") as file1:
            file1.write(FinalWrite)
    # 写区域站数据到文件
    with open("E:\\data\\" + "temp.txt", "a") as file2:
        WindCalShowLongYangXia = windCal(WindD12LongYangXia, WindD24LongYangXia, WindS12LongYangXia, WindS24LongYangXia)
        WindCalShowDaoTangHe = windCal(WindD12DaoTangHe, WindD24DaoTangHe, WindS12DaoTangHe, WindS24DaoTangHe)
        WindCalShowHeKa = windCal(WindD12HeKa, WindD24HeKa, WindS12HeKa, WindS24HeKa)
        WindCalShowGuoMaYing = windCal(WindD12GuoMaYing, WindD24GuoMaYing, WindS12GuoMaYing, WindS24GuoMaYing)
        WindCalShowGaRang = windCal(WindD12GaRang, WindD24GaRang, WindS12GaRang, WindS24GaRang)
        WindCalShowRiYueShan = windCal(WindD12RiYueShan, WindD24RiYueShan, WindS12RiYueShan, WindS24RiYueShan)
        WindCalShowQingHaiHu = windCal(WindD12QingHaiHu, WindD24QingHaiHu, WindS12QingHaiHu, WindS24QingHaiHu)
        WindCalShowQiaBuQia = windCal(WindD12QiaBuQia, WindD24QiaBuQia, WindS12QiaBuQia, WindS24QiaBuQia)
        TMinShowLongYangXia = TempCalculation(TMinLongYangXia)
        TMaxShowLongYangXia = TempCalculation(TMaxLongYangXia)
        TMinShowDaoTangHe = TempCalculation(TMinDaoTangHe)
        TMaxShowDaoTangHe = TempCalculation(TMaxDaoTangHe)
        TMinShowHeKa = TempCalculation(TMinHeKa)
        TMaxShowHeKa = TempCalculation(TMaxHeKa)
        TMinShowGuoMaYing = TempCalculation(TMinGuoMaYing)
        TMaxShowGuoMaYing = TempCalculation(TMaxGuoMaYing)
        TMinShowGaRang = TempCalculation(TMinGaRang)
        TMaxShowGaRang = TempCalculation(TMaxGaRang)
        TMinShowRiYueShan = TempCalculation(TMinRiYueShan)
        TMaxShowRiYueShan = TempCalculation(TMaxRiYueShan)
        TMinShowQingHaiHu = TempCalculation(TMinQingHaiHu)
        TMaxShowQingHaiHu = TempCalculation(TMaxQingHaiHu)
        TMinShowQiaBuQia = TempCalculation(TMinQiaBuQia)
        TMaxShowQiaBuQia = TempCalculation(TMaxQiaBuQia)
        FinalWrite1 = "2" + "%02d" % Weather12LongYangXia + "%02d" % Weather24LongYangXia + " " + WindCalShowLongYangXia + " 0" + TMinShowLongYangXia + TMaxShowLongYangXia + "\n"
        FinalWrite2 = "2" + "%02d" % Weather12DaoTangHe + "%02d" % Weather24DaoTangHe + " " + WindCalShowDaoTangHe + " 0" + TMinShowDaoTangHe + TMaxShowDaoTangHe + "\n"
        FinalWrite3 = "2" + "%02d" % Weather12HeKa + "%02d" % Weather24HeKa + " " + WindCalShowHeKa + " 0" + TMinShowHeKa + TMaxShowHeKa + "\n"
        FinalWrite4 = "2" + "%02d" % Weather12GuoMaYing + "%02d" % Weather24GuoMaYing + " " + WindCalShowGuoMaYing + " 0" + TMinShowGuoMaYing + TMaxShowGuoMaYing + "\n"
        FinalWrite5 = "2" + "%02d" % Weather12GaRang + "%02d" % Weather24GaRang + " " + WindCalShowGaRang + " 0" + TMinShowGaRang + TMaxShowGaRang + "\n"
        FinalWrite6 = "2" + "%02d" % Weather12QiaBuQia + "%02d" % Weather24QiaBuQia + " " + WindCalShowQiaBuQia + " 0" + TMinShowQiaBuQia + TMaxShowQiaBuQia + "\n"
        FinalWrite7 = "2" + "%02d" % Weather12DaoTangHe + "%02d" % Weather24DaoTangHe + " " + WindCalShowDaoTangHe + " 0" + TMinShowDaoTangHe + TMaxShowDaoTangHe + "\n"
        FinalWrite8 = "2" + "%02d" % Weather12RiYueShan + "%02d" % Weather24RiYueShan + " " + WindCalShowRiYueShan + " 0" + TMinShowRiYueShan + TMaxShowRiYueShan + "\n"
        FinalWrite9 = "2" + "%02d" % Weather12LongYangXia + "%02d" % Weather24LongYangXia + " " + WindCalShowLongYangXia + " 0" + TMinShowLongYangXia + TMaxShowLongYangXia + "\n"
        FinalWrite0 = "2" + "%02d" % Weather12QingHaiHu + "%02d" % Weather24QingHaiHu + " " + WindCalShowQingHaiHu + " 0" + TMinShowQingHaiHu + TMaxShowQingHaiHu + "\n"
        file2.write(FinalWrite1)
        file2.write(FinalWrite2)
        file2.write(FinalWrite3)
        file2.write(FinalWrite4)
        file2.write(FinalWrite5)
        file2.write(FinalWrite6)
        file2.write(FinalWrite7)
        file2.write(FinalWrite8)
        file2.write(FinalWrite9)
        file2.write(FinalWrite0)

with open("E:\\data\\" + "temp.txt") as file0:
    originData = file0.readlines()
    ZangQiaBuQia = "00000 " + originData[0].strip("\n") + " 恰卜恰 藏州01.rec hnd003.wav"
    ZangHeYin = "00001 " + originData[1].strip("\n") + " 河阴 藏州02.rec hnd005.wav"
    ZangZiKeTan = "00002 " + originData[2].strip("\n") + " 子科滩 藏州03.rec hnd007.wav"
    ZangMangQu = "00003 " + originData[3].strip("\n") + " 茫曲 藏州04.rec hnd009.wav"
    ZangGaBaSongDuo = "00004 " + originData[4].strip("\n") + " 尕巴松多 藏州05.rec hnd011.wav"
    ZangLongYangXia = "00005 " + originData[5].strip("\n") + " 龙羊峡 藏州06.rec hnd028.wav"
    ZangDaoTangHe = "00006 " + originData[6].strip("\n") + " 倒淌河镇 藏州07.rec hnd014.wav"
    ZangHeKa = "00007 " + originData[7].strip("\n") + " 河卡镇 藏州08.rec hnd013.wav"
    ZangGuoMaYing = "00008 " + originData[8].strip("\n") + " 过马营镇 藏州09.rec hnd016.wav"
    ZangGaRang = "00009 " + originData[9].strip("\n") + " 尕让 藏州10.rec hnd074.wav"
    ZangGongHeQiaBuQia = "00010 " + originData[10].strip("\n") + " 共和恰卜恰 藏县01.rec hnd003.wav"
    ZangGongHeDaoTangHe = "00011 " + originData[11].strip("\n") + " 共和倒淌河 藏县02.rec hnd017.wav"
    ZangGongHeRiYueShan = "00012 " + originData[12].strip("\n") + " 共和日月山 藏县03.rec hnd029.wav"
    ZangGongHeLongYangXia = "00013 " + originData[13].strip("\n") + " 共和龙羊峡 藏县04.rec hnd028.wav"
    ZangGongHeQingHaHu = "00014 " + originData[14].strip("\n") + " 共和青海湖 藏县05.rec hnd031.wav"

    print(ZangQiaBuQia)
    print(ZangHeYin)
    print(ZangZiKeTan)
    print(ZangMangQu)
    print(ZangGaBaSongDuo)
    print(ZangLongYangXia)
    print(ZangDaoTangHe)
    print(ZangHeKa)
    print(ZangGuoMaYing)
    print(ZangGaRang)
    print(ZangGongHeQiaBuQia)
    print(ZangGongHeDaoTangHe)
    print(ZangGongHeRiYueShan)
    print(ZangGongHeLongYangXia)
    print(ZangGongHeQingHaHu)
    print("#####")
with open("D:\qx00\\dat\\" + "藏语96小时.dat", "w") as file1:
    file1.write(ZangQiaBuQia + "\n")
    file1.write(ZangHeYin + "\n")
    file1.write(ZangZiKeTan + "\n")
    file1.write(ZangMangQu + "\n")
    file1.write(ZangGaBaSongDuo + "\n")
    file1.write(ZangLongYangXia + "\n")
    file1.write(ZangDaoTangHe + "\n")
    file1.write(ZangHeKa + "\n")
    file1.write(ZangGuoMaYing + "\n")
    file1.write(ZangGaRang + "\n")
    file1.write(ZangGongHeQiaBuQia + "\n")
    file1.write(ZangGongHeDaoTangHe + "\n")
    file1.write(ZangGongHeRiYueShan + "\n")
    file1.write(ZangGongHeLongYangXia + "\n")
    file1.write(ZangGongHeQingHaHu + "\n")
    file1.write("#####")
print("DONE")



