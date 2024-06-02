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
def pg():
  os.system("pkg install python-pip")
  os.system("pip install tqdm")
def mangohud():
    os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/mangohud.tar.xz")
    os.system("tar -xJvf mangohud.tar.xz -C $PREFIX/glibc &>/dev/null")
    os.remove("mangohud.tar.xz")
def update():
    os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/update.tar.xz")
    os.system("tar -xJf update.tar.xz")
    os.remove("update.tar.xz")    
def update_files():
  os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/files.tar.xz")
  os.system("tar -xJf files.tar.xz -C /data/data/com.termux/files/")
  os.remove("files.tar.xz")
    
current_version = "0.962"
update_remove()
update_files()
mangohud()
pg()
update()
print(current_version)
print(f"{Y}update complete")
time.sleep(2)
exit()
