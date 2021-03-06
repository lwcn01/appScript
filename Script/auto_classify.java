package com.ui.test;  
import android.os.RemoteException;

import com.android.uiautomator.core.UiObject;
import com.android.uiautomator.core.UiObjectNotFoundException;

import com.android.uiautomator.core.UiSelector;
import com.android.uiautomator.testrunner.UiAutomatorTestCase;

public class Uiautomator extends UiAutomatorTestCase {  
	
    public void testDemo() throws UiObjectNotFoundException, RemoteException {  
    	//回到桌面
    	getUiDevice().pressBack();
    	getUiDevice().pressHome();
    	getUiDevice().pressBack();
    	getUiDevice().unfreezeRotation();
    	getUiDevice().setOrientationLeft();
    	getUiDevice().setOrientationRight();
        // 进入更多分类
        UiObject More = new UiObject(new UiSelector().text("More"));  
        More.click(); 
        // 进入壁纸设置
 
    	UiObject Wallpaper= new UiObject(new UiSelector().text("Wallpaper"));  
    	Wallpaper.click(); 
    	getUiDevice().pressEnter(); 
    	getUiDevice().pressBack();
    	   //休眠3秒  
        try {  
            Thread.sleep(3000);  
        } catch (InterruptedException e1) {  
            e1.printStackTrace();  
        }
    	UiObject App_uninstall= new UiObject(new UiSelector().textContains("uninstall")); 
    	if(App_uninstall.exists() && App_uninstall.isEnabled())
    	{
    		App_uninstall.click(); 
    	}
        for(;;)
        {   sleep(3000);
         	getUiDevice().pressDPadDown();
            getUiDevice().pressKeyCode(23);
            UiObject okButton = new UiObject(new UiSelector().text("OK").className("android.widget.Button"));
            if(!okButton.exists())
            {
            	break;
            }
            else okButton.clickAndWaitForNewWindow();
           
        }
        
        testDemo1();
    	UiObject AppStore= new UiObject(new UiSelector().text("App Store"));
    	AppStore.click();
    	sleep(3000);
    	UiObject Recommend= new UiObject(new UiSelector().text("Recommend"));
    	Recommend.click();
    	sleep(3000);
    	UiObject Install= new UiObject(new UiSelector().textContains("Five"));
    	Install.click();
    	 try {  
             Thread.sleep(3000);  
         } catch (InterruptedException e2) {  
             e2.printStackTrace();  
         }
    	 UiObject successfully= new UiObject(new UiSelector().textContains("the exit key"));
    	 UiObject failed= new UiObject(new UiSelector().textContains("the OK button"));
        if(!successfully.exists()&&!failed.exists())
       {  
    	 sleep(3000);
        }
        else if(failed.exists())
               {  for(int i=1;i<=3;i++)
                     { getUiDevice().pressKeyCode(23);}
                } else getUiDevice().pressBack();
       } 
    	
    public void testDemo1() throws UiObjectNotFoundException{
    	
        getUiDevice().pressBack();
     	getUiDevice().pressHome();
     	getUiDevice().pressBack();
     	UiObject TV= new UiObject(new UiSelector().text("TV"));
     	TV.click();
     	sleep(3000);
     	getUiDevice().pressBack();
     	UiObject Demand= new UiObject(new UiSelector().text("Demand"));
     	Demand.click();
     	sleep(3000);
     	getUiDevice().pressBack();
    }
 
}

