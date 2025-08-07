import os, time, shutil, sys, subprocess, urllib.request, urllib.error, fnmatch

R = "\033[1;31m"
G = "\033[1;32m"
Y = "\033[1;33m"
B = "\033[1;34m"
C = "\033[1;36m"
W = "\033[1;37m"
BOLD = "\033[1m"

current_version = "0.971"
url = 'https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/currently%20version.txt'

def remove():
    """Remove tar.xz files from home directory"""
    folder_path = '/data/data/com.termux/files/home'
    try:
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                if fnmatch.fnmatch(filename, '*.tar.xz*'):
                    file_path = os.path.join(folder_path, filename)
                    try:
                        os.remove(file_path)
                        print(f'{filename} has been deleted.')
                    except Exception as e:
                        print(f"Error deleting {filename}: {e}")
        else:
            print(f"Directory {folder_path} does not exist.")
    except Exception as e:
        print(f"Error in remove function: {e}")

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

# Main update process
try:
    safe_system_command("am start -n com.termux/.HomeActivity")
    safe_system_command("clear")
    safe_system_command("python3 $PREFIX/bin/photo.py")
    time.sleep(2)   
    print("")
    print(f"{R}[{W}-{R}]{G}{BOLD} Shutdown OS.... {W}")
    print("")
    print(f"{R}[{W}-{R}]{G}{BOLD} checking 🔎..... {W}")
    time.sleep(1)
    
    # Check for updates with error handling
    response = urllib.request.urlopen(url)
    latest_version = response.read().decode('utf-8').strip()
    
    if latest_version > current_version:
        print(f"{R}[{W}-{R}]{G}{BOLD} update available..... {C}updating......📥 {W}")
        
        # Remove old files
        files_to_remove = [
            "darkos.py", "update-darkos.py", "run-darkos.py", 
            "debug-darkos.py", "setting-darkos.py", "darkos"
        ]
        for file in files_to_remove:
            safe_system_command(f"rm $PREFIX/bin/{file}", f"removing {file}")
        
        # Download new files
        download_commands = [
            "wget -O run-darkos.py https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/run-darkos.py",
            "wget -O darkos.py https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/darkos.py",
            "wget -O darkos https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/darkos",
            "wget -O debug-darkos.py https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/debug-darkos.py",
            "wget -O setting-darkos.py https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/setting-darkos.py",
            "wget -O update-darkos.py https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/update-darkos.py",
            "wget -O new-update.py https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/new-update.py"
        ]
        
        for cmd in download_commands:
            safe_system_command(cmd, "downloading files")
        
        safe_system_command("chmod +x darkos", "making darkos executable")
        safe_system_command("mv update-darkos.py darkos.py run-darkos.py debug-darkos.py setting-darkos.py darkos $PREFIX/bin/", "moving files to bin")
        safe_system_command("python3 new-update.py", "running new-update.py")
        time.sleep(2)
        remove()
        safe_system_command("rm new-update.py", "removing new-update.py")
        print(f"{R}[{W}-{R}]{G}{BOLD} update completed 🎉 {W}")
        print(f"{G}{BOLD} rebooting.... {W}")
        time.sleep(3)
    else:
        print(f"{C} no update available {W}")
        time.sleep(3)
        
except urllib.error.HTTPError as e:
    if e.code == 404:
        print(f"{R} no internet connection 😵 {C}rebooting..... {W}")
        time.sleep(2)
    else:
        print(f"{R} HTTP Error {e.code}: {e.reason} {W}")
        time.sleep(2)
except Exception as e:
    print(f"{R} Error during update: {e} {W}")
    time.sleep(2)

# Final reboot
safe_system_command("python3 $PREFIX/bin/run-darkos.py", "rebooting system")
