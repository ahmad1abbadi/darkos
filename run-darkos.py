import os
import re
import subprocess
import time
import threading
import shutil
import sys, urllib.request, urllib.error
search_paths = [
    "/data/data/com.termux/files/usr/glibc/opt/wine/4",
    "/data/data/com.termux/files/usr/glibc/opt/wine/2",
    "/data/data/com.termux/files/usr/glibc/opt/wine/3"
]
def extract_and_delete_tar_files():
    for path in search_paths:
        for filename in os.listdir(path):
            if filename.endswith(".tar"):
                tar_file = os.path.join(path, filename)
                if os.path.exists(os.path.join(path, ".wine")):
                    shutil.rmtree(os.path.join(path, ".wine"))
                if os.path.exists(os.path.join(path, "wine")):
                    shutil.rmtree(os.path.join(path, "wine"))
                subprocess.run(["tar", "-xf", tar_file, "-C", path])
                os.remove(tar_file)
extract_and_delete_tar_files()                
conf_path = "/data/data/com.termux/files/usr/glibc/opt/wine/os.conf"
conf_res = "/data/data/com.termux/files/usr/glibc/opt/darkos/res.conf"
exec(open(conf_path).read())
exec(open(conf_res).read())
exec(open('/sdcard/darkos/darkos_dynarec.conf').read())
exec(open('/sdcard/darkos/darkos_dynarec_box86.conf').read())
exec(open('/sdcard/darkos/darkos_custom.conf').read())
os.system("chmod +x $PREFIX/glibc/bin/box86")
os.system("chmod +x $PREFIX/glibc/bin/box64")

### AZ DARK 
if not os.path.exists(wine_prefix):
    if not os.path.exists(f"/data/data/com.termux/files/usr/glibc/opt/wine/{container}/wine/bin/wine64"):
        os.system(f"ln -sf /data/data/com.termux/files/usr/glibc/opt/wine/{container}/wine/bin/wine $PREFIX/glibc/bin/wine64")
        os.system(f"ln -sf /data/data/com.termux/files/usr/glibc/opt/wine/{container}/wine/bin/wine $PREFIX/glibc/opt/wine/{container}/wine/bin/wine64")
    print("Creating wine prefix 💫")
    os.system(f'WINEDLLOVERRIDES="mscoree=disabled" taskset -c 4-7 box64 wine64 wineboot -u &>/dev/null')
    os.system(f'cp -r $PREFIX/glibc/opt/Startxmenu/* "{wine_prefix}/drive_c/ProgramData/Microsoft/Windows/Start Menu"')
    os.system(f'rm "{wine_prefix}/dosdevices/z:"')
    os.system(f'ln -s /sdcard/Download "{wine_prefix}/dosdevices/o:" &>/dev/null')
    os.system(f'ln -s /sdcard/darkos "{wine_prefix}/dosdevices/e:" &>/dev/null')
    os.system(f'ln -s /data/data/com.termux/files "{wine_prefix}/dosdevices/z:"')
    print("Installing OS stuff...")
    os.system(f'box64 wine64 "$PREFIX/glibc/opt/apps/Install OS stuff.bat" &>/dev/null')
    print("Done!")
    print("prefix done enjoy 🤪 ")
    time.sleep(3)
    os.system("box64 wineserver -k &>/dev/null")
    os.system("python3 $PREFIX/bin/run-darkos.py") 

if res == "auto":
    xrandr_output = os.popen('xrandr').read()
    current_resolution_match = re.search(r'current\s+(\d+) x (\d+)', xrandr_output)
    if current_resolution_match:
        current_resolution = f"{current_resolution_match.group(1)}x{current_resolution_match.group(2)}"
    else:
        current_resolution = "800x600"
    res = current_resolution
os.system("taskset -c 4-7 box64 wine64 explorer /desktop=shell," + res + " $PREFIX/glibc/opt/apps/DARKOS_configuration.exe &>/dev/null &")
os.system("am start -n com.termux.x11/com.termux.x11.MainActivity &>/dev/null")
os.system("clear")
os.system("python3 $PREFIX/bin/photo.py")
print("")
print("DARK OS is running......")
print("")
print("to SHUTDOWN.. it Press 1 or anything else to REBOOT..")

def restart_wine():
    while True:
        file_path = "/data/data/com.termux/files/usr/glibc/opt/darkos/file.reboot"
        while os.path.exists(file_path):
            time.sleep(1) 
        os.system("box64 wineserver -k &>/dev/null")
        print("Restarting WINE")
        os.system(f"touch {file_path}")
        os.system("python3 $PREFIX/bin/run-darkos.py") 
def update_wine():
    while True:
        file_path = "/data/data/com.termux/files/usr/glibc/opt/darkos/file.update"
        while os.path.exists(file_path):
            time.sleep(1)
        os.system("box64 wineserver -k &>/dev/null")
        print("Restarting WINE")
        os.system(f"touch {file_path}")
        os.system("python3 $PREFIX/bin/update-darkos.py")  
def shutdown_wine():
    while True:
        file_path = "/data/data/com.termux/files/usr/glibc/opt/darkos/file.shutdown"
        while os.path.exists(file_path):
            time.sleep(1) 
        os.system("box64 wineserver -k")
        os.system('pkill -f "app_process / com.termux.x11"')
        os.system('pkill -f pulseaudio')
        print("shutdown........")
        os.system(f"touch {file_path}")
        os.system("am startservice -a com.termux.service_stop com.termux/.app.TermuxService")
def debug_wine():
    while True:
        file_path = "/data/data/com.termux/files/usr/glibc/opt/darkos/file.debug"
        while os.path.exists(file_path):
            time.sleep(1) 
        os.system("box64 wineserver -k &>/dev/null")
        print("Restarting WINE")
        os.system(f"touch {file_path}")
        os.system("python3 $PREFIX/bin/debug-darkos.py")
def settings_wine():
    while True:
        file_path = "/data/data/com.termux/files/usr/glibc/opt/darkos/file.setting"
        while os.path.exists(file_path):
            time.sleep(1) 
        os.system("box64 wineserver -k &>/dev/null")
        print("Restarting WINE")
        os.system(f"touch {file_path}")
        os.system("chmod +x /data/data/com.termux/files/usr/bin/install.sh")
        os.system("am start -n com.termux/.app.TermuxActivity &>/dev/null")
        subprocess.run(["bash", "install.sh"])
        time.sleep(1)
        os.system("python3 $PREFIX/bin/run-darkos.py") 
def stop_wine():
    stop = input()
    if stop != "1":
        print("")
        print("Rebooting.........")
        os.system("box64 wineserver -k &>/dev/null")
        time.sleep(1)
        os.system("python3 $PREFIX/bin/run-darkos.py")
    elif stop == "1":
        os.system("box64 wineserver -k")
        os.system('pkill -f "app_process / com.termux.x11"')
        os.system('pkill -f pulseaudio')
        print("shutdown........")
        time.sleep(1)
        os.system("am startservice -a com.termux.service_stop com.termux/.app.TermuxService")
        
        
thread1 = threading.Thread(target=restart_wine)
thread2 = threading.Thread(target=stop_wine)
thread3 = threading.Thread(target=update_wine)
thread4 = threading.Thread(target=settings_wine)
thread5 = threading.Thread(target=debug_wine)
thread6 = threading.Thread(target=shutdown_wine)

thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()


thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()
thread6.join()
