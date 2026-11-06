# Community Infinix & Tecno Theme Creation Tool — Comprehensive Guide

This reference document provides an in-depth overview of the **Infinix & Tecno Theme Creation Tool**, developed by community theme developer **Nadeem Haider** for Transsion Holdings devices (**Tecno HiOS**, **Infinix XOS**, and **itelOS**).

---

## 1. Background & Why the Tool Exists

Unlike major smartphone manufacturers (such as Samsung with *Theme Park / Galaxy Themes Studio* or Xiaomi with *MIUI / HyperOS Theme Studio*), **Transsion does not maintain a public web-based developer portal** for third-party theme designers.

Historically, community creators had to:
- Manually configure XML manifests (`description.xml`, `manifest.xml`).
- Manually look up OEM package intents (e.g. `com.sh.smart.caller` for the Tecno dialer or `com.transsion.aigallery` for AI Gallery).
- Manually compress assets into `.zip` containers and rename them to `.zth` or `.xth`.
- Wrestle with strict directory level structures where an extra root folder breaks the theme engine parser.

Nadeem Haider developed the desktop **Theme Creation Tool** to automate this entire workflow through a unified visual interface.

---

## 2. Where to Find the Tool & Distribution Channels

Because Transsion does not host third-party theming utilities on official app stores, the software is distributed directly through developer community channels:

### Primary Distribution Channels:
1. **Telegram Community Hub**:
   - **Channel**: [`@TecnoInfinixThemes`](https://t.me/TecnoInfinixThemes)
   - **How to locate the latest build**: Open the channel feed and search for `#ThemeCreationTool`, `#ThemeMaker`, or "Theme Creation Tool". Release ZIP archives and changelogs are pinned periodically.
2. **Developer YouTube Channel**:
   - **Channel**: [`Infinix & Tecno Apps | Themes` (`@Infinix_Tecno_APPS_THEMES`)](https://www.youtube.com/@Infinix_Tecno_APPS_THEMES)
   - **Content**: Video tutorials, feature demonstrations, and direct Google Drive / Mega download links in the video descriptions and pinned comments.

---

## 3. Key Capabilities & Technical Features

| Feature | Technical Implementation |
|---|---|
| **Automated Package Generation** | Compiles assets directly into valid `.zth` (HiOS / itelOS) and `.xth` (XOS) archive formats recognized by the stock *Hi Theme* and *XTheme* managers. |
| **Automatic Icon Processing** | Scales, rounds, and formats custom transparent PNGs or vector SVGs, automatically binding them to Transsion system component package names. |
| **Cross-Format Conversion** | Imports themes formatted for other OEM engines—such as Xiaomi's `.mtz`, Huawei's `.hwt`, or backup archives (`.bak`)—extracting and re-mapping graphics to Transsion layout specifications. |
| **Real-Time Preview Engine** | Simulates the homescreen grid, icon masks, dock, and wallpaper together before compiling the file. |
| **"Send to Mobile" (ADB)** | Bundles an ADB bridge that automatically detects a phone connected with USB Debugging enabled, pushes the `.zth` into the proper DIY folder, and triggers the theme manager. |
| **Security & Access Model** | The tool utilizes a server-synced login/credit system managed via the community developer's server. |
| **Platform Compatibility** | Built primarily as a 64-bit Windows desktop executable (`.exe`). Can be run on Linux (Ubuntu / Mint / Arch) via **Wine**: `wine ThemeCreationTool.exe`. |

---

## 4. How to Use the Tool With This Space Neon Project

This repository already provides all the source assets prepared specifically for Nadeem Haider's tool:

### Assets Provided in This Repo:
1. **Raw Monochrome Transparent PNGs**:
   - `raw_monochrome_pngs_256/` (256×256 px high-DPI transparent icons)
   - `raw_monochrome_pngs_512/` (512×512 px ultra-high-DPI transparent icons)
2. **Mobile Wallpapers**:
   - `wallpapers/space-neon-orange-nebula-phone.jpg` (1080×2400 mobile crop)
   - `wallpapers/neon-orange-blackhole-phone.jpg` (Alternate cyber black hole)

### Step-by-Step Workflow in the Desktop Tool:
1. Launch the **Theme Creation Tool**.
2. Go to the **Wallpaper** tab:
   - Click **Browse** and load `wallpapers/space-neon-orange-nebula-phone.jpg`.
3. Go to the **Icons** tab:
   - Select **Batch Import** and choose the `raw_monochrome_pngs_256/` or `512/` folder.
   - In the **Icon Style / Mask** dropdown, choose your preferred border or keep them transparent.
4. Go to the **Icon Mapping** tab:
   - Click **Auto-Bind**. Because our PNGs are already named after official package strings (e.g. `com.sh.smart.caller.png`, `com.transsion.camera.png`), the tool automatically maps them to the corresponding Transsion launcher components.
5. Go to the **Theme Details / Manifest** tab:
   - Title: `Space Neon Minimal`
   - Author: `heli-toon & Antigravity`
   - Target UI: `Tecno HiOS`
6. Click **Generate .ZTH**.
7. If your phone is connected with USB Debugging enabled, click **Send to Mobile** to push it directly, or save the `.zth` file to transfer manually.

---

## 5. Local Linux / Open-Source Alternative (Included)

If you prefer not to use Wine or server-authenticated tools, this repository includes a standalone local Python build and deployment pipeline:

- **Local Compilation Engine**:
  ```bash
  python3 builder/build_theme.py
  ```
  *(Generates squircle icons with neon orange borders, crops 4K wallpapers, renders UI previews, and builds both `.zth` and `.xth` packages locally with zero external network dependencies).*

- **Local 1-Click ADB Deployment**:
  ```bash
  ./adb_deploy.sh
  ```
  *(Detects any connected Tecno/Infinix device, inspects the Android version, creates target directories, and transfers the theme immediately).*
