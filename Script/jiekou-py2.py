#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-01-21 09:23:02
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import urllib,urllib2   #导入这两个模块
import requests        # 导入这个模块
count = 1000000          #书籍ID
if count <=2000000:     #如果书籍的ID小于200W
    while True:                 # 条件为真
        count += 1             #循环开始，并且count += 1 
        try:                          #try 捕获异常
            url = 'https://api.douban.com/v2/book/%s' %count    #自动通过count数量的变化请求接口数据 

            url2 = urllib2.Request(url)                         # 使用urllib2的request方法
            response = urllib2.urlopen(url2)                    #用urlopen打开上一步返回的结果，得到请求后的响应内容
            apicon = response.read()                            #读取response
            print apicon
        except urllib2.HTTPError:                               #如果频繁请求，会被判定为恶意请求， 并被封IP 这个只是一个实例，没有加时间间隔，想深入做的同学可以加一下
            print "error , urllib2.HTTPError : %s " %count      # 如果捕获异常， 则返回异常坐标