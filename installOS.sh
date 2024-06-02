#!/data/data/com.termux/files/usr/bin/bash
R="$(printf '\033[1;31m')"                           
G="$(printf '\033[1;32m')"
Y="$(printf '\033[1;33m')"
B="$(printf '\033[1;34m')"
C="$(printf '\033[1;36m')"                                       
W="$(printf '\033[1;37m')"
BOLD="$(printf '\033[1m')"

package_install_and_check() {
	packs_list=($@)
	for package_name in "${packs_list[@]}"; do
    echo "${R}[${W}-${R}]${G}${BOLD} Installing package: ${C}$package_name "${W}
    pkg install "$package_name" -y &>/dev/null
	if [ $? -ne 0 ]; then
    apt --fix-broken install -y
	dpkg --Configuring -a
    fi
	if dpkg -s "$package_name" >/dev/null 2>&1; then
    echo "${R}[${W}-${R}]${G} $package_name installed successfully "${W}
	else
	if
    type -p "$package_name" &>/dev/null || [ -e "$PREFIX/bin/$package_name"* ] || [ -e "$PREFIX/bin/"*"$package_name" ]; then
        echo "${R}[${W}-${R}]${C} $package_name ${G}installed successfully "${W}
	fi
    fi
done

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
apt update &>/dev/null
yes 2>/dev/null | apt-get --only-upgrade install termux-tools &>/dev/null
unlink "$PREFIX/etc/termux/chosen_mirrors" &>/dev/null
ln -s "$PREFIX/etc/termux/mirrors/all" "$PREFIX/etc/termux/chosen_mirrors" &>/dev/null
echo -e "${G}${BOLD}Selecting best termux packages mirror please wait\n"${W}
TERMUX_APP_PACKAGE_MANAGER=apt pkg --check-mirror update
clear
echo -e "${G}${BOLD}Upgrading termux packages...this might take some time\n"${W}
yes 2>/dev/null | apt-get full-upgrade &>/dev/null
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