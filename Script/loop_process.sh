#!/bin/bash

EXE_PATH="/root/scrapy/tutorial"
PROCESS="python"
EXE="epg_router.py"
LOGFILE=""

CHECK="ps aux | grep $EXE | grep -v grep | awk '{print $2}'"

function check()
{
	cmd="ps aux | grep $EXE | grep -v grep"
	res=$(eval $cmd)
	#echo $res
	if [ "$res" == "" ]; then
		return 0
	else
		tmp=$(echo "$res" | awk '{print $2}')
		echo $tmp
		return 1
	fi
}

function log()
{
	echo $1
	text="[loop] [`date`] $1"
	if [ "$LOGFILE" == "" ]; then
		echo $text
	else
		echo $text >> "$LOGFILE"
	fi
}


while true
do
	#pid=$(eval $CHECK)
	pid=$(check)
	echo "pid = $pid"
	
	if [ "$pid" == "" ]; then
		#cd $EXE_PATH
		echo "enter here.."
		cd `pwd`/tutorial
		nohup $PROCESS $EXE > /dev/null 2>&1 &
		sleep 1
		pid=$(check)
		echo "pid = $pid"
		if [ "$pid" == "" ]; then
			log "$EXE start error!"
			exit 1
		else
			log "$EXE start runing..."
		fi
	fi
	sleep 10
done
exit 0
