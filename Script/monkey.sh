#!/system/bin/sh
c_log(){
logcat -c
logcat -v time >$log_f &
check_error=$!
}
output_error(){
if [ -f $1 ];then
    local times1=`grep -c "ANR in" $1`
    anr=$((anr+times1))
    local times2=`grep -c "FATAL EXCEPTION" $1`
    fatal=$((fatal+times2))
    local times3=`grep -c "Build fingerprint" $1`
    fingerprint=$((fingerprint+times3))
    local result="type:"
    if [ $times1 -ne 0 ];then
        result=$result"ANR;"
    fi
    if [ $times2 -ne 0 ];then
        result=$result"FATAL EXCEPTION;"
    fi
    if [ $times3 -ne 0 ];then
        result=$result"Build fingerprint;"
    fi
    if [ $times1 -ne 0 -o $times2 -ne 0 -o $times3 -ne 0 ];then
        if [ ! -d $testresult/log ];then
            mkdir $testresult/log
        fi
        local time_name="`date +%Y%m%d%H%M%S`"
        busybox mv $1 $testresult/log/$mac_$time_name.log
        su -c dmesg >$testresult/log/$mac_$time_name.dmesg
        busybox top -b -n 1 >$testresult/log/$mac_$time_name.top
        procrank >$testresult/log/$mac_$time_name.procrank
        su -c screencap $testresult/log/$mac_$time_name.png
        comment "$result" "$mac_$time_name.log"
    fi
fi
}

comment(){
if [ ! -f $testresult/comments.csv ];then
    echo "Date,Error Type,Log Name" >$testresult/comments.csv
fi
echo "`date +%m-%d" "%H":"%M":"%S`,$1,$2" >>$testresult/comments.csv
}

#Global variables
anr=0
fatal=0
fingerprint=0
log_f="/sdcard/check_error.log"
testresult="$EXTERNAL_STORAGE/monkey"
if [ -d $testresult ];then
    rm -rf $testresult
fi
mkdir $testresult
mac=`cat /sys/class/net/*/address|busybox sed -n '1p'|busybox tr -d ':'`
build=`getprop ro.build.fingerprint`
if [ -z $build ];then
    build=`getprop ro.build.description`
fi

#等待monkey进程执行完毕函数
waitmonkey(){
local a=0
while [ $a != 1 ];do
    local a=`/system/bin/ps |grep -c "monkey"`
done
while [ $a != 0 ];do
    c_log
    local a=`/system/bin/ps |grep -c "monkey"`
    sleep 10
    kill $check_error
    output_error $log_f
    echo -e "local mac=$mac
build id=$build
ANR=$anr
Fatal=$fatal
tombstone=$fingerprint" >$testresult/statistics.txt
done
}
su -c busybox pkill monkey
#以下为monkey脚本逻辑
monkey -p com.media.tv --throttle 1500 --ignore-crashes --monitor-native-crashes --ignore-security-exceptions --ignore-timeouts --ignore-native-crashes --pct-syskeys 10 --pct-nav 50 --pct-majornav 30 --pct-anyevent 10 -v -v -v 2400 >>$testresult/monkey.log &
waitmonkey
sleep 10
monkey -p com.stv.launcher --throttle 1500 --ignore-crashes --monitor-native-crashes --ignore-security-exceptions --ignore-timeouts --ignore-native-crashes --pct-syskeys 10 --pct-nav 50 --pct-majornav 30 --pct-anyevent 10 -v -v -v 2400 >>$testresult/monkey.log &
waitmonkey
sleep 10
monkey -p com.guoguang.tvos.appstore --throttle 1500 --ignore-crashes --monitor-native-crashes --ignore-security-exceptions --ignore-timeouts --ignore-native-crashes --pct-syskeys 10 --pct-nav 50 --pct-majornav 30 --pct-anyevent 10 -v -v -v 2400 >>$testresult/monkey.log &
waitmonkey
sleep 10
monkey -p com.stv.tvos.gamecenter --throttle 1500 --ignore-crashes --monitor-native-crashes --ignore-security-exceptions --ignore-timeouts --ignore-native-crashes --pct-syskeys 10 --pct-nav 50 --pct-majornav 30 --pct-anyevent 10 -v -v -v 2400 >>$testresult/monkey.log &
waitmonkey
sleep 10
monkey -p com.media.tv -p com.stv.launcher -p com.guoguang.tvos.appstore -p com.stv.tvos.gamecenter --throttle 1500 --ignore-crashes --monitor-native-crashes --ignore-security-exceptions --ignore-timeouts --ignore-native-crashes --pct-syskeys 10 --pct-nav 50 --pct-majornav 30 --pct-anyevent 10 -v -v -v 14400 >>$testresult/monkey.log &
waitmonkey
