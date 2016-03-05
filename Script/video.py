#coding=utf-8
#Version 1.0 
#update 2015-11-25
import os
import re
import unittest
import time
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, WebDriverException
class AndroidTest(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4.2'
        desired_caps['deviceName'] = '192.168.8.130'
        desired_caps['appPackage'] = 'com.chinesevideo.app'
        desired_caps['appActivity'] = '.WelcomeActivity'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    def test_dashijie(self):
        time.sleep(6)           
		#check exit tips
        self.driver.keyevent(4)
        pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
        out = os.popen("adb shell dumpsys window w | %s \/ | %s name=" %('findstr', 'findstr')).read()
        package = pattern.findall(out)[0].split("/")[0]        
        # showtime      
        #click the left page
        time.sleep(3)		
        TouchAction(self.driver).press(None, x=90, y=338).release().perform()	
        time.sleep(3)      
        self.driver.keyevent(4)
        time.sleep(3) 
        TouchAction(self.driver).press(None, x=90, y=501).release().perform()
        time.sleep(3)      
        self.driver.keyevent(4)
        #check home post
        try:
            el0 = self.driver.find_element_by_id(package+':id/HomeMoudle_remtv')
        except:
            print('No el0 Element' )
        else:	
            action = TouchAction(self.driver)
            action.tap(el0).perform()
            time.sleep(3)      
            self.driver.keyevent(4)
        try:			
            el1 = self.driver.find_element_by_id(package+':id/HomeMoudle_remvar')
        except:
            print('No el1 Element' )
        else:
            action = TouchAction(self.driver)
            action.tap(el1).perform()
            time.sleep(3)      
            self.driver.keyevent(4) 
        try:	
            el2 = self.driver.find_element_by_id(package+':id/HomeMoudle_remtopic')
        except:
            print('No el2 Element' )
        else:
            action = TouchAction(self.driver)
            action.tap(el2).perform()
            time.sleep(3)      
            self.driver.keyevent(4)
        #check channel play
        try:
            el3 = self.driver.find_element_by_id(package+':id/HomeMoudle_1')
        except:
            print('No el3 Element' )
        else:	
            el3.click() 
            self.driver.find_element_by_id(package+':id/b_details_colection').click()
            time.sleep(3) 
            # collect channel
            self.driver.find_element_by_id(package+':id/b_details_play').click() 		
            time.sleep(6)         
            #page+/-
            self.driver.keyevent(82)
            time.sleep(1)
            self.driver.keyevent(59)
            time.sleep(3)
            self.driver.keyevent(60)
            # quick
            time.sleep(8)
            self.driver.press_keycode(22)
            self.driver.press_keycode(22).implicitly_wait(10)
            # volume
            time.sleep(3)
            self.driver.keyevent(164)
            time.sleep(3)
            self.driver.keyevent(24)
            time.sleep(3)
            self.driver.keyevent(25)
            time.sleep(20) 
            self.driver.keyevent(4)
            #restore the window of replay & continue, continue auto-playing 
            WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_id(package+':id/b_details_play')).click()
            time.sleep(3)
            self.driver.save_screenshot("G:/job/APK/点播/replay & continue.png") 
            time.sleep(20)
            self.driver.keyevent(4)
            #play_continue button	
            time.sleep(3)
            self.driver.find_element_by_id(package+':id/b_details_play').click()
            try:
                els = self.driver.find_elements_by_class_name('android.widget.Button')
            except:
                print('No Button' )
            else:	            
                els[1].click()
            time.sleep(20)
            # pause
            self.driver.keyevent(23)
            self.driver.save_screenshot("G:/job/APK/点播/pause.png")
            time.sleep(3)
            self.driver.keyevent(23)
            time.sleep(10)			
            self.driver.keyevent(4)
            #replay button
            time.sleep(3)
            self.driver.find_element_by_id(package+':id/b_details_play').click()
            els = self.driver.find_elements_by_class_name('android.widget.Button')
            els[0].click()
            time.sleep(20)
            self.driver.keyevent(4)
            #positive &reverse button
            try:
                el9 = self.driver.find_element_by_id(package+':id/b_details_choose')                
            except:
                print('No el9 Element' )
            else:	
                TouchAction(self.driver).tap(el9).perform()
                time.sleep(3)
                self.driver.save_screenshot("G:/job/APK/点播/positive.png")
                self.driver.keyevent(82)
                self.driver.save_screenshot("G:/job/APK/点播/reverse.png")
                time.sleep(3)
                try:
                    el9a = self.driver.find_element_by_xpath("//android.widget.TextView[contains(@text,'2')]")
                except:
                    print('No choose Element' )
                else:
                   el9a.click()                  				   
                   time.sleep(8)				   
                   self.driver.keyevent(4)
                   #close choose window
                   time.sleep(1)
                   self.driver.keyevent(4)
        #back  detail page
        time.sleep(3)		
        self.driver.keyevent(4)
        #other classify
        time.sleep(3)
        self.driver.find_element_by_id(package+':id/HomeMoudle_2').click()
        time.sleep(3)  
        self.driver.keyevent(4) 
        self.driver.find_element_by_id(package+':id/HomeMoudle_3').click()
        time.sleep(3)
        self.driver.keyevent(4)
        try:		
            el4 = self.driver.find_element_by_id(package+':id/HomeMoudle_4')
        except:
            print('No el4 Element' )
        else:	
            TouchAction(self.driver).tap(el4).perform()
            time.sleep(3)      
            self.driver.keyevent(4)      
		#move to the avilable area 
        time.sleep(3)
        if (package=='com.chinesevideo.app'):
            self.driver.keyevent(20)
            self.driver.keyevent(20).implicitly_wait(10)	
            self.driver.keyevent(22).implicitly_wait(10)		
            self.driver.keyevent(22).implicitly_wait(10)	
            self.driver.keyevent(22).implicitly_wait(10)	
            self.driver.keyevent(22).implicitly_wait(10)		
            #click other page       
            self.driver.find_element_by_id(package+':id/HomeMoudle_5').click()
            time.sleep(3)
            self.driver.keyevent(4) 
            self.driver.find_element_by_id(package+':id/HomeMoudle_6').click()
            time.sleep(3)
            self.driver.keyevent(4) 
            self.driver.find_element_by_id(package+':id/HomeMoudle_7').click()
            time.sleep(3)
            self.driver.keyevent(4)
            time.sleep(3)
            out1 = os.popen("adb shell getprop ro.build.version.sdk").read()
            if(out1 != '19'):		
                print ('The box isn\'t HTV3')
            else:                
                el265 = self.driver.find_element_by_id(package+':id/HomeMoudle_h265')
                action = TouchAction(self.driver)
                action.tap(el265).perform()
                time.sleep(3)
                self.driver.keyevent(4)           
        else:
            print ("No such package")
        time.sleep(3)			
        # video
        #self.driver.keyevent(22)
        #time.sleep(3)
        self.driver.keyevent(22)
        time.sleep(3)
        # move 
        try:
            self.driver.find_element_by_id(package+':id/HomeMoudle_movie')
        except:
            print('No movie Element' )
        else:	
            self.driver.find_element_by_id(package+':id/HomeMoudle_movie').click()
            time.sleep(3)
            self.driver.keyevent(20)            			
            self.driver.keyevent(20)
            self.driver.keyevent(20)
            self.driver.implicitly_wait(30)
            self.driver.keyevent(22)
            self.driver.keyevent(22)
            time.sleep(6)
            # select button
            self.driver.find_element_by_id(package+':id/shaixuan').click()	
            time.sleep(2)
            self.driver.keyevent(4)
            time.sleep(2)
        self.driver.keyevent(4)
        # TV move
        try:
            self.driver.find_element_by_id(package+':id/HomeMoudle_TV')
        except:
            print('No tv Element' )
        else:	
            self.driver.find_element_by_id(package+':id/HomeMoudle_TV').click()
            time.sleep(3)
            self.driver.keyevent(20)            			
            self.driver.keyevent(20)
            self.driver.keyevent(20)
            time.sleep(6)
            self.driver.keyevent(22)
            self.driver.keyevent(22)
            time.sleep(3)
            # search function
            self.driver.find_element_by_id(package+':id/sousou').click()
            time.sleep(3)            
            #self.driver.find_element_by_xpath("//android.widget.Button[contains(@text,'A')]").click()
            #self.driver.implicitly_wait(30)		            	
            #self.driver.find_element_by_id(package+':id/search_keybord_full_del').click()
            #time.sleep(3)
            #self.driver.find_element_by_id(package+':id/search_keybord_full_clear').click()
            #time.sleep(2)			
            #self.driver.keyevent(4)
            #time.sleep(2)	
            self.driver.keyevent(4)
            time.sleep(2)	
            self.driver.keyevent(4)
        try:
            elc = self.driver.find_element_by_id(package+':id/HomeMoudle_variety')
        except:
            print('No elc Element' )
        else:	
            TouchAction(self.driver).tap(elc).perform()
            time.sleep(3) 			
            self.driver.keyevent(4)
        try:
            eld = self.driver.find_element_by_id(package+':id/HomeMoudle_katoon')
        except:
            print('No eld Element' )
        else:	
            TouchAction(self.driver).tap(eld).perform()
            time.sleep(3)      
            self.driver.keyevent(4)
        try:
            ele = self.driver.find_element_by_id(package+':id/HomeMoudle_singner')
        except:
            print('No ele Element' )
        else:	
            TouchAction(self.driver).tap(ele).perform()
            time.sleep(3)      
            self.driver.keyevent(4)
        # special
        time.sleep(3)		
        self.driver.keyevent(22)
        time.sleep(2)
        self.driver.keyevent(22)
        time.sleep(2)
        try:
           el5 = self.driver.find_element_by_xpath("//android.widget.ImageView[contains(@resource-id,'1')]")
        except:
            print('No el5 Element' )
        else:	
            TouchAction(self.driver).tap(el5).perform()
            time.sleep(3) 	
            self.driver.keyevent(4)	
        time.sleep(3)		
        el6 = self.driver.find_element_by_xpath("//android.widget.ImageView[contains(@resource-id,'2')]")
        TouchAction(self.driver).tap(el6).perform() 
        # waiting for show all channel post  in special		
        time.sleep(15)
        self.driver.keyevent(22)
        self.driver.keyevent(22)
        time.sleep(3)
        self.driver.keyevent(23)
        time.sleep(3)
        # collect special channel
        self.driver.find_element_by_id(package+':id/b_details_colection').click()
        time.sleep(2)
        self.driver.keyevent(4)	
        time.sleep(3)
        self.driver.keyevent(4)	
        time.sleep(3)
        el7 = self.driver.find_element_by_xpath("//android.widget.ImageView[contains(@resource-id,'3')]")
        TouchAction(self.driver).tap(el7).perform()        
        time.sleep(3)
        self.driver.keyevent(4)	
        time.sleep(3)
        el8 = self.driver.find_element_by_xpath("//android.widget.ImageView[contains(@resource-id,'4')]")
        TouchAction(self.driver).tap(el8).perform()       
        time.sleep(3)
        # move in special
        self.driver.keyevent(22)
        time.sleep(2)
        self.driver.keyevent(23)
        # waiting for show all channel post  in special
        time.sleep(15)
        # play one special
        self.driver.keyevent(23)
        time.sleep(2)	
        try:
            self.driver.find_element_by_id(package+':id/b_details_play')
        except:
            print('No play button' )
        else:	
            self.driver.find_element_by_id(package+':id/b_details_play').click()
            time.sleep(10)
            # back play
            self.driver.keyevent(4)
            time.sleep(2)
            # back detail page
            self.driver.keyevent(4)
            time.sleep(2)
            # back one special post
            self.driver.keyevent(4)
            time.sleep(2)
            # back the special			
            self.driver.keyevent(4)
            time.sleep(2)
        #setting
        self.driver.keyevent(22)
        time.sleep(2)		
        self.driver.keyevent(22)
        time.sleep(2)
        self.driver.keyevent(22)
        time.sleep(2)
        self.driver.keyevent(22)
        time.sleep(2)
        self.driver.find_element_by_id(package+':id/iv_install').click()
        time.sleep(3)
        self.driver.keyevent(4)
        self.driver.find_element_by_id(package+':id/iv_update').click()
        time.sleep(3)
        self.driver.keyevent(4)
        self.driver.find_element_by_id(package+':id/iv_palysetting').click()
        time.sleep(3)
        self.driver.keyevent(4)
        self.driver.find_element_by_id(package+':id/iv_cleanmemory').click()
        time.sleep(3)
        self.driver.keyevent(4)
        self.driver.find_element_by_id(package+':id/iv_about').click()
        time.sleep(3)
        self.driver.keyevent(4)
    # 关闭应用
    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AndroidTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

'''
try：
     button1 = self.driver.find_element_by_name("登录")
except:
     print "用户已登录，执行用户已登录时的测试流程"
else：
      print “用户未登录，执行用户未登录时的测试流程”

        self.driver.swipe(0, 0, 100, 100, 200);
        el = self.driver.find_element_by_accessibility_id('freetv.box.yuetv:id/image_red')
        self.assertIsNotNone(el)
		els = self.driver.find_elements_by_accessibility_id('Animation')
        self.assertIsInstance(els, list)
		els = self.driver.find_elements_by_android_uiautomator('new UiSelector().clickable(true)')
#self.assertIsInstance(els, list)
swipe start_x: 200, start_y: 200, end_x: 200, end_y: 400, duration: 2000
webdriver.ActionChains(dr).move_to_element(menu).perform()
driver.get('http://www.baidu.com')

 els = self.driver.find_elements_by_xpath('//android.widget.TextView')
        self.driver.scroll(els[7], els[3])
         els = self.driver.find_elements_by_class_name('android.widget.TextView')
        self.driver.scroll(els[len(els)-1], els[0])


driver.background_app(5)
driver.launch_app()
driver.start_activity('com.example.android.apis', '.Foo')
driver.find_element_by_id("name").send_keys("XXXXX") 

action = TouchAction(driver)
action.press(element=el, x=10, y=10).release().perform()

driver.swipe(start_x=75, start_y=500, end_x=75, end_y=0, duration=800)

driver.scroll_to
driver.switch_to.context("WEBVIEW")

        WebDriverWait(driver, 10).until(lambda x: x.touch('com.chinesevideo.app:id/HomeMoudle_remtv')).click()

driver.implicitly_wait(10) 
        driver = self.driver 
		self.driver.keyevent(20)

driver.start_activity('com.example.android.apis', '.Foo')
driver.open_notifications()
driver.get('http://saucelabs.com/test/guinea-pig');
self.driver.switch_to.context(self.driver.contexts.first)
driver.launch_app()
#ActionChains(self.driver).drag_and_drop(el6, el9).perform()

self.driver.find_elements_by_xpath("//android.widget.RelativeLayout[4]/android.support.v4.view.ViewPager[0]/Android.widget\.FrameLayout[0]/Android.widget\
		.LinearLayout[0]/Android.widget.HorizontalScrollView[0]/Android.widget.RelativeLayout[5]/Android.widget.RelativeLayout[0]/Android.widget.ImageView[0]").click()
 #swipe start_x: 200, start_y: 200, end_x: 200, end_y: 400, duration: 2000
 
 
 Set<String> context = driver.getContextHandles();
        for (String contextName : context) {
            System.out.println(contextName);
context = driver.getContextHandles()
        width=self.driver.manage().window().getSize().width
        height=self.driver.manage().window().getSize().height

        self.driver.swipe(width/2,height*3/4, width/2,height/4, 1000)
		self.driver.swipe(start_x=90, start_y=178, end_x=1222, end_y=178, duration=1500)
    driver.get(“http://www.baidu.com”);
TouchAction().longPress(el).release().perform()
        #WebDriverWait(self.driver, 10).until(lambda driver: driver.long_press_keycode(22))
        #self.driver.long_press_keycode(22).(10000).release().perform()

try catch
        self.driver.getContextHandles()	

el = driver.findElementByAndroidUIAutomator("new UiSelector().text(\"Add note\")");
assertThat(el.getText(),equalTo("Add note"));
        self.driver.manage().timeouts().implicitlyWait(60, TimeUnit.SECONDS)

'''

