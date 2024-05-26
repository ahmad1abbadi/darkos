import os, shutil, time
import subprocess

R = "\033[1;31m"
G = "\033[1;32m"
Y = "\033[1;33m"
B = "\033[1;34m"
C = "\033[1;36m"
W = "\033[1;37m"
BOLD = "\033[1m"

def package_install_and_check(*packs_list):
    for package_name in packs_list:
        print(f"{R}[{W}-{R}]{G}{BOLD} Installing package: {C}{package_name} {W}")
        result = subprocess.run(["pkg", "install", package_name, "-y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            subprocess.run(["apt", "--fix-broken", "install", "-y", "--no-install-recommends"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["dpkg", "--configure", "-a"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if subprocess.run(["dpkg", "-s", package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
            print(f"{R}[{W}-{R}]{G}{BOLD} {package_name} installed successfully {W}")
        else:
            which_output = shutil.which(package_name)
            if which_output:
                print(f"{R}[{W}-{R}]{G} {package_name} installed successfully {W}")
            else:
                print(f"{R}[{W}-{R}]{G} {package_name} installation failed {W}")
                
def check_and_backup(file_path):

    home_dir = os.path.expanduser("~")
    full_path = os.path.join(home_dir, file_path)

    if os.path.exists(full_path):
        backup_path = f"{full_path}.bak"
        os.rename(full_path, backup_path)

def start_darkos():
    os.system("clear")
    if "LD_PRELOAD" in os.environ:
        del os.environ["LD_PRELOAD"]
    print(f"{R}[{W}-{R}]{G}{BOLD} Starting {W}")
    os.system("termux-x11 :0 &>/dev/null &")
    os.system('pulseaudio --start --load="module-native-protocol-tcp auth-ip-acl=127.0.0.1 auth-anonymous=1" --exit-idle-time=-1 &>/dev/null')
    
def termux_pkg():
    print(f"{R}[{W}-{R}]{G}{BOLD} This takes a few minutes it depends on your internet connection {W}")
    os.system("pkg install glibc-repo x11-repo -y &>/dev/null")
    print(f"{R}[{W}-{R}]{G}{BOLD} glibc-repo + x11-repo installed {W}")
    package_install_and_check("pulseaudio", "patchelf", "xkeyboard-config", "freetype", "fontconfig", "termux-x11-nightly", "termux-am zenity", "which", "alsa-lib-glibc", "bash", "curl", "sed", "cabextract")
    print(f"{R}[{W}-{R}]{G}{BOLD}pulseaudio + termux-am +........... installed successfully {W}")
    package_install_and_check("wget", "make", "libpng", "xorg-xrandr", "cmake", "unzip", "p7zip", "patchelf", "tur-repo", "virglrenderer-android", "virglrenderer-mesa-zink")
    print(f"{R}[{W}-{R}]{G}{BOLD} patchelf + wget + make +........ installed successfully {W}")
    print("")
def install_glibc_AZ():
    os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/glibc-darkos.tar.xz")
    os.system("tar -xJf glibc-darkos.tar.xz -C $PREFIX/")
def update():
    os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/update.tar.xz")
    os.system("tar -xJf update.tar.xz")
    os.remove("update.tar.xz")
def alsa():
    os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/alsa.tar.xz")
    os.system("tar -xJf alsa.tar.xz -C /data/data/com.termux/files/ &>/dev/null")
    os.remove("alsa.tar.xz")    
def mangohud():
    os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/mangohud.tar.xz")
    os.system("tar -xvvf mangohud.tar.xz --strip-components=6 -C $PREFIX/glibc &>/dev/null")
    os.remove("mangohud.tar.xz")
def install_AZ():
    os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/AZ.tar.xz")
    os.system("tar -xJf AZ.tar.xz -C $PREFIX/glibc/")
    os.remove("AZ.tar.xz")
def install_box():
    os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/box.tar.xz")
    os.system("tar -xJf box.tar.xz -C $PREFIX/glibc/bin")
    os.remove("box.tar.xz")
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
                    print(f"{R}[{W}-{R}]{G}{BOLD} Welcome back again ☺️ {W}")
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
    print(f"{R}[{W}-{R}]{G}{BOLD} Creating wine prefix 💫 {W}")
    os.system(f"tar -xJf $PREFIX/glibc/opt/darkos/XinputBridge.tar.xz -C /data/data/com.termux/files/usr/glibc/opt/wine/1/wine/lib/wine/ &>/dev/null")
    os.system(f'WINEUSERNAME="DARKOS" WINEDLLOVERRIDES="mscoree=disabled" box64 wine64 wineboot &>/dev/null')
    os.system(f'cp -r $PREFIX/glibc/opt/Startxmenu/* "{wine_prefix}/drive_c/ProgramData/Microsoft/Windows/Start Menu"')
    os.system(f'rm "{wine_prefix}/dosdevices/z:"')
    os.system(f'ln -s /sdcard/Download "{wine_prefix}/dosdevices/o:" &>/dev/null')
    os.system(f'ln -s /data/data/com.termux/files/usr/glibc/opt/G_drive "{wine_prefix}/dosdevices/g:" &>/dev/null')
    os.system(f'ln -s /sdcard/darkos "{wine_prefix}/dosdevices/e:" &>/dev/null')
    os.system(f'ln -s /data/data/com.termux/files "{wine_prefix}/dosdevices/z:"')
    print(f"{R}[{W}-{R}]{G}{BOLD} Installing OS stuff... {W}")
    os.system(f'box64 wine "$PREFIX/glibc/opt/apps/Install OS stuff.bat" &>/dev/null')
    print(f"{R}[{W}-{R}]{G}{BOLD} Done! {W}")
    print(f"{R}[{W}-{R}]{G}{BOLD} prefix done enjoy 🤪 {W}")
    time.sleep(3)
    os.system("box64 wineserver -k &>/dev/null")
    print(f'{R}[{W}-{R}]{G}{BOLD} done {W}')
    print("")
    print(f"{R}[{W}-{R}]{G}{BOLD} Starting DARK OS {W}")
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
    os.system("apt reinstall vulkan-icd-loader-glibc -y &>/dev/null")
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
    os.system("chmod +x $PREFIX/glibc/opt/scripts/termux-x11.sh")
    os.system("mv darkos update-darkos.py darkos.py winetricks setting-darkos.py debug-darkos.py run-darkos.py cpu_boost.py photo.py $PREFIX/bin/")
    check_and_backup(".termux/colors.properties")
    os.system("wget -O $HOME/.termux/colors.properties https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/terminal_utility/colors.properties &>/dev/null")
    check_and_backup(os.getenv("PREFIX") + "/etc/motd-playstore")
    check_and_backup(os.getenv("PREFIX") + "/ect/motd")
    os.system("wget -O $PREFIX/etc/darkos-motd.sh https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/terminal_utility/darkos-motd.sh &>/dev/null")
    os.system(f'echo "bash {os.getenv("PREFIX")}/etc/darkos-motd.sh" >> {os.getenv("PREFIX")}/etc/termux-login.sh')
    check_and_backup(".termux/font.ttf")
    os.system("wget -O $HOME/.termux/font.ttf https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/terminal_utility/ubuntu-mono.ttf &>/dev/null")
def remove():
    os.system("rm glibc-darkos.tar.xz install installglibc.py")
    os.system("clear")
os.system("clear")
print(f"{R}[{W}-{R}]{G}{BOLD} DarkOS installation is begining 😉 {W}")
print("")
edit_bashrc()
print("")
print(f"{R}[{W}-{R}]{G}{BOLD} please wait ....... {W}")
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
install_box()
print(" 👣 👣 👣 👣 👣 👣 👣 👣")
update()
print(" 👣 👣 👣 👣 👣 👣 👣 👣 👣 ")
alsa()
print(" 👣 👣 👣 👣 👣 👣 👣 👣 👣 👣")
scripts()
print(" 👣 👣 👣 👣 👣 👣 👣 👣 👣 👣👣")
remove()
print(f"{R}[{W}-{R}]{G}{BOLD}   Installation finished successfully {W}")
print("")
start_darkos()
create_prefix()
