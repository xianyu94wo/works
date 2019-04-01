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
    if now2Str >= 430 and now2Str < 1230:
        dateToday = datetime.datetime.strftime(today1, "%Y%m%d") + "00"
    elif now2Str >= 1230:
        dateToday = datetime.datetime.strftime(today1, "%Y%m%d") + "12"
    return dateToday
#遍历文件目录下所有文件，并正则配对所需文件
def checkFile(filePath, dateToday):
    fileList = os.listdir(filePath)
    p1 = r"((Z_SEVP_C_BABJ_).*?(_P_RFFC-SCMOC-)"+dateToday+".*?)"
    pattern1 = re.compile(p1)
    for singleFile in fileList:
        match1 = re.match(pattern1, singleFile)
        if match1 != None:
            return singleFile


#主程序
if __name__ == "__main__":
    filePath = "E:\\指导预报\\国家指导\\"
    dateToday = getTime()
    fileName = checkFile(filePath,dateToday)
    fileInputPath = filePath + fileName
    lenthOfFile = checkFileLenth(fileInputPath)

    stationNum = ['52856','52868','52943','52955','52957']
    listOfStep = [4, 8, 12, 16, 18, 20]
    #写文件

    with open("E:\\指导预报\\国家指导海南预报\\"+"SCMOC"+dateToday+".txt",'w') as fileWrite:
        for i in stationNum:
            lineNum = numCheck(fileInputPath, lenthOfFile, i)
            fileWrite.write("%10.5s"%i)
            fileWrite.write("\n")
            for j in listOfStep:
                aa = pickOut(fileInputPath,lineNum,j)
                print(aa)
                for k in aa:
                    fileWrite.write("%7.5s"%k)

    print("Done!")

