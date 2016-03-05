set process=cn.microinvestment.weitou
@adb sehll dumpsys meminfo %process% | findstr "Pss"
:m
@adb sehll dumpsys meminfo %process% | findstr "TOTAL"
@ping -n 5 127.1>nul
@goto m