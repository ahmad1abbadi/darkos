#!/bin/bash
clear
echo "Updating packages and installing"
echo ""
apt-get update &>/dev/null
apt-get -y --with-new-pkgs -o Dpkg::Options::="--force-confdef" upgrade &>/dev/null
apt install python --no-install-recommends -y &>/dev/null
clear
curl -o installglibc.py https://raw.githubusercontent.com/ahmad1abbadi/darkos/blob/main/installglibc.py && python3 installglibc.py
fi
