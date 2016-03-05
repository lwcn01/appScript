import urllib
import urllib.parse
from urllib import request
count = 1000000                                                  #书籍ID
if count <=2000000:                                              #如果书籍的ID小于200W
    while True:                                                  # 条件为真
        count += 1                                               #循环开始，并且count += 1 
        try:                                                     #try 捕获异常
            url = 'https://api.douban.com/v2/book/%s' %count     #自动通过count数量的变化请求接口数据 
            url2 = urllib.request.Request(url)                   #使用urllib的request方法
            response = urllib.request.urlopen(url2)              #用urlopen打开上一步返回的结果，得到请求后的响应内容			
            apicon = response.read().decode('utf-8','ignore')    #读取response,将utf-8编码的字符串解码成Unicode编码,忽略无法编码的字符          
            print (apicon.encode('gbk','ignore'))			#将Unicode编码的字符串编码成GBK编码
        except urllib.request.HTTPError:           #如果频繁请求，会被判定为恶意请求， 并被封IP 这个只是一个实例，没有加时间间隔，想深入做的同学可以加一下
            print ("error , urllib.request.HTTPError : %s " %count  )     # 如果捕获异常， 则返回异常坐标
