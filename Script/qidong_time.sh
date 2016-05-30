#! /bin/bash
adb shell pm clear xxx # 打开注释，可以计算第一次打开的情况。
adb shell input keyevent 3
adb shell am start com.xxx.xxx.LauncherActivity
start_time=`adb shell cat /proc/timer_list | awk 'NR==3{printf("%.0f",$3/1000000)}'`
while true
do
# activity=`adb shell dumpsys SurfaceFlinger | grep "| xxxx"` # 登录界面

if [ $? = "0" ]; then
    echo $activity
    break
fi

done
end_time=`adb shell cat /proc/timer_list | awk 'NR==3{printf("%.0f",$3/1000000)}'`
# echo $start_time, $end_time, $((end_time-start_time)) >> test.csv
echo $((end_time-start_time)) >> test.csv
sleep 1
adb shell am force-stop xxx
