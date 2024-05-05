import os, time, shutil, sys, subprocess, urllib.request, urllib.error
import tarfile
import socket
import fnmatch

R = "\033[1;31m"
G = "\033[1;32m"
Y = "\033[1;33m"
B = "\033[1;34m"
C = "\033[1;36m"
W = "\033[1;37m"
BOLD = "\033[1m"

tar_xz_file_path ='/sdcard/darkos/airidosas252builds/wine.tar.xz'
target_folders = ['bin', 'lib', 'lib64', 'share']
destination_dir = '/data/data/com.termux/files/usr/glibc/opt/wine/3/wine'
root_dir = "/data/data/com.termux/files/usr/glibc/opt/temp"
os.system("am start -n com.termux/.HomeActivity")
def remove():
    folder_path = '/data/data/com.termux/files/home'
    for filename in os.listdir(folder_path):
        if fnmatch.fnmatch(filename, '*.tar.xz*'):
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)
            print(f'{C}{filename} {G}has been deleted.{W}')
def uninstall_wine9():
    if os.path.exists("/data/data/com.termux/files/usr/glibc/opt/wine/1/wine/bin"):
        os.system("rm -r /data/data/com.termux/files/usr/glibc/opt/wine/1/wine")
        if os.path.exists("/data/data/com.termux/files/usr/glibc/opt/wine/1/.wine"):
            shutil.rmtree('/data/data/com.termux/files/usr/glibc/opt/wine/1/.wine')
    if os.path.exists("/sdcard/darkos"):
        os.system("rm -r /sdcard/darkos")
def install_wine9():
    os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/AZ.tar.xz")
    os.system("tar -xJf AZ.tar.xz -C $PREFIX/glibc")
    os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/wine-default.tar.xz")
    os.system("tar -xJf wine-default.tar.xz -C $PREFIX/glibc/opt/wine/1")
    os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/darkos.tar.xz")
    os.system("tar -xJf darkos.tar.xz -C /sdcard/")
    os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/update.tar.xz")
    os.system("tar -xJf update.tar.xz")
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
    os.system("chmod +x darkos")
    os.system("mv update-darkos.py darkos.py run-darkos.py debug-darkos.py setting-darkos.py darkos $PREFIX/bin/")
    remove()
    print("")
    print(f"{G} DARKOS files repaired successfully {W}")
def internet_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=1)
        return True
    except OSError:
        pass
    return False
def wine_manager():
  os.system("clear")
  photo()
  print(f"{R}[{W}-{R}]{G}{BOLD} Wine Manager ⚙️ {W}")
  print(f"{Y} 1) install wine manually in container 3 📥 {W}")
  print(f"{Y} 2) uninstall wine 📤 {W}")
  print(f"{Y} 3) Repair DARKOS files 🔧 {W}")
  print(f"{Y} 4) back to main menu 🔙  {W}")
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
    print(f"{G}{BOLD} share log on our Telegram group {W}")
    print(f"{G}{BOLD} to exit dev mode {C} kill termux {G}or press {C}Ctrl + C {W}")
    exec(open(conf_path).read())
    exec(open('/sdcard/darkos/darkos_dynarec.conf').read())
    os.system("BOX86_LOG=1 BOX86_SHOWSEGV=1 BOX86_DYNAREC_LOG=1 BOX86_DYNAREC_MISSING=1 BOX86_DLSYM_ERROR=1 BOX64_LOG=1 BOX64_SHOWSEGV=1 BOX64_DYNAREC_LOG=1 BOX64_DYNAREC_MISSING=1 WINEDEBUG=warn+all BOX64_DLSYM_ERROR=1 WINEDEBUG=+err taskset -c 4-7 box64 wine explorer /desktop=shell,800x600 $PREFIX/glibc/opt/apps/pc.ex >/sdcard/darkos.log")
  elif choice == "2":
      uninstall_wine()
  elif choice == "3":
      print(f"{Y} Do you really want to repair Wine files ? This will delete all your files inside the drive C in container 1 {W}")
      print(f"{C} yes = y {W}")
      print(f"{C} no = n {W}")
      stop = input()
      if stop != "y" and choice != "n":
          print(f"{R} wrong choice going back to main menu {W}")
          time.sleep(1)
          wine_manager()
      elif stop == "y":
          if internet_connected():
               uninstall_wine9()
               time.sleep(1)
               install_wine9()
               print(f"{G} done.... {W}")
               time.sleep(1)
               wine_manager()
          else:
               print(f"{R} No internet connection available. Aborting operation. {W}")
               time.sleep(1)
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
    print(f"{Y} Are you sure you want to delete the wine version? {W}")
    print("")
    
    for i in range(2, 6):
        if os.path.exists(f"/data/data/com.termux/files/usr/glibc/opt/wine/{i}/wine/bin"):
            print(f"{Y} {i - 1}) Delete wine on container {C}{i} {W}")
            
    print(f"{Y} else) setting menu ⬅️ {W}")
    print("")
    
    choice = input()
    
    if choice != "1" and choice != "2" and choice != "3" and choice != "4":
        print(f"{G} backing {W}")
        wine_manager()
    else:
        container_number = int(choice) + 1
        if os.path.exists(f"/data/data/com.termux/files/usr/glibc/opt/wine/{container_number}/wine/bin"):
            print(f"{G}{BOLD} Deleting wine, please wait.... {W}")
            print("")
            os.system(f"rm -r /data/data/com.termux/files/usr/glibc/opt/wine/{container_number}/wine")
            os.system("rm -r /data/data/com.termux/files/usr/glibc/opt/wine/os.conf")
            os.system("cp /data/data/com.termux/files/usr/glibc/opt/wine/1/os.conf /data/data/com.termux/files/usr/glibc/opt/wine")
        wine_manager()
def install_wine3():
    if os.path.exists("/sdcard/darkos/airidosas252builds/wine.tar.xz"):
        os.remove("/sdcard/darkos/airidosas252builds/wine.tar.xz")
    conf_path = f"/data/data/com.termux/files/usr/glibc/opt/wine/3/os.conf"
    wine_prefix = f"/data/data/com.termux/files/usr/glibc/opt/wine/3/.wine"
    exec(open(conf_path).read())
    print(f"{R}[{W}-{R}]{G}{BOLD} Creating wine prefix 💫 {W}")
    if not os.path.exists("/data/data/com.termux/files/usr/glibc/opt/wine/3/wine/bin/wine64"):
        os.system(f"ln -sf /data/data/com.termux/files/usr/glibc/opt/wine/3/wine/bin/wine $PREFIX/glibc/bin/wine64")
        os.system(f"ln -sf /data/data/com.termux/files/usr/glibc/opt/wine/3/wine/bin/wine $PREFIX/glibc/opt/wine/3/wine/bin/wine64")
    os.system(f'WINEDLLOVERRIDES="mscoree=disabled" box64 wine64 wineboot  >/sdcard/darkos/boot64_log.txt 2>&1')
    os.system(f'cp -r $PREFIX/glibc/opt/Startxmenu/* "{wine_prefix}/drive_c/ProgramData/Microsoft/Windows/Start Menu"')
    os.system(f'rm "{wine_prefix}/dosdevices/z:"')
    os.system(f'ln -s /sdcard/Download "{wine_prefix}/dosdevices/o:" &>/dev/null')
    os.system(f'ln -s /sdcard/darkos "{wine_prefix}/dosdevices/e:" &>/dev/null')
    os.system(f'ln -s /data/data/com.termux/files "{wine_prefix}/dosdevices/z:"')
    print(f"{R}[{W}-{R}]{G}{BOLD} Installing DXVK+Zink... {W}")
    os.system(f'box64 wine64 "$PREFIX/glibc/opt/apps/Install OS stuff.bat" &>/dev/null')
    print(f"{G}{BOLD} Done! {W}")
    print(f"{G}{BOLD} prefix done enjoy 🤪 {W}")
    print("to select installed wine please choose container 3 ")
    time.sleep(3)
    os.system("box64 wineserver -k &>/dev/null")
    time.sleep(1)
    wine_manager()
def wine_select():
    os.system("clear")
    photo()
    print(f"{C}{BOLD} welcome to installation airidosas bulid of wine . {Y} \nplease make sure you have wine setup file in this path {G}/sdcard/darkos/airidosas252builds/wine.tar.xz {W}")
    print("")
    if os.path.exists("/data/data/com.termux/files/usr/glibc/opt/wine/3/wine/bin"):
        print(f"{R} error ...there is a wine installed in container 3 {W}")
    if not os.path.exists("/data/data/com.termux/files/usr/glibc/opt/wine/3/wine/bin"):
        print("")
        print(f"{Y} 1) install airidosas252builds wine on container 3. {W}")
        print("")
        print(f"{G} please make sure you have renamed file to {C}wine.tar.xz {W}")
        print("")
    print(f"{Y} else) back to wine manger menu ⬅️ {W}")
    print("")
    choice = input()
    if choice != "1":
        print(f"{G} back to wine manger.... {W}")
        wine_manager()
    elif choice == "1":
        print(f"{G} installing airidosas252builds wine please wait..... {W}")
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

