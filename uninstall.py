#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'new'

import os
import subprocess
import time

def uninstall0():
    try:
        package = os.popen('adb shell pm list package -3').read()
        package = str(package).split('=')
    except RuntimeError:
        print('adb连接失败')
    else:
        print('\n开始卸载\n')
        for x in range(1,len(package),1):
            package_name = package[x].split('\n')[0]
            out = subprocess.Popen('adb shell pm uninstall %s' %(package_name),shell = True,stdout = subprocess.PIPE,stderr = subprocess.STDOUT)
            time.sleep(3)
            if out.stdout.read() is 'Failure':
                print('%s' %(package_name) + ':' + '卸载失败')
            else:
                print('%s' %(package_name) + ':' + '卸载成功')

def uinstall1():
    try:
        package = os.popen('adb shell pm list package -3').read()
        package = str(package).split(':')
    except RuntimeError:
        print('adb连接失败')
    else:
        print('\n开始卸载\n')
        for x in range(1,len(package)):
            package_name = package[x].split('\n')[0]
            out = subprocess.Popen('adb shell pm uninstall %s' %(package_name),shell = True,stdout = subprocess.PIPE,stderr = subprocess.STDOUT)
            time.sleep(3)
            if out.stdout.read() is 'Failure':
                print('%s' %(package_name) + ':' + '卸载失败')
            else:
                print('%s' %(package_name) + ':' + '卸载成功')

if __name__ == '__main__':
    out1 = os.popen("adb shell getprop ro.build.version.sdk").read()
    if(int(out1) == 19):
        uninstall0()
        print('\n卸载完成\n')
    else:
        uinstall1()
        print('\n卸载完成\n')
    os.system("pause")
