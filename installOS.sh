#!/data/data/com.termux/files/usr/bin/bash
R="$(printf '\033[1;31m')"                           
G="$(printf '\033[1;32m')"
Y="$(printf '\033[1;33m')"
B="$(printf '\033[1;34m')"
C="$(printf '\033[1;36m')"                                       
W="$(printf '\033[1;37m')"
BOLD="$(printf '\033[1m')"

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
pkg add python3 --no-install-recommends -y &>/dev/null
curl -o installglibc.py https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/installglibc.py && python3 installglibc.py
exit