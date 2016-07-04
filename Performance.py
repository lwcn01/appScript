#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Date    : 2016-07-01
@Author  : new
'''
import os,re
import time
import subprocess

PATH = lambda p: os.path.abspath(p)

def shell(args):
    """
    :Args:
    - args - shell command
    :Usage:
        Adb.shell('command')
    """
    cmd = "%s shell %s" % ('adb' , str(args))
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def BatteryCapacity():
    """
    电池电量
    """
    capacity = shell("dumpsys battery | %s level" %find).stdout.read().decode('utf-8')
    return int(capacity.split(':')[-1])

def BatteryTemp():
    """
    电池温度
    """
    temperature = shell("dumpsys battery | %s temperature" %find).stdout.read().decode('utf-8')

    return int(temperature.split(':')[-1]) / 10.0

def BatteryStatus():
    '''
    电池充电状态
    BATTERY_STATUS_UNKNOWN：未知状态
    BATTERY_STATUS_CHARGING: 充电状态
    BATTERY_STATUS_DISCHARGING: 放电状态
    BATTERY_STATUS_NOT_CHARGING：未充电
    BATTERY_STATUS_FULL: 充电已满
    '''
    status = {1 : "BATTERY_STATUS_UNKNOWN",
              2 : "BATTERY_STATUS_CHARGING",
              3 : "BATTERY_STATUS_DISCHARGING",
              4 : "BATTERY_STATUS_NOT_CHARGING",
              5 : "BATTERY_STATUS_FULL"}
    batterystatus = shell("dumpsys battery | %s status" %find).stdout.read().decode('utf-8')
    return status[int(batterystatus.split(':')[-1])]

def DisplaySize():
    """
    屏幕分辨率
    """
    display = shell("dumpsys display | %s PhysicalDisplayInfo" %find).stdout.read().decode('utf-8')
    size = re.findall(r"\d+",display)
    return int(size[0]), int(size[1])

def CurrentAppInfo():
    pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
    output = shell("dumpsys window w | %s \/ | %s name=" %(find, find)).stdout.read()
    PackageName = pattern.findall(str(output))[0].split("/")[0]
    Activity = pattern.findall(str(output))[0].split("/")[1]
    return PackageName,Activity

def Top(times):
    """
    cpu占用率
    memeroy占用率RSS 单位KB
    """
    cpu = []
    mem = []
    Info = shell("top -n %s | %s %s$" %(int(times), find, CurrentAppInfo()[0])).stdout.readlines()
    for i in Info:
        j = i.decode('utf-8').split()
        cpu.append(j[2])
        mem.append(j[6])
    return cpu,mem

def CpuInfo():
    """
    应用CPU
    """
    output1 = shell("dumpsys cpuinfo %s" %(app[0])).stdout.read().decode('utf-8').strip()
    for data in output1.splitlines():
        if "TOTAL" in data:
            cpu_info = data
            break
    return cpu_info.split()[0]

def CpuFreq():
    """
    cpuinfo_min_freq : CPU最小频率
    cpuinfo_max_freq : CPU最大频率
    scaling_cur_freq : CPU当前频率
    scaling_available_frequencies : CPU可选工作频率范围
    """
    freq = {1 : "cpuinfo_min_freq",
            2 : "cpuinfo_max_freq",
            3 : "scaling_cur_freq",
            4 : "scaling_available_frequencies"}
    f = []
    for values in freq.values():
        cmd = "cat /sys/devices/system/cpu/cpu0/cpufreq/"
        info = shell(cmd + values).stdout.read().decode('utf-8').strip()
        f.append(info)
    cpu_freq = dict(zip([1,2,3,4],f))
    return cpu_freq

def CpuTemp():
    """
    CPU温度
    """
    for zone in ["thermal_zone0","thermal_zone1"]:
        cmd = "cat /sys/class/thermal/%s/temp" %zone
        cpu_temp = shell(cmd).stdout.read().decode('utf-8').strip().splitlines()
    return cpu_temp

def MemeroyPss():
    """
    应用内存 PSS 单位KB
    """
    #Dalvik Heap Size
    output2 = shell("dumpsys meminfo %s | %s Heap" %(app[0],find)).stdout.read().decode('utf-8').strip()
    mem_state = float(output2.splitlines()[-1].split()[6])/1024.0
    #PSS Total
    output3 = shell("dumpsys meminfo %s | %s TOTAL" %(app[0],find)).stdout.read().decode('utf-8').strip()
    MemPss = output3.split()[1]
    #单个应用程序最大内存限制
    output4 = shell("getprop dalvik.vm.heapgrowthlimit").stdout.read().decode('utf-8').strip()
    #应用启动后分配的初始内存
    output5 = shell("getprop dalvik.vm.heapstartsize").stdout.read().decode('utf-8').strip()
    #单个java虚拟机最大的内存限制
    output6 = shell("getprop dalvik.vm.heapsize").stdout.read().decode('utf-8').strip()
    if mem_state > float(output4.replace('m','')):

        return False

    return MemPss

def MemeroyUss():
    """
    VSS- Virtual Set Size 虚拟耗用内存（包含共享库占用的内存）
    RSS- Resident Set Size 实际使用物理内存（包含共享库占用的内存）
    PSS- Proportional Set Size 实际使用的物理内存（比例分配共享库占用的内存）
    USS- Unique Set Size 进程独自占用的物理内存（不包含共享库占用的内存）
    """
    #Dalvik Heap Size
    mem_data = shell("procrank | %s %s" %(find,app[0])).stdout.read().decode('utf-8').strip()
    MemUss = mem_data.split()[4]
    #单位 KB
    return MemUss

def DataTraffic():
    """
    数据流量 单位MB
    """
    uid = shell("dumpsys package %s | %s userId=" %(app[0],find)).stdout.read().decode('utf-8').strip()
    uid = int(re.split("[= ]",uid)[1])
    rx = [] # 接收
    tx = [] # 发送
    try:
        shell("cat /proc/net/xt_qtaguid/stats")
    except Exception as e:
        return print(e)
    else:
        net_status = shell("cat /proc/net/xt_qtaguid/stats | {0} {1}".format(find,uid)).stdout.read().decode('utf-8').strip()
        for item in net_status.splitlines():
            if len(item) != 0:
                rx_bytes = item.split()[5] # 接收网络数据流量
                tx_bytes = item.split()[7] # 发送网络数据流量
                rx.append(int(rx_bytes))
                tx.append(int(tx_bytes))
        total_data_traffic = round(((sum(rx) + sum(tx))/1024.0/1024.0),4)  #四舍五入求值，单位兆字节：MB

        return total_data_traffic

def StartUpTime():
    """
    启动时间 单位ms
    """
    shell("am force-stop %s" %app[0])
    time.sleep(2)
    try:
        info = shell("am start -W -n %s/%s" %(app[0],app[1])).stdout.read().decode('utf-8').strip()
        time.sleep(2)
    except Exception as e:
        return e
    else:
        TakeTime = {}
        for i in info.splitlines():
            if i != '':
                if ":" in i:
                    TakeTime.setdefault(i.split(":")[0],i.split(":")[1])
        try:
            TakeTime["TotalTime"]
        except:
            return TakeTime
        else:
            return TakeTime["TotalTime"]

def StartTime():
    """
    启动时间 单位ms
    """
    shell("pm clear {}".format(app[0]))
    shell("input keyevent 3").wait()
    shell("monkey -p {} -c android.intent.category.LAUNCHER 1".format(app[0]))
    try:
        start_time_info = shell("cat /proc/timer_list").stdout.read().decode('utf-8').strip().splitlines()
        while '' in start_time_info:
            start_time_info.remove('')
        start_time = float(start_time_info[2].split()[2])/1000000
    except:
        return
    else:
        end_time_info= shell("cat /proc/timer_list").stdout.read().decode('utf-8').strip().splitlines()
        while '' in end_time_info:
            end_time_info.remove('')
        end_time = float(end_time_info[2].split()[2])/1000000 
        took_time = end_time - start_time
        time.sleep(2)
        shell("am force-stop {}".format(app[0]))
        
        return took_time

def Fps():
    fps_data = shell("dumpsys SurfaceFlinger --latency %s/%s" %(app[0],app[1])).stdout.read().decode('utf-8').strip()
    print(fps_data)

def FpsGfx():
    """
    打开设备开发者选项 ==> GPU呈现模式分析 ==> 勾选adb shell dumpsys gfxinfo
    Draw ：消耗在构建java显示列表的时间
    Process ：消耗在Android的2D渲染器执行显示列表的时间。视图层次越多，要执行的绘图命令就越多
    Execute ：消耗在排列每个发送过来的帧的顺序的时间.这部分的图通常是很小的
    为了达到 60 fps，每帧所花费的时间不应超过 16ms
    """
    gfx_info = shell("dumpsys gfxinfo {}".format(app[0])).stdout.read().decode('utf-8').strip()
    for i in range(len(gfx_info.splitlines())):
        if "Profile data in ms" in gfx_info.splitlines()[i]:
            info = gfx_info.splitlines()[i:]
            for j in range(len(info)):
                if "View hierarchy" in info[j]:
                    results = info[:j]
                    while '' in results:
                        results.remove('')
    frame_time = []
    try:
        results = results[3:]
    except RuntimeError:
        return False
    else:
        for result in results:
            #每一帧三列数据：Draw  Process  Execute
            time = float(result.split()[0]) + float(result.split()[1]) + float(result.split()[2])
            #单位 ms
            frame_time.append(time)
    #1000ms / 消耗时间 = 每秒帧数
    try:
        FPS = 1000/sum(frame_time)
    except ZeroDivisionError:
        return
    else:
        return FPS

if __name__ == '__main__':
    if os.name == 'nt':
        find = 'findstr'
    else:
        find = 'grep'
    if os.popen('adb get-state').read().strip() != 'device':
        print('CheckOut ADB')
    else:
        global app
        app = CurrentAppInfo()
        desktop = os.path.expanduser('~') + '\Desktop'
        root_dir = desktop + "\\" + 'log'
        if not os.path.exists(root_dir):
            mkdir(root_dir)
        f = open(PATH(os.path.join(root_dir,'test.csv')),'w')
        capacity = BatteryCapacity()
        f.write("电池电量：{}\n".format(capacity))
        batterytemp = BatteryTemp()
        f.write("电池温度：{}\n".format(batterytemp))
        batterystate = BatteryStatus()
        f.write("电池充电状态：{}\n".format(batterystate))
        display = DisplaySize()
        f.write("屏幕分辨率：{}\n".format(display))
        cpufreq = CpuFreq()
        f.write("CPU最小频率：{}\n".format(cpufreq[1]))
        f.write("CPU最大频率：{}\n".format(cpufreq[2]))
        f.write("CPU当前频率：{}\n".format(cpufreq[3]))
        f.write("CPU可选工作频率：{}\n".format(cpufreq[4]))
        cputemp = CpuTemp()
        f.write("CPU温度：{}\n".format(cputemp))
        top = Top(3)
        f.write("========{}========\n".format(app[0]))
        f.write("应用CPU占用率：{}\n".format(top[0]))
        f.write("应用MemRss占用率：{}\n".format(top[1]))
        cpu = CpuInfo()
        f.write("应用CPU占用率：{}\n".format(cpu))
        mempss = MemeroyPss()
        f.write("应用MemPss占用率：{} KB\n".format(mempss))
        try:
            memuss = MemeroyUss()
        except:
            f.write("应用MemUss占用率：Error\n")
        else:
            f.write("应用MemUss占用率：{} KB\n".format(memuss))
        data = DataTraffic()
        f.write("应用数据流量：{} MB\n".format(data))  
        timef = StartUpTime()
        f.write("应用启动时间：{} ms\n".format(timef))
        time.sleep(3)
        timep = StartTime()
        f.write("应用启动时间：{} ms\n".format(timep))
        time.sleep(3)
        shell("am start -n %s/%s" %(app[0],app[1])).wait()
        time.sleep(3)
        try:
            fps = FpsGfx()
        except:
            f.write("应用刷新帧率：Error\n")
        else:
            f.write("应用刷新帧率：{} fps\n".format(fps))
        f.close()