import os, time, shutil, sys, subprocess, urllib.request, urllib.error, fnmatch

R = "\033[1;31m"
G = "\033[1;32m"
Y = "\033[1;33m"
B = "\033[1;34m"
C = "\033[1;36m"
W = "\033[1;37m"
BOLD = "\033[1m"

current_version = "0.962"
url = 'https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/currently%20version.txt'
def remove():
    folder_path = '/data/data/com.termux/files/home'
    for filename in os.listdir(folder_path):
        if fnmatch.fnmatch(filename, '*.tar.xz*'):
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)
            print(f'{filename} has been deleted.')
os.system("am start -n com.termux/.HomeActivity")
os.system("clear")
os.system("python3 $PREFIX/bin/photo.py")
time.sleep(2)   
print("")
print(f"{R}[{W}-{R}]{G}{BOLD} Shutdown OS.... {W}")
print("")
print(f"{R}[{W}-{R}]{G}{BOLD} checking 🔎..... {W}")
time.sleep(1)
response = urllib.request.urlopen(url)
latest_version = response.read().decode('utf-8').strip()
try:
  if latest_version > current_version:
    print(f"{R}[{W}-{R}]{G}{BOLD} update available..... {C}updating......📥 {W}")
    os.system("rm $PREFIX/bin/darkos.py")
    os.system("rm $PREFIX/bin/update-darkos.py")
    os.system("rm $PREFIX/bin/run-darkos.py")
    os.system("rm $PREFIX/bin/debug-darkos.py")
    os.system("rm $PREFIX/bin/setting-darkos.py")
    os.system("rm $PREFIX/bin/darkos")
    os.system("wget -O run-darkos.py https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/run-darkos.py")
    os.system("wget -O darkos.py https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/darkos.py")
    os.system("wget -O darkos https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/darkos")
    os.system("wget -O debug-darkos.py https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/debug-darkos.py")
    os.system("wget -O setting-darkos.py https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/setting-darkos.py")
    os.system("wget -O update-darkos.py https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/update-darkos.py")
    os.system("wget -O new-update.py https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/new-update.py")
    os.system("chmod +x darkos")
    os.system("mv update-darkos.py darkos.py run-darkos.py debug-darkos.py setting-darkos.py darkos $PREFIX/bin/")
    os.system("python3 new-update.py")
    time.sleep(2)
    remove()
    os.system("rm new-update.py")
    print(f"{R}[{W}-{R}]{G}{BOLD} update completed 🎉 {W}")
    print(f"{G}{BOLD} rebooting.... {W}")
    time.sleep(3)
except urllib.error.HTTPError as e:
  if e.code == 404:
    print(f"{R} no internet connection 😵 {C}rebooting..... {W}")
    time.sleep(2)
  else:
    os.system("rm $PREFIX/bin/darkos.py")
    os.system("wget -O darkos.py https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/darkos.py")
    os.system("mv darkos.py")
    print(f"{C} no update available {W}")
    time.sleep(3)
os.system("python3 $PREFIX/bin/run-darkos.py")
