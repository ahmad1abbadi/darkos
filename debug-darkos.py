import os
import re
import subprocess
import time
import threading
exec(open('/data/data/com.termux/files/usr/glibc/opt/wine/os.conf').read())
exec(open('/sdcard/darkos/darkos_dynarec.conf').read())
exec(open('/sdcard/darkos/darkos_dynarec_box86.conf').read())
exec(open('/sdcard/darkos/darkos_custom.conf').read())
os.environ["BOX64_TRACE_FILE"]="/sdcard/darkos/trace/trace-%pid.txt"
os.system("BOX64_LOG=1 BOX64_SHOWSEGV=1 BOX64_DYNAREC_LOG=1 BOX64_DYNAREC_MISSING=1 WINEDEBUG=warn+all BOX64_DLSYM_ERROR=1 WINEDEBUG=+err taskset -c 4-7 box64 wine64 explorer /desktop=shell,800x600 $PREFIX/glibc/opt/apps/DARKOS_configuration.exe >/sdcard/darkos/darkos.log 2>&1 &")
os.system("am start -n com.termux.x11/com.termux.x11.MainActivity &>/dev/null")
os.system("clear")
os.system("python3 $PREFIX/bin/photo.py")
def recreate_prefix():
    os.system("clear")
    os.system("python3 $PREFIX/bin/photo.py")
    print("select wine to recreate:")
    
    wine_paths = {
        "1": "/data/data/com.termux/files/usr/glibc/opt/wine/1/wine/bin",
        "2": "/data/data/com.termux/files/usr/glibc/opt/wine/2/wine/bin",
        "3": "/data/data/com.termux/files/usr/glibc/opt/wine/3/wine/bin"
    }
    
    for key, path in wine_paths.items():
        if os.path.exists(path):
            if key == "1":
                print("1) wine 1")
            if key == "2":
                print("2) wine 2")
            if key == "3":
                print("3) wine 3")
    
    print("Else) Back to the settings menu ")
    print("")
    
    prefix_path = input("Enter your selection: ")
    
    if prefix_path not in wine_paths.keys():
      print("no prefix found backing to debug menu")
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
        print("Creating wine prefix 💫")
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
        print("Installing DXVK+Zink...")
        os.system(f'box64 wine "$PREFIX/glibc/opt/apps/Install OS stuff.bat" &>/dev/null')
        print("Done!") 
        print("prefix done enjoy 🤪 ")
        time.sleep(1)
        os.system("box64 wineserver -k &>/dev/null")
        print("os will start on debug mode see log file if there any issues ")
        time.sleep(2)
        os.system("BOX86_LOG=2 BOX86_SHOWSEGV=1 BOX86_DYNAREC_LOG=1 BOX86_DYNAREC_MISSING=1 BOX86_DLSYM_ERROR=1 BOX64_LOG=3 BOX64_SHOWSEGV=1 BOX64_DYNAREC_LOG=1 BOX64_DYNAREC_MISSING=1 BOX64_DLSYM_ERROR=1 taskset -c 4-7 box64 wine explorer /desktop=shell,800x600 $PREFIX/glibc/opt/apps/pc.ex >/sdcard/darkos.log 2>&1 &")
        os.system("am start -n com.termux.x11/com.termux.x11.MainActivity &>/dev/null")
        os.system("clear")
        os.system("python3 $PREFIX/bin/photo.py")
        print("exit 1️⃣")
        user_input = input("Enter 1 to stop: ")
        if user_input == "1":
          os.system("box64 wineserver -k")
          print("Exiting 👋")
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
  print(" you are in debug mode... choose what you need to do :")
  print(" note :- this option available just in safe mode.")
  print("")
  print("1) reboot debug in 32bit mode using box64 and box68")
  print("2) recreate prefix ")
  print("3) restart os")
  print("4) kill all proceeds and exit")
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
      print("Rebooting.........")
      os.system('pkill -f "app_process / com.termux.x11"')
      os.system('pkill -f pulseaudio')
      time.sleep(1)
      subprocess.run(["bash", "darkos"])
  elif choice == "4":
      os.system("box64 wineserver -k")
      os.system('pkill -f "app_process / com.termux.x11"')
      os.system('pkill -f pulseaudio')
      print("shutdown........")
      time.sleep(1)
      os.system("am startservice -a com.termux.service_stop com.termux/.app.TermuxService")
reboot()        
      
    
