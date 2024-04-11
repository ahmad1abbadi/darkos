![logo](img/logo.png "logo")

**Darkos** is a project designed to run Windows x86_64 applications and games in [Termux](https://github.com/termux/termux-app) native GLIBC.
It utilizes [Box86](https://github.com/ptitSeb/box86)
and [Box64](https://github.com/ptitSeb/box86)
to run [Wine](https://www.winehq.org/) on android.

# Installation:
1. Install
[Termux](https://f-droid.org/repo/com.termux_118.apk),
[Termux-X11](https://github.com/ahmad1abbadi/extra/releases/download/apps/termux-x11.apk) and
[Input Bridge v0.1.9.9](https://github.com/ahmad1abbadi/extra/releases/download/apps/InputBridge_v0.1.9.9.apk) or [Input Bridge v0.0.7](https://github.com/ahmad1abbadi/extra/releases/download/apps/input+bridge+0.0.7.apk)

2. Open Termux and paste the following command:
```bash
curl -o install https://raw.githubusercontent.com/ahmad1abbadi/darkos/main/installOS.sh && chmod +x install && ./install
```

3. **Darkos** will automatically start after installation is complete.
   Remember each time you open Termux, Darkos will auto-start.
   
   To exit **Darkos** and use Termux normally, press '1' within the first 4 seconds. Otherwise, Darkos will start and run Wine + Termux-X11.
   
# Features:
1. Gstreamer support, which is required for games like:
* resident evil 7
* devil may cry 5
* amid evil
2. Dedicated configuration app

  And many more, you can discover by your self.
# Configuration:

## Box64/Box86 Configuration + Dynarec
The configuration can be easily done from the Darkos configuration app. Simply modify the Box options, click "Apply," and then "Reboot" to apply the changes.

For more information about dynarec variables see [Box64 usage](https://github.com/ptitSeb/box64/blob/main/docs/USAGE.md) and [Box86 usage](https://github.com/ptitSeb/box86/blob/master/docs/USAGE.md)

## Update OS
This option updates Darkos to the latest version.

## Wine Manager 
Wine can be installed or uninstalled from the Darkos configuration embedded within Wine. Simply select the "Wine manager" option.

To select a Wine container, use the container dropdown menu from the Darkos configuration and then click "Change container."


## Debug Mode
This mode enables printing Wine and Box64 debug information to a log file located at /sdcard/darkos/darkos.log. You can share this file to our Telegram group.

## Toggle Mangohud
Mangohud is an on-screen display (OSD) that shows useful information like FPS, CPU usage, GPU load, and GPU temperature.

Currently, to see GPU load and temperature stats, you need to disable SELinux by running the following command in Termux:
```
su -c setenforce 0
```
To re-enable SELinux:

```
su -c setenforce 1
```

## GPU Driver Changer
This option allows you to change the GPU driver.

## Switch IB
This toggle lets you switch the input bridge between version 0.1.9.9 and version 0.0.7. Choose the version that works best for you.

## Kill Services
Use this toggle to kill services.exe without needing to open the task manager.

## Hit F5 key
This will open the task manager.

## DXVK changer 
This option lets you choose the DXVK version, allowing you to select the one that works best for a specific game.

## Install Tweaks
This option lets you install Wine tricks like apps, DLLs, and fonts.

## Personalize
You can change the theme, background, or resolution of the Wine desktop.

## Termux-X11 resolution 
The fallback resolution is only used when the X11 resolution cannot be detected automatically. The default fallback resolution is 800x600.

## Termux and termux-x11 preferences
### recommend setup for termux:
* `Allow apps to open new windows while running in the background`
* `Allow apps to display pop-up windows`

### recommend setup for termux-x11:
* `Display resolution mode` exact
* `Display resolution` 1280x720
* `Reseed Screen While Soft Keyboard is open` OFF
* `Fullscreen on device display` ON
* `Force Landscape orientation` ON
* `Hide display cutout` ON
* `Show additional keyboard` OFF
* `Prefer scancodes when possible` ON
* `Enable Accessibility service for intercepting
system shortcuts manually.` enable termux-x11 from android accessibility menu so you can use external keyboard (wired/wireless) without issues.
* `Enable Accessibility service for intercepting system shortcuts automatically.` ON

## Controls
For touch controls Input Bridge app is required.

## Support status
**Android 10 or higher is recommended.

### Device
* Most Android phones equipped with a Mali GPU can run DirectX 9 games using [Mesa VirGL](https://github.com/alexvorxx/Mesa-VirGL) . It is recommended to use a Snapdragon device with Adreno 6xx or Adreno 7xx for optimal performance and compatibility with Turnip and [DXVK](https://github.com/doitsujin/dxvk).

### Root
* Root is not required.

## Known issues
* termux app can show signal 9 when using wine or while compiling box64, in this case you have to disable phantom process.

## To-do list
* virgl
* support for non Snapdragon chips
  
## Support Darkos
#
Big thanks to our testers:

GhostDz36

#
Huge thanks to:

[airidosas252](https://github.com/airidosas252) for his turnip and wine builds.

#
Special thanks to ptitSeb, Maxython, glibc-runner, hardray, Tωaik and others for help.

[Darkos telegram group](https://t.me/DARKOS4android)

## Third party applications

[glibc-packages](https://github.com/termux-pacman/glibc-packages)

[Box64](https://github.com/ptitSeb/box64)

[Box86](https://github.com/ptitSeb/box86)

[DXVK](https://github.com/doitsujin/dxvk)

[DXVK-ASYNC](https://github.com/Sporif/dxvk-async)

[DXVK-GPLASYNC](https://gitlab.com/Ph42oN/dxvk-gplasync)

[VKD3D](https://github.com/lutris/vkd3d)

[D8VK](https://github.com/AlpyneDreams/d8vk)

[Termux-app](https://github.com/termux/termux-app)

[Termux-x11](https://github.com/termux/termux-x11)

[Wine](https://wiki.winehq.org/Licensing)

[wine-ge-custom](https://github.com/GloriousEggroll/wine-ge-custom)

[Mesa](https://docs.mesa3d.org/license.html)

[Mesa-VirGL](https://github.com/alexvorxx/Mesa-VirGL)
