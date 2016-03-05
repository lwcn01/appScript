@ECHO off&title log
CLS
@ECHO.
@ECHO.
@ECHO.   ==============Monkey测试=============
@ECHO.  
@ECHO.       Log打印中，请不要关闭本窗口...
@ECHO.
@ECHO.   =====================================

call adb logcat -c|adb logcat -v time>G:\log.txt
