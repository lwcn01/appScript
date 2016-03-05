@ECHO off&title monkey
@ECHO.
@ECHO.   Monkey测试前，请先打开log.bat文件...
ECHO.&pause
CLS

@ECHO.
@ECHO.
@ECHO.   ==============Monkey测试=============
@ECHO.  
@ECHO.       开始测试，请不要关闭本窗口...
@ECHO.
@ECHO.   =====================================
@ECHO.
set /p packagename=请输入APK包名：
set /p a=请输入Monkey测试次数：
adb shell monkey -p org.coolx.htvlauncher -v %a%

for /f "tokens=2" %%i in (
  'tasklist/v^|find/i "cmd.exe"^|find/i /v "monkey"'
)do taskkill/pid %%i>nul 2>nul


@ECHO.   ==============测试结束===============
@ECHO.   %errorlevel%
@ECHO.   Log文件已写入G盘log.txt
ECHO.&pause


