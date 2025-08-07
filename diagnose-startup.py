#!/usr/bin/env python3
"""
Dark OS Startup Diagnostic and Fix Tool
Addresses issue #39: Dark OS is not opening
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

def check_termux_x11():
    """Check if Termux-X11 is properly installed and configured"""
    print(f"{Y}Checking Termux-X11 installation...{W}")
    
    # Check if termux-x11 command exists
    if os.system("which termux-x11 >/dev/null 2>&1") != 0:
        print(f"{R}✗ termux-x11 command not found{W}")
        return False
    
    print(f"{G}✓ termux-x11 command found{W}")
    
    # Check if Termux-X11 app is installed
    result = subprocess.run(['pm', 'list', 'packages', 'com.termux.x11'], 
                          capture_output=True, text=True)
    
    if 'com.termux.x11' not in result.stdout:
        print(f"{R}✗ Termux-X11 app not installed{W}")
        print(f"{Y}  Please install Termux-X11 from GitHub releases{W}")
        return False
    
    print(f"{G}✓ Termux-X11 app is installed{W}")
    return True

def check_glibc_installation():
    """Check if glibc is properly installed"""
    print(f"{Y}Checking glibc installation...{W}")
    
    glibc_path = "/data/data/com.termux/files/usr/glibc"
    if not os.path.exists(glibc_path):
        print(f"{R}✗ glibc directory not found: {glibc_path}{W}")
        return False
    
    print(f"{G}✓ glibc directory exists{W}")
    
    # Check critical glibc components
    critical_components = [
        "/data/data/com.termux/files/usr/glibc/bin/box64",
        "/data/data/com.termux/files/usr/glibc/bin/box86"
    ]
    
    all_good = True
    for component in critical_components:
        if os.path.exists(component) and os.access(component, os.X_OK):
            print(f"{G}✓ {os.path.basename(component)} is executable{W}")
        elif os.path.exists(component):
            print(f"{Y}! {os.path.basename(component)} exists but not executable{W}")
            try:
                os.chmod(component, 0o755)
                print(f"{G}  Fixed permissions for {os.path.basename(component)}{W}")
            except:
                print(f"{R}  Could not fix permissions{W}")
                all_good = False
        else:
            print(f"{R}✗ {os.path.basename(component)} not found{W}")
            all_good = False
    
    return all_good

def check_wine_installation():
    """Check if Wine is properly installed"""
    print(f"{Y}Checking Wine installation...{W}")
    
    wine_containers = [1, 2, 3]
    wine_found = False
    
    for container in wine_containers:
        wine_path = f"/data/data/com.termux/files/usr/glibc/opt/wine/{container}/wine/bin/wine"
        wine64_path = f"/data/data/com.termux/files/usr/glibc/opt/wine/{container}/wine/bin/wine64"
        
        if os.path.exists(wine_path) or os.path.exists(wine64_path):
            print(f"{G}✓ Wine container {container} found{W}")
            wine_found = True
            
            # Check if wine is executable
            if os.path.exists(wine_path) and not os.access(wine_path, os.X_OK):
                print(f"{Y}  Fixing wine permissions...{W}")
                os.chmod(wine_path, 0o755)
            
            if os.path.exists(wine64_path) and not os.access(wine64_path, os.X_OK):
                print(f"{Y}  Fixing wine64 permissions...{W}")
                os.chmod(wine64_path, 0o755)
    
    if not wine_found:
        print(f"{R}✗ No Wine installation found{W}")
        return False
    
    return True

def check_display_environment():
    """Check display environment variables and setup"""
    print(f"{Y}Checking display environment...{W}")
    
    # Start X11 server if not running
    print(f"{Y}Starting X11 server...{W}")
    os.system("pkill -f termux-x11 2>/dev/null")
    time.sleep(1)
    os.system("termux-x11 :0 >/dev/null 2>&1 &")
    time.sleep(3)
    
    # Test display connection
    result = os.system("DISPLAY=:0 xset q >/dev/null 2>&1")
    if result == 0:
        print(f"{G}✓ Display :0 is accessible{W}")
        return True
    else:
        print(f"{R}✗ Cannot connect to display :0{W}")
        
        # Try alternative displays
        for display in [":1", ":2"]:
            result = os.system(f"DISPLAY={display} xset q >/dev/null 2>&1")
            if result == 0:
                print(f"{G}✓ Display {display} is accessible{W}")
                os.environ['DISPLAY'] = display
                return True
        
        print(f"{R}✗ No accessible display found{W}")
        return False

def check_storage_permissions():
    """Check if storage permissions are granted"""
    print(f"{Y}Checking storage permissions...{W}")
    
    storage_path = os.path.expanduser("~/storage")
    if os.path.exists(storage_path):
        print(f"{G}✓ Storage permission granted{W}")
        return True
    else:
        print(f"{R}✗ Storage permission not granted{W}")
        print(f"{Y}  Run: termux-setup-storage{W}")
        return False

def check_darkos_files():
    """Check if Dark OS files are present"""
    print(f"{Y}Checking Dark OS files...{W}")
    
    required_paths = [
        "/sdcard/darkos",
        "/data/data/com.termux/files/usr/glibc/opt",
        "/data/data/com.termux/files/usr/glibc/opt/apps"
    ]
    
    all_present = True
    for path in required_paths:
        if os.path.exists(path):
            print(f"{G}✓ {path} exists{W}")
        else:
            print(f"{R}✗ {path} missing{W}")
            all_present = False
    
    return all_present

def fix_common_issues():
    """Apply common fixes for startup issues"""
    print(f"{Y}Applying common fixes...{W}")
    
    fixes_applied = 0
    
    # Fix 1: Clean up any stale lock files
    try:
        lock_files = glob.glob("/tmp/.X*-lock")
        for lock_file in lock_files:
            os.remove(lock_file)
            fixes_applied += 1
        if lock_files:
            print(f"{G}✓ Removed {len(lock_files)} X11 lock files{W}")
    except:
        pass
    
    # Fix 2: Reset display environment
    try:
        if 'DISPLAY' in os.environ:
            del os.environ['DISPLAY']
        os.environ['DISPLAY'] = ':0'
        print(f"{G}✓ Reset DISPLAY environment variable{W}")
        fixes_applied += 1
    except:
        pass
    
    # Fix 3: Fix Wine server issues
    try:
        os.system("wineserver -k >/dev/null 2>&1")
        time.sleep(1)
        print(f"{G}✓ Stopped Wine server{W}")
        fixes_applied += 1
    except:
        pass
    
    # Fix 4: Clear temporary files
    try:
        temp_patterns = [
            "/tmp/wine-*",
            "/tmp/.wine-*",
            "/data/data/com.termux/files/usr/tmp/wine*"
        ]
        
        cleaned = 0
        for pattern in temp_patterns:
            files = glob.glob(pattern)
            for file in files:
                try:
                    if os.path.isdir(file):
                        shutil.rmtree(file)
                    else:
                        os.remove(file)
                    cleaned += 1
                except:
                    pass
        
        if cleaned > 0:
            print(f"{G}✓ Cleaned {cleaned} temporary files{W}")
            fixes_applied += 1
    except:
        pass
    
    return fixes_applied

def test_startup():
    """Test if Dark OS can start"""
    print(f"{Y}Testing Dark OS startup...{W}")
    
    # Try to start a simple Wine application
    test_cmd = "DISPLAY=:0 timeout 10 wine64 --version >/dev/null 2>&1"
    result = os.system(test_cmd)
    
    if result == 0:
        print(f"{G}✓ Wine can start successfully{W}")
        return True
    else:
        print(f"{R}✗ Wine failed to start{W}")
        return False

def main():
    os.system("clear")
    print(f"{C}{BOLD}Dark OS Startup Diagnostic Tool{W}")
    print(f"{C}Checking for common startup issues...{W}")
    print("")
    
    checks = [
        ("Termux-X11", check_termux_x11),
        ("glibc", check_glibc_installation),
        ("Wine", check_wine_installation),
        ("Display", check_display_environment),
        ("Storage", check_storage_permissions),
        ("Dark OS Files", check_darkos_files)
    ]
    
    passed_checks = 0
    total_checks = len(checks)
    
    for name, check_func in checks:
        print(f"{R}[{W}{name}{R}]{W}")
        if check_func():
            passed_checks += 1
        print("")
    
    print(f"{G}Diagnostic Summary: {passed_checks}/{total_checks} checks passed{W}")
    print("")
    
    if passed_checks < total_checks:
        print(f"{Y}Applying fixes for detected issues...{W}")
        fixes = fix_common_issues()
        print(f"{G}Applied {fixes} fixes{W}")
        print("")
    
    # Final test
    print(f"{Y}Running final startup test...{W}")
    if test_startup():
        print(f"{G}Dark OS should now be able to start!{W}")
        print(f"{Y}Try running 'darkos' again{W}")
    else:
        print(f"{R}Startup test failed.{W}")
        print(f"{Y}Manual intervention may be required.{W}")
        print("")
        print(f"{Y}Common solutions:{W}")
        print(f"{W}- Reinstall Termux-X11 app{W}")
        print(f"{W}- Run: termux-setup-storage{W}")
        print(f"{W}- Restart Termux completely{W}")
        print(f"{W}- Check if your device supports hardware acceleration{W}")
    
    print("")
    input(f"{Y}Press Enter to exit...{W}")

if __name__ == "__main__":
    main()
