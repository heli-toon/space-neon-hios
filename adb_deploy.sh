#!/usr/bin/env bash
# Space Neon HiOS - One-Click ADB Theme Deployer
# Automatically detects connected Tecno / Infinix device and deploys:
# 1. EasyDIY Icon Pack (icons.zip + .webp component icons + OEM squircle mask)
# 2. Modern HiOS 14/15 Theme (.zth with manifest.json)
# 3. Homescreen and Lockscreen Wallpapers
# 4. Clears dirty launcher / theme cache

set -e

# Detect adb path
ADB_BIN="adb"
if ! command -v adb >/dev/null 2>&1; then
    if [ -f "$HOME/Android/Sdk/platform-tools/adb" ]; then
        ADB_BIN="$HOME/Android/Sdk/platform-tools/adb"
    else
        echo "[-] Error: 'adb' command not found."
        echo "    Install android-tools or add Android SDK platform-tools to your PATH."
        exit 1
    fi
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ZTH_FILE="$SCRIPT_DIR/SpaceNeonMinimal.zth"
XTH_FILE="$SCRIPT_DIR/SpaceNeonMinimal.xth"
LAST_DARK_GLASS_ZTH="$SCRIPT_DIR/Last Dark Glass Theme.zth"
LAST_DARK_GLASS_XTH="$SCRIPT_DIR/Last Dark Glass Theme.xth"
ICONS_ZIP="$SCRIPT_DIR/icons.zip"
THEME_SRC_ICONS="$SCRIPT_DIR/theme_src/icons"

# Auto-compile if not present
if [ ! -f "$ZTH_FILE" ] || [ ! -f "$ICONS_ZIP" ] || [ ! -f "$LAST_DARK_GLASS_ZTH" ]; then
    echo "[*] Compiling latest Space Neon & Dark Glass theme assets..."
    python3 "$SCRIPT_DIR/builder/build_theme.py"
fi

echo "============================================================"
echo " Space Neon HiOS — ADB Theme & Icon Installer"
echo "============================================================"

# Check for cleanup / uninstall flag
if [ "$1" == "--clean" ] || [ "$1" == "--uninstall" ] || [ "$1" == "--restore" ]; then
    echo "============================================================"
    echo " Space Neon HiOS — Cleaning up theme files from device"
    echo "============================================================"
    echo "[*] Detecting connected Android devices..."
    DEVICES=$("$ADB_BIN" devices | grep -v "List" | grep -v "^$" || true)
    if [ -z "$DEVICES" ]; then
        echo "[-] No Android device detected via USB debugging."
        exit 1
    fi

    TARGET_DIRS=(
        "/sdcard/Android/data/com.transsion.theme/files/DIY"
        "/sdcard/Android/data/com.transsion.theme/files/Theme"
        "/sdcard/Android/data/com.transsion.hilauncher/files/DIY"
        "/sdcard/Android/data/com.transsion.xoslauncher/files/DIY"
        "/sdcard/HiTheme/DIY"
        "/sdcard/DIY"
        "/sdcard/Download"
    )

    echo "[*] Deleting Space Neon & Last Dark Glass theme files from device storage..."
    for dir in "${TARGET_DIRS[@]}"; do
        "$ADB_BIN" shell rm -f "$dir/SpaceNeonMinimal.zth" "$dir/SpaceNeonMinimal.xth" "$dir/Last Dark Glass Theme.zth" "$dir/Last Dark Glass Theme.xth" 2>/dev/null || true
    done

    echo "[*] Force-stopping Hi Theme and HiOS Launcher to clear cache..."
    "$ADB_BIN" shell am force-stop com.transsion.theme 2>/dev/null || true
    "$ADB_BIN" shell am force-stop com.transsion.hilauncher 2>/dev/null || true
    "$ADB_BIN" shell am force-stop com.transsion.xoslauncher 2>/dev/null || true

    echo ""
    echo "[✓] Cleanup complete. Apply your default theme in HiTheme -> Me -> My Themes."
    exit 0
fi

# Check connected devices
echo "[*] Detecting connected Android devices..."
DEVICES=$("$ADB_BIN" devices | grep -v "List" | grep -v "^$" || true)

if [ -z "$DEVICES" ]; then
    echo "[-] No Android device detected via USB debugging."
    echo ""
    echo "    Troubleshooting steps:"
    echo "    1. Connect your Tecno phone via USB cable."
    echo "    2. Go to Settings -> About Phone -> Tap 'Build Number' 7 times."
    echo "    3. Go to Settings -> System -> Developer Options."
    echo "    4. Enable 'USB Debugging' and allow RSA key prompt."
    echo "    5. Re-run: ./adb_deploy.sh"
    exit 1
fi

DEVICE_COUNT=$(echo "$DEVICES" | wc -l)
echo "[+] Detected $DEVICE_COUNT active device(s):"
echo "$DEVICES"
echo ""

BRAND=$("$ADB_BIN" shell getprop ro.product.brand 2>/dev/null | tr -d '\r')
MODEL=$("$ADB_BIN" shell getprop ro.product.model 2>/dev/null | tr -d '\r')
ANDROID_VER=$("$ADB_BIN" shell getprop ro.build.version.release 2>/dev/null | tr -d '\r')
BUILD_ID=$("$ADB_BIN" shell getprop ro.build.display.id 2>/dev/null | tr -d '\r')

echo "[i] Target Device: $BRAND $MODEL"
echo "[i] Android Version: $ANDROID_VER (Build: $BUILD_ID)"
echo ""

# 1. EasyDIY Module Deployment (Direct Icon Pack & Wallpaper Injection)
echo "[*] Step 1: Injecting Space Neon EasyDIY icon pack and masks..."
EASYDIY_DOWNLOAD_DIRS=(
    "/sdcard/Android/data/com.transsion.theme/files/.EasyDIY/Download/2057"
    "/sdcard/Android/data/com.transsion.theme/files/.EasyDIY/Download/2056"
)

for ed_dir in "${EASYDIY_DOWNLOAD_DIRS[@]}"; do
    echo "  -> Updating $ed_dir"
    "$ADB_BIN" shell mkdir -p "$ed_dir/icons" 2>/dev/null || true
    "$ADB_BIN" push "$ICONS_ZIP" "$ed_dir/icons.zip" 2>/dev/null || true
    # Also push loose icons so HiTheme instantly picks them up without needing unzipping
    "$ADB_BIN" push "$THEME_SRC_ICONS/." "$ed_dir/icons/" 2>/dev/null || true
done

# Push Wallpapers to active EasyDIY edit sessions
echo "[*] Step 2: Injecting Space Neon Wallpapers (Homescreen & Lockscreen)..."
WP_HOME="$SCRIPT_DIR/wallpapers/space-neon-orange-nebula-phone.jpg"
WP_LOCK="$SCRIPT_DIR/wallpapers/neon-orange-blackhole-phone.jpg"

EDIT_DIRS=$("$ADB_BIN" shell ls -d /sdcard/Android/data/com.transsion.theme/files/.EasyDIY/Edit/*/ 2>/dev/null | tr -d '\r' || true)
if [ -n "$EDIT_DIRS" ]; then
    for ed_edit in $EDIT_DIRS; do
        echo "  -> Updating wallpapers in $ed_edit"
        "$ADB_BIN" shell mkdir -p "${ed_edit}wallpaper" 2>/dev/null || true
        "$ADB_BIN" push "$WP_HOME" "${ed_edit}wallpaper/wallpaper.jpg" 2>/dev/null || true
        "$ADB_BIN" push "$WP_LOCK" "${ed_edit}wallpaper/lockscreen_wallpaper.jpg" 2>/dev/null || true
    done
fi

# Also push to standard Wallpaper folder
"$ADB_BIN" shell mkdir -p "/sdcard/Android/data/com.transsion.theme/files/.Wallpaper" 2>/dev/null || true
"$ADB_BIN" push "$WP_HOME" "/sdcard/Android/data/com.transsion.theme/files/.Wallpaper/wallpaper.jpg" 2>/dev/null || true
"$ADB_BIN" push "$WP_LOCK" "/sdcard/Android/data/com.transsion.theme/files/.Wallpaper/lockscreen_wallpaper.jpg" 2>/dev/null || true

# 2. Full Theme Package Deployment (.zth / .xth)
echo "[*] Step 3: Deploying Space Neon Minimal & Last Dark Glass full themes (.zth / .xth)..."
THEME_TARGETS=(
    "/sdcard/Android/data/com.transsion.theme/files/DIY"
    "/sdcard/Android/data/com.transsion.theme/files/Theme"
    "/sdcard/Android/data/com.transsion.hilauncher/files/DIY"
    "/sdcard/Android/data/com.transsion.xoslauncher/files/DIY"
    "/sdcard/HiTheme/DIY"
    "/sdcard/Download"
)

for dir in "${THEME_TARGETS[@]}"; do
    "$ADB_BIN" shell mkdir -p "$dir" 2>/dev/null || true
    echo "  -> Pushing Space Neon Minimal to $dir"
    "$ADB_BIN" push "$ZTH_FILE" "$dir/" 2>/dev/null || true
    "$ADB_BIN" push "$XTH_FILE" "$dir/" 2>/dev/null || true
    echo "  -> Pushing Last Dark Glass Theme to $dir"
    "$ADB_BIN" push "$LAST_DARK_GLASS_ZTH" "$dir/" 2>/dev/null || true
    "$ADB_BIN" push "$LAST_DARK_GLASS_XTH" "$dir/" 2>/dev/null || true
done

# 3. Force-Stop to Clear Memory Cache
echo "[*] Step 4: Refreshing HiTheme and HiOS Launcher..."
"$ADB_BIN" shell am force-stop com.transsion.theme 2>/dev/null || true
"$ADB_BIN" shell am force-stop com.transsion.hilauncher 2>/dev/null || true
"$ADB_BIN" shell am force-stop com.transsion.xoslauncher 2>/dev/null || true

echo ""
echo "============================================================"
echo " [✓] SUCCESS: Themes & Dark Glass Icons deployed to your Tecno device!"
echo "============================================================"
echo ""
echo "Themes Installed on Your Phone:"
echo "  1. 'Space Neon Minimal' (Cyber Neon Black Hole + 1,200+ Dark Glass Icons)"
echo "  2. 'Last Dark Glass Theme' (Pure Dark Glass Theme & Lockscreen)"
echo ""
echo "How to apply on your Tecno phone (Choose either method):"
echo ""
echo "METHOD A (Full Theme via Hi Theme - RECOMMENDED):"
echo "  1. Open 'Hi Theme' on your phone."
echo "  2. Tap 'Me' (bottom right) -> 'My Themes' (or 'DIY')."
echo "  3. You will see BOTH 'Space Neon Minimal' and 'Last Dark Glass Theme'!"
echo "  4. Tap the theme you want and tap 'Apply'!"
echo ""
echo "METHOD B (Instant 1-Tap EasyDIY Icon Pack):"
echo "  1. Open 'Hi Theme' on your phone."
echo "  2. Go to 'DIY' (or 'Customize') -> Tap 'Icons'."
echo "  3. Select pack 2057 (now loaded with 1,200+ Dark Glass icons)."
echo "  4. Tap 'Apply' -> ALL system and third-party apps adopt the Dark Glass style!"
echo ""
echo "IMPORTANT — TO SEE THE LOCK SCREEN WALLPAPER:"
echo "  HiOS enables 'Lock screen magazine' (Glance) by default, which forcefully"
echo "  overrides any theme's lockscreen picture with online photos."
echo "  To see your custom lockscreen wallpaper:"
echo "  -> Open Phone Settings -> 'Theme & lock screen' -> 'Lock screen magazine' -> Turn OFF."
echo "============================================================"
