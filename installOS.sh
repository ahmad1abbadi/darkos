#!/data/data/com.termux/files/usr/bin/bash
clear
echo -e "Updating termux packages list please wait\n"
apt update &>/dev/null
echo -e "Upgrading termux packages...this might take some time\n"
yes | apt-get full-upgrade &>/dev/null
unlink "$PREFIX/etc/termux/chosen_mirrors" &>/dev/null
ln -s "$PREFIX/etc/termux/mirrors/all" "$PREFIX/etc/termux/chosen_mirrors" &>/dev/null
echo -e "Selecting best termux packages mirror please wait\n"
TERMUX_APP_PACKAGE_MANAGER=apt pkg --check-mirror update
echo -e "please allow storage permission\n"
while true; do
	termux-setup-storage
	sleep 4
    if [[ -d ~/storage ]]; then
        break
    else
        echo "Storage permission denied\n"
    fi
    sleep 2
done

apt install python --no-install-recommends -y &>/dev/null
echo "be patient"
curl -o installglibc.py https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/installglibc.py && python3 installglibc.py
exit
