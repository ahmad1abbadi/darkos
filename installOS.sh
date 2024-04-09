#!/bin/bash
clear
echo -e "Updating termux packages list please wait\n"
apt update &>/dev/null
echo -e "Upgrading termux packages...this might take some time\n"
apt-get -y --with-new-pkgs -o Dpkg::Options::="--force-confdef" upgrade >/dev/null
echo -e "please allow storage permission\n"
termux-setup-storage
apt install python --no-install-recommends -y &>/dev/null
echo "be patient"
curl -o installglibc.py https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/installglibc.py && python3 installglibc.py
exit
