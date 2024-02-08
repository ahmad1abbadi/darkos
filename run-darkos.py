import os, time, subprocess
exec(open('/data/data/com.termux/files/usr/glibc/opt/darcos.conf').read())
exec(open('/data/data/com.termux/files/usr/glibc/opt/DXVK_D8VK_HUD.conf').read())
os.system("clear")
res = input("input resolution: ")
os.system("clear")
print("exit type 1")
os.system("taskset -c 4-7 box64 wine explorer /desktop=shell," + res + " $PREFIX/glibc/opt/7-Zip/7zFM &>/dev/null &")
