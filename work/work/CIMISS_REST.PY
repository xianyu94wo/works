from urllib import request
from urllib.request import urlopen

if __name__ == '__main__':
    # 1. 调用方法的参数定义，并赋值
    # 1.1 接口url
    # 1.2 用户名&密码
    # 1.3 接口ID
    # 1.4 必选参数（按需加可选参数）
    #     资料：中国地面逐小时
    #     检索要素：站号、站名、小时降水、气压、相对湿度、能见度、2分钟平均风速、2分钟风向
    #     检索时间
    #     排序：按照站号从小到大
    '''
    baseUrl = "http://10.181.89.55/cimiss-web/api?" \
              "userId=BEXN_QXT_ZNWG&" \
              "pwd=qxt6145537&" \
              "interfaceId=getSurfEleInRegionByTimeRange&" \
              "dataCode=SURF_CHN_MUL_HOR&" \
              "timeRange=[20180401000000,20180501000000]&" \
              "adminCodes=630000&" \
              "elements=Station_Name,City,Cnty,Station_Id_C,Year,Mon,Day,Hour,PRE_1h&" \
             "eleValueRanges=PRE_1h:(0,100)&" \
              "dataFormat=text"
    
    baseUrl = "http://10.181.89.55/cimiss-web/api?" \
              "userId=BEXN_QXT_ZNWG&pwd=qxt6145537&" \
              "interfaceId=getSurfEleInRegionByTimeRange&" \
              "dataCode=SURF_CHN_MUL_HOR&" \
              "timeRange=[20180430000000,20180531000000]&" \
              "adminCodes=630000&" \
              "elements=Station_Id_C,PRE_1h&" \
              "dataFormat=text"
    

    baseUrl = "http://10.181.89.55/cimiss-web/api?" \
              "userId=BEXN_QXT_Yousangjie&" \
              "pwd=Ysj8894315&" \
              "interfaceId=getNafpFileByTime&" \
              "dataCode=NAFP_NWFD_SPCC&" \
              "time=20181110000000&" \
              "dataFormat=text"
    
    baseUrl = "http://10.181.89.55/cimiss-web/api?" \
              "userId=BEXN_QXT_Yousangjie&" \
              "pwd=Ysj8894315&" \
              "interfaceId=getSurfEleInRegionByTimeRange&" \
              "dataCode=SURF_CHN_MUL_HOR&" \
              "timeRange=[20180401000000,20180402010000]&" \
              "adminCodes=630000&" \
              "elements=Cnty,Station_Id_C,Year,Mon,Day,Hour,PRE_1h&" \
              "dataFormat=text"
    '''
    baseUrl = "http://10.181.89.55/cimiss-web/api?" \
              "userId=BEXN_QXT_Yousangjie&" \
              "pwd=Ysj8894315&" \
              "interfaceId=getSurfEleInRegionByTimeRange&" \
              "dataCode=SURF_CHN_MUL_HOR&" \
              "timeRange=[20180901000000,20181001010000]&" \
              "adminCodes=630000&" \
              "elements=Station_Id_C,Year,Mon,Day,Hour,PRE_1h&" \
              "eleValueRanges=PRE_1h:[10,999)&" \
              "dataFormat=text"
    # 2. 调用接口

    req = request.Request(baseUrl)
    print(baseUrl)

    response = urlopen(req).read().decode("utf-8")
    print(response)
    # 3. 输出接口
    path = "E:\\data\\"
    filename = "rain1h.txt"
    file1 =  open(path+filename, "w")
    file1.write(response.strip("\n"))
    file1.close()
    print('Done!')

