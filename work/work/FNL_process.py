import numpy as np
import matplotlib.pyplot as plt
'''
#(1)grads中用grads2ascii函数生成txt文件，并用loadtxt读取
#缺点是需要通过grads生成CTL，并用grads2ascii函数，且只能生成一个要素一层值
#http://bbs.06climate.com/forum.php?mod=viewthread&tid=11515
a = np.loadtxt("I:\\data\\fnl\\1.txt",dtype = float)
np.set_printoptions(suppress=True)#去除科学计数法
'''
#(2)直接用numpy读取二进制数据，数据为单一要素
'''
data = np.fromfile("I:\\data\\fnl\\fnldata.dat",dtype = np.float32)
np.set_printoptions(suppress=True)
data2 = data.reshape(2,31,41)
x = np.arange(0,41,1)
y = np.arange(0,31,1)
X, Y = np.meshgrid(x,y)
plt.contour(X,Y,data2[0,:,:])
plt.show()
np.savetxt("i:\\data\\fnl\\np2txt.txt",data2[0,:,:],fmt = "%.3f")
print('done')
'''
#(3)用numpy读取二进制数据，数据为多要素
data2 = np.fromfile("I:\\data\\fnl\\fnldata2.dat",dtype = np.float32)
np.set_printoptions(suppress=True)

data3 = data2.reshape(2,2,31,41)
np.savetxt("i:\\data\\fnl\\np2txt2.txt",data3[0,0,:,:],fmt = "%.3f")
print('done')