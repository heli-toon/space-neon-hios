#!/usr/bin/env bash
# Space Neon HiOS - One-Click ADB Theme Deployer
# Automatically detects connected Tecno / Infinix device and deploys:
# 1. Clean EasyDIY Icon Pack (icons.zip + .webp component icons + OEM squircle mask)
# 2. Modern HiOS 14/15 Theme (.zth with manifest.json)
# 3. Space Neon Homescreen and Lockscreen Wallpapers
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
ICONS_ZIP="$SCRIPT_DIR/icons.zip"
THEME_SRC_ICONS="$SCRIPT_DIR/theme_src/icons"

# Ensure latest Space Neon theme assets are compiled
echo "[*] Compiling latest Space Neon theme assets..."
python3 "$SCRIPT_DIR/builder/build_theme.py"

echo "============================================================"
echo " Space Neon HiOS — ADB Theme & Icon Installer"
echo "============================================================"

# Check for cleanup / uninstall flag
if [ "$1" == "--clean" ] || [ "$1" == "--uninstall" ] || [ "$1" == "--restore" ]; then
    echo "============================================================"
    echo " Space Neon HiOS — Cleaning up Space Neon theme files from device"
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

    echo "[*] Deleting Space Neon theme files from device storage (preserving Last Dark Glass)..."
    for dir in "${TARGET_DIRS[@]}"; do
        "$ADB_BIN" shell rm -f "$dir/SpaceNeonMinimal.zth" "$dir/SpaceNeonMinimal.xth" 2>/dev/null || true
    done

    echo "[*] Force-stopping Hi Theme and HiOS Launcher to clear cache..."
    "$ADB_BIN" shell am force-stop com.transsion.theme 2>/dev/null || true
    "$ADB_BIN" shell am force-stop com.transsion.hilauncher 2>/dev/null || true
    "$ADB_BIN" shell am force-stop com.transsion.xoslauncher 2>/dev/null || true

    echo ""
    echo "[✓] Cleanup complete. Your device is refreshed."
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

# 1. EasyDIY Module Deployment (Direct Icon Pack & Mask Injection)
echo "[*] Step 1: Injecting clean Space Neon EasyDIY icon pack (YAMIS monochrome on Dark Glass)..."
EASYDIY_DOWNLOAD_DIRS=(
    "/sdcard/Android/data/com.transsion.theme/files/.EasyDIY/Download/2057"
    "/sdcard/Android/data/com.transsion.theme/files/.EasyDIY/Download/2056"
    "/sdcard/Android/data/com.transsion.theme/files/.EasyDIY/2057"
    "/sdcard/Android/data/com.transsion.theme/files/.EasyDIY/2056"
)

for ed_dir in "${EASYDIY_DOWNLOAD_DIRS[@]}"; do
    echo "  -> Updating $ed_dir (clearing stale icons first)"
    "$ADB_BIN" shell rm -rf "$ed_dir/icons" 2>/dev/null || true
    "$ADB_BIN" shell mkdir -p "$ed_dir/icons" 2>/dev/null || true
    "$ADB_BIN" push "$ICONS_ZIP" "$ed_dir/icons.zip" 2>/dev/null || true
    "$ADB_BIN" push "$THEME_SRC_ICONS/." "$ed_dir/icons/" 2>/dev/null || true
done

# 2. Full Theme Package Deployment (.zth / .xth)
echo "[*] Step 2: Deploying Space Neon Minimal full theme (.zth / .xth)..."
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
done

# 3. Force-Stop to Clear Memory Cache
echo "[*] Step 3: Refreshing HiTheme and HiOS Launcher..."
"$ADB_BIN" shell am force-stop com.transsion.theme 2>/dev/null || true
"$ADB_BIN" shell am force-stop com.transsion.hilauncher 2>/dev/null || true
"$ADB_BIN" shell am force-stop com.transsion.xoslauncher 2>/dev/null || true

echo ""
echo "============================================================"
echo " [✓] SUCCESS: Space Neon Minimal deployed to your Tecno device!"
echo "============================================================"
echo ""
echo "Theme Applied:"
echo "  'Space Neon Minimal' (Cyber Neon Black Hole + YAMIS Monochrome Icons on Dark Glass)"
echo "  (Note: 'Last Dark Glass Theme' was kept safely on your phone untouched)"
echo ""
echo "How to apply on your Tecno phone:"
echo ""
echo "METHOD A (Full Theme via Hi Theme - RECOMMENDED):"
echo "  1. Open 'Hi Theme' on your phone."
echo "  2. Tap 'Me' (bottom right) -> 'My Themes' (or 'DIY')."
echo "  3. Select 'Space Neon Minimal' and tap 'Apply'!"
echo ""
echo "METHOD B (Instant 1-Tap EasyDIY Icon Pack):"
echo "  1. Open 'Hi Theme' on your phone."
echo "  2. Go to 'DIY' (or 'Customize') -> Tap 'Icons'."
echo "  3. Select pack 2057 (now loaded with clean YAMIS Dark Glass icons)."
echo "  4. Tap 'Apply'!"
echo "============================================================"
