import os, time, shutil, sys, subprocess, urllib.request, urllib.error
import tarfile
tar_xz_file_path ='/sdcard/darkos/airidosas252builds/wine.tar.xz'
target_folders = ['bin', 'lib', 'lib64', 'share']
destination_dir = '/data/data/com.termux/files/usr/glibc/opt/wine/3/wine'
root_dir = "/data/data/com.termux/files/usr/glibc/opt/temp"
os.system("am start -n com.termux/.HomeActivity")
def uninstall_wine9():
    if os.path.exists("/data/data/com.termux/files/usr/glibc/opt/wine/1/wine/bin"):
        os.system("rm -r /data/data/com.termux/files/usr/glibc/opt/wine/1/wine")
        if os.path.exists("/data/data/com.termux/files/usr/glibc/opt/wine/1/.wine"):
            shutil.rmtree('/data/data/com.termux/files/usr/glibc/opt/wine/1/.wine')
def install_wine9():
  os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/wine-default.tar.xz")
  os.system("tar -xJf wine-default.tar.xz -C $PREFIX/glibc/opt/wine/1")
  os.remove("wine-default.tar.xz")
def wine_manager():
  os.system("clear")
  photo()
  print("Wine Manager ⚙️")
  print("1) install wine 📥")
  print("2) uninstall wine 📤")
  print("3) Repair default wine files 🔧")
  print("4) back to main menu 🔙")
  print("")
  choice = input()
  if choice != "1" and choice != "2" and choice != "3" and choice != "4" and choice != "dev":
    print("wrong")
    wine_manager()
  elif choice == "1":
    wine_select()
  elif choice == "dev":
    os.system("clear")
    conf_path = "/data/data/com.termux/files/usr/glibc/opt/wine/os.conf"
    print("share log on our Telegram group ")
    print("to exit dev mode kill termux or press Ctrl + C ")
    exec(open(conf_path).read())
    exec(open('/sdcard/darkos/darkos_dynarec.conf').read())
    os.system("BOX86_LOG=1 BOX86_SHOWSEGV=1 BOX86_DYNAREC_LOG=1 BOX86_DYNAREC_MISSING=1 BOX86_DLSYM_ERROR=1 BOX64_LOG=1 BOX64_SHOWSEGV=1 BOX64_DYNAREC_LOG=1 BOX64_DYNAREC_MISSING=1 WINEDEBUG=warn+all BOX64_DLSYM_ERROR=1 WINEDEBUG=+err taskset -c 4-7 box64 wine explorer /desktop=shell,800x600 $PREFIX/glibc/opt/apps/pc.ex >/sdcard/darkos.log")
  elif choice == "2":
      uninstall_wine()
  elif choice == "3":
      print(" Do you really want to repair Wine files ? This will delete all your files inside the drive C  ")
      print(" yes = y")
      print(" no = n")
      stop = input()
      if stop != "y" and choice != "n":
          print("wrong choice backing to main menu")
          time.sleep(1)
          wine_manager()
      elif stop == "y":
          uninstall_wine9()
          time.sleep(1)
          install_wine9()
          print("default wine fixed....")
          time.sleep(2)
          wine_manager()
      elif stop == "n":
          wine_manager()
  elif choice == "4":
      os.system("python3 $PREFIX/bin/darkos.py")
      os.system("exit")
def photo():
  os.system("python3 $PREFIX/bin/photo.py")
def uninstall_wine():
  os.system("clear")
  photo()
  print("Are you sure you want to delete the wine version?")
  print("")
  if os.path.exists("/data/data/com.termux/files/usr/glibc/opt/wine/2/wine/bin"):
    print("1) Delete wine on container 2")
  if os.path.exists("/data/data/com.termux/files/usr/glibc/opt/wine/3/wine/bin"):
    print("2) Delete wine on container 3")
    print(" else) setting menu ⬅️")
    print("")
  choice = input()
  if choice != "1" and choice != "2":
    print("Incorrect or empty option!")
    wine_manager()
  elif choice == "1" and os.path.exists("/data/data/com.termux/files/usr/glibc/opt/wine/2/wine/bin"):
    print("Deleting wine, please wait")
    print("")
    uninstall_wine1()
  elif choice == "2" and os.path.exists("/data/data/com.termux/files/usr/glibc/opt/wine/3/wine/bin"):
    print("Deleting wine , please wait")
    print("")
    uninstall_wine2()
  wine_manager()
def uninstall_wine2():
  if os.path.exists("/data/data/com.termux/files/usr/glibc/opt/wine/3/wine/bin"):
    os.system("rm -r /data/data/com.termux/files/usr/glibc/opt/wine/3/wine")
def uninstall_wine1():
  if os.path.exists("/data/data/com.termux/files/usr/glibc/opt/wine/2/wine/bin"):
    os.system("rm -r /data/data/com.termux/files/usr/glibc/opt/wine/2/wine")
def install_wine2():
  if not os.path.exists("/data/data/com.termux/files/usr/glibc/opt/wine/2/wine/bin"):
    os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/wine2.tar.xz")
    os.system("tar -xJf wine2.tar.xz -C $PREFIX/glibc/opt/wine/2")
    os.remove("wine2.tar.xz")
    conf_path = f"/data/data/com.termux/files/usr/glibc/opt/wine/2/os.conf"
    wine_prefix = f"/data/data/com.termux/files/usr/glibc/opt/wine/2/.wine"
    exec(open(conf_path).read())
    print("Creating wine prefix 💫")
    os.system(f'WINEDLLOVERRIDES="mscoree=disabled" box64 wine64 wineboot &>/dev/null')
    os.system(f'cp -r $PREFIX/glibc/opt/Startxmenu/* "{wine_prefix}/drive_c/ProgramData/Microsoft/Windows/Start Menu"')
    os.system(f'rm "{wine_prefix}/dosdevices/z:"')
    os.system(f'ln -s /sdcard/Download "{wine_prefix}/dosdevices/o:" &>/dev/null')
    os.system(f'ln -s /sdcard/darkos "{wine_prefix}/dosdevices/e:" &>/dev/null')
    os.system(f'ln -s /data/data/com.termux/files "{wine_prefix}/dosdevices/z:"')
    print("Installing DXVK+Zink...")
    os.system(f'box64 wine "$PREFIX/glibc/opt/apps/Install OS stuff.bat" &>/dev/null')
    print("Done!")
    print("prefix done enjoy 🤪 ")
    print("to select installed wine please choose container 2 ")
    time.sleep(3)
    os.system("box64 wineserver -k &>/dev/null")
    wine_manager()
def install_wine3():
    if os.path.exists("/sdcard/darkos/airidosas252builds/wine.tar.xz"):
        os.remove("/sdcard/darkos/airidosas252builds/wine.tar.xz")
    conf_path = f"/data/data/com.termux/files/usr/glibc/opt/wine/3/os.conf"
    wine_prefix = f"/data/data/com.termux/files/usr/glibc/opt/wine/3/.wine"
    exec(open(conf_path).read())
    print("Creating wine prefix 💫")
    if not os.path.exists("/data/data/com.termux/files/usr/glibc/opt/wine/3/wine/bin/wine64"):
        os.system(f"ln -sf /data/data/com.termux/files/usr/glibc/opt/wine/3/wine/bin/wine $PREFIX/glibc/bin/wine64")
        os.system(f"ln -sf /data/data/com.termux/files/usr/glibc/opt/wine/3/wine/bin/wine $PREFIX/glibc/opt/wine/3/wine/bin/wine64")
    os.system(f'WINEDLLOVERRIDES="mscoree=disabled" box64 wine64 wineboot  >/sdcard/darkos/boot64_log.txt 2>&1')
    os.system(f'cp -r $PREFIX/glibc/opt/Startxmenu/* "{wine_prefix}/drive_c/ProgramData/Microsoft/Windows/Start Menu"')
    os.system(f'rm "{wine_prefix}/dosdevices/z:"')
    os.system(f'ln -s /sdcard/Download "{wine_prefix}/dosdevices/o:" &>/dev/null')
    os.system(f'ln -s /sdcard/darkos "{wine_prefix}/dosdevices/e:" &>/dev/null')
    os.system(f'ln -s /data/data/com.termux/files "{wine_prefix}/dosdevices/z:"')
    print("Installing DXVK+Zink...")
    os.system(f'box64 wine64 "$PREFIX/glibc/opt/apps/Install OS stuff.bat" &>/dev/null')
    print("Done!")
    print("prefix done enjoy 🤪 ")
    print("to select installed wine please choose container 3 ")
    time.sleep(3)
    os.system("box64 wineserver -k &>/dev/null")
    time.sleep(1)
    wine_manager()
def wine_select():
    os.system("clear")
    photo()
    print("please select wine version:")
    print("")
    if not os.path.exists("/data/data/com.termux/files/usr/glibc/opt/wine/2/wine/bin"):
        print("")
        print(" 1) install stable wine on container 2")
        print("")
    if not os.path.exists("/data/data/com.termux/files/usr/glibc/opt/wine/3/wine/bin"):
        print("")
        print(" 2) install airidosas252builds wine on container 3 .....please make sure you have renamed file to wine.tar.xz")
        print("")
    print(" else) setting wine menu ⬅️")
    print("")
    choice = input()
    if choice != "1" and choice != "2":
        print("Incorrect or empty option!")
        wine_manager()
    elif choice == "1":
        print("downloading wine please wait")
        print("")
        install_wine2()
    elif choice == "2":
        print("installing airidosas252builds wine please wait.....")
        print("")
        if not os.path.exists("/data/data/com.termux/files/usr/glibc/opt/wine/3/wine/bin"):
            if os.path.exists("/sdcard/darkos/airidosas252builds/wine.tar.xz"):
                os.system("tar -xJf /sdcard/darkos/airidosas252builds/wine.tar.xz -C $PREFIX/glibc/opt/temp")
            search_and_move_folders(root_dir, target_folders, destination_dir)
        install_wine3()
        time.sleep(1)
    wine_manager()
def search_and_move_folders(root_dir, target_folders, destination_dir):
    for root, dirs, files in os.walk(root_dir):
        for folder in dirs:
            if folder in target_folders:
                source_path = os.path.join(root, folder)
                destination_path = os.path.join(destination_dir, folder)
                if not os.path.exists(destination_path):
                    shutil.move(source_path, destination_path)
wine_manager()
