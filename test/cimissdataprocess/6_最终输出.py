import numpy as np
import pandas as pd
import os


basePath = 'E:\\workspace\\test\\cimissdataprocess\\result\\'
listall = []
filesList = os.listdir(basePath+'6h\\')
for file in filesList:
    filePath = basePath + '6h\\' + file
    with open(filePath,'r') as fileTemp:
        list1 = fileTemp.readlines()
        for i in list1:
            listall.append(i)
with open(basePath+'12h大于25mmall.txt','w') as fw:
    for j in listall:
        fw.write(j)
