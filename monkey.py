#!/usr/bin/env python
# -*- coding: utf-8 -*-

__auther__ = 'new'

import re
import os,sys
import subprocess
import time
import datetime

PATH = lambda p: os.path.abspath(p)

def which_os():
    if os.name == 'nt':
        os.system('color 0c')
    else:
        return False

def exist_env():
    env = os.getenv('PATH')
    adb_env = re.findall('platform-tools', env)
    aapt_env = re.findall('platform-tools', env)
    if len(adb_env) == 0:
        print('Adb not found in ANDRIOD Environment platform-tools！')
        return False
    if len(aapt_env) != 0:
        return True
    else:
        raise EnvironmentError("aapt not found in $ANDRIOD Environment: %s" %aapt_env)

def exist_dir(app_name):
    global t,log_dir
    t = time.strftime('%Y-%m-%d_%H-%M-%S')
    pwd = os.path.join(os.path.expanduser('~'), 'Desktop')
    log_dir = os.path.join(pwd, '%s'%app_name)
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

def log_cat(packageName):
    filename = packageName + '_logcat_' + t + '.txt'
    log_path = os.path.join(log_dir,filename)
    txt = '> ' + log_path
    subprocess.Popen('adb logcat -c | adb logcat -v time %s' %txt,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def Devices_status():
    Devices = os.popen('adb devices')
    DevicesInfo = Devices.read()
    DevicesList = re.findall('(.*?)\\tdevice\\b', DevicesInfo)
    return DevicesList

def package(path):
    path = path.strip()
    package_info = subprocess.check_output('aapt dump badging {0}'.format(path))
    package_name = package_info.decode('utf-8').split('\n')[0].split('\'')[1]
    return package_name

def monkey(packageName,event):
    monkeylogfile = packageName + '_MonkeyTest_' + t + '.txt'
    monkeylogpath = os.path.join(log_dir,monkeylogfile)
    monkeytxt = '> ' + monkeylogpath
    throttleTime = 50
    #monkey = 'adb -s %s shell monkey -p %s -s 250 --ignore-crashes --ignore-timeouts --monitor-native-crashes --throttle %s -v %s %s' % (
        #device, packagName, throttleTime, evnet, txt)
    monkey = 'adb shell monkey -p {0} --throttle {1} -v {2} {3}'.format(packageName,throttleTime,event,monkeytxt)
    start_time = datetime.datetime.now()
    subprocess.Popen(monkey, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).wait()
    end_time = datetime.datetime.now()
    take_time = (end_time-start_time).seconds
    print('\nMonkey测试用时: %s\n' %take_time)

def get_crash_log(packageName):
    try:
        os.system('adb pull /data/anr/traces.txt ' + PATH(os.path.join(log_dir,packageName + '_Crash_' + t +'.txt')))
    except Exception as e:
        print('ANR not found:',e)
    else:
        os.system('adb shell rm /data/anr/traces.txt')
#def Devices_connect():

if __name__ == '__main__':
    Device_list = Devices_status()
    if len(Device_list) == 0:
       print('\n...ADB未连接...\n')
       os.system('pause')
    else:
        try:
            which_os()
            exist_env()
        except Exception as e:
            print(e)
        else:
            for x in range(10):
                path = input('\n...将APK文件拖入本窗口中...')
                if not os.path.exists(path.strip()):
                    print('\n...文件路径错误...\n')
                else:
                    try:
                        if re.findall(r'.apk$',path)[0] == ".apk":
                            app_name = os.path.splitext(path)[0].split('\\')[-1]
                    except:
                        print('\n...APK文件不存在或非APK文件...\n')
                    else:
                        try:
                            packageName = package(path)
                            exist_dir(app_name)
                            log_cat(packageName)
                        except Exception as e:
                            print(e)
                        except:
                            print('\n...APK文件异常...\n')
                        else:
                            print('\n\'%s\'...开始Monkey压力测试...\n' %app_name)
                            try:
                                event = int(input('MonkeyTest events: '))
                            except Exception as e:
                                print(e)
                            else:
                                if event < 0:
                                    print('\n...event数值错误...\n')
                                else:
                                    try:
                                        monkey(packageName,event)
                                    except Exception as e:
                                        print(e)
                                    else:
                                        get_crash_log(packageName)
                                        print('\n...Monkey测试已完成，桌面生成%s目录文件...\n'%app_name)
        finally:
            os.system('pause')
        sys.exit()
