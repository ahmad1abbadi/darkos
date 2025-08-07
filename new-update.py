import os, time, shutil, sys, subprocess, urllib.request, urllib.error, fnmatch

R = "\033[1;31m"
G = "\033[1;32m"
Y = "\033[1;33m"
B = "\033[1;34m"
C = "\033[1;36m"
W = "\033[1;37m"
BOLD = "\033[1m"

file_path = "/data/data/com.termux/files/usr/glibc/opt/box/V2.8( 5 june).tar.xz"
file_path2 = "/data/data/com.termux/files/usr/glibc/opt/box/V2.8( 3 july).tar.xz"
file_path3 = "/data/data/com.termux/files/usr/glibc/opt/box/V2.7( 3 mar).tar.xz"
file_path4 = "/data/data/com.termux/files/usr/glibc/opt/box/V2.7( 14 feb).tar.xz"

def update_remove():
    """Remove old update files if they exist"""
    files_to_remove = [file_path, file_path2, file_path3, file_path4]
    
    for filepath in files_to_remove:
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"Removed old file: {filepath}")
        except Exception as e:
            print(f"Error removing {filepath}: {e}")

def safe_system_command(command, description=""):
    """Execute system command with error handling"""
    try:
        result = os.system(command)
        if result != 0 and description:
            print(f"Warning: {description} returned exit code {result}")
        return result
    except Exception as e:
        print(f"Error executing command '{command}': {e}")
        return -1

def pg():
    """Install additional packages"""
    try:
        print("Installing traceroute and samba...")
        safe_system_command("apt install traceroute samba -y", "installing packages")
    except Exception as e:
        print(f"Error in pg function: {e}")

def mangohud():
    """Download and install mangohud"""
    try:
        print("Downloading mangohud...")
        result = safe_system_command("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/mangohud.tar.xz", "downloading mangohud")
        if result == 0 and os.path.exists("mangohud.tar.xz"):
            safe_system_command("tar -xJvf mangohud.tar.xz -C $PREFIX/glibc &>/dev/null", "extracting mangohud")
            os.remove("mangohud.tar.xz")
            print("Mangohud installed successfully")
        else:
            print("Failed to download mangohud")
    except Exception as e:
        print(f"Error in mangohud function: {e}")

def update():
    """Download and extract update"""
    try:
        print("Downloading update...")
        result = safe_system_command("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/update.tar.xz", "downloading update")
        if result == 0 and os.path.exists("update.tar.xz"):
            safe_system_command("tar -xJf update.tar.xz", "extracting update")
            os.remove("update.tar.xz")
            print("Update extracted successfully")
        else:
            print("Failed to download update")
    except Exception as e:
        print(f"Error in update function: {e}")

def update_files():
    """Download and update system files"""
    try:
        print("Downloading system files...")
        result = safe_system_command("wget -q --show-progress https://github.com/ahmad1abbadi/darkos/releases/download/beta/files.tar.xz", "downloading files")
        if result == 0 and os.path.exists("files.tar.xz"):
            safe_system_command("tar -xJf files.tar.xz -C /data/data/com.termux/files/", "extracting files")
            os.remove("files.tar.xz")
            print("System files updated successfully")
        else:
            print("Failed to download system files")
    except Exception as e:
        print(f"Error in update_files function: {e}")

# Main update process
current_version = "0.971"

try:
    print(f"Starting update process for version {current_version}")
    update_remove()
    update_files()
    pg()
    print(f"{G}Update complete for version {current_version}{W}")
    time.sleep(2)
except Exception as e:
    print(f"{R}Error during update: {e}{W}")
    time.sleep(2)

exit()
