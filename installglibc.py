import os, shutil, time
def packages():
    os.system("pkg install x11-repo -y &>/dev/null")
    os.system("pkg install pulseaudio wget xkeyboard-config freetype fontconfig libpng xorg-xrandr termux-x11-nightly termux-am zenity which bash curl sed cabextract -y --no-install-recommends &>/dev/null")
def install_glibc():
    os.system("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/dev/glibc-prefix.tar.xz")
    os.system("tar -xJf glibc-prefix.tar.xz -C $PREFIX/")
def scripts():
    os.system("wget https://raw.githubusercontent.com/ahmad1abbadi/darkos/blob/main/darkos &>/dev/null")
    os.system("wget https://raw.githubusercontent.com/ahmad1abbadi/darkos/blob/main/darkos.py &>/dev/null")
    os.system("wget https://raw.githubusercontent.com/ahmad1abbadi/darkos/blob/main/run-darkos.py &>/dev/null")
    os.system("chmod +x darkos")
    os.system("mv darkos darkos.py run-darkos.py $PREFIX/bin/")
    os.system("ln -s $PREFIX/glibc/opt/wine/bin/wine $PREFIX/glibc/bin/wine")
    os.system("ln -s $PREFIX/glibc/opt/wine/bin/wine64 $PREFIX/glibc/bin/wine64")
    os.system("ln -s $PREFIX/glibc/opt/wine/bin/wineserver $PREFIX/glibc/bin/wineserver")
    os.system("ln -s $PREFIX/glibc/opt/wine/bin/wineboot $PREFIX/glibc/bin/wineboot")
    os.system("ln -s $PREFIX/glibc/opt/wine/bin/winecfg $PREFIX/glibc/bin/winecfg")
def clear_waste():
    os.system("rm glibc-prefix.tar.xz install installglibc.py")
    os.system("clear")
def storage():
    os.system("termux-setup-storage")
    time.sleep(2)
os.system("clear")
print(" DarkOS installation is begining 😉 ")
print("allow storage permission)
storage()
print("")
packages()
print(" Downloading and unpacking glibc-prefix")
print("")
install_glibc()
print("")
scripts()
print("")
clear_waste()
print(" Installation finished starting OS")
