#!/bin/bash

echo "OR-Monitor started"
PROCESS_NUM=$(ps -ef | grep "python3 `dirname "$0"`/WebChangeNotify.py" | grep -v `basename $0` | grep -v "grep" | wc -l)
ts=`date +%T`

if [ $PROCESS_NUM -gt 0 ]; then
        echo "$ts: Process is running"
else
        echo "$ts: Process is not running. Starting..."
        python3 "`dirname "$0"`/WebChangeNotify.py" &

fi