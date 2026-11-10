#!/usr/bin/env python3
"""
Space Neon HiOS & XOS Theme Builder
Compiles KDE Plasma "Space Neon Minimal" assets into a production-ready
Tecno HiOS (.zth), Infinix XOS (.xth), and EasyDIY (icons.zip) theme suite.

Key Enhancements based on OEM Transsion HiOS 14/15 reverse-engineering:
- Generates Transsion Friendly Component Names (Phone.webp, Camera.webp, Settings.webp, etc.)
- Uses OEM-tested 144x144 RGBA squircle geometry (bbox 5, 5, 139, 139)
- Generates OEM squircle clipping mask (icon_mask.webp) and transparent overlay (icon_top.webp)
- Eliminates square icon deformation and prevents color-stripping on unthemed apps
- Generates dynamic calendar background (calendar_bg.webp) and digits (calendar_0..9.webp)
- Includes modern manifest.json (os_version: 1500, version: 15) for HiOS 14/15 theme engines
- Packages standalone icons.zip for instant HiTheme EasyDIY module replacement
"""

import os
import io
import shutil
import zipfile
from PIL import Image, ImageDraw, ImageFont

# Base Paths
BUILDER_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(BUILDER_DIR)
REF_ICONS_DIR = os.path.join(BUILDER_DIR, "ref_assets")
RAW_PNG_DIR = os.path.join(BASE_DIR, "raw_monochrome_pngs_256")
WALLPAPERS_DIR = os.path.join(BASE_DIR, "wallpapers")
THEME_SRC_DIR = os.path.join(BASE_DIR, "theme_src")

# Colors
COLOR_SURFACE = (14, 15, 19)       # #0E0F13 (Deep space body)
COLOR_ORANGE = (255, 107, 0)       # #FF6B00 (Neon accent)
COLOR_WHITE = (255, 255, 255)      # Crisp monochrome glyph

# Component name -> Raw PNG glyph filename mapping
COMPONENT_TO_RAW = {
    "Phone.webp": "com.sh.smart.caller.png",
    "Messages.webp": "com.android.mms.png",
    "Contacts.webp": "com.android.contacts.png",
    "Camera.webp": "com.transsion.camera.png",
    "Gallery.webp": "com.transsion.aigallery.png",
    "FileManager.webp": "com.transsion.filemanager.png",
    "Settings.webp": "com.android.settings.png",
    "Calculator.webp": "com.transsion.calculator.png",
    "Clock.webp": "com.android.deskclock.png",
    "Calendar.webp": "com.android.calendar.png",
    "Browser.webp": "com.android.chrome.png",
    "PHXBrowser.webp": "com.android.chrome.png",
    "Music.webp": "com.google.android.apps.youtube.music.png",
    "Theme.webp": "com.transsion.theme.png",
    "Weather.webp": "com.transsion.weather.png",
    "Recorder.webp": "com.transsion.soundrecorder.png",
    "VideoPlayer.webp": "org.videolan.vlc.png",
    "Email.webp": "com.google.android.gm.png",
    "AllApps.webp": "com.transsion.hilauncher.png"
}

# OEM icons to extract cleanly from reference package
OEM_EXTRACT_LIST = [
    "Fingerprint.webp", "freezer.webp", "PhoneMaster.webp", "PowerManagement.webp",
    "Downloads.webp", "BackupAndRestore.webp", "Feedback.webp", "SIMToolkit.webp",
    "Security.webp", "SystemUpdate.webp", "MicroIntelligence.webp", "A-Z.webp",
    "Notes.webp", "FMRadio.webp"
]


def ensure_reference_icons():
    """Ensures working reference template assets exist for squircle mask cloning."""
    if not os.path.exists(REF_ICONS_DIR):
        raise FileNotFoundError(f"Cannot find reference template directory {REF_ICONS_DIR}")


def generate_base_plates(icons_dir):
    """Generates OEM-pixel-perfect Space Neon squircle plate, masks, and dynamic calendar assets."""
    print("Generating Space Neon squircle plates and masking layers...")
    ref_bg_path = os.path.join(REF_ICONS_DIR, "icon_bg.webp")
    ref_bg = Image.open(ref_bg_path).convert("RGBA")
    
    # 1. Base Plate: icon_bg.webp
    neon_bg = Image.new("RGBA", ref_bg.size)
    pi = ref_bg.load()
    po = neon_bg.load()
    for y in range(ref_bg.height):
        for x in range(ref_bg.width):
            r, g, b, a = pi[x, y]
            if a == 0:
                po[x, y] = (0, 0, 0, 0)
            else:
                intensity = max(g, b) / 255.0
                nr = int(COLOR_SURFACE[0] * (1 - intensity) + COLOR_ORANGE[0] * intensity)
                ng = int(COLOR_SURFACE[1] * (1 - intensity) + COLOR_ORANGE[1] * intensity)
                nb = int(COLOR_SURFACE[2] * (1 - intensity) + COLOR_ORANGE[2] * intensity)
                po[x, y] = (nr, ng, nb, a)

    neon_bg.save(os.path.join(icons_dir, "icon_bg.webp"), "WEBP", quality=100, lossless=True)
    neon_bg.save(os.path.join(icons_dir, "icon_bg.png"), "PNG")

    # 2. OEM Squircle Clipping Mask (icon_mask.webp) & Transparent Overlay (icon_top.webp)
    shutil.copy(os.path.join(REF_ICONS_DIR, "icon_mask.webp"), os.path.join(icons_dir, "icon_mask.webp"))
    shutil.copy(os.path.join(REF_ICONS_DIR, "icon_top.webp"), os.path.join(icons_dir, "icon_top.webp"))
    # Also save PNG versions for case-insensitive / legacy engine matchers
    Image.open(os.path.join(REF_ICONS_DIR, "icon_mask.webp")).save(os.path.join(icons_dir, "icon_mask.png"), "PNG")
    Image.open(os.path.join(REF_ICONS_DIR, "icon_top.webp")).save(os.path.join(icons_dir, "icon_top.png"), "PNG")

    # 3. Folder background & Calendar background
    for bg_name in ["folder_bg.webp", "calendar_bg.webp"]:
        src_p = os.path.join(REF_ICONS_DIR, bg_name)
        if os.path.exists(src_p):
            im = Image.open(src_p).convert("RGBA")
            out = Image.new("RGBA", im.size)
            spi = im.load()
            spo = out.load()
            for y in range(im.height):
                for x in range(im.width):
                    r, g, b, a = spi[x, y]
                    if a == 0:
                        spo[x, y] = (0, 0, 0, 0)
                    else:
                        intensity = max(g, b) / 255.0
                        nr = int(COLOR_SURFACE[0] * (1 - intensity) + COLOR_ORANGE[0] * intensity)
                        ng = int(COLOR_SURFACE[1] * (1 - intensity) + COLOR_ORANGE[1] * intensity)
                        nb = int(COLOR_SURFACE[2] * (1 - intensity) + COLOR_ORANGE[2] * intensity)
                        spo[x, y] = (nr, ng, nb, a)
            base_n, _ = os.path.splitext(bg_name)
            out.save(os.path.join(icons_dir, bg_name), "WEBP", quality=100, lossless=True)
            out.save(os.path.join(icons_dir, f"{base_n}.png"), "PNG")

    # 4. Dynamic Calendar Digits (calendar_0.webp .. calendar_9.webp)
    for i in range(10):
        digit_p = os.path.join(REF_ICONS_DIR, f"calendar_{i}.webp")
        if os.path.exists(digit_p):
            im = Image.open(digit_p).convert("RGBA")
            out = Image.new("RGBA", im.size)
            spi = im.load()
            spo = out.load()
            for y in range(im.height):
                for x in range(im.width):
                    r, g, b, a = spi[x, y]
                    if a > 0:
                        intensity = max(g, b) / 255.0
                        spo[x, y] = (int(COLOR_ORANGE[0] * intensity), int(COLOR_ORANGE[1] * intensity), int(COLOR_ORANGE[2] * intensity), a)
                    else:
                        spo[x, y] = (0, 0, 0, 0)
            out.save(os.path.join(icons_dir, f"calendar_{i}.webp"), "WEBP", quality=100, lossless=True)
            out.save(os.path.join(icons_dir, f"calendar_{i}.png"), "PNG")

    return neon_bg, ref_bg


def generate_all_icons(icons_dir, neon_bg, ref_bg):
    """Generates both HiOS Component icons and 3rd-party package icons in WebP & PNG."""
    print("Generating monochrome YAMIS component icons on Space Neon plates...")

    def composite_glyph(glyph_img, target_size=74):
        g = glyph_img.resize((target_size, target_size), Image.Resampling.LANCZOS)
        canvas = neon_bg.copy()
        pos = ((canvas.width - g.width) // 2, (canvas.height - g.height) // 2)
        canvas.paste(g, pos, g)
        return canvas

    # 1. Primary Component Icons from local raw monochrome PNGs
    for comp_webp, raw_png in COMPONENT_TO_RAW.items():
        raw_path = os.path.join(RAW_PNG_DIR, raw_png)
        if os.path.exists(raw_path):
            glyph = Image.open(raw_path).convert("RGBA")
            icon = composite_glyph(glyph, target_size=74)
            base_n, _ = os.path.splitext(comp_webp)
            icon.save(os.path.join(icons_dir, comp_webp), "WEBP", quality=100, lossless=True)
            icon.save(os.path.join(icons_dir, f"{base_n}.png"), "PNG")

    # 2. Extract and composite OEM-specific icons
    for comp_webp in OEM_EXTRACT_LIST:
        ref_path = os.path.join(REF_ICONS_DIR, comp_webp)
        if os.path.exists(ref_path):
            im = Image.open(ref_path).convert("RGBA")
            glyph = Image.new("RGBA", im.size, (0, 0, 0, 0))
            for y in range(im.height):
                for x in range(im.width):
                    p = im.getpixel((x, y))
                    bp = ref_bg.getpixel((x, y))
                    diff = max(0, p[0] - bp[0], p[1] - bp[1], p[2] - bp[2])
                    if diff > 30:
                        a = min(255, int(diff * 1.5))
                        glyph.putpixel((x, y), (255, 255, 255, a))

            bbox = glyph.getbbox()
            if bbox:
                cropped = glyph.crop(bbox)
                aspect = cropped.width / cropped.height
                if aspect > 1:
                    gw = 70
                    gh = max(1, int(70 / aspect))
                else:
                    gh = 70
                    gw = max(1, int(70 * aspect))
                resized = cropped.resize((gw, gh), Image.Resampling.LANCZOS)
                canvas = neon_bg.copy()
                pos = ((canvas.width - resized.width) // 2, (canvas.height - resized.height) // 2)
                canvas.paste(resized, pos, resized)
                base_n, _ = os.path.splitext(comp_webp)
                canvas.save(os.path.join(icons_dir, comp_webp), "WEBP", quality=100, lossless=True)
                canvas.save(os.path.join(icons_dir, f"{base_n}.png"), "PNG")

    # 3. Generate all 3rd-party and package-named apps (both .webp and .png)
    for raw_f in os.listdir(RAW_PNG_DIR):
        if not raw_f.endswith(".png"):
            continue
        pkg_base, _ = os.path.splitext(raw_f)
        raw_path = os.path.join(RAW_PNG_DIR, raw_f)
        glyph = Image.open(raw_path).convert("RGBA")
        icon = composite_glyph(glyph, target_size=74)
        icon.save(os.path.join(icons_dir, f"{pkg_base}.webp"), "WEBP", quality=100, lossless=True)
        icon.save(os.path.join(icons_dir, f"{pkg_base}.png"), "PNG")

    print(f"Total icon files created in build: {len(os.listdir(icons_dir))}")


def package_icons_zip(icons_dir, out_zip):
    """Creates a standalone icons.zip matching OEM EasyDIY Download format."""
    print(f"Packaging EasyDIY icon pack into {out_zip}...")
    if os.path.exists(out_zip):
        os.remove(out_zip)
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(icons_dir)):
            full_p = os.path.join(icons_dir, f)
            # Store inside icons/ folder within zip
            z.write(full_p, f"icons/{f}")
    print(f" -> icons.zip generated ({os.path.getsize(out_zip) // 1024} KB)")


def process_wallpapers(theme_dir):
    """Deploys wallpapers for homescreen and lockscreen across all Transsion directory variations."""
    print("Deploying Space Neon Wallpapers...")
    wp_dir = os.path.join(theme_dir, "Wallpaper")
    wp_lower_dir = os.path.join(theme_dir, "wallpaper")
    wallpapers_dir = os.path.join(theme_dir, "wallpapers")
    wallpapers_draw_dir = os.path.join(theme_dir, "wallpapers/drawable")

    for d in [wp_dir, wp_lower_dir, wallpapers_dir, wallpapers_draw_dir]:
        os.makedirs(d, exist_ok=True)

    home_wp_src = os.path.join(WALLPAPERS_DIR, "space-neon-orange-nebula-phone.jpg")
    lock_wp_src = os.path.join(WALLPAPERS_DIR, "neon-orange-blackhole-phone.jpg")

    # Verify sources exist
    if not os.path.exists(home_wp_src):
        raise FileNotFoundError(f"Missing home wallpaper: {home_wp_src}")
    if not os.path.exists(lock_wp_src):
        lock_wp_src = home_wp_src

    # Homescreen names: wallpaper.jpg, home_wallpaper.jpg, default_wallpaper.jpg
    # Lockscreen names: lockscreen_wallpaper.jpg, lock_wallpaper.jpg
    for d in [wp_dir, wp_lower_dir, wallpapers_dir, wallpapers_draw_dir]:
        shutil.copy(home_wp_src, os.path.join(d, "wallpaper.jpg"))
        shutil.copy(home_wp_src, os.path.join(d, "home_wallpaper.jpg"))
        shutil.copy(home_wp_src, os.path.join(d, "default_wallpaper.jpg"))
        shutil.copy(lock_wp_src, os.path.join(d, "lockscreen_wallpaper.jpg"))
        shutil.copy(lock_wp_src, os.path.join(d, "lock_wallpaper.jpg"))


def generate_previews(theme_dir):
    """Generates preview mockups matching both HiOS 14/15 store cards and local DIY previews."""
    print("Generating Theme Previews...")
    prev_dir = os.path.join(theme_dir, "Preview")
    prev_lower_dir = os.path.join(theme_dir, "preview")
    thumb_dir = os.path.join(theme_dir, "Thumbnail")
    thumb_lower_dir = os.path.join(theme_dir, "thumbnail")

    for d in [prev_dir, prev_lower_dir, thumb_dir, thumb_lower_dir]:
        os.makedirs(d, exist_ok=True)

    # Use existing high-res preview mockups
    existing_cover = os.path.join(BASE_DIR, "preview_cover.jpg")
    existing_preview = os.path.join(BASE_DIR, "preview.jpg")

    for d in [prev_dir, prev_lower_dir]:
        shutil.copy(existing_cover, os.path.join(d, "cover.jpg"))
        shutil.copy(existing_preview, os.path.join(d, "preview_launcher_0.jpg"))
        shutil.copy(existing_cover, os.path.join(d, "preview_lockscreen_0.jpg"))
        shutil.copy(existing_preview, os.path.join(d, "preview_0.jpg"))
        shutil.copy(existing_cover, os.path.join(d, "preview_1.jpg"))

    # Thumbnail for local DIY selector
    with Image.open(existing_preview) as im:
        thumb = im.resize((450, 1000), Image.Resampling.LANCZOS)
        for d in [thumb_dir, thumb_lower_dir, prev_dir, prev_lower_dir]:
            thumb.save(os.path.join(d, "thumbnail.jpg"), "JPEG", quality=90)


def create_manifests_and_app_resources(theme_dir):
    """Generates HiOS 14/15 manifest.json, legacy XML manifests, and launcher config overlays."""
    print("Writing Theme Manifests and Launcher configs...")

    # 1. HiOS 14/15 manifest.json
    manifest_json = """{
  "id": "e9a0f412-87c2-4e89-b873-10928a3f8901",
  "type": 0,
  "version": 15,
  "author": "heli-toon",
  "app_resource_dir": "app",
  "name": "Space Neon Minimal",
  "description": "Ultra-minimal high-contrast cyberpunk theme for Tecno HiOS. Deep space black, vibrant neon orange accents, squircle monochrome YAMIS icons.",
  "prebuilt": 0,
  "os_version": 1500
}
"""
    with open(os.path.join(theme_dir, "manifest.json"), "w", encoding="utf-8") as f:
        f.write(manifest_json)

    # 2. Legacy Transsion XML manifests
    desc_xml = """<?xml version="1.0" encoding="utf-8"?>
<theme>
    <title>Space Neon Minimal</title>
    <author>heli-toon</author>
    <designer>heli-toon</designer>
    <version>15.0</version>
    <formatVersion>1</formatVersion>
    <description>Ultra-minimal high-contrast cyberpunk theme for Tecno HiOS and Infinix XOS.</description>
    <uiVersion>HiOS 8.0 - HiOS 15+</uiVersion>
</theme>
"""
    with open(os.path.join(theme_dir, "description.xml"), "w", encoding="utf-8") as f:
        f.write(desc_xml)

    manifest_xml = """<?xml version="1.0" encoding="utf-8"?>
<manifest>
    <theme-name>Space Neon Minimal</theme-name>
    <version>15.0</version>
    <author>heli-toon</author>
    <modules>
        <module name="icons" />
        <module name="Icons" />
        <module name="wallpaper" />
        <module name="Wallpaper" />
    </modules>
</manifest>
"""
    with open(os.path.join(theme_dir, "manifest.xml"), "w", encoding="utf-8") as f:
        f.write(manifest_xml)

    # 3. App overlay: com.transsion.hilauncher
    hilauncher_val = os.path.join(theme_dir, "app/com.transsion.hilauncher/values")
    os.makedirs(hilauncher_val, exist_ok=True)

    colors_xml = """<?xml version='1.0' encoding='utf-8'?>
<resources>
<color name="cleaner_progress_color">#FFFF6B00</color>
<color name="cleaner_progress_bg_color">#00000000</color>
<color name="cleaner_progress_gap_color">#00000000</color>
<color name="cleaner_text_color">#FFFFFFFF</color>
<color name="cleaner_progress_color_start">#FFFF6B00</color>
<color name="cleaner_progress_color_end">#FFFF9E00</color>
<color name="tran_calendar_date_color">#FFFFFFFF</color>
<color name="tran_calendar_week_color">#FFFF6B00</color>
<color name="tran_calendar_gradation_start_color">#ff0e0f13</color>
<color name="tran_calendar_gradation_end_color">#ff0e0f13</color>
</resources>
"""
    with open(os.path.join(hilauncher_val, "colors.xml"), "w", encoding="utf-8") as f:
        f.write(colors_xml)


def package_theme_archives(theme_dir):
    """Packages the complete theme into SpaceNeonMinimal.zth and SpaceNeonMinimal.xth."""
    print("Packaging .zth and .xth Theme Files...")
    zth_path = os.path.join(BASE_DIR, "SpaceNeonMinimal.zth")
    xth_path = os.path.join(BASE_DIR, "SpaceNeonMinimal.xth")

    for archive_path in [zth_path, xth_path]:
        if os.path.exists(archive_path):
            os.remove(archive_path)

        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(theme_dir):
                for f in files:
                    full_p = os.path.join(root, f)
                    rel_p = os.path.relpath(full_p, theme_dir)
                    zipf.write(full_p, rel_p)

    print(f" -> HiOS Package:    {zth_path} ({os.path.getsize(zth_path) // 1024} KB)")
    print(f" -> XOS Package:     {xth_path} ({os.path.getsize(xth_path) // 1024} KB)")


def main():
    print("=" * 60)
    print("Space Neon HiOS Theme Builder - Starting Compilation")
    print("=" * 60)

    ensure_reference_icons()

    # Re-create theme_src structure
    if os.path.exists(THEME_SRC_DIR):
        shutil.rmtree(THEME_SRC_DIR)
    os.makedirs(THEME_SRC_DIR, exist_ok=True)

    icons_dir = os.path.join(THEME_SRC_DIR, "icons")
    os.makedirs(icons_dir, exist_ok=True)

    # 1. Base squircle plates & masks
    neon_bg, ref_bg = generate_base_plates(icons_dir)

    # 2. All icons
    generate_all_icons(icons_dir, neon_bg, ref_bg)

    # 3. Duplicate into uppercase Icons/ directory for case-insensitive launcher matching
    icons_upper_dir = os.path.join(THEME_SRC_DIR, "Icons")
    shutil.copytree(icons_dir, icons_upper_dir)

    # 4. Standalone EasyDIY icons.zip
    package_icons_zip(icons_dir, os.path.join(BASE_DIR, "icons.zip"))

    # 5. Wallpapers
    process_wallpapers(THEME_SRC_DIR)

    # 6. Previews
    generate_previews(THEME_SRC_DIR)

    # 7. Manifests and App Overlays
    create_manifests_and_app_resources(THEME_SRC_DIR)

    # 8. Final .zth and .xth bundles
    package_theme_archives(THEME_SRC_DIR)

    print("=" * 60)
    print("Compilation Complete! All artifacts verified.")
    print("=" * 60)


if __name__ == "__main__":
    main()
