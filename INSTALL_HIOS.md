# Tecno HiOS Theme Installation Guide

This guide explains how to install and apply `.zth` custom themes on Tecno smartphones running HiOS (tested on HiOS 8, 12, 13, 14, and 15+).

---

## 1. Directory Paths by HiOS Version

Transsion changed the location of the local DIY themes directory across Android and HiOS versions:

| Software Version | Theme Target Directory |
|---|---|
| **HiOS 15+ (Android 14 / 15)** | `Internal Storage/Android/data/com.transsion.theme/files/DIY/` |
| **HiOS 13 / 14 / 14.5 (Android 13 / 14)** | `Internal Storage/Android/data/com.transsion.hilauncher/files/DIY/` |
| **HiOS 12 and below (Android 11 / 12)** | `Internal Storage/HiTheme/DIY/` or `Internal Storage/DIY/` |
| **Infinix XOS Devices** | `Internal Storage/Android/data/com.transsion.xoslauncher/files/DIY/` |

---

## 2. Recommended Installation Methods

### Method A: One-Click ADB Push (Fastest & No Scoped Storage Hassle)

Modern versions of Android (Android 11+) restrict standard file manager apps from browsing `Android/data`. However, **ADB pushes directly into protected app data without restriction**.

1. Connect your Tecno phone to your computer via USB.
2. Ensure **USB Debugging** is toggled ON under **Settings → System → Developer Options**.
3. In this directory on your PC, execute:
   ```bash
   ./adb_deploy.sh
   ```
4. The script automatically checks for device connectivity and pushes `SpaceNeonMinimal.zth` to every valid target directory simultaneously.
5. On your phone: Open **Hi Theme → Me / My Themes → DIY**, tap **Space Neon Minimal**, and select **Apply**.

---

### Method B: Manual File Placement Using MT Manager or ZArchiver

If you do not have a computer available:

1. Download or copy `SpaceNeonMinimal.zth` onto your phone's internal storage (e.g., `Download` folder).
2. Install **MT Manager** or **ZArchiver** from the Play Store or official website.
3. Open the file manager and grant it the requested Storage / Document Tree permission to access the `Android/data` folder.
4. Navigate to:
   - For HiOS 15+: `Android/data/com.transsion.theme/files/`
   - For HiOS 14.5 or older: `Android/data/com.transsion.hilauncher/files/`
5. If the `DIY` folder does not exist inside `files/`, tap **New Folder** and name it `DIY` (case-sensitive).
6. Copy `SpaceNeonMinimal.zth` into `DIY`.
7. Force-close the **Hi Theme** app from recent apps to ensure its database refreshes.
8. Re-open **Hi Theme**, go to **Me → DIY**, and apply the theme.

---

### Method C: Renaming to .zip for Inspection

If you ever want to check or replace assets directly:
1. Rename `SpaceNeonMinimal.zth` to `SpaceNeonMinimal.zip`.
2. Extract it using any zip explorer.
3. Replace wallpapers or edit `Icons/com.pkg.name.png`.
4. Select the contents (**not** the outer folder) and compress them back to `.zip`.
5. Rename the extension back to `.zth`.

---

## 3. Troubleshooting

- **Theme does not show up under DIY?**
  - Verify that the folder name is strictly `DIY` (capitalized).
  - Check whether your phone uses `com.transsion.theme` or `com.transsion.hilauncher`. If unsure, copy the file to both.
  - Clear cache for the Hi Theme app under **Settings → Apps → Hi Theme → Storage → Clear Cache**.
- **Icons are not changing on homescreen?**
  - Go to **HiOS Launcher Settings** (pinch on homescreen or long-press an empty area → Desktop Settings).
  - Check **Icon Size** or toggle **Desktop Style** to trigger a launcher redraw.
  - Restart your phone.
- **Some third-party apps look unthemed?**
  - Space Neon HiOS includes `icon_background.png` and `icon_mask.png` in `Icons/` to wrap unthemed apps in the cyber squircle. If your specific HiOS build does not enable dynamic icon masking, you can add that app's package name into `builder/build_theme.py` and re-run the build script.
