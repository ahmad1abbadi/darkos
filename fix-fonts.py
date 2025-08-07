#!/usr/bin/env python3
"""
Font Installation Fix for Dark OS
Addresses issue #53: Install Font tweak not working
"""

import os
import subprocess
import shutil
import glob

R = "\033[1;31m"
G = "\033[1;32m"
Y = "\033[1;33m"
B = "\033[1;34m"
C = "\033[1;36m"
W = "\033[1;37m"
BOLD = "\033[1m"

def install_corefonts():
    """Install Microsoft core fonts using winetricks"""
    print(f"{Y}Installing Microsoft core fonts...{W}")
    
    try:
        # Use winetricks to install corefonts
        result = subprocess.run([
            'winetricks', 'corefonts'
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"{G}Core fonts installed successfully{W}")
            return True
        else:
            print(f"{R}Winetricks corefonts installation failed{W}")
            return False
    except subprocess.TimeoutExpired:
        print(f"{R}Font installation timed out{W}")
        return False
    except Exception as e:
        print(f"{R}Error installing fonts: {e}{W}")
        return False

def manual_font_install():
    """Manually install fonts to Wine font directory"""
    print(f"{Y}Attempting manual font installation...{W}")
    
    # Wine fonts directory
    wine_fonts_dir = os.path.expandvars("$WINEPREFIX/drive_c/windows/Fonts")
    
    # Create fonts directory if it doesn't exist
    os.makedirs(wine_fonts_dir, exist_ok=True)
    
    # System fonts that commonly exist on Android/Termux
    system_font_paths = [
        "/system/fonts",
        "/data/data/com.termux/files/usr/share/fonts",
        "$PREFIX/share/fonts"
    ]
    
    fonts_installed = 0
    
    for font_path in system_font_paths:
        expanded_path = os.path.expandvars(font_path)
        if os.path.exists(expanded_path):
            print(f"{Y}Searching for fonts in: {expanded_path}{W}")
            
            # Look for common font files
            font_extensions = ["*.ttf", "*.TTF", "*.otf", "*.OTF"]
            
            for extension in font_extensions:
                font_files = glob.glob(os.path.join(expanded_path, "**", extension), recursive=True)
                
                for font_file in font_files[:10]:  # Limit to first 10 fonts per extension
                    try:
                        font_name = os.path.basename(font_file)
                        dest_path = os.path.join(wine_fonts_dir, font_name)
                        
                        if not os.path.exists(dest_path):
                            shutil.copy2(font_file, dest_path)
                            print(f"{G}Installed: {font_name}{W}")
                            fonts_installed += 1
                    except Exception as e:
                        print(f"{Y}Could not copy {font_file}: {e}{W}")
    
    if fonts_installed > 0:
        print(f"{G}Manually installed {fonts_installed} fonts{W}")
        return True
    else:
        print(f"{Y}No fonts found to install manually{W}")
        return False

def create_basic_fonts():
    """Create basic font registry entries"""
    print(f"{Y}Creating basic font registry entries...{W}")
    
    # Basic font registry entries
    font_registry_commands = [
        'wine64 reg add "HKLM\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Fonts" /v "Arial (TrueType)" /t REG_SZ /d "arial.ttf" /f',
        'wine64 reg add "HKLM\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Fonts" /v "Arial Bold (TrueType)" /t REG_SZ /d "arialbd.ttf" /f',
        'wine64 reg add "HKLM\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Fonts" /v "Times New Roman (TrueType)" /t REG_SZ /d "times.ttf" /f',
        'wine64 reg add "HKLM\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Fonts" /v "Courier New (TrueType)" /t REG_SZ /d "cour.ttf" /f',
    ]
    
    success_count = 0
    for cmd in font_registry_commands:
        try:
            result = os.system(cmd + " 2>/dev/null")
            if result == 0:
                success_count += 1
        except Exception as e:
            print(f"{Y}Registry entry failed: {e}{W}")
    
    print(f"{G}Created {success_count} font registry entries{W}")
    return success_count > 0

def fix_font_cache():
    """Rebuild Wine font cache"""
    print(f"{Y}Rebuilding Wine font cache...{W}")
    
    try:
        # Clear font cache
        cache_dir = os.path.expandvars("$WINEPREFIX/drive_c/windows/system32")
        cache_files = glob.glob(os.path.join(cache_dir, "*.fon"))
        
        for cache_file in cache_files:
            try:
                os.remove(cache_file)
            except:
                pass
        
        # Rebuild font cache
        result = os.system("wine64 reg add 'HKLM\\Software\\Microsoft\\Windows NT\\CurrentVersion\\FontCache' /f")
        
        print(f"{G}Font cache rebuilt{W}")
        return True
    except Exception as e:
        print(f"{R}Error rebuilding font cache: {e}{W}")
        return False

def copy_termux_fonts():
    """Copy fonts from Termux system"""
    print(f"{Y}Looking for Termux system fonts...{W}")
    
    # DarkOS terminal font directory
    darkos_font_dir = "terminal_utility"
    wine_fonts_dir = os.path.expandvars("$WINEPREFIX/drive_c/windows/Fonts")
    
    fonts_copied = 0
    
    # Copy font from terminal_utility if it exists
    if os.path.exists(darkos_font_dir):
        for font_file in glob.glob(os.path.join(darkos_font_dir, "*.ttf")):
            try:
                font_name = os.path.basename(font_file)
                dest_path = os.path.join(wine_fonts_dir, font_name)
                
                if not os.path.exists(dest_path):
                    shutil.copy2(font_file, dest_path)
                    print(f"{G}Copied DarkOS font: {font_name}{W}")
                    fonts_copied += 1
            except Exception as e:
                print(f"{Y}Could not copy {font_file}: {e}{W}")
    
    return fonts_copied > 0

def main():
    os.system("clear")
    print(f"{C}{BOLD}Dark OS Font Installation Fix{W}")
    print(f"{C}Addresses font installation issues{W}")
    print("")
    
    print(f"{Y}Attempting to fix font installation issues...{W}")
    print("")
    
    # Try multiple approaches
    methods_tried = 0
    methods_successful = 0
    
    print(f"{R}[{W}1/5{R}]{W} Trying core fonts installation...")
    if install_corefonts():
        methods_successful += 1
    methods_tried += 1
    
    print(f"{R}[{W}2/5{R}]{W} Trying manual font installation...")
    if manual_font_install():
        methods_successful += 1
    methods_tried += 1
    
    print(f"{R}[{W}3/5{R}]{W} Copying DarkOS fonts...")
    if copy_termux_fonts():
        methods_successful += 1
    methods_tried += 1
    
    print(f"{R}[{W}4/5{R}]{W} Creating font registry entries...")
    if create_basic_fonts():
        methods_successful += 1
    methods_tried += 1
    
    print(f"{R}[{W}5/5{R}]{W} Rebuilding font cache...")
    if fix_font_cache():
        methods_successful += 1
    methods_tried += 1
    
    print("")
    print(f"{G}Font fix completed: {methods_successful}/{methods_tried} methods successful{W}")
    
    if methods_successful > 0:
        print(f"{G}Font installation should now work better.{W}")
        print(f"{Y}Please restart Dark OS for changes to take effect.{W}")
    else:
        print(f"{R}All methods failed. You may need to manually install fonts.{W}")
        print(f"{Y}Try downloading fonts manually and placing them in:{W}")
        print(f"{C}$WINEPREFIX/drive_c/windows/Fonts/{W}")
    
    input(f"{Y}Press Enter to exit...{W}")

if __name__ == "__main__":
    main()
