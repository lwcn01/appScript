from urllib import request, parse

f = open('G:\monkeytest.txt','r',encoding='gbk',errors='ignore')  #打开gbk编码的文件，忽略非法编码字符
f.read()    #读取文件
f.close()   #关闭文件

f = open('G:\monkeytest.txt','w')  #写文件
f.write('Hello world')            #写入hello world
f.close()    #关闭文件
