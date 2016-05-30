package com.ui.test;  
import android.os.RemoteException;

import com.android.uiautomator.core.UiObject;
import com.android.uiautomator.core.UiObjectNotFoundException;
import com.android.uiautomator.core.UiScrollable;
import com.android.uiautomator.core.UiSelector;
import com.android.uiautomator.testrunner.UiAutomatorTestCase;
  
public class Uiautomator extends UiAutomatorTestCase {  
    public void testDemo() throws UiObjectNotFoundException, RemoteException {  
    	//回到桌面
    	getUiDevice().pressHome();
    	getUiDevice().pressBack();
    	getUiDevice().unfreezeRotation();
    	getUiDevice().setOrientationLeft();
    	getUiDevice().setOrientationRight();
        // 进入电视分类
        UiObject TV = new UiObject(new UiSelector().text("TV"));  
        TV.click();  
        // 进入中文电视
    	UiObject Chinese= new UiObject(new UiSelector().text("ChineseTV"));  
    	if(Chinese.exists() && Chinese.isEnabled())
    	{
    		Chinese.click(); 
    	}
    	
        //休眠10秒  
        try {  
            Thread.sleep(10000);  
        } catch (InterruptedException e1) {  
            e1.printStackTrace();  
        }
        
      // 进入节目列表
        UiObject okButton = new UiObject(new UiSelector().text("OK").className("android.widget.Button"));
    	if(okButton.exists() && okButton.isEnabled())
    	{
    	okButton.clickAndWaitForNewWindow();
    	}
    	else 
    	getUiDevice().pressKeyCode(23);
    	getUiDevice().pressDPadRight();
        getUiDevice().pressDPadLeft();
        getUiDevice().pressDPadLeft();
        for(int i=1;i<=7;i++)
        {getUiDevice().pressDPadDown();}
        getUiDevice().pressDPadRight();
        
        for(int j=1;j<=18;j++)
        {
         getUiDevice().pressDPadDown();
		}
       
        UiObject Pagedown= new UiObject(new UiSelector().text("Page-"));
        if(Pagedown.exists() && Pagedown.isEnabled())
    	{
        	Pagedown.click();
    	}
        else
        	{
        	UiObject Pageup= new UiObject(new UiSelector().text("Page+"));
            Pageup.click();
        }
        UiScrollable EPG = new UiScrollable( new UiSelector().scrollable(true));  
        UiObject channel = EPG.getChildByText(  
            new UiSelector().textContains("5"), "5", true);  
        channel.clickAndWaitForNewWindow();  
        sleep(20000);
        
        getUiDevice().pressHome();
        getUiDevice().pressBack();
        UiObject More = new UiObject(new UiSelector().text("More"));  
        More.click();  
        UiObject Browser = new UiObject(new UiSelector().text("Browser"));  
        Browser.click();  
        Browser = new UiObject(new UiSelector().className("android.widget.EditText"));  
        Browser.setText("www.baidu.com");  
        getUiDevice().pressEnter(); 
        
    } 

}

