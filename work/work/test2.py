import os
import re
import datetime
def getTime():
    Now = datetime.datetime.now()
    now2Str = int(datetime.datetime.strftime(Now,"%H%M"))
    today1 = datetime.date.today()
    if now2Str >= 530 and now2Str < 1430:
        dateToday = datetime.datetime.strftime(today1, "%Y%m%d") + "00"
    elif now2Str >= 1430:
        dateToday = datetime.datetime.strftime(today1, "%Y%m%d") + "12"
    return dateToday
path1 = "E:\\指导预报\\省台指导\\"
list1 = os.listdir(path1)
dateToday = getTime()
print(dateToday)
p1 = r"(Z_SEVP_C_BEXN_)(.*?)(224000_P_RFFC-)(.*?)" + dateToday + "(.*?)"
pattern1 = re.compile(p1)
for i in list1:
    match1 = re.match(pattern1, i )
    if match1 != None:
        print(match1.group(1)+match1.group(2)+match1.group(3)+"SPCC-"+dateToday+"00-16812.TXT")
        print(i)
