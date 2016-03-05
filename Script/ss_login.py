import json
import requests
#这是基于闪送app的api实现的模拟登陆
a = 1453900350630
def login():
    get_cookies = 'http://www.ishansong.com/web/admin/order/list'
    r = requests.get(get_cookies)
    cookies = r.cookies
    headers = {
        "Host":"www.ishansong.com",
        "Origin":"http://www.ishansong.com",
        "Referer":"http://www.ishansong.com/user/login",
        }
    
    url = 'http://www.ishansong.com/user/doLogin'
    data = {"service":"","tab":"tab2","username":xxxx,"password":xxxx}#注册后，在这里把username、password的参数修改成自己的用户名和密码即可

    r = requests.post(url ,data = data ,headers = headers , cookies = cookies )
    print (r.ok)
    #print (r.text)

                
if __name__ =='__main__':
    login()


    
