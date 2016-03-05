#!/usr/bin/python
# -*- coding: UTF-8 -*-

def screenshot(self):
        path = PATH(os.getcwd()+"/output/pic")
        timestamp = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
        os.popen("adb wait-for-device")
        os.popen("adb shell screencap -p /data/local/tmp.png")
        if not os.path.isdir(PATH(os.getcwd()+"/output/pic")):
            os.makedirs(path)
        os.popen("adb pull /data/local/tmp.png " + PATH(path + "/" + timestamp + ".png"))
        os.popen("adb shell rm /data/local/tmp.png")
        print "success"