# ========================================================
# Summary        :run
# Author         :tong shan
# Create Date    :2015-10-09
# Amend History  :
# Amended by     :
# ========================================================

#import readConfig
#readConfigLocal = readConfig.ReadConfig()
import unittest
from testSet.common.DRIVER import myDriver
import testSet.common.Log as Log
import os
from time import sleep

from selenium.common.exceptions import WebDriverException
import threading

mylock = threading.RLock()
log = Log.myLog.getLog()

# ========================================================
# Summary        :myServer
# Author         :tong shan
# Create Date    :2015-10-10
# Amend History  :
# Amended by     :
# ========================================================
class myServer(threading.Thread):

    def __init__(self):
        global appiumPath
        threading.Thread.__init__(self)
        self.appiumPath = readConfigLocal.getConfigValue("appiumPath")

    def run(self):

        log.outputLogFile("start appium server")
        rootDirectory = self.appiumPath[:2]
        startCMD = "node node_modules\\appium\\bin\\appium.js"

        #cd root directory ;cd appiuu path; start server
        os.system(rootDirectory+"&"+"cd "+self.appiumPath+"&"+startCMD)

# ========================================================
# Summary        :Alltest
# Author         :tong shan
# Create Date    :2015-10-10
# Amend History  :
# Amended by     :
# ========================================================
class Alltest(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        global casePath, caseListLpath, caseList, suiteList, appiumPath
        self.caseListPath = readConfig.logDir+"\\caseList.txt"
        self.casePath = readConfig.logDir+"\\testSet\\"
        self.caseList = []
        self.suiteList = []
        self.appiumPath = readConfigLocal.getConfigValue("appiumPath")

# =================================================================
# Function Name   : driverOn
# Function        : open the driver
# Input Parameters: -
# Return Value    : -
# =================================================================
    def driverOn(self):
        myDriver.GetDriver()

# =================================================================
# Function Name   : driverOff
# Function        : colse the driver
# Input Parameters: -
# Return Value    : -
# =================================================================
    def driverOff(self):
        myDriver.GetDriver().quit()

# =================================================================
# Function Name   : setCaseList
# Function        : read caseList.txt and set caseList
# Input Parameters: -
# Return Value    : -
# =================================================================
    def setCaseList(self):

        print(self.caseListPath)

        fp = open(self.caseListPath)

        for data in fp.readlines():

            sData = str(data)
            if sData != '' and not sData.startswith("#"):
                self.caseList.append(sData)

# =================================================================
# Function Name   : createSuite
# Function        : get testCase in caseList
# Input Parameters: -
# Return Value    : testSuite
# =================================================================
    def createSuite(self):

        self.setCaseList()
        testSuite = unittest.TestSuite()

        if len(self.caseList) > 0:

            for caseName in self.caseList:

                discover = unittest.defaultTestLoader.discover(self.casePath, pattern=caseName+'.py', top_level_dir=None)
                self.suiteList.append(discover)

        if len(self.suiteList) > 0:

            for test_suite in self.suiteList:
                for casename in test_suite:
                    testSuite.addTest(casename)
        else:
            return None

        return testSuite

# =================================================================
# Function Name   : runTest
# Function        : run test
# Input Parameters: -
# Return Value    : -
# =================================================================
    def run(self):

        try:


            while not isStartServer():
                mylock.acquire()
                sleep(1)
                log.outputLogFile("wait 1s to start appium server")
                mylock.release()
            else:
                log.outputLogFile("start appium server success")
                suit = self.createSuite()
                if suit != None:

                    log.outputLogFile("open Driver")
                    self.driverOn()
                    log.outputLogFile("Start to test")
                    unittest.TextTestRunner(verbosity=2).run(suit)
                    log.outputLogFile("end to test")
                    log.outputLogFile("close to Driver")
                    self.driverOff()

                else:
                    log.outputLogFile("Have no test to run")
        except Exception as ex:
            log.outputError(myDriver.GetDriver(), str(ex))

def isStartServer():

    try:
        driver = myDriver.GetDriver()
        if driver == None:
            return False
        else:
            return True
    except WebDriverException:
        raise


if __name__ == '__main__':

    thread1 = myServer()
    thread2 = Alltest()

    thread2.start()
    thread1.start()

    while thread2.is_alive():
        sleep(10)#"allTest is alive,sleep10"
    else:
        #kill myServer
        os.system('taskkill /f /im node.exe')
        log.outputLogFile("stop appium server")
