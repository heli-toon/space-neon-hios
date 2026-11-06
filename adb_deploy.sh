#!/usr/bin/env bash
# Space Neon HiOS - One-Click ADB Theme Deployer
# Automatically detects connected Tecno / Infinix device and deploys .zth / .xth theme

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

if [ ! -f "$ZTH_FILE" ]; then
    echo "[-] Error: $ZTH_FILE not found. Running builder first..."
    python3 "$SCRIPT_DIR/builder/build_theme.py"
fi

echo "============================================================"
echo " Space Neon HiOS — ADB Theme Installer"
echo "============================================================"

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
    echo "    4. Enable 'USB Debugging' and grant the RSA key prompt on your phone screen."
    echo "    5. Re-run this script: ./adb_deploy.sh"
    exit 1
fi

DEVICE_COUNT=$(echo "$DEVICES" | wc -l)
echo "[+] Detected $DEVICE_COUNT active device(s):"
echo "$DEVICES"
echo ""

# Get device metadata
BRAND=$("$ADB_BIN" shell getprop ro.product.brand 2>/dev/null | tr -d '\r')
MODEL=$("$ADB_BIN" shell getprop ro.product.model 2>/dev/null | tr -d '\r')
ANDROID_VER=$("$ADB_BIN" shell getprop ro.build.version.release 2>/dev/null | tr -d '\r')
BUILD_ID=$("$ADB_BIN" shell getprop ro.build.display.id 2>/dev/null | tr -d '\r')

echo "[i] Target Device: $BRAND $MODEL"
echo "[i] Android Version: $ANDROID_VER (Build: $BUILD_ID)"
echo ""

# Define target paths for HiOS and XOS
TARGET_DIRS=(
    "/sdcard/Android/data/com.transsion.theme/files/DIY"
    "/sdcard/Android/data/com.transsion.hilauncher/files/DIY"
    "/sdcard/Android/data/com.transsion.xoslauncher/files/DIY"
    "/sdcard/HiTheme/DIY"
    "/sdcard/DIY"
    "/sdcard/Download"
)

echo "[*] Creating DIY Theme directories on device storage..."
for dir in "${TARGET_DIRS[@]}"; do
    "$ADB_BIN" shell mkdir -p "$dir" 2>/dev/null || true
done

echo "[*] Pushing Space Neon Minimal theme archives..."
# Primary HiOS 15+ & modern Theme Store directory
echo "  -> Pushing to /sdcard/Android/data/com.transsion.theme/files/DIY/"
"$ADB_BIN" push "$ZTH_FILE" "/sdcard/Android/data/com.transsion.theme/files/DIY/" 2>/dev/null || true

# HiOS 14.5 and below launcher directory
echo "  -> Pushing to /sdcard/Android/data/com.transsion.hilauncher/files/DIY/"
"$ADB_BIN" push "$ZTH_FILE" "/sdcard/Android/data/com.transsion.hilauncher/files/DIY/" 2>/dev/null || true

# Infinix XOS directory (with .xth)
echo "  -> Pushing to /sdcard/Android/data/com.transsion.xoslauncher/files/DIY/"
"$ADB_BIN" push "$XTH_FILE" "/sdcard/Android/data/com.transsion.xoslauncher/files/DIY/" 2>/dev/null || true

# Standard DIY and Download directories
echo "  -> Pushing backup copy to /sdcard/HiTheme/DIY/ and /sdcard/Download/"
"$ADB_BIN" push "$ZTH_FILE" "/sdcard/HiTheme/DIY/" 2>/dev/null || true
"$ADB_BIN" push "$ZTH_FILE" "/sdcard/Download/" 2>/dev/null || true

echo ""
echo "============================================================"
echo " [✓] SUCCESS: Space Neon Minimal deployed to your Tecno phone!"
echo "============================================================"
echo ""
echo "How to apply on your Tecno device:"
echo "1. Open the built-in 'Hi Theme' app on your phone."
echo "2. Tap on the bottom 'Me' or 'My Themes' tab."
echo "3. Select 'DIY' or 'Local Themes'."
echo "4. You will see 'Space Neon Minimal' with its deep black & neon orange preview."
echo "5. Tap it and hit 'Apply'!"
echo ""
echo "Note: If your launcher doesn't refresh automatically, swipe up to recent apps"
echo "      and clear Hi Theme / HiOS Launcher, or restart your phone."
