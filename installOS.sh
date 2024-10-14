#!/data/data/com.termux/files/usr/bin/bash
R="$(printf '\033[1;31m')"                           
G="$(printf '\033[1;32m')"
Y="$(printf '\033[1;33m')"
B="$(printf '\033[1;34m')"
C="$(printf '\033[1;36m')"                                       
W="$(printf '\033[0m')" #reset the color
BOLD="$(printf '\033[1m')"

package_install_and_check() {
	packs_list=($@)
for package_name in "${packs_list[@]}"; do
    echo "${R}[${W}-${R}]${G}${BOLD} Installing package: ${C}$package_name ${W}"
	if type -p pacman >/dev/null 2>&1; then
	    pacman -Sy --noconfirm --overwrite '*' "$package_name" &>/dev/null
	else
	   if dpkg -s "$package_name" >/dev/null 2>&1; then
		pkg reinstall "$package_name" -y &>/dev/null
	   else
	    pkg install "$package_name" -y &>/dev/null
	   fi
	fi
    if [ $? -ne 0 ]; then
        echo "${R}[${W}-${R}]${G}${BOLD} Error detected during installation of: ${C}$package_name ${W}"
	  if type -p pacman >/dev/null 2>&1; then
	    pacman -Sy --overwrite '*' $package_name &>/dev/null
	    pacman -Sy --noconfirm $package_name &>/dev/null
	  else
        pkg --fix-broken install -y &>/dev/null
        dpkg --configure -a &>/dev/null
	  fi
        pkg install "$package_name" -y &>/dev/null
    fi
   if type -p pacman >/dev/null 2>&1; then
     if pacman -Qi "$package_name" >/dev/null 2>&1; then
        echo "${R}[${W}-${R}]${G} $package_name installed successfully ${W}"
    else
        if type -p "$package_name" &>/dev/null || [ -e "$PREFIX/bin/$package_name"* ] || [ -e "$PREFIX/bin/"*"$package_name" ]; then
            echo "${R}[${W}-${R}]${C} $package_name ${G}installed successfully ${W}"
        fi
    fi
   else
    if dpkg -s "$package_name" >/dev/null 2>&1; then
        echo "${R}[${W}-${R}]${G} $package_name installed successfully ${W}"
    else
        if type -p "$package_name" &>/dev/null || [ -e "$PREFIX/bin/$package_name"* ] || [ -e "$PREFIX/bin/"*"$package_name" ]; then
            echo "${R}[${W}-${R}]${C} $package_name ${G}installed successfully ${W}"
        fi
    fi
   fi
done
echo ""

}

pip_install_and_check() {
    pip_list=($@)
    for pip_name in "${pip_list[@]}"; do
        echo -e "${R}[${W}-${R}]${G}${BOLD} Installing module: ${C}$pip_name ${W}"
        pip install "$pip_name" &>/dev/null

        # Check if the installation was successful
        if [ $? -ne 0 ]; then
            echo -e "${R}[${W}-${R}]${R}${BOLD} Error installing: ${C}$pip_name ${W}"
        else
            if python3 -c "import $pip_name" &>/dev/null; then
                echo -e "${R}[${W}-${R}]${G} $pip_name installed successfully ${W}"
            else
                echo -e "${R}[${W}-${R}]${R}${BOLD} $pip_name installation failed ${W}"
            fi
	fi
    done
}

clear
echo -e "${G}${BOLD}Updating termux packages list please wait\n"${W}
if type -p pacman >/dev/null 2>&1; then
	pacman -Syu --noconfirm &>/dev/null
	else
    pkg update -y -o Dpkg::Options::="--force-confold" &>/dev/null
	pkg upgrade -y -o Dpkg::Options::="--force-confold" &>/dev/null
	fi
    package_install_and_check "termux-tools"
if type -p apt >/dev/null 2>&1; then
unlink "$PREFIX/etc/termux/chosen_mirrors" &>/dev/null
ln -s "$PREFIX/etc/termux/mirrors/all" "$PREFIX/etc/termux/chosen_mirrors" &>/dev/null
echo -e "${G}${BOLD}Selecting best termux packages mirror please wait\n"${W}
TERMUX_APP_PACKAGE_MANAGER=apt pkg --check-mirror update
clear
echo -e "${G}${BOLD}Upgrading termux packages...this might take some time\n"${W}
yes 2>/dev/null | apt-get full-upgrade &>/dev/null
fi
echo -e "${C}${BOLD}please allow storage permission"${W}
while true; do
	termux-setup-storage
	sleep 4
    if [[ -d ~/storage ]]; then
        break
    else
        echo -e "${R}${BOLD}Storage permission denied\n"${W}
    fi
    sleep 2
done
echo -e "${G}${BOLD}be patient\n"${W}
package_install_and_check "python3 python-pip"
pip_install_and_check "tqdm"
curl -o installglibc.py https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/installglibc.py && python3 installglibc.py
exit