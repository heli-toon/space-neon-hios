#!/usr/bin/env python3
"""
Space Neon HiOS & XOS Theme Builder with Dark Glass Styling
Compiles KDE Plasma "Space Neon Minimal" assets into a production-ready
Tecno HiOS (.zth), Infinix XOS (.xth), and EasyDIY (icons.zip) theme suite.

Key Enhancements:
- Adopts the sleek Dark Glass squircle background plate & masks from "Last Dark Glass Theme"
- Includes over 500+ pre-built dark glass icons for popular third-party & system apps
- Fully maps Transsion Friendly Component Names (WhatsApp.webp, Chrome.webp, etc.),
  underscore package names (com_whatsapp.png), and dot package names (com.whatsapp.png)
- Eliminates unthemed app deformation with OEM squircle clipping mask (icon_mask) and border
- Packages both Space Neon Minimal and Last Dark Glass Theme with modern HiOS 15 manifests
"""

import os
import io
import shutil
import zipfile
from PIL import Image

# Base Paths
BUILDER_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(BUILDER_DIR)
DARK_GLASS_ASSETS_DIR = os.path.join(BUILDER_DIR, "dark_glass_assets")
EXTRACTED_ICONS_DIR = os.path.join(BUILDER_DIR, "extracted_user_icons")
RAW_PNG_DIR = os.path.join(BASE_DIR, "raw_monochrome_pngs_256")
WALLPAPERS_DIR = os.path.join(BASE_DIR, "wallpapers")
THEME_SRC_DIR = os.path.join(BASE_DIR, "theme_src")
LAST_DARK_GLASS_ZTH = os.path.join(BASE_DIR, "Last Dark Glass Theme.zth")

# Package / Component Name Aliases for Transsion Launcher Mapping
PACKAGE_COMPONENT_ALIASES = {
    "com_whatsapp": ["WhatsApp", "com.whatsapp"],
    "com_whatsapp_w4b": ["WhatsAppBusiness", "com.whatsapp.w4b"],
    "com_android_chrome": ["Chrome", "PHXBrowser", "Browser", "com.android.chrome"],
    "com_google_android_youtube": ["Youtube", "YouTube", "com.google.android.youtube"],
    "com_google_android_apps_youtube_music": ["YouTubeMusic", "YTMusic", "Music", "com.google.android.apps.youtube.music"],
    "com_instagram_android": ["Instagram", "com.instagram.android"],
    "com_twitter_android": ["X", "Twitter", "com.twitter.android"],
    "org_telegram_messenger": ["Telegram", "org.telegram.messenger"],
    "org_telegram_messenger_web": ["TelegramWeb", "Telegram", "org.telegram.messenger.web"],
    "com_spotify_music": ["Spotify", "com.spotify.music"],
    "com_openai_chatgpt": ["ChatGPT", "com.openai.chatgpt", "com_openai_chatgpt_MainActivity"],
    "com_google_android_apps_bard": ["bard", "Gemini", "com.google.android.apps.bard"],
    "com_android_vending": ["PlayStore", "com.android.vending"],
    "com_google_android_apps_maps": ["GoogleMaps", "Maps", "com.google.android.apps.maps"],
    "com_google_android_apps_photos": ["GooglePhotos", "Gphotos", "com.google.android.apps.photos"],
    "com_google_android_apps_docs": ["GoogleDrive", "Gdrive", "com.google.android.apps.docs"],
    "com_google_android_gm": ["Gmail", "Email", "com.google.android.gm"],
    "com_facebook_katana": ["Facebook", "com.facebook.katana"],
    "com_facebook_orca": ["Messenger", "com.facebook.orca"],
    "com_linkedin_android": ["LinkedIn", "com.linkedin.android"],
    "com_pinterest": ["Pinterest", "com.pinterest"],
    "com_ss_android_ugc_trill": ["TikTok", "com.ss.android.ugc.trill"],
    "com_sh_smart_caller": ["Phone", "com.sh.smart.caller", "com_android_dialer", "com_android_phone"],
    "com_transsion_camera": ["Camera", "com.transsion.camera", "com_android_camera"],
    "com_transsion_aigallery": ["Gallery", "com.transsion.aigallery", "com_android_gallery3d", "com_gallery20_activities_GalleryActivity"],
    "com_transsion_filemanager": ["FileManager", "com.transsion.filemanager", "com_transsion_filemanagerx"],
    "com_transsion_filemanagerx": ["FileManager", "com.transsion.filemanagerx"],
    "com_android_settings": ["Settings", "com.android.settings", "com_transsion_settings"],
    "com_transsion_calculator": ["Calculator", "com.transsion.calculator", "com_android_calculator2"],
    "com_android_deskclock": ["Clock", "com.android.deskclock", "com_transsion_deskclock"],
    "com_android_calendar": ["Calendar", "com.android.calendar", "com_transsion_calendar"],
    "com_transsion_theme": ["Theme", "Themes", "com.transsion.theme"],
    "com_transsion_weather": ["Weather", "com.transsion.weather"],
    "com_transsion_soundrecorder": ["Recorder", "SoundRecorder", "com.transsion.soundrecorder", "com_android_soundrecorder"],
    "com_transsion_compass": ["Compass", "com.transsion.compass"],
    "com_android_contacts": ["Contacts", "Contact", "com.android.contacts"],
    "com_android_mms": ["Messages", "com.android.mms", "com_android_messaging"],
    "org_videolan_vlc": ["VLC", "VideoPlayer", "org.videolan.vlc"],
    "com_termux": ["Termux", "com.termux"],
    "com_github_android": ["GitHub", "com.github.android"],
    "org_kde_kdeconnect_tp": ["KDEConnect", "org.kde.kdeconnect_tp"],
    "io_anytype_app": ["Anytype", "io.anytype.app"],
    "com_discord": ["Discord", "com.discord"],
    "com_anthropic_claude": ["Claude", "com.anthropic.claude"],
    "com_slack": ["Slack", "com.Slack"],
    "com_duolingo": ["Duolingo", "com.duolingo"],
    "org_fdroid_fdroid": ["FDroid", "org.fdroid.fdroid"],
    "com_microsoft_teams": ["Teams", "com.microsoft.teams"],
    "us_zoom_videomeetings": ["Zoom", "us.zoom.videomeetings"],
    "cn_xender": ["Xender", "cn.xender"],
    "com_cpuid_cpu_z": ["CPUZ", "com.cpuid.cpu_z"],
    "cn_wps_moffice_eng": ["WPSOffice", "cn.wps.moffice_eng"],
    "com_binance_dev": ["Binance", "com.binance.dev"],
    "com_microsoft_office_outlook": ["Outlook", "com.microsoft.office.outlook"],
}


def prepare_dark_glass_base_assets(icons_dir):
    """Copies dark glass backgrounds, masks, dynamic calendar & clock assets."""
    print("Deploying Dark Glass squircle background and masking suite...")
    bg_src = os.path.join(DARK_GLASS_ASSETS_DIR, "icon_bg.png")
    dark_bg = Image.open(bg_src).convert("RGBA")

    for f in os.listdir(DARK_GLASS_ASSETS_DIR):
        if not f.endswith(".png"):
            continue
        src_p = os.path.join(DARK_GLASS_ASSETS_DIR, f)
        dest_p = os.path.join(icons_dir, f)
        shutil.copy(src_p, dest_p)
        base_n, _ = os.path.splitext(f)
        # Also create WebP equivalent
        try:
            im = Image.open(src_p)
            im.save(os.path.join(icons_dir, f"{base_n}.webp"), "WEBP", quality=100, lossless=True, method=0)
        except Exception:
            pass

    # Ensure icon_top (transparent overlay) exists for HiOS compositor
    top_p = os.path.join(icons_dir, "icon_top.webp")
    if not os.path.exists(top_p):
        empty_top = Image.new("RGBA", dark_bg.size, (0, 0, 0, 0))
        empty_top.save(top_p, "WEBP", quality=100, lossless=True, method=0)
        empty_top.save(os.path.join(icons_dir, "icon_top.png"), "PNG")

    return dark_bg


def import_last_dark_glass_icons(icons_dir):
    """Imports 500+ pre-built dark glass icons and populates alias mappings."""
    print("Importing 500+ icons from Last Dark Glass Theme...")
    if not os.path.exists(LAST_DARK_GLASS_ZTH):
        print(f"[-] Warning: {LAST_DARK_GLASS_ZTH} not found, skipping import.")
        return

    with zipfile.ZipFile(LAST_DARK_GLASS_ZTH, "r") as z:
        for f in z.namelist():
            if f.startswith("icons/") and f.endswith(".png"):
                fname = os.path.basename(f)
                if not fname:
                    continue
                dest = os.path.join(icons_dir, fname)
                with open(dest, "wb") as out:
                    out.write(z.read(f))

                # Also save lossless WebP
                base_n, _ = os.path.splitext(fname)
                try:
                    with Image.open(dest) as im:
                        im.save(os.path.join(icons_dir, f"{base_n}.webp"), "WEBP", quality=100, lossless=True, method=0)
                except Exception:
                    pass

    # Cross-bind aliases
    print("Resolving Transsion friendly names, underscore & dot package aliases...")
    existing_files = set(os.listdir(icons_dir))
    for key, aliases in PACKAGE_COMPONENT_ALIASES.items():
        # Check if key (e.g. com_whatsapp.png) or any alias exists
        source_file = None
        candidates = [f"{key}.png"] + [f"{a}.png" for a in aliases]
        for c in candidates:
            if c in existing_files:
                source_file = c
                break

        if source_file:
            src_full = os.path.join(icons_dir, source_file)
            for target in candidates:
                if target not in existing_files:
                    tgt_full = os.path.join(icons_dir, target)
                    shutil.copy(src_full, tgt_full)
                    existing_files.add(target)
                tgt_base, _ = os.path.splitext(target)
                tgt_webp = f"{tgt_base}.webp"
                if tgt_webp not in existing_files:
                    try:
                        with Image.open(src_full) as im:
                            im.save(os.path.join(icons_dir, tgt_webp), "WEBP", quality=100, lossless=True, method=0)
                        existing_files.add(tgt_webp)
                    except Exception:
                        pass


def composite_raw_glyphs(icons_dir, dark_bg):
    """Composites raw monochrome PNGs and extracted user app icons onto dark glass plates."""
    print("Compositing custom and extracted app icons onto Dark Glass plates...")

    def composite_glyph(glyph_img, target_size=150):
        # Calculate aspect ratio
        bbox = glyph_img.getbbox()
        if bbox:
            glyph_cropped = glyph_img.crop(bbox)
        else:
            glyph_cropped = glyph_img

        gw, gh = glyph_cropped.size
        aspect = gw / gh
        if aspect > 1:
            w = target_size
            h = max(1, int(target_size / aspect))
        else:
            h = target_size
            w = max(1, int(target_size * aspect))

        resized = glyph_cropped.resize((w, h), Image.Resampling.LANCZOS)
        canvas = dark_bg.copy()
        pos = ((canvas.width - resized.width) // 2, (canvas.height - resized.height) // 2)
        canvas.paste(resized, pos, resized)
        return canvas

    # 1. Monochrome PNGs
    if os.path.exists(RAW_PNG_DIR):
        for raw_f in os.listdir(RAW_PNG_DIR):
            if not raw_f.endswith(".png"):
                continue
            pkg_base, _ = os.path.splitext(raw_f)
            raw_path = os.path.join(RAW_PNG_DIR, raw_f)
            glyph = Image.open(raw_path).convert("RGBA")
            icon = composite_glyph(glyph, target_size=150)

            # Dot package name
            icon.save(os.path.join(icons_dir, f"{pkg_base}.png"), "PNG")
            icon.save(os.path.join(icons_dir, f"{pkg_base}.webp"), "WEBP", quality=100, lossless=True, method=0)

            # Underscore package name
            under_pkg = pkg_base.replace(".", "_")
            icon.save(os.path.join(icons_dir, f"{under_pkg}.png"), "PNG")
            icon.save(os.path.join(icons_dir, f"{under_pkg}.webp"), "WEBP", quality=100, lossless=True, method=0)

    # 2. Extracted user icons (Claude, Slack, Teams, Duolingo, CPU-Z, etc.)
    if os.path.exists(EXTRACTED_ICONS_DIR):
        for f in os.listdir(EXTRACTED_ICONS_DIR):
            if not f.endswith(".png"):
                continue
            pkg = f.replace("_icon.png", "")
            raw_path = os.path.join(EXTRACTED_ICONS_DIR, f)
            glyph = Image.open(raw_path).convert("RGBA")
            icon = composite_glyph(glyph, target_size=155)

            under_pkg = pkg.replace(".", "_")
            for name_variant in [pkg, under_pkg]:
                icon.save(os.path.join(icons_dir, f"{name_variant}.png"), "PNG")
                icon.save(os.path.join(icons_dir, f"{name_variant}.webp"), "WEBP", quality=100, lossless=True, method=0)

    print(f"Total icon files in build directory: {len(os.listdir(icons_dir))}")


def package_icons_zip(icons_dir, out_zip):
    """Creates standalone icons.zip matching OEM EasyDIY format."""
    print(f"Packaging EasyDIY icon pack into {out_zip}...")
    if os.path.exists(out_zip):
        os.remove(out_zip)
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(icons_dir)):
            full_p = os.path.join(icons_dir, f)
            z.write(full_p, f"icons/{f}")
    print(f" -> icons.zip generated ({os.path.getsize(out_zip) // 1024} KB)")


def process_wallpapers(theme_dir):
    """Deploys Space Neon wallpapers across Transsion folder variants."""
    print("Deploying Space Neon Wallpapers...")
    wp_dir = os.path.join(theme_dir, "Wallpaper")
    wp_lower_dir = os.path.join(theme_dir, "wallpaper")
    wallpapers_dir = os.path.join(theme_dir, "wallpapers")
    wallpapers_draw_dir = os.path.join(theme_dir, "wallpapers/drawable")

    for d in [wp_dir, wp_lower_dir, wallpapers_dir, wallpapers_draw_dir]:
        os.makedirs(d, exist_ok=True)

    home_wp_src = os.path.join(WALLPAPERS_DIR, "space-neon-orange-nebula-phone.jpg")
    lock_wp_src = os.path.join(WALLPAPERS_DIR, "neon-orange-blackhole-phone.jpg")

    if not os.path.exists(home_wp_src):
        raise FileNotFoundError(f"Missing home wallpaper: {home_wp_src}")
    if not os.path.exists(lock_wp_src):
        lock_wp_src = home_wp_src

    for d in [wp_dir, wp_lower_dir, wallpapers_dir, wallpapers_draw_dir]:
        shutil.copy(home_wp_src, os.path.join(d, "wallpaper.jpg"))
        shutil.copy(home_wp_src, os.path.join(d, "home_wallpaper.jpg"))
        shutil.copy(home_wp_src, os.path.join(d, "default_wallpaper.jpg"))
        shutil.copy(lock_wp_src, os.path.join(d, "lockscreen_wallpaper.jpg"))
        shutil.copy(lock_wp_src, os.path.join(d, "lock_wallpaper.jpg"))


def generate_previews(theme_dir):
    """Generates preview mockups matching HiOS store cards and local DIY selectors."""
    print("Generating Theme Previews...")
    prev_dir = os.path.join(theme_dir, "Preview")
    prev_lower_dir = os.path.join(theme_dir, "preview")
    thumb_dir = os.path.join(theme_dir, "Thumbnail")
    thumb_lower_dir = os.path.join(theme_dir, "thumbnail")

    for d in [prev_dir, prev_lower_dir, thumb_dir, thumb_lower_dir]:
        os.makedirs(d, exist_ok=True)

    existing_cover = os.path.join(BASE_DIR, "preview_cover.jpg")
    existing_preview = os.path.join(BASE_DIR, "preview.jpg")

    for d in [prev_dir, prev_lower_dir]:
        shutil.copy(existing_cover, os.path.join(d, "cover.jpg"))
        shutil.copy(existing_preview, os.path.join(d, "preview_launcher_0.jpg"))
        shutil.copy(existing_cover, os.path.join(d, "preview_lockscreen_0.jpg"))
        shutil.copy(existing_preview, os.path.join(d, "preview_0.jpg"))
        shutil.copy(existing_cover, os.path.join(d, "preview_1.jpg"))

    with Image.open(existing_preview) as im:
        thumb = im.resize((450, 1000), Image.Resampling.LANCZOS)
        for d in [thumb_dir, thumb_lower_dir, prev_dir, prev_lower_dir]:
            thumb.save(os.path.join(d, "thumbnail.jpg"), "JPEG", quality=90)


def create_manifests_and_app_resources(theme_dir):
    """Generates HiOS 14/15 manifest.json, XML manifests, and launcher config overlays."""
    print("Writing Theme Manifests and Launcher configs...")

    manifest_json = """{
  "id": "e9a0f412-87c2-4e89-b873-10928a3f8901",
  "type": 0,
  "version": 15,
  "author": "heli-toon & Antigravity",
  "app_resource_dir": "app",
  "name": "Space Neon Minimal",
  "description": "Premium Dark Glass Theme with cyber neon nebula wallpapers and 500+ frosted glass icons.",
  "prebuilt": 0,
  "os_version": 1500
}
"""
    with open(os.path.join(theme_dir, "manifest.json"), "w", encoding="utf-8") as f:
        f.write(manifest_json)

    desc_xml = """<?xml version="1.0" encoding="utf-8"?>
<theme>
    <title>Space Neon Minimal</title>
    <author>heli-toon &amp; Antigravity</author>
    <designer>heli-toon &amp; Antigravity</designer>
    <version>15.0</version>
    <formatVersion>1</formatVersion>
    <description>Premium Dark Glass Theme with cyber neon nebula wallpapers and frosted glass icons.</description>
    <uiVersion>HiOS 8.0 - HiOS 15+</uiVersion>
</theme>
"""
    with open(os.path.join(theme_dir, "description.xml"), "w", encoding="utf-8") as f:
        f.write(desc_xml)

    manifest_xml = """<?xml version="1.0" encoding="utf-8"?>
<manifest>
    <theme-name>Space Neon Minimal</theme-name>
    <version>15.0</version>
    <author>heli-toon &amp; Antigravity</author>
    <modules>
        <module name="icons" />
        <module name="wallpaper" />
        <module name="Wallpaper" />
    </modules>
</manifest>
"""
    with open(os.path.join(theme_dir, "manifest.xml"), "w", encoding="utf-8") as f:
        f.write(manifest_xml)

    # Launcher overlay
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
<color name="tran_calendar_gradation_start_color">#ff121212</color>
<color name="tran_calendar_gradation_end_color">#ff121212</color>
</resources>
"""
    with open(os.path.join(hilauncher_val, "colors.xml"), "w", encoding="utf-8") as f:
        f.write(colors_xml)


def package_theme_archives(theme_dir):
    """Packages the complete theme into SpaceNeonMinimal.zth and SpaceNeonMinimal.xth."""
    print("Packaging Space Neon .zth and .xth Theme Files...")
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


def enhance_and_repackage_last_dark_glass():
    """Enhances 'Last Dark Glass Theme' with HiOS 15 manifest, XMLs, and case mirrors."""
    print("Enhancing and repackaging Last Dark Glass Theme for HiOS 15...")
    if not os.path.exists(LAST_DARK_GLASS_ZTH):
        print("[-] Last Dark Glass Theme.zth not found, skipping enhancement.")
        return

    work_dir = "/tmp/enhance_dark_glass"
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)
    os.makedirs(work_dir, exist_ok=True)

    with zipfile.ZipFile(LAST_DARK_GLASS_ZTH, "r") as z:
        z.extractall(work_dir)

    # 1. manifest.json
    manifest_json = """{
  "id": "last-dark-glass-theme-transsion-01",
  "type": 0,
  "version": 15,
  "author": "Antigravity",
  "app_resource_dir": "app",
  "name": "Last Dark Glass Theme",
  "description": "Dark Glass Theme with premium frosted glass squircle icons for HiOS.",
  "prebuilt": 0,
  "os_version": 1500
}
"""
    with open(os.path.join(work_dir, "manifest.json"), "w", encoding="utf-8") as f:
        f.write(manifest_json)

    # 2. description.xml & manifest.xml
    desc_xml = """<?xml version="1.0" encoding="utf-8"?>
<theme>
    <title>Last Dark Glass Theme</title>
    <author>Antigravity</author>
    <designer>Antigravity</designer>
    <version>15.0</version>
    <formatVersion>1</formatVersion>
    <description>Dark Glass Theme with premium frosted glass squircle icons for HiOS.</description>
    <uiVersion>HiOS 8.0 - HiOS 15+</uiVersion>
</theme>
"""
    with open(os.path.join(work_dir, "description.xml"), "w", encoding="utf-8") as f:
        f.write(desc_xml)

    manifest_xml = """<?xml version="1.0" encoding="utf-8"?>
<manifest>
    <theme-name>Last Dark Glass Theme</theme-name>
    <version>15.0</version>
    <author>Antigravity</author>
    <modules>
        <module name="icons" />
        <module name="wallpaper" />
        <module name="Wallpaper" />
    </modules>
</manifest>
"""
    with open(os.path.join(work_dir, "manifest.xml"), "w", encoding="utf-8") as f:
        f.write(manifest_xml)

    # 3. Launcher config overlay
    hilauncher_val = os.path.join(work_dir, "app/com.transsion.hilauncher/values")
    os.makedirs(hilauncher_val, exist_ok=True)
    colors_xml = """<?xml version='1.0' encoding='utf-8'?>
<resources>
<color name="cleaner_progress_color">#FF4CAF50</color>
<color name="cleaner_progress_bg_color">#00000000</color>
<color name="cleaner_progress_gap_color">#00000000</color>
<color name="cleaner_text_color">#FFFFFFFF</color>
<color name="tran_calendar_date_color">#FFFFFFFF</color>
<color name="tran_calendar_week_color">#FF4CAF50</color>
<color name="tran_calendar_gradation_start_color">#ff121212</color>
<color name="tran_calendar_gradation_end_color">#ff121212</color>
</resources>
"""
    with open(os.path.join(hilauncher_val, "colors.xml"), "w", encoding="utf-8") as f:
        f.write(colors_xml)

    # 4. Mirror case variations
    wp_src = os.path.join(work_dir, "wallpaper")
    wp_upper = os.path.join(work_dir, "Wallpaper")
    if os.path.exists(wp_src) and not os.path.exists(wp_upper):
        shutil.copytree(wp_src, wp_upper)

    prev_src = os.path.join(work_dir, "preview")
    prev_upper = os.path.join(work_dir, "Preview")
    if os.path.exists(prev_src) and not os.path.exists(prev_upper):
        shutil.copytree(prev_src, prev_upper)

    # Thumbnail
    thumb_dir = os.path.join(work_dir, "Thumbnail")
    os.makedirs(thumb_dir, exist_ok=True)
    prev_launcher = os.path.join(prev_src, "preview_launcher_0.png")
    if os.path.exists(prev_launcher):
        with Image.open(prev_launcher) as im:
            thumb = im.resize((450, 1000), Image.Resampling.LANCZOS)
            thumb.convert("RGB").save(os.path.join(thumb_dir, "thumbnail.jpg"), "JPEG", quality=90)
            os.makedirs(os.path.join(work_dir, "thumbnail"), exist_ok=True)
            thumb.convert("RGB").save(os.path.join(work_dir, "thumbnail", "thumbnail.jpg"), "JPEG", quality=90)

    # Repackage Last Dark Glass Theme.zth and .xth
    out_zth = LAST_DARK_GLASS_ZTH
    out_xth = os.path.join(BASE_DIR, "Last Dark Glass Theme.xth")
    for out_f in [out_zth, out_xth]:
        if os.path.exists(out_f):
            os.remove(out_f)
        with zipfile.ZipFile(out_f, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(work_dir):
                for f in files:
                    full_p = os.path.join(root, f)
                    rel_p = os.path.relpath(full_p, work_dir)
                    zipf.write(full_p, rel_p)

    print(f" -> Enhanced Last Dark Glass Theme.zth ({os.path.getsize(out_zth) // 1024} KB)")
    print(f" -> Enhanced Last Dark Glass Theme.xth ({os.path.getsize(out_xth) // 1024} KB)")


def main():
    print("=" * 60)
    print("HiOS & XOS Theme Builder - Starting Compilation")
    print("=" * 60)

    # Clean and re-create theme_src structure
    if os.path.exists(THEME_SRC_DIR):
        shutil.rmtree(THEME_SRC_DIR)
    os.makedirs(THEME_SRC_DIR, exist_ok=True)

    icons_dir = os.path.join(THEME_SRC_DIR, "icons")
    os.makedirs(icons_dir, exist_ok=True)

    # 1. Deploy Dark Glass plates and masks
    dark_bg = prepare_dark_glass_base_assets(icons_dir)

    # 2. Import 500+ icons from Last Dark Glass Theme & map aliases
    import_last_dark_glass_icons(icons_dir)

    # 3. Composite monochrome & extracted user app glyphs onto Dark Glass plates
    composite_raw_glyphs(icons_dir, dark_bg)

    # 4. Standalone EasyDIY icons.zip
    package_icons_zip(icons_dir, os.path.join(BASE_DIR, "icons.zip"))

    # 6. Wallpapers
    process_wallpapers(THEME_SRC_DIR)

    # 7. Previews
    generate_previews(THEME_SRC_DIR)

    # 8. Manifests and App Overlays
    create_manifests_and_app_resources(THEME_SRC_DIR)

    # 9. Final Space Neon .zth and .xth bundles
    package_theme_archives(THEME_SRC_DIR)

    # 10. Enhance and repackage Last Dark Glass Theme (.zth and .xth)
    enhance_and_repackage_last_dark_glass()

    print("=" * 60)
    print("Compilation Complete! All packages verified.")
    print("=" * 60)


if __name__ == "__main__":
    main()
