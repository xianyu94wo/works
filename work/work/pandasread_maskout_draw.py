import cmaps
import maskout
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.interpolate import Rbf
from mpl_toolkits.basemap import Basemap


plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号


data = pd.read_csv('I:\\data\\data.dat', sep='  ', engine = 'python', header=None, 
    names=['站号 ','lon','lat','闪电'] )

# 插值

lon = data['lon']
lat = data['lat']
lighting_data = data['闪电']
print(lighting_data)

olon = np.linspace(89,118,90)
olat = np.linspace(31,90,90)
olon,olat = np.meshgrid(olon,olat)



# 插值处理
func = Rbf(lon, lat, lighting_data,function='linear')
lighting_data_new = func(olon, olat)

# 画图
fig = plt.figure(figsize=(16,9))
plt.rc('font',size=15,weight='bold')
ax = fig.add_subplot(111)
m = Basemap(projection='cyl',llcrnrlat=31,llcrnrlon=89,urcrnrlat=35,urcrnrlon=97)
m.readshapefile('I:\\data\\yushu\\yushu','yushu.shp', linewidth=1, color='k')
#m.readshapefile('I:\\data\\xingzhengquhua_shp\\dijishi_2004','dijishi_2004.shp', linewidth=1, color='k')
x,y = m(olon,olat)
xx,yy = m(lon,lat)
levels = np.linspace(40,70,50)
cf = m.contourf(x,y,lighting_data_new, levels=levels, cmap=cmaps.CBR_wet)
cbar = m.colorbar(cf,location='right',format='%d',size=0.3,
    ticks=np.linspace(0,np.max(lighting_data_new),10),label='毫米')
st = m.scatter(xx-0.1,yy,c='k',s=10,marker='o')
#for i in range(0,len(xx)):
#    plt.text(xx[i],yy[i],data['站号'][i],va='center',fontsize=10)
lon_num = np.arange(89,100,3)
lon_label = ['89°','92°','95°','98°E']
lat_num =  np.arange(31,37.5,1)
lat_label = ['31°','32°','33°','34°','35°','36°','37°N']
plt.yticks(lat_num,lat_label)
plt.xticks(lon_num,lon_label)
plt.title('测试图')
# 白化
#clip = maskout.shp2clip(cf,ax,m,'I:\\data\\xingzhengquhua_shp\\dijishi_2004',[632700]) 
plt.savefig('test1.png', bbox_inches='tight',dpi=300)
print('over')