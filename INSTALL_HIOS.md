# Tecno HiOS Theme Installation Guide

This guide explains how to install and apply the **Space Neon Minimal** custom theme and icon pack on Tecno smartphones running HiOS (tested on HiOS 8, 12, 13, 14, and 15+ / Android 14 & 15).

---

## 1. Why HiOS 14/15 Failed Previously & How It Was Fixed

By reverse-engineering the working OEM themes and EasyDIY packages pulled directly from HiOS:
1. **Component Names vs. Package Names**:
   HiOS's native theme engine and launcher ignore Android package-named PNGs (e.g. `com.sh.smart.caller.png`, `com.android.settings.png`). Instead, HiOS requires **Transsion Friendly Component Names in WebP format** (`Phone.webp`, `Camera.webp`, `Settings.webp`, `Messages.webp`, `FileManager.webp`, etc.).
2. **Squircle Masking for Unthemed Apps**:
   HiOS composites unthemed 3rd-party apps using three special 144×144 RGBA WebP layers:
   - `icon_bg.webp`: Background plate (`#0E0F13` deep space surface with `#FF6B00` neon rim, bbox `5, 5, 139, 139`).
   - `icon_mask.webp`: Anti-aliased OEM squircle alpha clipping mask (bbox `8, 8, 136, 136`).
   - `icon_top.webp`: Transparent overlay layer (all alpha=0, preventing color washing or darkening).
   With these layers in place, **all third-party apps keep their native squircle shape and full background colors without deformation**.
3. **HiOS 14/15 `manifest.json`**:
   Modern HiOS requires a JSON manifest declaring `"os_version": 1500` and `"version": 15` alongside launcher overlay values in `app/com.transsion.hilauncher/`.
4. **Lock Screen Wallpaper**:
   HiOS has **"Lock screen magazine"** (Glance / Pictorial) enabled by default in system settings. It forcefully displays online rotating pictures over any custom theme's lockscreen. **Disabling Lock screen magazine in Settings allows your Space Neon lockscreen wallpaper to display instantly.**

---

## 2. Directory Paths on Your Device

| Component | Target Device Directory |
|---|---|
| **EasyDIY Icon Pack** | `/sdcard/Android/data/com.transsion.theme/files/.EasyDIY/Download/2057/` |
| **EasyDIY Active Edit** | `/sdcard/Android/data/com.transsion.theme/files/.EasyDIY/Edit/*/wallpaper/` |
| **HiOS 15+ Full Theme** | `/sdcard/Android/data/com.transsion.theme/files/DIY/` |
| **HiOS 13 / 14 Full Theme** | `/sdcard/Android/data/com.transsion.hilauncher/files/DIY/` |
| **Infinix XOS Theme** | `/sdcard/Android/data/com.transsion.xoslauncher/files/DIY/` |

---

## 3. Installation Methods

### Method A: One-Click ADB Deploy (PC via USB — Recommended)

1. Connect your Tecno phone to your computer via USB with **USB Debugging** enabled.
2. In your terminal inside the `space-neon-hios` workspace folder, run:
   ```bash
   ./adb_deploy.sh
   ```
3. The script automatically:
   - Injects `icons.zip` and unpacked `.webp` icons directly into the active EasyDIY folder (`2057`).
   - Injects `wallpaper.jpg` and `lockscreen_wallpaper.jpg` into EasyDIY and Theme folders.
   - Pushes `SpaceNeonMinimal.zth` to `/sdcard/Android/data/com.transsion.theme/files/DIY/`.
   - Clears the launcher and theme app caches so changes take effect immediately.

---

### Method B: Applying on Your Phone

Once deployed, choose either method below:

#### Option 1: Instant 1-Tap Apply via EasyDIY (Fastest & Guaranteed)
1. Open the built-in **Hi Theme** app on your phone.
2. Tap on **DIY** (or **Customize**) at the bottom.
3. Tap **Icons** → Select the **Space Neon** icon pack (pack `2057`).
4. Tap **Apply**.
   - All system apps immediately adopt the monochrome YAMIS style.
   - All unthemed apps retain their native HiOS squircle curves and original colors.

#### Option 2: Apply the Full Theme
1. Open **Hi Theme** → Tap **Me** (bottom right) → **My Themes** (or **DIY** / **Local Themes**).
2. Tap **Space Neon Minimal**.
3. Tap **Apply**.

---

## 4. Enabling the Lock Screen Wallpaper

To see your Space Neon lockscreen wallpaper instead of stock magazine photos:

1. Open your phone's **Settings**.
2. Go to **Theme & lock screen** (or **Display & Brightness → Lock screen**).
3. Find **Lock screen magazine** (or **Glance / Pictorial**).
4. Toggle it **OFF**.
5. Lock your screen — your high-res Space Neon black hole wallpaper will now be displayed!

---

## 5. Cleanup / Restore to Default

If you ever want to remove the theme files from your device storage:
```bash
./adb_deploy.sh --clean
```
Then open **Hi Theme → Me → My Themes**, and tap your stock **Default Theme** to re-apply.
