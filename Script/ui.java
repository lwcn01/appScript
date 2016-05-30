package com.ui.test;  
import com.android.uiautomator.core.UiObject;  
import com.android.uiautomator.core.UiObjectNotFoundException;  
import com.android.uiautomator.core.UiScrollable;  
import com.android.uiautomator.core.UiSelector;  

import com.android.uiautomator.testrunner.UiAutomatorTestCase;  
  
public class Uiautomator extends UiAutomatorTestCase {  
  
    public void testDemo() throws UiObjectNotFoundException {  
    	//回到桌面
    	getUiDevice().pressHome();
    	getUiDevice().pressBack();
        // 进入电视分类
    	UiObject TV = new UiObject(new UiSelector().text("TV"));  
    	TV.click(); 
    	getUiDevice().pressBack();
        // 进入更多分类
        UiObject Others = new UiObject(new UiSelector().text("More"));  
        Others.click();  
        //休眠3秒  
        try {  
            Thread.sleep(3000);  
        } catch (InterruptedException e1) {  
            e1.printStackTrace();  
        }
        
    }
     // 进入
    public void scrollClickObject(String targetClassName,String targetName) throws UiObjectNotFoundException 
         {
          UiScrollable collectionObject = new UiScrollable(new UiSelector().scrollable(true));
          if(collectionObject.exists()) 
          {
          UiObject scrollableObject = collectionObject.getChildByText(new UiSelector().className("com.kaiboer.huibo"), "MainActivity");
          scrollableObject.clickAndWaitForNewWindow();
      } else {
        UiObject targetObject = new UiObject(new UiSelector().className("com.kaiboer.huibo").text("MainActivity"));
        targetObject.clickAndWaitForNewWindow();
        }
              }
}
