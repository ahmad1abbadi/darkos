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
        print("exit press 1 then enter")
        os.system("am start -n com.termux.x11/com.termux.x11.MainActivity &>/dev/null")
        stop = input()
        if stop == "1":
            print(" Stopping Wine...")
            os.system("box64 wineserver -k &>/dev/null")
            main_menu()
    elif choice == "4":
        recreate_prefix()
        create_prefix()
    elif choice == "3":
        print("")
        print("Stopping Termux-X11...")
        print("")
        os.system('pkill -f "app_process / com.termux.x11"')
        os.system('pkill -f pulseaudio')
        exit()
elif sys.argv[1] == "--start":
    start_darkos()
    check_config()
    check_prefix()
    main_menu()
elif sys.argv[1] == "":
    start_darkos()
    check_config()
    check_prefix()
    main_menu()
