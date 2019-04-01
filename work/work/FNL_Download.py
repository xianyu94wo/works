'''
Created on 2018年7月31日

@author: ysj
'''
import requests
import datetime
def builtSession():
    email = "yousangjie@hotmail.com" #此处改为注册邮箱
    passwd = "Ysj8894315" #此处为登陆密码
    loginurl = "https://rda.ucar.edu/cgi-bin/login"
    #loginurl = "https://rda.ucar.edu/index.html?hash=data_user&action=signin"
    params = {"email":email, "password":passwd, "action":"login"}
    sess = requests.session()
    sess.post(loginurl,data=params)
    return sess
def download(sess, dt):
    g1 = datetime.datetime(1999,7,30,18)
    g2 = datetime.datetime(2007,12,6,12)
    if dt >= g2:
        suffix = "grib2"
    elif dt >= g1 and dt <g2:
        suffix = "grib1"
    else:
        raise StandardError("DateTime excess limit")
    print(suffix)
    url = r"http://rda.ucar.edu/data/ds083.2"
    #url = "https://rda.ucar.edu/datasets/ds083.2/"
    folder = "{}/{}/{}.{:0>2d}".format(suffix, dt.year, dt.year, dt.month)
    filename = "fnl_{}.{}".format(dt.strftime('%Y%m%d_%H_00'), suffix)
    fullurl = "/".join([url, folder, filename])
    r = sess.get(fullurl)
    with open(filename, "wb") as fw:
        fw.write(r.content)
    print(filename + " downloaded")
if __name__ == '__main__':
    print("downloading...")
    s = builtSession()
    for i in range(4):                                          #共下载多少个时次
        startdt = datetime.datetime(2018, 6, 30, 0)  #开始时次
        interval = datetime.timedelta(hours = i * 6)
        dt =startdt + interval
        download(s,dt)
    print("download completed!")