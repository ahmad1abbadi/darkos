import os, time, shutil, sys, subprocess, urllib.request, urllib.error, fnmatch

R = "\033[1;31m"
G = "\033[1;32m"
Y = "\033[1;33m"
B = "\033[1;34m"
C = "\033[1;36m"
W = "\033[1;37m"
BOLD = "\033[1m"

file_path = "/data/data/com.termux/files/usr/glibc/opt/box/V2.7( 11 may).tar.xz"
def update_remove():
  if os.path.exists(file_path):
          os.remove(file_path)
    
def update_alsa():
  os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/alsa.tar.xz")
  os.system("tar -xJf alsa.tar.xz -C /data/data/com.termux/files/")
  os.remove("alsa.tar.xz")
    
def update_files():
  os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/files.tar.xz")
  os.system("tar -xJf files.tar.xz -C /data/data/com.termux/files/")
  os.remove("files.tar.xz")
    
current_version = "0.96"
update_remove()
update_files()
print(current_version)
print(f"{Y}update complete")
time.sleep(2)
exit()
