import datetime
import os
import re
import shutil
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
#拷贝中央台指导预报
def copySCMOC(SCMOCPath, dateToday):
    listSCMOC = os.listdir(SCMOCPath)
    p1 = r"((Z_SEVP_C_BABJ_).*?(_P_RFFC-SCMOC-)" + dateToday + ".*?)"
    pattern1 = re.compile(p1)
    for singleFile in listSCMOC:
        match1 = re.match(pattern1, singleFile)
        if match1 != None:
            shutil.copy(SCMOCPath+singleFile, "E:\\MakeYbIniDATA\\")
            return "国家指导拷贝完成"
#拷贝省台指导并改名：
def copySLMOF2SPCC(SLMOFPath,dateToday):
    listSLMOF = os.listdir(SLMOFPath)
    now2 = datetime.datetime.now()
    now2Str2 = int(datetime.datetime.strftime(now2,"%H%M"))
    if now2Str2 >= 430 and now2Str2 < 1230:
        p1 = r"(Z_SEVP_C_BEXN_)(.*?)(224000_P_RFFC-)(.*?)" + dateToday + "(.*?)"
    elif now2Str2 >= 1230:
        p1 = r"(Z_SEVP_C_BEXN_)(.*?)(073000_P_RFFC-)(.*?)" + dateToday + "(.*?)"
    pattern1 = re.compile(p1)
    for singleFile in listSLMOF:
        match1 = re.match(pattern1, singleFile)
        if match1 != None:
            dstFileName = match1.group(1)+match1.group(2)+match1.group(3)+"SPCC-"+dateToday+"00-16812.TXT"
            shutil.copy(SLMOFPath+singleFile, "E:\\MakeYbIniDATA\\"+dstFileName)
            return "省台指导拷贝完成"
#主程序
if __name__ == "__main__":
    SCMOCPath = "E:\\指导预报\\国家指导\\"
    SLMOFPath = "E:\\指导预报\\省台指导\\"
    dateToday = getTime()
    a = copySCMOC(SCMOCPath, dateToday)
    b = copySLMOF2SPCC(SLMOFPath, dateToday)
    print("Done")


