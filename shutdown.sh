#!/data/data/com.termux/files/usr/bin/bash

export PATH=/data/data/com.termux/files/usr/bin
unset LD_LIBRARY_PATH

sleep 1
box64 wineserver -k &>/dev/null
pkill -f "app_process / com.termux.x11"
pkill -f pulseaudio
sleep 1

exit 
