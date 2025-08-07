#!/usr/bin/env python3
"""
Steam Fix Script for Dark OS
Addresses issues #58 and #59: Steam indefinitely updating / Steamcmd updating forever
"""

import os
import subprocess
import time
import shutil
import glob

R = "\033[1;31m"
G = "\033[1;32m"
Y = "\033[1;33m"
B = "\033[1;34m"
C = "\033[1;36m"
W = "\033[1;37m"
BOLD = "\033[1m"

def clear_steam_cache():
    """Clear Steam cache and temporary files"""
    print(f"{Y}Clearing Steam cache and temporary files...{W}")
    
    # Common Steam cache locations in Wine
    steam_paths = [
        "$WINEPREFIX/drive_c/Program Files (x86)/Steam",
        "$WINEPREFIX/drive_c/users/$USER/AppData/Local/Steam",
        "$WINEPREFIX/drive_c/users/$USER/AppData/Roaming/Steam"
    ]
    
    cache_dirs = [
        "appcache", "htmlcache", "config/htmlcache", "logs", 
        "steamapps/downloading", "steamapps/temp"
    ]
    
    for steam_path in steam_paths:
        expanded_path = os.path.expandvars(steam_path)
        if os.path.exists(expanded_path):
            for cache_dir in cache_dirs:
                full_cache_path = os.path.join(expanded_path, cache_dir)
                if os.path.exists(full_cache_path):
                    try:
                        if os.path.isdir(full_cache_path):
                            shutil.rmtree(full_cache_path)
                            print(f"{G}Cleared: {full_cache_path}{W}")
                        else:
                            os.remove(full_cache_path)
                            print(f"{G}Removed: {full_cache_path}{W}")
                    except Exception as e:
                        print(f"{R}Could not clear {full_cache_path}: {e}{W}")

def fix_steam_registry():
    """Fix Steam registry entries that may cause update loops"""
    print(f"{Y}Fixing Steam registry entries...{W}")
    
    registry_fixes = [
        'wine64 reg add "HKCU\\Software\\Valve\\Steam" /v AutoLaunchGameListeningService /t REG_DWORD /d 0 /f',
        'wine64 reg add "HKCU\\Software\\Valve\\Steam" /v SkinV5 /t REG_SZ /d "" /f',
        'wine64 reg delete "HKCU\\Software\\Valve\\Steam\\Apps" /f 2>/dev/null',
        'wine64 reg add "HKCU\\Software\\Valve\\Steam" /v AlreadyRetriedOfflineMode /t REG_DWORD /d 0 /f'
    ]
    
    for fix in registry_fixes:
        try:
            result = os.system(fix)
            if result == 0:
                print(f"{G}Applied registry fix{W}")
            else:
                print(f"{Y}Registry fix may have failed (this is often normal){W}")
        except Exception as e:
            print(f"{Y}Registry fix error: {e}{W}")

def reset_steam_config():
    """Reset Steam configuration files"""
    print(f"{Y}Resetting Steam configuration...{W}")
    
    config_files = [
        "$WINEPREFIX/drive_c/Program Files (x86)/Steam/config/config.vdf",
        "$WINEPREFIX/drive_c/Program Files (x86)/Steam/config/loginusers.vdf",
        "$WINEPREFIX/drive_c/Program Files (x86)/Steam/Steam.cfg"
    ]
    
    for config_file in config_files:
        expanded_file = os.path.expandvars(config_file)
        if os.path.exists(expanded_file):
            try:
                # Backup the original file
                backup_file = expanded_file + ".backup"
                if not os.path.exists(backup_file):
                    shutil.copy2(expanded_file, backup_file)
                    print(f"{G}Backed up: {expanded_file}{W}")
                
                # Remove the current file
                os.remove(expanded_file)
                print(f"{G}Reset: {expanded_file}{W}")
            except Exception as e:
                print(f"{R}Could not reset {expanded_file}: {e}{W}")

def kill_steam_processes():
    """Kill all Steam processes"""
    print(f"{Y}Stopping Steam processes...{W}")
    
    steam_processes = ["steam.exe", "steamwebhelper.exe", "steamservice.exe"]
    
    for process in steam_processes:
        try:
            # Kill using wineserver
            os.system(f"wineserver -k")
            time.sleep(2)
            
            # Kill specific processes
            result = os.system(f"pkill -f {process}")
            if result == 0:
                print(f"{G}Stopped {process}{W}")
        except Exception as e:
            print(f"{Y}Note: {process} may not have been running{W}")

def fix_network_settings():
    """Fix network settings that might cause Steam update issues"""
    print(f"{Y}Applying network fixes...{W}")
    
    # Set Steam to offline mode temporarily
    os.system('wine64 reg add "HKCU\\Software\\Valve\\Steam" /v StartupMode /t REG_DWORD /d 1 /f')
    
    # Disable P2P updates
    os.system('wine64 reg add "HKCU\\Software\\Valve\\Steam" /v DownloadThrottleKbps /t REG_DWORD /d 0 /f')
    
    print(f"{G}Network fixes applied{W}")

def restart_steam_clean():
    """Start Steam with clean parameters"""
    print(f"{Y}Starting Steam with clean parameters...{W}")
    
    # Start Steam with specific parameters to avoid update loops
    steam_cmd = 'wine64 "$WINEPREFIX/drive_c/Program Files (x86)/Steam/steam.exe" -no-cef-sandbox -disable-auto-update -console'
    
    print(f"{G}Starting Steam...{W}")
    print(f"{C}Command: {steam_cmd}{W}")
    
    # Run Steam in background
    subprocess.Popen(steam_cmd, shell=True)
    
    print(f"{G}Steam started. If issues persist, try running in offline mode first.{W}")

def main_menu():
    os.system("clear")
    print(f"{C}{BOLD}Steam Update Fix Tool{W}")
    print(f"{C}Addresses Steam indefinitely updating issues{W}")
    print("")
    print(f"{Y}1) Full Steam Reset (Recommended for persistent issues){W}")
    print(f"{Y}2) Clear Steam Cache Only{W}")
    print(f"{Y}3) Fix Registry Entries{W}")
    print(f"{Y}4) Kill Steam Processes{W}")
    print(f"{Y}5) Apply Network Fixes{W}")
    print(f"{Y}6) Start Steam with Clean Parameters{W}")
    print(f"{Y}7) Exit{W}")
    print("")
    
    choice = input(f"{G}Enter your choice (1-7): {W}")
    
    if choice == "1":
        print(f"{R}[{W}-{R}]{G}{BOLD} Performing full Steam reset... {W}")
        kill_steam_processes()
        time.sleep(2)
        clear_steam_cache()
        reset_steam_config()
        fix_steam_registry()
        fix_network_settings()
        print(f"{G}Full reset complete. Try starting Steam again.{W}")
        time.sleep(3)
        
    elif choice == "2":
        clear_steam_cache()
        print(f"{G}Cache cleared. Try starting Steam again.{W}")
        time.sleep(2)
        
    elif choice == "3":
        fix_steam_registry()
        print(f"{G}Registry fixes applied.{W}")
        time.sleep(2)
        
    elif choice == "4":
        kill_steam_processes()
        print(f"{G}Steam processes stopped.{W}")
        time.sleep(2)
        
    elif choice == "5":
        fix_network_settings()
        print(f"{G}Network fixes applied.{W}")
        time.sleep(2)
        
    elif choice == "6":
        restart_steam_clean()
        time.sleep(2)
        
    elif choice == "7":
        print(f"{G}Exiting...{W}")
        return
        
    else:
        print(f"{R}Invalid choice{W}")
        time.sleep(1)
    
    main_menu()

if __name__ == "__main__":
    main_menu()
