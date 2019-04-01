import os
from cimissDataFirstLineDelete import CimissDataFirstLineDel

filePath =  "E:\\workspace\\work\\work\\cimissdataprocess\\2018_pre\\"
fileList = os.listdir(filePath)
for file in fileList:
    a = CimissDataFirstLineDel(filePath, file)
    a.firstLineDel()