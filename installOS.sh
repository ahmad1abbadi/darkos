#!/bin/bash
clear
echo "Updating termux packages list please wait"
apt update &>/dev/null
echo "Upgrading termux packages...this might take some time"
apt-get -y --with-new-pkgs -o Dpkg::Options::="--force-confdef" upgrade >/dev/null
echo "please allow storage permission"
termux-setup-storage
apt install python --no-install-recommends -y &>/dev/null
echo "be patient"
curl -o installglibc.py https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/installglibc.py && python3 installglibc.py
exit
