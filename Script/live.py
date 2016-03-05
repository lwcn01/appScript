#coding=utf-8
#Version 1.0
#ipdate 2015-11-14
import os
import unittest
import time 
#import HTMLTestRunner
from appium import webdriver
class AndroidTest(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        #desired_caps['platformVersion'] = '4.4.2'
        desired_caps['deviceName'] = '192.168.8.130'
        desired_caps['appPackage'] = 'freetv.box.taimin'
        desired_caps['appActivity'] = 'com.taimintv.app.WelcomeActivity'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    '''
    desired_caps={
            'platformName': 'Android',
            'platformVersion': '4.4.2',
            'deviceName': '192.168.8.130',
            #'appPackage': 'freetv.box.yuetv',
            #'appActivity': 'com.yuetv.app.WelcomeActivity'
            }
    desired_caps2={
            'platformName': 'Android',
            'platformVersion': '4.4.2',
            'deviceName': '192.168.8.130',
            'appPackage': 'com.android.settings',
            'appActivity': '.Settings'
            }
    '''    

    def test_live1(self):
        #check voice button
        time.sleep(10)        
        self.driver.press_keycode(25)
        time.sleep(1)
        self.driver.press_keycode(24)
        time.sleep(1)
        self.driver.press_keycode(164)
        time.sleep(1)
        self.driver.press_keycode(164)
        time.sleep(1)
        #check whether right or left key can set free Mute key
        self.driver.press_keycode(164)
        time.sleep(1)
        self.driver.press_keycode(21)
        time.sleep(1)
        self.driver.press_keycode(164)
        time.sleep(1)
        self.driver.press_keycode(22)
        time.sleep(1)
        #check mouse button
        self.driver.press_keycode(56)
        time.sleep(1)
        self.driver.press_keycode(56)
        time.sleep(1)
        #check recall button for tips
        self.driver.press_keycode(169)
        time.sleep(2)
        #els = self.driver.find_elements_by_class_name("android.widget.TextView")
        #els[1].click()
        #to collect fav &&swith channal by digital
        self.driver.press_keycode(77)
        time.sleep(3)
        self.driver.press_keycode(8)
        self.driver.press_keycode(77)
        time.sleep(8)
        self.driver.press_keycode(10)
        self.driver.press_keycode(77)
        time.sleep(8)
        self.driver.press_keycode(12)
        self.driver.press_keycode(77)
        time.sleep(8)
        self.driver.press_keycode(14)
        self.driver.press_keycode(77)
        time.sleep(8)
        self.driver.press_keycode(16)
        self.driver.press_keycode(77)
        time.sleep(8)
        #to recall in channallist
        self.driver.press_keycode(169)    #to 7
        time.sleep(8)
        self.driver.press_keycode(169)    #to 9
        time.sleep(8)
        #check the invalid number for channallist
        self.driver.press_keycode(7)
        time.sleep(3)
        #to fav show 4 channals in picture
        self.driver.press_keycode(23)
        self.driver.press_keycode(21)
        self.driver.press_keycode(19)
        self.driver.press_keycode(22)
        time.sleep(1)
        self.driver.save_screenshot("G:/job/APK/直播/favlist1.png")
        time.sleep(3)
        #to recall in favlist
        self.driver.press_keycode(169)    #to 7
        time.sleep(8)
        self.driver.press_keycode(169)    #to 9
        time.sleep(8)
        #check the favlist move
        self.driver.press_keycode(23)
        self.driver.press_keycode(2012)
        time.sleep(1)
        self.driver.press_keycode(2012)
        time.sleep(1)
        self.driver.press_keycode(168)
        time.sleep(1)
        self.driver.press_keycode(168)
        time.sleep(8)
        #check the invalid number for favlist
        self.driver.press_keycode(7)
        time.sleep(3)
        self.driver.press_keycode(13)        
        time.sleep(3)
        #cancel the fav 9 channal
        self.driver.press_keycode(23)
        self.driver.press_keycode(77)
        self.driver.save_screenshot("G:/job/APK/直播/favlist2.png")
        #back to channal list && pre-channal info
        self.driver.press_keycode(21)
        self.driver.press_keycode(20)
        self.driver.press_keycode(22)
        self.driver.press_keycode(22)
        self.driver.press_keycode(4)
        #check the channal info
        self.driver.press_keycode(61)
        time.sleep(3)
        self.driver.press_keycode(61)
        time.sleep(3)
        self.driver.press_keycode(82)
        self.driver.save_screenshot("G:/job/APK/直播/ChannalBar.png")
        time.sleep(10)          
        #check the channallist move
        self.driver.press_keycode(23)
        self.driver.press_keycode(59)
        time.sleep(1)
        self.driver.press_keycode(59)
        time.sleep(1)
        self.driver.press_keycode(60)
        time.sleep(1)
        self.driver.press_keycode(60)
        time.sleep(1)
        self.driver.press_keycode(4)
        #check switch channals by direction keys in channallist mode
        for num in (1,5):
            self.driver.press_keycode(19)
        self.driver.press_keycode(20)        
        time.sleep(8)
        self.driver.press_keycode(4)
        '''
    def test_live2(self):
        #swith system language to english
        #self.driver = webdriver.Remote('http://localhost:4726/wd/hub',desired_caps2)
        #self.driver.startActivity('com.android.settings','com.android.settings.Settings')
        #self.driver.find_element_by_android_uiautomator('new UiScrollable(new UiSelector().scrollable(true).\
        #instance(11)).scrollIntoView(new UiSelector().text("语言和输入法").instance(11));')
        self.driver.execute_script("mobile: scroll", {"direction": "down"})
        #self.driver.scroll(el1, el2)
        #el1 = self.driver.find_element_by_android_uiautomator('new UiSelector().text("语言和输入法")')
        #self.assertIsNotNone(el1)
        #el2 = self.driver.find_element_by_android_uiautomator('new UiSelector().text("English(United States)")')
        #self.assertIsNotNone(el2)
        self.driver.press_keycode(4) #back
        self.driver.press_keycode(4)
        self.driver.press_keycode(3)
        pakageName = 'hottv.box.tomsoccer'
        componentName = 'com.tomsoccer.app.WelcomeActivity'
        startTime = 5
        #self.driver.startActivity(component=componentName)
        #return test_live1(self)
	#view list
        #el0=self.driver.press_keycode(23)
	#action = TouchAction(driver)
        #action.longpress(el0).perform()
       # self.driver.perform(TouchAction().logpress(el))
        #self.driver.execute_script("mobile: scroll", {"direction": "down"})
        #self.driver.execute_script("mobile: scroll", {"direction": "down", element: element.getAttribute("android.widget.RelativeLayout")})
        #for num in range(1,25):
        #self.driver.press_keycode(20)
        #el2=self.driver.find_element_by_android_uiautomator('new UiScrollable(new UiSelector().scrollable(true).\
	#instance(0)).scrollIntoView(new UiSelector().className("android.widget.LinearLayout").instance(0));')
       # el2.click()
        #els = self.driver.find_elements_by_android_uiautomator("new UiSelector().clickable(true)")
       # self.assertGreaterEqual(13, len(els))

       # self.driver.save_screenshot("C:/Users/Administrator/Desktop/test1.jpg")
       '''
        textviews = self.driver.find_elements_by_class_name('android.widget.RelativeLayout')
        for textview in textviews:
          print ("textview")
        time.sleep(10)
    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AndroidTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
'''
    filename =  "G:\\Appium\\Report\\"+unicode(now,'utf-8')+"result.html"
    fp = file(filename, 'wb+')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='Report_title',description='Report_description')

try：
     button1 = self.driver.find_element_by_name("登录")
except:
     print "用户已登录，执行用户已登录时的测试流程"
else：
      print “用户未登录，执行用户未登录时的测试流程”

        self.driver.swipe(0, 0, 100, 100, 200);
        el=driver.find_Element_By_Classname('android.widget.TextView')

        el = self.driver.find_element_by_accessibility_id('freetv.box.yuetv:id/image_red')
        self.assertIsNotNone(el)
		els = self.driver.find_elements_by_accessibility_id('Animation')
        self.assertIsInstance(els, list)
		els = self.driver.find_elements_by_android_uiautomator('new UiSelector().clickable(true)')
#self.assertIsInstance(els, list)
swipe start_x: 200, start_y: 200, end_x: 200, end_y: 400, duration: 2000
el1 = self.driver.find_element_by_id('freetv.box.yuetv:id/text_red')
        assertEqual('freetv.box.yuetv:id/text_red', el3.text)

		els = driver.find_elements_by_android_uiautomator("new UiSelector().clickable(true)")
'''

