import numpy as np
import pandas as pd


stationFilePath =  "E:\\workspace\\work\\work\\cimissdataprocess\\2018_Station_ID.txt"
with open(stationFilePath) as file1:
    list1 = file1.readlines()
    list2 = []
    for i in list1:
        list2.append(i.strip('\n'))


path = 'E:\\workspace\\test\\cimissdataprocess\\'

with open(path+'3h_1.csv') as file2:
    df1 = pd.read_csv(file2, index_col=['Time'])
    for i in list2:
        dfTemp = df1[[i]].sort_values(by=i,ascending=False)
        dfTemp2 = dfTemp[dfTemp[i]>25]
        if dfTemp2.empty == False:
            dfTemp2.to_csv(path+'3h大于25mm_'+i+'.txt')

with open(path+'6h_1.csv') as file2:
    df1 = pd.read_csv(file2, index_col=['Time'])
    for i in list2:
        dfTemp = df1[[i]].sort_values(by=i,ascending=False)
        dfTemp2 = dfTemp[dfTemp[i]>25]
        if dfTemp2.empty == False:
            dfTemp2.to_csv(path+'6h大于25mm_'+i+'.txt')

with open(path+'12h_1.csv') as file2:
    df1 = pd.read_csv(file2, index_col=['Time'])
    for i in list2:
        dfTemp = df1[[i]].sort_values(by=i,ascending=False)
        dfTemp2 = dfTemp[dfTemp[i]>25]
        if dfTemp2.empty == False:
            dfTemp2.to_csv(path+'12h大于25mm_'+i+'.txt')

print('DONE!')
