import re
from urllib import request
from urllib.request import urlopen
#目录设置
#站号读取
stationFilePath =  "E:\\work\\站点信息_全\\2018_Station_ID.txt"
#资料目录
oneStationDataFilePath = "E:\\work\\DATA\\2018_pre\\"
#生成time.txt
timeUrlPath = "http://10.181.89.55/cimiss-web/api?" \
          "userId=BEXN_QXT_ZNWG&pwd=qxt6145537&" \
          "interfaceId=getSurfEleByTimeRangeAndStaID&" \
          "dataCode=SURF_CHN_MUL_HOR&" \
          "elements=Year,Mon,Day,Hour&" \
          "timeRange=[20180331160000,20180927010000]&" \
          "staIds=52866&dataFormat=text"
req = request.Request(timeUrlPath)
oneStationDataFile = oneStationDataFilePath + "time.txt"
response = urlopen(req).read().decode("utf-8")
with open(oneStationDataFile, "w") as timefile:
    timefile.write(response)

#CIMISS地址
urlPath = "http://10.181.89.55/cimiss-web/api?" \
          "userId=BEXN_QXT_ZNWG&pwd=qxt6145537&" \
          "interfaceId=getSurfEleByTimeRangeAndStaID&" \
          "dataCode=SURF_CHN_MUL_HOR&" \
          "elements=Year,Mon,Day,Hour,PRE_1h&" \
          "timeRange=[20180331160000,20180927010000]&" \
          "staIds=52866&dataFormat=text"
#下载逐站资料，并以站名保存文件
with open(stationFilePath,"r") as file1:
    list1 = file1.readlines()
    for i in range(len(list1)):
        stationId = list1[i].strip("\n")
        newUrlPath = re.sub(r"52866", stationId, urlPath, 1)
        oneStationDataFile = oneStationDataFilePath + stationId + ".txt"
        req = request.Request(newUrlPath)
        response = urlopen(req).read().decode("utf-8")
        with open(oneStationDataFile,"w") as file2:
            file2.write(response)
            print("file "+ stationId+" Donwload has Done!")




