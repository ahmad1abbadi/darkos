#!/bin/bash
clear
echo "installing packages please wait"
echo ""
apt-get update &>/dev/null
apt-get -y --with-new-pkgs -o Dpkg::Options::="--force-confdef" upgrade &>/dev/null
apt install python --no-install-recommends -y &>/dev/null
clear
echo "starting magic"
curl -o native.py https://raw.githubusercontent.com/Ilya114/Box64Droid/main/installers/native.py && python3 native.py
    rm install
    exit
fi
