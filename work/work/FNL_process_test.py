import numpy as np
import matplotlib.pyplot as plt
#常量声明
pi = np.around(np.pi,decimals = 5) 
d = 1.0
ds = 2*d
a1 = 1/63.71
print(pi)
#作图参考
'''
x = np.arange(0,81,1)
y = np.arange(0,51,1)
X, Y = np.meshgrid(x,y)
plt.contour(X,Y,data2[0,:,:])
plt.show()
'''
#边界数值替换函数
def Boundary_numerical_replacement(ndarray,d1,d2,d3):
	for k in range(0,d1):
		for j in range(1,d2-1):
			ndarray[k,j,0] = ndarray[k,j,1]
	for k in range(0,d1):
		for i in range(0,d3):
			ndarray[k,0,i] = ndarray[k,1,i]
	return ndarray
#读取提取后的FNL资料，共u、v、w、h、t、rh6个要素，21层，lon：50-130，lat：10-60
data2 = np.fromfile("I:\\data\\fnl\\fnldata2.dat",dtype = np.float32)
np.set_printoptions(suppress=True)
data3 = data2.reshape(6,21,51,81)
shape = data3.shape
print(shape)
#计算物理量
#计算uv风
uv1 = []
for k in range(0,shape[1]):
	for j in range(0,shape[2]):
		for i in range(0,shape[3]):
			rst = np.sqrt(data3[0,k,j,i]**2 + data3[1,k,j,i]**2)
			uv1.append(rst)
uv = np.array(uv1).reshape(shape[1],shape[2],shape[3])
#计算地转风分量ugf,vgf，计算涡度wdf，散度sdf
ug1 = []
vg1 = []
wd1 = []
sd1 = []
for k in range(0,shape[1]):
	for j in range(1,shape[2]-1):
		for i in range(1,shape[3]-1):
			rst_ug1 = -((0.672*(data3[3,k,j+1,i]-data3[3,k,j-1,i]))/((ds*pi/180.0)*6371000.0*
				np.sin(d*(j)*pi/180.0)))*100000.0
			rst_vg1 = -((0.672*(data3[3,k,j,i+1]-data3[3,k,j,i-1]))/((ds*pi/180.0)*6371000.0*
				np.sin(d*(j)*pi/180.0)))*100000.0
			rst_wd1 = a1*(data3[1,k,j,i+1]-data3[1,k,j,i-1])/np.cos((d*(j)*pi/180.0)*(ds*pi/180.0))-(data3[0,k,j+1,i]-data3[0,k,j-1,i])/(ds*pi/180.0)
			rst_sd1 = a1*(data3[0,k,j,i+1]-data3[0,k,j,i-1])/np.cos((d*(j)*pi/180.0)*(ds*pi/180.0))+(data3[1,k,j+1,i]-data3[1,k,j-1,i])/(ds*pi/180.0)
			ug1.append(rst_ug1)
			vg1.append(rst_vg1)
			wd1.append(rst_wd1)
			sd1.append(rst_sd1)
ug2 = np.array(ug1).reshape(shape[1],shape[2]-2,shape[3]-2)
vg2 = np.array(vg1).reshape(shape[1],shape[2]-2,shape[3]-2)
wd2 = np.array(wd1).reshape(shape[1],shape[2]-2,shape[3]-2)
sd2 = np.array(sd1).reshape(shape[1],shape[2]-2,shape[3]-2)
ug3 = np.zeros((21,51,81),dtype = float)
vg3 = np.zeros((21,51,81),dtype = float)
wd3 = np.zeros((21,51,81),dtype = float)
sd3 = np.zeros((21,51,81),dtype = float)
for k in range(0,shape[1]):
	ug3[k,1:shape[2]-1,1:shape[3]-1] = ug2[k,:,:,]
	vg3[k,1:shape[2]-1,1:shape[3]-1] = vg2[k,:,:,]
	wd3[k,1:shape[2]-1,1:shape[3]-1] = wd2[k,:,:,]
	sd3[k,1:shape[2]-1,1:shape[3]-1] = sd2[k,:,:,]
ugf = Boundary_numerical_replacement(ug3,shape[0],shape[1],shape[2])
vgf = Boundary_numerical_replacement(vg3,shape[0],shape[1],shape[2])
wdf = Boundary_numerical_replacement(wd3,shape[0],shape[1],shape[2])
sdf = Boundary_numerical_replacement(sd3,shape[0],shape[1],shape[2])
level = [x*50 for x in range(-180,90) ]
print(level)
x = np.arange(0,81,1)
y = np.arange(0,51,1)
X, Y = np.meshgrid(x,y)
plt.contour(X,Y,sdf[0,:,:],levels = level)
plt.show()

print('done')
#边界数值替换函数

