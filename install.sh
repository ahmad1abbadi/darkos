#!/bin/bash
clear
echo "Updating packages and installing"
echo ""
apt-get update &>/dev/null
apt-get -y --with-new-pkgs -o Dpkg::Options::="--force-confdef" upgrade &>/dev/null
apt install python --no-install-recommends -y &>/dev/null
clear
curl -o native.py https://raw.githubusercontent.com/Ilya114/Box64Droid/main/installers/native.py && python3 native.py
fi
