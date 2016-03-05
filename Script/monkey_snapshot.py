#!/usr/bin/env monkeyrunner
# Copyright 2010, The Android Open Source Project
#coding=utf8
import sys  
from com.android.monkeyrunner import MonkeyDevice
from com.android.monkeyrunner import MonkeyImage
from com.android.monkeyrunner import MonkeyRunner 

CMD_MAP = {  
    'TOUCH': lambda dev, arg: dev.touch(**arg),  
    'DRAG': lambda dev, arg: dev.drag(**arg),  
    'PRESS': lambda dev, arg: dev.press(**arg),  
    'TYPE': lambda dev, arg: dev.type(**arg),  
    'WAIT': lambda dev, arg: MonkeyRunner.sleep(**arg)  
    }

def process_file(fp, device,photo_id):
    for line in fp:
        (cmd, rest) = line.split('|')
        try:
            rest = eval(rest)  
        except:
            print 'unable to parse options'
            continue

        if cmd not in CMD_MAP:
            print 'unknown command: ' + cmd
            continue

        CMD_MAP[cmd](device, rest)
        print cmd
        pic_name='./shot'+str(photo_id)+'.png'
        result = device.takeSnapshot()

        #compare picture
        result2 = MonkeyRunner.loadImageFromFile("E:\MD\shot"+str(photo_id)+".png")
        print "E:\MD\shot"+str(photo_id)+".png"

        flag = result.sameAs(result2,0.8)
        if (flag == False):
            print 'prapre to save new png '+pic_name
            result.writeToFile(pic_name,'png')


        photo_id+=1
    print "All PlayBack Action Captured,Total:"+str(photo_id)+' PNG Saved'
    print "==============================================================="

def main():
    print  "Ok,Now StarRuning MyZXX MonkeyRuner SnopShoot Shell"
    print "==============================================================="
    device = MonkeyRunner.waitForConnection()
    package = 'com.qunsheng.md'
    activity = 'com.qunsheng.md.activity.WelcomeActivity'
    runComponent = package + '/' + activity
    device.startActivity(component=runComponent)
    MonkeyRunner.sleep(30)
    #device.press('KEYCODE_MENU','DOWN_AND_UP')
    #result = device.takeSnapshot()
    #result.writeToFile('./shot5.png','png')

    file = sys.argv[1]
    fp = open(file, 'r')
    photo_id=0
    process_file(fp, device,photo_id)
    fp.close();

if __name__ == '__main__':
    main()