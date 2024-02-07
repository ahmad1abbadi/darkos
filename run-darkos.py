import os, time, subprocess
exec(open('/data/data/com.termux/files/usr/glibc/opt/darcos.conf').read())
exec(open('/data/data/com.termux/files/usr/glibc/opt/DXVK_D8VK_HUD.conf').read())
os.system("clear")
res = input("Write need resolution: ")
if res == "":
print("Empty resolution!")
os.system("python3 $PREFIX/bin/start-box64.py")
exit()
os.system("clear")
print("exit type 1")
os.system("taskset -c 4-7 box64 wine explorer /desktop=shell," + res + " $PREFIX/glibc/opt/7-Zip/7zFM &>/dev/null &")
