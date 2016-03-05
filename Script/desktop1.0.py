#coding=utf-8
#Version 1.0 
#CreateDate 2015-11-25
import os
import re
import unittest
import time
import HTMLTestRunner
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from selenium.common.exceptions import NoSuchElementException,WebDriverException
# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
class AndroidTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):    
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4.2'
        desired_caps['deviceName'] = '192.168.8.130'
        desired_caps['appPackage'] = 'org.coolx.htvlauncher'
        desired_caps['appActivity'] = '.YiYongActivity' 
        cls.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def test_simpleLauncher(self):
        time.sleep(3) 
 	    #testing begin from  the simpleLauncher	
        package='org.coolx.htvlauncher'        		
        try:
            el0 = self.driver.find_element_by_id(package+':id/btn_live')
        except:
            self.driver.keyevent(82)
            time.sleep(3)
            self.driver.find_element_by_id(package+':id/menu_tosimpleLauncher').click()
        else:
            action = TouchAction(self.driver)
            action.tap(el0).perform()
            time.sleep(3)
        self.driver.keyevent(4)			
 	    #check notifications
        self.driver.keyevent(82)
        time.sleep(3)             
        self.driver.keyevent(4)
        time.sleep(3) 
		#live add icon
        #a=input('输入当前页面元素数目: ')
        #num =range(int(a))
        #el = self.driver.find_element_by_class_name('android.widget.GridView')
        #els =el.find_elements_by_android_uiautomator('new UiSelector().resource_id('package+':id/gv_show_app')')
        #self.assertIsInstance(els, list)
        #els[1].click
       #find_elements_by_android_uiautomator('new UiSelector().class_name('android.widget.GridView').clickable(true)')
       # self.driver.find_element_by_xpath("//android.widget.GridView/android.widget.RelativeLayout[@index=1]").click()
        #time.sleep(3)
        #self.driver.find_element_by_xpath("//android.widget.GridView/android.widget.RelativeLayout[contains(@index,'0')]").click()
        #live remove icon
        #self.driver.find_element_by_xpath("//android.widget.GridView/android.widget.RelativeLayout[contains(@index,num[-1])]").click()
        #self.driver.find_element_by_xpath("//android.widget.GridView/android.widget.RelativeLayout[contains(@index,'1')]").click()
        #time.sleep(3)
        #self.driver.find_element_by_xpath("//android.widget.GridView/android.widget.RelativeLayout[contains(@index,'0')]").click()
        try:
            self.driver.find_element_by_id(package+':id/btn_vod')
        except:
            print('No vod Element' )
        else:  
            self.driver.find_element_by_id(package+':id/btn_vod').click()
            time.sleep(3)            
        try:
            self.driver.find_element_by_id(package+':id/btn_playback')
        except:
            print('No playback Element' )
        else:  
            self.driver.find_element_by_id(package+':id/btn_playback').click()
            time.sleep(3)
        try:
            self.driver.find_element_by_id(package+':id/btn_other')
        except:
            print('No other Element' )
        else:
            self.driver.find_element_by_id(package+':id/btn_other').click()
            time.sleep(3)
    def test_CleanMemory(self):
        self.driver.start_activity('com.cvte.taskmanager', '.OneClickCleaner')
        time.sleep(5)
        self.driver.find_element_by_id('com.cvte.taskmanager:id/clean_button').click()
        #self.assertIsNotNone(el1)
        time.sleep(3)
        self.driver.keyevent(4)
        time.sleep(3)
    def test_Calculator(self):
        self.driver.start_activity('com.android.calculator2', '.Calculator')
        self.driver.find_element_by_name('2').click()
        self.driver.find_element_by_name('+').click()
        self.driver.find_element_by_name('8').click()
        self.driver.find_element_by_name('=').click()
        time.sleep(3)
        self.driver.keyevent(4)
    def test_Browser(self):
        self.driver.start_activity('com.android.browser', '.BrowserActivity')
        time.sleep(3)
        self.driver.find_element_by_class_name("android.widget.EditText").send_keys("https://www.baidu.com/")
        time.sleep(5)
        self.driver.keyevent(AndroidKeyCode.ENTER)
        time.sleep(3)
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close_app()
        cls.driver.quit()

if __name__ == '__main__':
    suite=unittest.TestSuite()
    suite.addTest(AndroidTest("test_simpleLauncher"))
    suite.addTest(AndroidTest("test_CleanMemory"))
    suite.addTest(AndroidTest("test_Calculator"))
    suite.addTest(AndroidTest("test_Browser"))
    timestr = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    filename="G:\\Report\\Report" + timestr + ".html"        #定义个报告存放路径，支持相对路径。
    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='Test_result',description='Test_report')  #使用HTMLTestRunner配置参数，输出报告路径、报告标题、描述
    runner.run(suite)
    fp.close() #测试报告关闭



#lis = self.driver.find_elements_by_android_uiautomator("new UiSelector().class_name("+"android.widget.RelativeLayout"+").index(0)")
#double Screen_X = driver.Manage().Window.Size.Width;//获取手机屏幕宽度
#double Screen_Y = driver.Manage().Window.Size.Height;//获取手机屏幕高度
#double startX = element.Location.X; //获取元素的起点坐标，即元素最左上角点的横坐标
#double startY = element.Location.Y; //获取元素的起点坐标，即元素最左上角点的纵坐标
#double elementWidth = element.Size.Width;  //获取元素的宽度
#double elementHight = element.Size.Height; //获取元素的宽度
#unittest.TextTestRunner(verbosity=2).run(suite)
