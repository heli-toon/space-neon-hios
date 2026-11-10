# Tecno HiOS Theme Installation Guide

This guide explains how to install and apply the **Space Neon Minimal** custom theme and icon pack on Tecno smartphones running HiOS (tested on HiOS 8, 12, 13, 14, and 15+ / Android 14 & 15).

---

## 1. Icon Architecture & Dark Glass Styling

### Why Previously Only System Icons Were Themed:
1. **Dot vs. Underscore Package Names**:
   Android packages use dot notation (e.g. `com.whatsapp`, `com.instagram.android`). However, Transsion's HiOS and XOS launcher theme engines **never match filenames containing dots**. HiOS exclusively matches:
   - **Transsion Friendly Component Names**: `WhatsApp.png`, `Chrome.png`, `Instagram.png`, `Telegram.png`, `YouTube.png`, `PlayStore.png`, `Phone.png`, `Camera.png`, `Settings.png`.
   - **Underscore Package Names**: `com_whatsapp.png`, `com_instagram_android.png`, `com_android_chrome.png`, `com_google_android_youtube.png`.
   - **Activity-Level Identifiers**: `org_telegram_messenger_DefaultIcon.png`, `com_openai_chatgpt_MainActivity.png`.
2. **Missing 3rd-Party Library**:
   Earlier builds only contained ~19 system app mappings. We have now expanded the theme to over **1,200 icon files** (500+ distinct apps) covering WhatsApp, Telegram, Chrome, YouTube, Instagram, X/Twitter, Spotify, TikTok, Netflix, ChatGPT, Claude, Slack, Teams, Outlook, Duolingo, Xender, Zoom, CPU-Z, Binance, and many more.
3. **Dark Glass Background Suite**:
   Instead of bright orange outlines, all icons and unthemed third-party apps now adopt the **Dark Glass frosted squircle plate** from `Last Dark Glass Theme`:
   - `icon_bg.png` / `icon_bg.webp`: 256×256 dark frosted glass squircle plate with subtle gradient.
   - `icon_border.png` / `icon_border.webp`: Anti-aliased translucent white glass highlight edge.
   - `icon_mask.png` / `icon_mask.webp`: OEM squircle clipping mask.
   - `tecno_icon_sharped_bg.png`: Tecno sharp squircle background.
   - `folder_bg.png`: Translucent frosted dark glass folder background.
   - `calendar_bg.png` & `calendar_0..9`: Dynamic dark glass calendar widget.
   - `hios_dynamic_icons_clock_bg.png`: Dark glass dynamic clock widget.
   Unthemed third-party apps are automatically clipped and nested inside the dark glass squircle without deformation or washed-out colors.

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

Once deployed via ADB, you have two complete themes available:

#### Option 1: Apply the Full Theme (Recommended)
1. Open **Hi Theme** on your phone.
2. Tap **Me** (bottom right) → **My Themes** (or **DIY** / **Local Themes**).
3. You will see both:
   - **Space Neon Minimal**: Cyber black hole & nebula wallpapers with 1,200+ Dark Glass icons.
   - **Last Dark Glass Theme**: Pure frosted dark glass theme and lockscreen.
4. Select your preferred theme and tap **Apply**!

#### Option 2: Instant 1-Tap Apply via EasyDIY Icons
1. Open **Hi Theme** → Tap **DIY** (or **Customize**) at the bottom.
2. Tap **Icons** → Select pack **2057**.
3. Tap **Apply** → All system and 3rd-party apps immediately adopt the Dark Glass squircle style!

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
