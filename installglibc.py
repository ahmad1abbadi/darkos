import os, shutil, time
def start_darkos():
    os.system("clear")
    if "LD_PRELOAD" in os.environ:
        del os.environ["LD_PRELOAD"]
    print("Starting")
    os.system("termux-x11 :0 &>/dev/null &")
    os.system('pulseaudio --start --load="module-native-protocol-tcp auth-ip-acl=127.0.0.1 auth-anonymous=1" --exit-idle-time=-1 &>/dev/null')
    
def termux_pkg():
    print("This takes a few minutes it depends on your internet connection")
    os.system("pkg install glibc-repo x11-repo -y &>/dev/null")
    print("glibc-repo + x11-repo installed")
    os.system("pkg install pulseaudio patchelf xkeyboard-config freetype fontconfig termux-x11-nightly termux-am zenity which bash curl sed cabextract -y --no-install-recommends &>/dev/null")
    print("pulseaudio + termux-am +........... installed successfully ")
    os.system("pkg install wget make libpng xorg-xrandr cmake unzip p7zip patchelf -y --no-install-recommends &>/dev/null")
    print("patchelf + wget + make +........ installed successfully")
    print("")
def install_glibc_AZ():
    os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/glibc-darkos.tar.xz")
    os.system("tar -xJf glibc-darkos.tar.xz -C $PREFIX/")
def update():
    os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/update.tar.xz")
    os.system("tar -xJf update.tar.xz")
    os.remove("update.tar.xz")
def mangohud():
    os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/mangohud.tar.xz")
    os.system("tar -xjvvf mangohud.tar.xz --strip-components=6 -C $PREFIX/glibc &>/dev/null")
    os.remove("mangohud.tar.xz")
def install_AZ():
    os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/AZ.tar.xz")
    os.system("tar -xJf AZ.tar.xz -C $PREFIX/glibc/")
    os.remove("AZ.tar.xz")
def install_conf():
    folder_path = "/sdcard/darkos"
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.mkdir(folder_path)
    os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/darkos.tar.xz")
    os.system("tar -xJf darkos.tar.xz -C /sdcard/")
    os.remove("darkos.tar.xz")
def edit_bashrc():
    command = "darkos"
    bashrc_path = os.path.expanduser('~/.bashrc')
    command_exists = False
    if os.path.exists(bashrc_path):
        with open(bashrc_path, 'r') as f:
            for line in f:
                if command in line:
                    command_exists = True
                    print("Welcome back again ☺️ ")
                    break
        if not command_exists:
            with open(bashrc_path, 'a') as f:
                f.write(command + '\n')
            print(" 📝")
    else:
        with open(bashrc_path, 'w') as f:
            f.write(command + '\n')
        print(" 📝")
def create_prefix():
    conf_path = f"/data/data/com.termux/files/usr/glibc/opt/wine/1/os.conf"
    wine_prefix = f"/data/data/com.termux/files/usr/glibc/opt/wine/1/.wine"
    os.system("ln -s $PREFIX/glibc/opt/wine/1/wine/bin/wine $PREFIX/glibc/bin/wine &>/dev/null")
    os.system("ln -s $PREFIX/glibc/opt/wine/1/wine/bin/wine64 $PREFIX/glibc/bin/wine64 &>/dev/null")
    os.system("ln -s $PREFIX/glibc/opt/wine/1/wine/bin/wineserver $PREFIX/glibc/bin/wineserver &>/dev/null")
    os.system("ln -s $PREFIX/glibc/opt/wine/1/wine/bin/wineboot $PREFIX/glibc/bin/wineboot &>/dev/null")
    os.system("ln -s $PREFIX/glibc/opt/wine/1/wine/bin/winecfg $PREFIX/glibc/bin/winecfg &>/dev/null")
    os.system("chmod +x $PREFIX/glibc/bin/box86")
    os.system("chmod +x $PREFIX/glibc/bin/box64")
    os.system("chmod +x /data/data/com.termux/files/usr/glibc/opt/wine/1/wine/bin/wine")
    os.system("chmod +x /data/data/com.termux/files/usr/glibc/opt/wine/1/wine/bin/wine64")
    os.system("chmod +x /data/data/com.termux/files/usr/glibc/opt/wine/1/wine/bin/wineserver")
    exec(open(conf_path).read())
    os.environ.pop('LD_PRELOAD', None)
    print("Creating wine prefix 💫")
    os.system(f'WINEUSERNAME="DARKOS" WINEDLLOVERRIDES="mscoree=disabled" box64 wine64 wineboot &>/dev/null')
    os.system(f'cp -r $PREFIX/glibc/opt/Startxmenu/* "{wine_prefix}/drive_c/ProgramData/Microsoft/Windows/Start Menu"')
    os.system(f'rm "{wine_prefix}/dosdevices/z:"')
    os.system(f'ln -s /sdcard/Download "{wine_prefix}/dosdevices/o:" &>/dev/null')
    os.system(f'ln -s /sdcard/darkos "{wine_prefix}/dosdevices/e:" &>/dev/null')
    os.system(f'ln -s /data/data/com.termux/files "{wine_prefix}/dosdevices/z:"')
    print("Installing OS stuff...")
    os.system(f'box64 wine "$PREFIX/glibc/opt/apps/Install OS stuff.bat" &>/dev/null')
    print("Done!")
    print("prefix done enjoy 🤪 ")
    time.sleep(3)
    os.system("box64 wineserver -k &>/dev/null")
    print(f'done')
    print("")
    print("starting DARK OS ")
    time.sleep(2)
    os.system("python3 $PREFIX/bin/run-darkos.py")
def install_mono():
    os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/mono.tar.xz")
    os.system("tar -xJf mono.tar.xz")
    os.remove("mono.tar.xz")
def install_wine9():
    os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/wine-default.tar.xz")
    os.system("tar -xJf wine-default.tar.xz -C $PREFIX/glibc/opt/wine/1")
    os.remove("wine-default.tar.xz")
def scripts():
    os.system("wget https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/update-darkos.py &>/dev/null")
    os.system("wget https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/debug-darkos.py &>/dev/null")
    os.system("wget https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/setting-darkos.py &>/dev/null")
    os.system("wget https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/photo.py &>/dev/null")
    os.system("wget https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/darkos &>/dev/null")
    os.system("wget https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/run-darkos.py &>/dev/null")
    os.system("wget https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/darkos.py &>/dev/null")
    os.system("wget https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks &>/dev/null")
    os.system("wget https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/cpu_boost.py &>/dev/null")
    os.system("chmod +x darkos")
    os.system("chmod +x winetricks")
    os.system("mv darkos update-darkos.py darkos.py winetricks setting-darkos.py debug-darkos.py run-darkos.py cpu_boost.py photo.py $PREFIX/bin/")
def remove():
    os.system("rm glibc-darkos.tar.xz install installglibc.py")
    os.system("clear")
os.system("clear")
print(" DarkOS installation is begining 😉")
print("")
edit_bashrc()
print("")
print("please wait .......")
termux_pkg()
print(" 👣")
install_glibc_AZ()
print(" 👣 👣 ")
mangohud()
print(" 👣 👣 👣")
install_conf()
print(" 👣 👣 👣 👣")
install_AZ()
print(" 👣 👣 👣 👣 👣")
install_mono()
print(" 👣 👣 👣 👣 👣 👣")
install_wine9()
print(" 👣 👣 👣 👣 👣 👣 👣")
update()
print(" 👣 👣 👣 👣 👣 👣 👣 👣")
scripts()
print(" 👣 👣 👣 👣 👣 👣 👣 👣 👣")
remove()
print("          Installation finished successfully ")
print("")
start_darkos()
create_prefix()
