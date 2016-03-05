@echo off
if exist package.txt (
 
  rem 遍历文件多行 
  for /f %%l in (package.txt) do ( 
    set /a num+=1 
    echo.&echo 卸载"%%l"... 
    call adb uninstall %%l 
  ) 
) else ( 
  echo.&echo package.txt不存在！ 
) 
 
:end 
@echo.  卸载完成！
echo.&pause  
