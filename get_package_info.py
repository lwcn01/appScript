#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'new'

import os
import re
import subprocess

def get_package_info(path):
    path = path.strip()
    package = subprocess.check_output('aapt dump badging %s' %path)
    package_info = package.decode('utf-8')
    package_name = package_info.split('\n')[0].split("'")[1]
    versionCode = package_info.split('\n')[0].split("'")[3]
    versionName = package_info.split('\n')[0].split("'")[5]
    app_activity = re.findall(r'[a-zA-Z]{10}\-\w{8}\:\s+\w{4}\=(.*?)\s',package_info)
    print('应用包名: '+package_name,'应用版本号: '+versionCode,'应用版本名: '+versionName,sep='\n')
    print('应用Activity名:',app_activity[0].strip("'"))

if __name__ == '__main__':
    print('========查看APK的基本信息========')
    try:
        path = input('输入APK绝对路径：')
        get_package_info(path)
    except Exception as e:
        print(e)
    else:
        for i in range(1,11):
            print('第%d次查看APK的信息' %i)
            path = input('输入APK绝对路径：')
            get_package_info(path)
    finally:
        os.system("pause")
