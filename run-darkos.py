import os
import re
import subprocess
import time
import threading
import shutil
import sys, urllib.request, urllib.error


R = "\033[1;31m"
G = "\033[1;32m"
Y = "\033[1;33m"
B = "\033[1;34m"
C = "\033[1;36m"
W = "\033[1;37m"
BOLD = "\033[1m"

def extract_and_delete_tar_files():
    search_paths = [
        "/data/data/com.termux/files/usr/glibc/opt/temp/box",
        "/data/data/com.termux/files/usr/glibc/opt/wine/5",
        "/data/data/com.termux/files/usr/glibc/opt/wine/4",
        "/data/data/com.termux/files/usr/glibc/opt/wine/2",
        "/data/data/com.termux/files/usr/glibc/opt/wine/3"
    ]
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
                if os.path.exists(os.path.join(path, "box64")):
                    destination_path = "/data/data/com.termux/files/usr/glibc/bin/box64"
                    if os.path.exists(destination_path):
                        os.remove(destination_path)
                    shutil.move(os.path.join(path, "box64"), destination_path)
                    time.sleep(1)
def load_conf():
    conf_paths = [
        "/data/data/com.termux/files/usr/glibc/opt/wine/os.conf",
        "/data/data/com.termux/files/usr/glibc/opt/darkos/res.conf",
        "/data/data/com.termux/files/usr/glibc/opt/darkos/language.conf",
        "/sdcard/darkos/darkos_dynarec.conf",
        "/sdcard/darkos/darkos_dynarec_box86.conf",
        "/sdcard/darkos/darkos_custom.conf",
        "/data/data/com.termux/files/usr/glibc/opt/scripts/hud-settings.conf"
    ]
    for conf_path in conf_paths:
        exec(open(conf_path).read(), globals())
    os.system("chmod +x $PREFIX/glibc/bin/box86")
    os.system("chmod +x $PREFIX/glibc/bin/box64")
def create_wine_prefix():
    if not os.path.exists(f"/data/data/com.termux/files/usr/glibc/opt/wine/{container}/wine/bin/wine64"):
        os.system(f"ln -sf /data/data/com.termux/files/usr/glibc/opt/wine/{container}/wine/bin/wine $PREFIX/glibc/bin/wine64")
        os.system(f"ln -sf /data/data/com.termux/files/usr/glibc/opt/wine/{container}/wine/bin/wine $PREFIX/glibc/opt/wine/{container}/wine/bin/wine64")
    print(f"{R}[{W}-{R}]{G}{BOLD} Creating wine prefix 💫 {W}")
    os.system(f'WINEDLLOVERRIDES="mscoree=disabled" taskset -c 4-7 box64 wine64 wineboot -u &>/dev/null')
    os.system(f'cp -r $PREFIX/glibc/opt/Startxmenu/* "{wine_prefix}/drive_c/ProgramData/Microsoft/Windows/Start Menu"')
    os.system(f'rm "{wine_prefix}/dosdevices/z:"')
    os.system(f'ln -s /sdcard/Download "{wine_prefix}/dosdevices/o:" &>/dev/null')
    os.system(f'ln -s /data/data/com.termux/files/usr/glibc/opt/G_drive "{wine_prefix}/dosdevices/g:" &>/dev/null')
    os.system(f'ln -s /sdcard/darkos "{wine_prefix}/dosdevices/e:" &>/dev/null')
    os.system(f'ln -s /data/data/com.termux/files "{wine_prefix}/dosdevices/z:"')
    print(f"{R}[{W}-{R}]{G}{BOLD} Installing OS stuff... {W}")
    os.system(f'box64 wine64 "$PREFIX/glibc/opt/apps/Install OS stuff.bat" &>/dev/null')
    if os.path.exists(f"/data/data/com.termux/files/usr/glibc/opt/wine/{container}/add-ons.bat"):
        os.system(f'box64 wine64 "$PREFIX/glibc/opt/wine/{container}/wine/add-ons.bat" &>/dev/null')
        print("add-ons installed")
        os.remove(f"/data/data/com.termux/files/usr/glibc/opt/wine/{container}/add-ons.bat")
    print(f"{R}[{W}-{R}]{G}{BOLD} Done! {W}")
    print(f"{G}{BOLD} prefix done enjoy 🤪 {W}")
    time.sleep(1)
    os.system("box64 wineserver -k &>/dev/null")
    print(f"{G}{BOLD} rebooting..... {W}")
    time.sleep(1)
    subprocess.run(["bash", "darkos"])
    exit()
def start_wine():
    os.system("$PREFIX/glibc/opt/scripts/termux-x11.sh displayResolutionMode:custom &>/dev/null &")
    os.system(f"$PREFIX/glibc/opt/scripts/termux-x11.sh displayResolutionCustom:{res} &>/dev/null &")
    os.system("box64 wine64 explorer /desktop=shell," + res + " $PREFIX/glibc/opt/apps/DARKOS_configuration.exe &>/dev/null &")
    os.system("am start -n com.termux.x11/com.termux.x11.MainActivity &>/dev/null")
    os.system("clear")
    os.system("python3 $PREFIX/bin/photo.py")
    print("")
    print(f" {R}{BOLD}D{G}{BOLD}A{Y}{BOLD}R{B}{W}{BOLD}K{R}{BOLD} O{C}{BOLD}S{G}{BOLD} is running...... {W}")
    print("")
    print(f"{G}{BOLD} Please choose an option: ")
    print("")
    print(f"{G}{BOLD} (1) for {C}SHUTDOWN{W}")
    print("")
    print(f"{G}{BOLD} (2) for exit to the {C}terminal{W}")
    print("")
    print(f"{G}{BOLD} Simply press any other key to {C}REBOOT{W}")
    print("")
def restart_wine():
    while True:
        file_path = "/data/data/com.termux/files/usr/glibc/opt/darkos/file.reboot"
        while os.path.exists(file_path):
            time.sleep(1) 
        os.system("box64 wineserver -k &>/dev/null")
        print(f"{G}{BOLD} Restarting WINE {W}")
        os.system("pkill -9 "\.exe$"")
        os.system(f"touch {file_path}")
        restart_program() 
def update_wine():
    while True:
        file_path = "/data/data/com.termux/files/usr/glibc/opt/darkos/file.update"
        while os.path.exists(file_path):
            time.sleep(1)
        os.system("box64 wineserver -k &>/dev/null")
        print(f"{G}{BOLD} Restarting WINE {W}")
        os.system(f"touch {file_path}")
        os.system("python3 $PREFIX/bin/update-darkos.py")
        exit()
        
def stop_virgl():
    while True:
        file_path = "/data/data/com.termux/files/usr/glibc/opt/darkos/file.stop-virgl"
        while os.path.exists(file_path):
            time.sleep(1)
        os.system(f"touch {file_path}")
        os.system("killall virgl_test_server")
        os.system("ln -sf /data/data/com.termux/files/usr/glibc/lib/libGL.so.1.7.0 /data/data/com.termux/files/usr/glibc/lib/libGL.so.1")
        unset_path = "/data/data/com.termux/files/usr/glibc/opt/scripts/unset.conf"
        exec(open(unset_path).read(), globals())
def start_virgl():
    while True:
        file_path = "/data/data/com.termux/files/usr/glibc/opt/darkos/file.start-virgl"
        while os.path.exists(file_path):
            time.sleep(1)
        os.system(f"touch {file_path}")
        unset_path = "/data/data/com.termux/files/usr/glibc/opt/scripts/unset.conf"
        exec(open(unset_path).read(), globals())
        time.sleep(2)
        virgl_path = "/data/data/com.termux/files/usr/glibc/opt/scripts/virgl-settings.conf"
        exec(open(virgl_path).read(), globals())
def reload_style():
    while True:
        file_path = "/data/data/com.termux/files/usr/glibc/opt/darkos/file.style"
        while os.path.exists(file_path):
            time.sleep(1)
        os.system(f"touch {file_path}")  
        os.system("python3 $PREFIX/glibc/opt/scripts/theme-changer.py")
def shutdown_wine():
    while True:
        file_path = "/data/data/com.termux/files/usr/glibc/opt/darkos/file.shutdown"
        while os.path.exists(file_path):
            time.sleep(1) 
        os.system(f"touch {file_path}")
        stop_darkos()
def debug_wine():
    while True:
        file_path = "/data/data/com.termux/files/usr/glibc/opt/darkos/file.debug"
        while os.path.exists(file_path):
            time.sleep(1) 
        os.system("box64 wineserver -k &>/dev/null")
        print(f"{G}{BOLD} Restarting WINE {W}")
        os.system(f"touch {file_path}")
        os.system("python3 $PREFIX/bin/debug-darkos.py")
        exit()
def settings_wine():
    while True:
        file_path = "/data/data/com.termux/files/usr/glibc/opt/darkos/file.setting"
        while os.path.exists(file_path):
            time.sleep(1) 
        os.system("box64 wineserver -k &>/dev/null")
        print(f"{G}{BOLD} Restarting WINE {W}")
        os.system(f"touch {file_path}")
        os.system("chmod +x /data/data/com.termux/files/usr/bin/install.sh")
        os.system("am start -n com.termux/.app.TermuxActivity &>/dev/null")
        subprocess.run(["bash", "install.sh"])
        time.sleep(1)
        restart_program() 
def input_action():
    while True:
        stop = input()
        if stop != "1" and stop != "2":
            print("")
            print(f"{G}{BOLD} Rebooting......... {W}")
            os.system("box64 wineserver -k &>/dev/null")
            time.sleep(1)
            restart_program() 
        elif stop == "1":
            stop_darkos()
        elif stop == "2":
            os.system("box64 wineserver -k")
            os.system('pkill -f "app_process / com.termux.x11"')
            os.system('pkill -f pulseaudio')
            print(f"{G}{BOLD} exiting to the terminal goodbye {W}")
            time.sleep(2)
            os._exit(0)
def restart_program():
    extract_and_delete_tar_files()                
    load_conf()
    if not os.path.exists(wine_prefix):
        create_wine_prefix()
        extract_and_delete_tar_files()                
        load_conf()
    start_wine()
def stop_darkos():
    os.system("box64 wineserver -k")
    os.system('pkill -f "app_process / com.termux.x11"')
    os.system('pkill -f pulseaudio')
    print(f"{G}{BOLD} shutdown........ {W}")
    os.system("am startservice -a com.termux.service_stop com.termux/.app.TermuxService")
    os.system("pkill -f com.termux.x11")
    subprocess.run(['am', 'broadcast', '-a', 'com.termux.x11.ACTION_STOP', '-p', 'com.termux.x11'])
    os._exit(0)

restart_program()

thread1 = threading.Thread(target=restart_wine)
thread2 = threading.Thread(target=input_action)
thread3 = threading.Thread(target=update_wine)
thread4 = threading.Thread(target=settings_wine)
thread5 = threading.Thread(target=debug_wine)
thread6 = threading.Thread(target=shutdown_wine)
thread7 = threading.Thread(target=start_virgl)
thread8 = threading.Thread(target=stop_virgl)
thread9 = threading.Thread(target=reload_style)

thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread8.start()
thread9.start()


thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()
thread6.join()
thread7.join()
thread8.join()
thread9.join()
