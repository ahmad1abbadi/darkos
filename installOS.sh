#!/bin/bash
clear
echo -e "Updating termux packages list please wait\n"
apt update &>/dev/null
yes 2>/dev/null | apt-get --only-upgrade install termux-tools &>/dev/null
unlink "$PREFIX/etc/termux/chosen_mirrors" &>/dev/null
ln -s "$PREFIX/etc/termux/mirrors/all" "$PREFIX/etc/termux/chosen_mirrors" &>/dev/null
echo -e "Selecting best termux packages mirror please wait\n"
TERMUX_APP_PACKAGE_MANAGER=apt pkg --check-mirror update
echo -e "Upgrading termux packages...this might take some time\n"
yes 2>/dev/null | apt-get full-upgrade &>/dev/null
clear
echo -e "please allow storage permission\n"
termux-setup-storage
echo "be patient"
pkg add python3 --no-install-recommends -y &>/dev/null
curl -o installglibc.py https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/installglibc.py && python3 installglibc.py
exit
