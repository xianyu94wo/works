import numpy as np
import pandas as pd

np.set_printoptions(suppress=True)
stationFilePath =  "E:\\workspace\\work\\work\\cimissdataprocess\\2018_Station_ID.txt"
path = 'E:\\workspace\\test\\cimissdataprocess\\'
with open(stationFilePath) as file1:
    list1 = file1.readlines()
    list2 = []
    for i in list1:
        list2.append(i.strip('\n'))
    print(list2)

with open(path+'base1.csv') as file1:
    df1 =  pd.read_csv(file1, index_col=['Date', 'Time'])
    ar1 = np.array(df1,dtype=float)
    print(ar1.shape)
    list3h = []
    list6h = []
    list12h = []
    for i in range(2, ar1.shape[0]):
        for j in range(ar1.shape[1]):
            sum3h = ar1[i-2,j]+ar1[i-1,j]+ar1[i,j]
            list3h.append(sum3h)
    ar3h = np.array(list3h).reshape(4304,680)
    np.set_printoptions(suppress=True)
    df3h = pd.DataFrame(ar3h, columns=[list2])
#        df3h.to_csv(path+'3h.csv')

    for i in range(5, ar1.shape[0]):
        for j in range(ar1.shape[1]):
            sum6h = ar1[i-5,j]+ar1[i-4,j]+ar1[i-3,j]+ar1[i-2,j]+ar1[i-1,j]+ar1[i,j]
            list6h.append(sum6h)
    ar6h = np.array(list6h).reshape(4301, 680)
    np.set_printoptions(suppress=True)
    df6h = pd.DataFrame(ar6h, columns=[list2])
#        df6h.to_csv(path+'6h.csv')

    for i in range(11, ar1.shape[0]):
        for j in range(ar1.shape[1]):
            sum12h = ar1[i-11,j]+ar1[i-10,j]+ar1[i-9,j]+ar1[i-8,j]+ar1[i-7,j]+ar1[i-6,j]+ar1[i-5,j]+ar1[i-4,j]+ar1[i-3,j]+ar1[i-2,j]+ar1[i-1,j]+ar1[i,j]
            list12h.append(sum12h)
    ar12h = np.array(list12h).reshape(4295, 680)
    np.set_printoptions(suppress=True)
    df12h = pd.DataFrame(ar12h, columns=[list2])
#        df12h.to_csv(path+'12h.csv')

print("Done!")




