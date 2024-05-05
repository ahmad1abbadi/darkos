import os
import re
import subprocess
import time
import threading

R = "\033[1;31m"
G = "\033[1;32m"
Y = "\033[1;33m"
B = "\033[1;34m"
C = "\033[1;36m"
W = "\033[1;37m"
BOLD = "\033[1m"

exec(open('/data/data/com.termux/files/usr/glibc/opt/wine/os.conf').read())
exec(open('/sdcard/darkos/darkos_dynarec.conf').read())
exec(open('/sdcard/darkos/darkos_dynarec_box86.conf').read())
exec(open('/sdcard/darkos/darkos_custom.conf').read())
os.environ["BOX64_TRACE_FILE"]="/sdcard/darkos/trace/trace-%pid.txt"
os.system("BOX64_LOG=1 BOX64_SHOWSEGV=1 BOX64_DYNAREC_LOG=1 BOX64_DYNAREC_MISSING=1 WINEDEBUG=warn+all BOX64_DLSYM_ERROR=1 WINEDEBUG=+err taskset -c 4-7 box64 wine64 explorer /desktop=shell,800x600 $PREFIX/glibc/opt/apps/DARKOS_configuration.exe >/sdcard/darkos/darkos.log 2>&1 &")
os.system("am start -n com.termux.x11/com.termux.x11.MainActivity &>/dev/null")
os.system("clear")
os.system("python3 $PREFIX/bin/photo.py")

def colored_input(prompt):
    print(f"{R}[{W}-{R}]{G}{BOLD} {prompt} {W}", end="")
    user_input = input()
    return user_input

def recreate_prefix():
    os.system("clear")
    os.system("python3 $PREFIX/bin/photo.py")
    print(f"{R}[{W}-{R}]{G}{BOLD} select wine to recreate: {W}")
    
    wine_paths = {
        "1": "/data/data/com.termux/files/usr/glibc/opt/wine/1/wine/bin",
        "2": "/data/data/com.termux/files/usr/glibc/opt/wine/2/wine/bin",
        "3": "/data/data/com.termux/files/usr/glibc/opt/wine/3/wine/bin"
    }
    
    for key, path in wine_paths.items():
        if os.path.exists(path):
            if key == "1":
                print(f"{Y} 1) wine 1 {W}")
            if key == "2":
                print(f"{Y} 2) wine 2 {W}")
            if key == "3":
                print(f"{Y} 3) wine 3 {W}")
    
    print(f"{Y} Else) Back to the settings menu {W}")
    print("")
    
    prefix_path = colored_input("Enter your selection:")
    
    if prefix_path not in wine_paths.keys():
      print(f"{R} no prefix found backing to debug menu {W}")
      time.sleep(1)
      reboot()
    else:
      conf_path = f"/data/data/com.termux/files/usr/glibc/opt/wine/{prefix_path}/os.conf"
      wine_prefix = f"/data/data/com.termux/files/usr/glibc/opt/wine/{prefix_path}/.wine"
      os.system("chmod +x $PREFIX/glibc/bin/box86")
      os.system("chmod +x $PREFIX/glibc/bin/box64")
      os.system(f"chmod +x /data/data/com.termux/files/usr/glibc/opt/wine/{prefix_path}/wine/bin/wine")
      os.system(f"chmod +x /data/data/com.termux/files/usr/glibc/opt/wine/{prefix_path}/wine/bin/wine64")
      os.system(f"chmod +x /data/data/com.termux/files/usr/glibc/opt/wine/{prefix_path}/wine/bin/wineserver")
      os.system("patchelf --force-rpath --set-rpath $PREFIX/glibc/lib --set-interpreter $PREFIX/glibc/lib/ld-linux-aarch64.so.1 $PREFIX/glibc/bin/box64")
      os.system("patchelf --force-rpath --set-rpath $PREFIX/glibc/lib32 --set-interpreter $PREFIX/glibc/lib32/ld-linux-armhf.so.3 $PREFIX/glibc/bin/box86")
      os.system("rm -rf $PREFIX/glibc/bin/wine $PREFIX/glibc/bin/wine64 $PREFIX/glibc/bin/wineserver")
      os.system(f"ln -sf /data/data/com.termux/files/usr/glibc/opt/wine/{prefix_path}/wine/bin/wine $PREFIX/glibc/bin/wine")
      os.system(f"ln -sf /data/data/com.termux/files/usr/glibc/opt/wine/{prefix_path}/wine/bin/wine64 $PREFIX/glibc/bin/wine64")
      os.system(f"ln -sf /data/data/com.termux/files/usr/glibc/opt/wine/{prefix_path}/wine/bin/wineserver $PREFIX/glibc/bin/wineserver")
      os.system(f"ln -sf /data/data/com.termux/files/usr/glibc/opt/wine/{prefix_path}/wine/bin/wineboot $PREFIX/glibc/bin/wineboot")
      os.system(f"ln -sf /data/data/com.termux/files/us/glibc/opt/wine/{prefix_path}/wine/bin/winecfg $PREFIX/glibc/bin/winecfg")
      os.environ.pop('LD_PRELOAD', None)
      def prefix_gstreamer():
        print(f"{R}[{W}-{R}]{G}{BOLD} Creating wine prefix 💫 {W}")
        os.environ.pop('BOX86_DYNAREC_BIGBLOCK', None)
        os.environ.pop('BOX64_DYNAREC_BIGBLOCK', None)
        os.environ.pop('WINEESYNC', None)
        os.environ.pop('WINEESYNC_TERMUX', None)
        os.environ.pop('BOX86_DYNAREC_CALLRET', None)
        os.environ.pop('BOX64_DYNAREC_CALLRET', None)
        os.system(f'WINEDLLOVERRIDES="mscoree=disabled,winegstreamer=disable" box64 wine64 wineboot &>/dev/null')
        os.system(f'cp -r $PREFIX/glibc/opt/Startxmenu/* "{wine_prefix}/drive_c/ProgramData/Microsoft/Windows/Start Menu"')
        os.system(f'rm "{wine_prefix}/dosdevices/z:"')
        os.system(f'ln -s /sdcard/Download "{wine_prefix}/dosdevices/o:" &>/dev/null')
        os.system(f'ln -s /sdcard/darkos "{wine_prefix}/dosdevices/e:" &>/dev/null')
        os.system(f'ln -s /data/data/com.termux/files "{wine_prefix}/dosdevices/z:"')
        print(f"{R}[{W}-{R}]{G}{BOLD} Installing DXVK+Zink... {W}")
        os.system(f'box64 wine "$PREFIX/glibc/opt/apps/Install OS stuff.bat" &>/dev/null')
        print(f"{G} Done! {W}") 
        print(f"{R}[{W}-{R}]{G}{BOLD} prefix done enjoy 🤪 {W}")
        time.sleep(1)
        os.system("box64 wineserver -k &>/dev/null")
        print(f"{R}[{W}-{R}]{G}{BOLD} os will start on debug mode see log file if there any issues {W}")
        time.sleep(2)
        os.system("BOX86_LOG=2 BOX86_SHOWSEGV=1 BOX86_DYNAREC_LOG=1 BOX86_DYNAREC_MISSING=1 BOX86_DLSYM_ERROR=1 BOX64_LOG=3 BOX64_SHOWSEGV=1 BOX64_DYNAREC_LOG=1 BOX64_DYNAREC_MISSING=1 BOX64_DLSYM_ERROR=1 taskset -c 4-7 box64 wine explorer /desktop=shell,800x600 $PREFIX/glibc/opt/apps/pc.ex >/sdcard/darkos.log 2>&1 &")
        os.system("am start -n com.termux.x11/com.termux.x11.MainActivity &>/dev/null")
        os.system("clear")
        os.system("python3 $PREFIX/bin/photo.py")
        print(f"{Y} exit 1️⃣ {W}")
        user_input = colored_input("Enter 1 to stop: ")
        if user_input == "1":
          os.system("box64 wineserver -k")
          print(f"{G} Exiting 👋 {w}")
          os.system('pkill -f "app_process / com.termux.x11"')
          os.system('pkill -f pulseaudio')
          reboot()
        if os.path.exists(wine_prefix):
          shutil.rmtree(wine_prefix)
          time.sleep(1)
          prefix_gstreamer()
      if not os.path.exists(wine_prefix):
        prefix_gstreamer()
def reboot():
  os.system("clear")
  os.system("python3 $PREFIX/bin/photo.py")
  print(f"{R}[{W}-{R}]{G}{BOLD} you are in debug mode... choose what you need to do : {W}")
  print(f"{R}[{W}-{R}]{C}{BOLD} note :- this option available just in safe mode. {W}")
  print("")
  print(f"{Y} 1) reboot debug in 32bit mode using box64 and box68 {W}")
  print(f"{Y} 2) recreate prefix {W}")
  print(f"{Y} 3) restart os {W}")
  print(f"{Y} 4) kill all proceeds and exit {W}")
  choice = input()
  if choice != "1" and choice != "2" and choice != "3" and choice != "4":
    reboot()
  elif choice == "1":
    exec(open('/data/data/com.termux/files/usr/glibc/opt/wine/os.conf').read())
    exec(open('/sdcard/darkos/darkos_dynarec.conf').read())
    exec(open('/sdcard/darkos/darkos_custom.conf').read())
    os.system("BOX64_LOG=1 BOX64_SHOWSEGV=1 BOX64_DYNAREC_LOG=1 BOX64_DYNAREC_MISSING=1 WINEDEBUG=warn+all BOX64_DLSYM_ERROR=1 WINEDEBUG=+err taskset -c 4-7 box64 wine explorer /desktop=shell,800x600 $PREFIX/glibc/opt/apps/DARKOS_configuration.exe >/sdcard/darkos/darkos.log 2>&1 &")
    os.system("am start -n com.termux.x11/com.termux.x11.MainActivity &>/dev/null")
    reboot()
  elif choice == "2":
    recreate_prefix()
  elif choice == "3":
      print("")
      os.system("box64 wineserver -k &>/dev/null")
      print(f"{R}[{W}-{R}]{G}{BOLD} Rebooting......... {W}")
      os.system('pkill -f "app_process / com.termux.x11"')
      os.system('pkill -f pulseaudio')
      time.sleep(1)
      subprocess.run(["bash", "darkos"])
  elif choice == "4":
      os.system("box64 wineserver -k")
      os.system('pkill -f "app_process / com.termux.x11"')
      os.system('pkill -f pulseaudio')
      print(f"{R}[{W}-{R}]{C}{BOLD} shutdown........ {W}")
      time.sleep(1)
      os.system("am startservice -a com.termux.service_stop com.termux/.app.TermuxService")
reboot()        
      
    
