import ftplib
import re
import datetime
#与22.5不同，60ftp用nlst后列表内要素包含路径，如['sevp/rffc/123.txt'，因此需片]
#FTP基本函数
def ftpConnect(host, port, username, passwd):
    ftp = ftplib.FTP()
    try:
        ftp.connect(host, port)
    except:
        raise IOError("FTP服务器连接失败")

    try:
        ftp.login(username, passwd)
    except:
        raise IOError("FTP用户名或密码错误")
    else:
        print("FTP连接登录成功")
        return ftp
#FTP下载，用到retrbinary
def ftpDownload(ftp, localPath, fileName):
    file_handle = open(localPath + fileName, "wb").write
    ftp.encoding = 'utf-8'
    ftp.retrbinary("RETR /sevp/rffc/%s" %fileName, file_handle)
#遍历文件目录下所有文件，并正则配对所需文件
def checkFile(ftp, ftpPath, dateToday):
    ftpFileslist = ftp.nlst(ftpPath)
    p1 = r"((Z_SEVP_C_BABJ_).*?(_P_RFFC-SCMOC-)"+dateToday+".*?)"
    pattern1 = re.compile(p1)
    fileNameList = []
    for singleFile in ftpFileslist:
        singleFileName = singleFile[11:]
        match1 = re.match(pattern1, singleFileName)
        if match1 != None:
            fileNameList.append(singleFileName)
    return fileNameList[-1]
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
#主程序
if __name__ == "__main__":
    ftp = ftpConnect("10.181.22.60",21,"cmacast","Wlbz6135")
    ftpPath = "/sevp/rffc"
    a = checkFile(ftp, ftpPath, getTime())
    ftpDownload(ftp,"E:/指导预报/国家指导/",a)
    print(a)
    ftp.close()
    print("Done!")