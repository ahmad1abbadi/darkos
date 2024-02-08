import os, time, shutil, sys
def start_darkos():
    os.system("clear")
    if "LD_PRELOAD" in os.environ:
        del os.environ["LD_PRELOAD"]
    print("Starting")
    os.system("termux-x11 :0 &>/dev/null &")
    os.system('pulseaudio --start --load="module-native-protocol-tcp auth-ip-acl=127.0.0.1 auth-anonymous=1" --exit-idle-time=-1 &>/dev/null')
def check_config():
    config_folder = "/data/data/com.termux/files/usr/glibc/opt"
    exec(open('/data/data/com.termux/files/usr/glibc/opt/darcos.conf').read())
    exec(open('/data/data/com.termux/files/usr/glibc/opt/DXVK_D8VK_HUD.conf').read())
def check_prefix():
    if not os.path.exists("/data/data/com.termux/files/home/.wine"):
        print("Creating prefix")
        create_prefix()
def recreate_prefix():
    prefix_path="/data/data/com.termux/files/home/.wine"
    os.system("clear")
    shutil.rmtree(prefix_path)
    print("Creating Wine prefix")
    create_prefix()
def create_prefix():
    os.system('WINEDLLOVERRIDES="mscoree=" box64 wine64 wineboot &>/dev/null')
    os.system('cp -r $PREFIX/glibc/opt/Shortcuts/* "$HOME/.wine/drive_c/ProgramData/Microsoft/Windows/Start Menu"')
    os.system("ln -s /sdcard/Download $HOME/.wine/dosdevices/d: &>/dev/null && ln -s /sdcard $HOME/.wine/dosdevices/e: &>/dev/null")
    print("Installing DXVK, D8VK and vkd3d-proton...")
    os.system('box64 wine "$PREFIX/glibc/opt/Resources64/Run if you will install on top of WineD3D.bat" &>/dev/null && box64 wine "$PREFIX/glibc/opt/Resources64/DXVK2.3/DXVK2.3.bat" &>/dev/null')
    os.system('box64 wine reg add "HKEY_CURRENT_USER\Software\Wine\DllOverrides" /v d3d12 /d native /f &>/dev/null && box64 wine reg add "HKEY_CURRENT_USER\Software\Wine\DllOverrides" /v d3d12core /d native /f &>/dev/null')
    os.system("cp $PREFIX/glibc/opt/Resources/vkd3d-proton2.11/* $HOME/.wine/drive_c/windows/syswow64 && cp $PREFIX/glibc/opt/Resources64/vkd3d-proton2.11/* $HOME/.wine/drive_c/windows/system32")
    print("Done!")
    main_menu()
def main_menu():
    os.system("clear")
    print("welcome to darkos")
    print("")
    print("Select what you need to do:")
    print("1) start DARK OS")
    print("2) settings")
    print("3) Exit")
    print("")
    choice = input()
    if choice != "1" and choice != "2" and choice != "3":
        print("what are you choosing genius")
        main_menu()
    elif choice == "1":
        os.system("python3 $PREFIX/bin/run-darkos.py")
        exit()
        os.system("clear")
        print("to exit OS press 1 then enter")
        os.system("am start -n com.termux.x11/com.termux.x11.MainActivity &>/dev/null")
        stop = input()
        if stop == "1":
            print(" Stopping Wine...")
            os.system("box64 wineserver -k &>/dev/null")
            main_menu()
    elif choice == "2":
        def change_setting():
            os.system("clear")
            print("settings:")
            print("1) update OS")
            print("2) update box version ")
            print("3) activate esync mod")
            print("4) debug mod")
            print("5) recreate prefix")
            print("6) back")
            choice = input()
            if choice != "1" and choice != "2" and choice != "3" and choice != "4" and choice != "5" and choice != "6":
                print("what are you choosing genius")
                main_menu()
            elif choice == "6":
                main_menu()
            elif choice == "1":
                os.system("curl -o install https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/update && chmod +x install && ./install")
                change_setting()
            elif choice == "2":
                os.system("curl -o install https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/update && chmod +x install && ./install")
                os.system("rm $PREFIX/usr/glibc/bin/box64")
                os.system("wget https://github.com/ahmad1abbadi/darkos/releases/download/dev/box64.tar.xz")
                os.system("tar -xJf box64.tar.xz -C $PREFIX/usr/glibc/bin/")
                change_setting()
            elif choice == "3":
                os.system("su -c setenforce 0 &>/dev/null")
                os.system("sudo mkdir /dev/shm &>/dev/null")
                os.system("sudo chmod 1777 /dev/shm &>/dev/null")
                os.system("export WINEESYNC=1")
                os.system("export WINEESYNC_TERMUX=1")
                change_setting()
            elif choice == "4":
                os.system("clear")
                print("share log file on our Telegram group ")
                print("to exit OS press 1 then enter")
                os.system("BOX86_LOG=1 BOX86_SHOWSEGV=1 BOX86_DYNAREC_LOG=1 BOX86_DYNAREC_MISSING=1 BOX86_DLSYM_ERROR=1 BOX64_LOG=1 BOX64_SHOWSEGV=1 BOX64_DYNAREC_LOG=1 BOX64_DYNAREC_MISSING=1 BOX64_DLSYM_ERROR=1 WINEDEBUG=+err taskset -c 4-7 box64 wine explorer /desktop=shell,800x600 $PREFIX/glibc/opt/7-Zip/7zFM >/sdcard/darkos.log 2>&1 &")
                os.system("am start -n com.termux.x11/com.termux.x11.MainActivity &>/dev/null")
            elif choice == "5":
                recreate_prefix()
                create_prefix()
    elif choice == "3":
        print("")
        print("Stopping Termux-X11...")
        print("")
        os.system('pkill -f "app_process / com.termux.x11"')
        os.system('pkill -f pulseaudio')
        exit()
start_darkos()
check_config()
check_prefix()
main_menu()
