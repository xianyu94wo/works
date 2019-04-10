import time
import datetime
import requests
from urllib import request
from urllib.request import urlopen

#获取雷达资料URL
def basrUrlStr(listTimeUTC):
    baseUrl1 = "http://10.181.89.55/cimiss-web/api?" \
              "userId=BEXN_QXT_Yousangjie&" \
              "pwd=Ysj8894315&" \
              "interfaceId=getRadaFileByTimeRangeAndStaId&" \
              "dataCode=RADA_L2_UFMT&"
    baseUrl2 = "timeRange="+listTimeUTC+"&staIds=Z9974&dataFormat=text"
    baseUrl = baseUrl1 + baseUrl2
    return baseUrl
#获取时间列表
def timeFormat():
    nowStamp = time.time()
    nowStamp60sEarly = nowStamp - 600
    timeBeginUTC = int(datetime.datetime.utcfromtimestamp(nowStamp60sEarly).strftime("%Y%m%d%H%M%S"))
    timeEndUTC = int(datetime.datetime.utcfromtimestamp(nowStamp).strftime("%Y%m%d%H%M%S"))
    finalTimeListStr = "[" + str(timeBeginUTC) + "," + str(timeEndUTC) + "]"
    return finalTimeListStr
#下载雷达资料
def downloadRadarData(baseUrl):
    req = request.Request(baseUrl)
    response = urlopen(req).read().decode("utf-8")
    print(response)
    path = "E:\\data\\"
    filename = "radar1.txt"
    file1 = open(path + filename, "w")
    file1.write(response.strip("\n"))
    file1.close()
    with open(path + filename, "r") as file2:
        a = file2.readlines()
        for i in range(4, len(a)):
            singleRadarFileName = a[i].split(" ")[0]
            downloatUrl = a[i].split(" ")[3]
#            print(singleRadarFileName, downloatUrl)
            downloadFile = requests.get(downloatUrl)
            with open("e:\\data\\" + singleRadarFileName, "wb") as code:
                code.write(downloadFile.content)
                print("Download finishied")
    return

if __name__ == "__main__":
    #timeRangeList = timeFormat()
    baseUrl = basrUrlStr(timeRangeList)
    #baseUrl = "http://10.181.89.55/cimiss-web/api?userId=BEXN_QXT_Yousangjie&pwd=Ysj8894315&interfaceId=getRadaFileByTimeRangeAndStaId&dataCode=RADA_L2_UFMT&timeRange=[20190410014509,20190410045509]&staIds=Z9974&dataFormat=text"
    print(baseUrl)
    downloadRadarData(baseUrl)
    print("Done")
