import os
import numpy as np
from sympy.utilities.iterables import flatten

rootdir = "E:\\work\\tang\\tongji\\"
list_dir = os.listdir(rootdir) #列出文件夹下所有的目录与文件
print(list_dir)

for k in range(0,len(list_dir)):
    filename1 = str(list_dir[k])
    filenameadd = '_rst.txt'
    if filename1[-3:] == 'txt':
        filename2 = filename1[:-4]+filenameadd
    path_file1 = rootdir + filename1
    print(path_file1)
    
    ic = np.loadtxt(path_file1,dtype = int)    
    print(ic)
    
    path_file2 = rootdir + filename2
    lenth = ic.shape
    print(lenth[0])
    
    fw = open(path_file2,'a')
    fw.write('该站共出现雷暴次数：')
    fw.write(str(lenth[0]))
    fw.write('\n')

    #####各年出现雷暴从少到多排列####
    fw.write('各年出现雷暴从少到多排列：')
    fw.write('\n')
    yy = flatten((ic[:,1:2]).tolist())
    mm = flatten((ic[:,2:3]).tolist())
    yy_set = set(yy)
    mm_set = set(mm)
    a = []
    b = []
    for i in yy_set:
        a.append(i)
        b.append(yy.count(i))
    c = dict(zip(a,b))
    d = zip(c.values(),c.keys())
    fw.write(str(sorted(d)))
    fw.write('\n')
    #####集合统计各年各月出现次数####
    fw.write('统计各年各月出现次数：')
    fw.write('\n')
    for i in yy_set:
        fw.write(str(i))
        fw.write(' ')
        fw.write(str(yy.count(i)))
        fw.write('\n')
    for j in mm_set:
        fw.write(str(j))
        fw.write(' ')
        fw.write(str(mm.count(j)))
        fw.write('\n')
    #####找出每年最早发生和最晚发生#####
    id = (ic[...,1:])
    fw.write('各年最早发生时间：')   
    fw.write('\n')     
    for j in range(lenth[0]-1,1,-1):
        if id[j-1][0] != id[j][0]:
            fw.write(str(id[j]))
            fw.write('\n')
    fw.write(str(id[0]))
    fw.write('\n')
    fw.write('各年最晚发生时间：') 
    fw.write('\n')       
    for i in range(lenth[0]-1):
        if id[i][0] != id[i+1][0]:
            fw.write(str(id[i]))
            fw.write('\n')
    fw.write(str(id[lenth[0]-1]))
    ####关闭文件######
    fw.close()
print('program end')







