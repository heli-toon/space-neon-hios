#!/usr/bin/env python3
"""
Space Neon HiOS & XOS Theme Builder - Pure YAMIS Monochrome & Dark Glass Edition
Compiles KDE Plasma "Space Neon Minimal" assets into a production-ready
Tecno HiOS (.zth), Infinix XOS (.xth), and EasyDIY (icons.zip) theme suite.

Design Philosophy:
- Core: Sleek Dark Glass squircle background plate & masks from "Last Dark Glass Theme"
- Glyphs: 100% YAMIS white monochrome minimalist icons composited on Dark Glass plates
- Fallback: Individual Dark Glass icons ONLY for apps without a YAMIS monochrome version
- Unthemed Apps: OEM squircle clipping mask (icon_mask) and background plate (icon_bg)
- Component Mapping: Full Transsion launcher friendly names, dot package, underscore package,
  and exact launcher activity component aliases (both .png and .webp)
"""

import os
import io
import shutil
import zipfile
import sys
from PIL import Image

# Ensure builder dir in sys.path
BUILDER_DIR = os.path.dirname(os.path.abspath(__file__))
if BUILDER_DIR not in sys.path:
    sys.path.insert(0, BUILDER_DIR)

try:
    import generate_fixed_icons
except ImportError:
    generate_fixed_icons = None
BASE_DIR = os.path.dirname(BUILDER_DIR)
DARK_GLASS_ASSETS_DIR = os.path.join(BUILDER_DIR, "dark_glass_assets")
EXTRACTED_ICONS_DIR = os.path.join(BUILDER_DIR, "extracted_user_icons")
RAW_PNG_512_DIR = os.path.join(BASE_DIR, "raw_monochrome_pngs_512")
RAW_PNG_256_DIR = os.path.join(BASE_DIR, "raw_monochrome_pngs_256")
WALLPAPERS_DIR = os.path.join(BASE_DIR, "wallpapers")
THEME_SRC_DIR = os.path.join(BASE_DIR, "theme_src")
LAST_DARK_GLASS_ZTH = os.path.join(BASE_DIR, "Last Dark Glass Theme.zth")

# Comprehensive Package / Component / Activity Aliases for HiOS Launcher
PACKAGE_COMPONENT_ALIASES = {
    # 1. Weather (Tecno HiOS OEM Weather: com.rlk.weathers)
    "com_rlk_weathers": [
        "Weather",
        "com.rlk.weathers",
        "com_rlk_weathers_activity_weathermainactivity",
        "com_rlk_weathers_ui_main_MainActivity",
        "com_rlk_weathers_MainActivity",
        "com.transsion.weather",
        "com_transsion_weather",
        "com.google.android.apps.weather",
        "com_google_android_apps_weather",
    ],
    # 2. WhatsApp & WhatsApp Business
    "com_whatsapp": [
        "WhatsApp",
        "com.whatsapp",
        "com_whatsapp_Main",
        "com_whatsapp_com_whatsapp_Main",
    ],
    "com_whatsapp_w4b": [
        "WhatsAppBusiness",
        "WhatsApp4b",
        "WhatsApp_Business",
        "com.whatsapp.w4b",
        "com_whatsapp_w4b_Main",
        "com_whatsapp_w4b_com_whatsapp_Main",
    ],
    # 3. Telegram & Telegram Web (including AquaIcon, DefaultIcon, etc.)
    "org_telegram_messenger_web": [
        "Telegram",
        "TelegramWeb",
        "TelegramX",
        "org.telegram.messenger",
        "org_telegram_messenger",
        "org.telegram.messenger.web",
        "org_telegram_messenger_AquaIcon",
        "org_telegram_messenger_web_AquaIcon",
        "org_telegram_messenger_web_org_telegram_messenger_AquaIcon",
        "org_telegram_messenger_DefaultIcon",
        "org_telegram_messenger_web_DefaultIcon",
        "org_telegram_messenger_web_org_telegram_messenger_DefaultIcon",
        "org_telegram_messenger_NoxIcon",
        "org_telegram_messenger_TurboIcon",
        "org_telegram_messenger_PremiumIcon",
        "org_telegram_messenger_VintageIcon",
        "org_telegram_messenger_web_LaunchActivity",
        "org_telegram_ui_LaunchActivity",
        "org_telegram_ui_LaunchActivityDefaultIcon",
        "org.telegram.plus",
        "org_telegram_plus",
    ],
    # 4. Twitter / X
    "com_twitter_android": [
        "X",
        "Twitter",
        "com.twitter.android",
        "com_twitter_android_MainActivity",
        "com_twitter_android_com_x_android_main_MainActivity",
        "com_x_android_main_MainActivity",
        "com_twitter_android_StartActivity",
    ],
    # 5. KDE Connect
    "org_kde_kdeconnect_tp": [
        "KDEConnect",
        "kdeconnect",
        "KdeConnect",
        "org.kde.kdeconnect_tp",
        "org.kde.kdeconnect",
        "org_kde_kdeconnect",
        "org_kde_kdeconnect_tp_MainActivity",
        "org_kde_kdeconnect_tp_org_kde_kdeconnect_ui_MainActivity",
        "org_kde_kdeconnect_ui_MainActivity",
        "org_kde_kdeconnect_KdeConnect",
    ],
    # 6. Anytype
    "io_anytype_app": [
        "Anytype",
        "anytype",
        "io.anytype.app",
        "io.anytype.mobile",
        "io_anytype_mobile",
        "io_anytype_app_MainActivity",
        "io_anytype_app_com_anytypeio_anytype_ui_main_MainActivity",
    ],
    # 7. Outlook (Dark Glass individual fallback)
    "com_microsoft_office_outlook": [
        "Outlook",
        "com.microsoft.office.outlook",
        "com_microsoft_office_outlook_MainActivity",
        "com_microsoft_office_outlook_com_microsoft_office_outlook_MainActivity",
    ],
    # 8. Gemini / Bard (Dark Glass individual fallback)
    "com_google_android_apps_bard": [
        "Gemini",
        "bard",
        "com.google.android.apps.bard",
        "com_google_android_apps_bard_BardEntryPointActivity",
        "com_google_android_apps_bard_shellapp_BardEntryPointActivity",
        "com_google_android_apps_bard_com_google_android_apps_bard_shellapp_BardEntryPointActivity",
        "com_google_android_apps_bard_MainActivity",
    ],
    # Chrome / Browser
    "com_android_chrome": [
        "Chrome",
        "PHXBrowser",
        "Browser",
        "com.android.chrome",
        "com_google_android_apps_chrome_Main",
        "com_android_chrome_Main",
    ],
    # Settings
    "com_android_settings": [
        "Settings",
        "com.android.settings",
        "com_transsion_settings",
        "com_android_settings_ic_launcher_settings",
        "com_android_settings_Settings",
    ],
    # Phone / Dialer
    "com_sh_smart_caller": [
        "Phone",
        "Dialer",
        "com.sh.smart.caller",
        "com_android_dialer",
        "com_android_phone",
        "com.android.dialer",
        "com.google.android.dialer",
        "com_google_android_dialer",
        "com_android_dialer_ic_launcher_phone",
        "com_sh_smart_caller_MainActivity",
        "com_sh_smart_caller_ui_main_MainActivity",
    ],
    # Contacts
    "com_android_contacts": [
        "Contacts",
        "Contact",
        "com.android.contacts",
        "com_android_contacts",
        "com.google.android.contacts",
        "com_google_android_contacts",
        "com.transsion.contacts",
        "com_transsion_contacts",
        "com_android_contacts_ic_launcher_contacts",
        "com_sh_smart_caller_ContactMainActivity",
        "com_google_android_contacts_activities_PeopleActivity",
    ],
    # Camera
    "com_transsion_camera": [
        "Camera",
        "com.transsion.camera",
        "com_android_camera",
        "com.android.camera",
        "com_android_camera_cameralauncher",
        "com_transsion_camera_CameraLauncher",
    ],
    # Calculator
    "com_transsion_calculator": [
        "Calculator",
        "com.transsion.calculator",
        "com_android_calculator2",
        "com.android.calculator2",
        "com.google.android.calculator",
        "com_google_android_calculator",
        "com_android_calculator2_ic_launcher_calculator",
    ],
    # Calendar
    "com_google_android_calendar": [
        "Calendar",
        "com.google.android.calendar",
        "com_android_calendar",
        "com.android.calendar",
        "com_transsion_calendar",
        "com.transsion.calendar",
        "com_android_calendar_AllInOneActivity",
    ],
    # Clock
    "com_transsion_deskclock": [
        "Clock",
        "com.transsion.deskclock",
        "com_android_deskclock",
        "com.android.deskclock",
        "com.google.android.deskclock",
        "com_google_android_deskclock",
        "com_transsion_deskclock_deskclock",
    ],
    # Gallery
    "com_transsion_aigallery": [
        "Gallery",
        "com.transsion.aigallery",
        "com_android_gallery3d",
        "com.android.gallery3d",
        "com_gallery20_homeactivity",
        "com_gallery20_activities_GalleryActivity",
    ],
    # File Manager
    "com_transsion_filemanager": [
        "FileManager",
        "com.transsion.filemanager",
        "com_transsion_filemanagerx",
        "com.transsion.filemanagerx",
        "com_transsion_filemanagerx_ui_main_mainactivity",
        "com.android.filemanager",
        "com_android_filemanager",
        "com.alphainventor.filemanager",
        "com_alphainventor_filemanager",
    ],
    # Files by Google
    "com_google_android_apps_nbu_files": [
        "Files",
        "GoogleFiles",
        "com.google.android.apps.nbu.files",
        "com_google_android_apps_nbu_files_home_HomeActivity",
    ],
    # Google Photos
    "com_google_android_apps_photos": [
        "GooglePhotos",
        "Gphotos",
        "Photos",
        "com.google.android.apps.photos",
        "com_google_android_apps_photos_home_HomeActivity",
    ],
    # Google Maps
    "com_google_android_apps_maps": [
        "GoogleMaps",
        "Maps",
        "com.google.android.apps.maps",
        "com_google_android_maps_MapsActivity",
    ],
    # Google Search / QuickSearchBox
    "com_google_android_googlequicksearchbox": [
        "QuickSearchBox",
        "Google",
        "com.google.android.googlequicksearchbox",
        "com_google_android_googlequicksearchbox_SearchActivity",
    ],
    # Gmail
    "com_google_android_gm": [
        "Gmail",
        "Email",
        "com.google.android.gm",
        "com_google_android_gm_ConversationListActivityGmail",
    ],
    # Google Messages / SMS
    "com_google_android_apps_messaging": [
        "Messages",
        "com.google.android.apps.messaging",
        "com_android_mms",
        "com.android.mms",
        "com_android_messaging",
        "com_google_android_apps_messaging_ConversationListActivity",
    ],
    # YouTube
    "com_google_android_youtube": [
        "Youtube",
        "YouTube",
        "com.google.android.youtube",
        "com_google_android_youtube_Shell_HomeActivity",
    ],
    # YouTube Music
    "com_google_android_apps_youtube_music": [
        "YouTubeMusic",
        "YTMusic",
        "Music",
        "com.google.android.apps.youtube.music",
        "com_google_android_apps_youtube_music_activities_MusicActivity",
    ],
    # Google Play Store
    "com_android_vending": [
        "PlayStore",
        "com.android.vending",
        "com_android_vending_AssetBrowserActivity",
    ],
    # Instagram
    "com_instagram_android": [
        "Instagram",
        "com.instagram.android",
        "com_instagram_android_activity_MainTabActivity",
    ],
    # Hi Theme
    "com_transsion_theme": [
        "Theme",
        "Themes",
        "com.transsion.theme",
        "com_transsion_theme_common_xthememain",
        "com.transsion.xtheme",
        "com_transsion_xtheme",
    ],
    # Sound Recorder
    "com_transsion_soundrecorder": [
        "Recorder",
        "SoundRecorder",
        "com.transsion.soundrecorder",
        "com_android_soundrecorder",
        "com.android.soundrecorder",
        "com_transsion_soundrecorder_SoundRecorder",
        "com_android_soundrecorder_ic_launcher_soundrecorder_am",
    ],
    # Compass
    "com_transsion_compass": [
        "Compass",
        "com.transsion.compass",
        "com_transsion_compass_CompassActivity",
    ],
    # VLC
    "org_videolan_vlc": [
        "VLC",
        "VideoPlayer",
        "org.videolan.vlc",
        "org_videolan_vlc_StartActivity",
    ],
    # Termux
    "com_termux": [
        "Termux",
        "com.termux",
        "com_termux_app_TermuxActivity",
    ],
    # GitHub
    "com_github_android": [
        "GitHub",
        "com.github.android",
        "com_github_android_main_MainActivity",
    ],
    # Claude
    "com_anthropic_claude": [
        "Claude",
        "com.anthropic.claude",
        "com_anthropic_claude_MainActivity",
        "com_anthropic_claude_mainactivity_MainActivity",
    ],
    # Slack
    "com_slack": [
        "Slack",
        "com.Slack",
        "com_Slack",
        "com_Slack_HomeActivity",
        "slack_app_HomeActivity",
    ],
    # Duolingo
    "com_duolingo": [
        "Duolingo",
        "com.duolingo",
        "com_duolingo_LoginActivity",
        "com_duolingo_app_LoginActivity",
    ],
    # F-Droid
    "org_fdroid_fdroid": [
        "FDroid",
        "F-Droid",
        "org.fdroid.fdroid",
        "org_fdroid_fdroid_IconActivity",
    ],
    # Microsoft Teams
    "com_microsoft_teams": [
        "Teams",
        "com.microsoft.teams",
        "com_microsoft_teams_Launcher",
        "com_microsoft_skype_teams_Launcher",
    ],
    # Zoom
    "us_zoom_videomeetings": [
        "Zoom",
        "us.zoom.videomeetings",
        "us_zoom_videomeetings_LauncherActivity",
        "com_zipow_videobox_LauncherActivity",
    ],
    # Xender
    "cn_xender": [
        "Xender",
        "cn.xender",
        "cn_xender_SplashActivity",
        "cn_xender_ui_activity_SplashActivity",
    ],
    # CPU-Z
    "com_cpuid_cpu_z": [
        "CPUZ",
        "CPU-Z",
        "com.cpuid.cpu_z",
        "com_cpuid_cpu_z_MainActivity",
    ],
    # Spotify
    "com_spotify_music": [
        "Spotify",
        "com.spotify.music",
    ],
    # ChatGPT
    "com_openai_chatgpt": [
        "ChatGPT",
        "com.openai.chatgpt",
        "com_openai_chatgpt_MainActivity",
    ],
    # Google Drive / Docs / Sheets
    "com_google_android_apps_docs": [
        "GoogleDrive",
        "Gdrive",
        "com.google.android.apps.docs",
        "com_google_android_apps_docs_app_NewMainProxyActivity",
    ],
    "com_google_android_apps_docs_editors_sheets": [
        "GoogleSheets",
        "Sheets",
        "com.google.android.apps.docs.editors.sheets",
        "com_google_android_apps_docs_editors_sheets_app_NewMainProxyActivity",
    ],
    # Facebook & Messenger
    "com_facebook_katana": [
        "Facebook",
        "com.facebook.katana",
        "com_facebook_katana_LoginActivity",
    ],
    "com_facebook_orca": [
        "Messenger",
        "com.facebook.orca",
        "com_facebook_orca_StartScreenActivity",
    ],
    # LinkedIn
    "com_linkedin_android": [
        "LinkedIn",
        "com.linkedin.android",
        "com_linkedin_android_LaunchActivityDefault",
    ],
    # Discord
    "com_discord": [
        "Discord",
        "com.discord",
        "com_discord_MainDefault",
    ],
    # WPS Office
    "cn_wps_moffice_eng": [
        "WPSOffice",
        "cn.wps.moffice_eng",
        "cn_wps_moffice_documentmanager_PreStartActivity",
    ],
    # Binance
    "com_binance_dev": [
        "Binance",
        "com.binance.dev",
        "com_binance_dev_MainActivity",
    ],
    # Notes / Notebook
    "com_transsion_notebook": [
        "Notes",
        "com.transsion.notebook",
        "com_transsion_notebook_NotesList",
    ],
}

# Individual apps installed on user device that need fallback Dark Glass icons
# (ONLY if a YAMIS monochrome icon is NOT present)
DARK_GLASS_INDIVIDUAL_FALLBACK_APPS = [
    "com_microsoft_office_outlook",
    "com_google_android_apps_bard",
    "cn_wps_moffice_eng",
    "com_binance_dev",
    "com_discord",
    "com_facebook_katana",
    "com_facebook_orca",
    "com_facebook_pages_app",
    "com_google_android_apps_adm",
    "com_google_android_apps_authenticator2",
    "com_google_android_apps_docs",
    "com_google_android_apps_docs_editors_sheets",
    "com_google_android_apps_googleassistant",
    "com_google_android_apps_safetyhub",
    "com_google_android_apps_tachyon",
    "com_google_android_apps_wellbeing",
    "com_google_android_play_games",
    "com_linkedin_android",
    "com_openai_chatgpt",
    "com_alphainventor_filemanager",
    "com_transsion_mobilecloner",
    "com_azure_authenticator",
    "com_transsion_notebook",
]


def prepare_dark_glass_base_assets(icons_dir):
    """Copies dark glass squircle background, masks, dynamic calendar & clock assets."""
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
        # Also create lossless WebP equivalent
        try:
            with Image.open(src_p) as im:
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


def composite_raw_glyphs(icons_dir, dark_bg):
    """
    Composites pure white monochrome YAMIS PNG glyphs onto the Dark Glass plate.
    Prioritizes 512x512 raw assets for maximum downsampling sharpness.
    """
    print("Compositing YAMIS pure white monochrome icons onto Dark Glass plates...")
    yamis_handled_keys = set()

    def composite_glyph(glyph_img, target_size=150):
        bbox = glyph_img.getbbox()
        glyph_cropped = glyph_img.crop(bbox) if bbox else glyph_img
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

    # Collect all available monochrome glyph sources (512 preferred, 256 fallback)
    available_monos = {}
    if os.path.exists(RAW_PNG_512_DIR):
        for f in os.listdir(RAW_PNG_512_DIR):
            if f.endswith(".png"):
                available_monos[f] = os.path.join(RAW_PNG_512_DIR, f)

    if os.path.exists(RAW_PNG_256_DIR):
        for f in os.listdir(RAW_PNG_256_DIR):
            if f.endswith(".png") and f not in available_monos:
                available_monos[f] = os.path.join(RAW_PNG_256_DIR, f)

    for raw_f, raw_path in available_monos.items():
        pkg_base, _ = os.path.splitext(raw_f)
        under_pkg = pkg_base.replace(".", "_")

        with Image.open(raw_path) as im:
            glyph = im.convert("RGBA")
            icon = composite_glyph(glyph, target_size=150)

            # Dot package name
            icon.save(os.path.join(icons_dir, f"{pkg_base}.png"), "PNG")
            icon.save(os.path.join(icons_dir, f"{pkg_base}.webp"), "WEBP", quality=100, lossless=True, method=0)

            # Underscore package name
            icon.save(os.path.join(icons_dir, f"{under_pkg}.png"), "PNG")
            icon.save(os.path.join(icons_dir, f"{under_pkg}.webp"), "WEBP", quality=100, lossless=True, method=0)

            yamis_handled_keys.add(pkg_base)
            yamis_handled_keys.add(under_pkg)

    # 2. Extracted user icons (Claude, Slack, Teams, Duolingo, CPU-Z, etc.)
    if os.path.exists(EXTRACTED_ICONS_DIR):
        for f in os.listdir(EXTRACTED_ICONS_DIR):
            if not f.endswith(".png"):
                continue
            pkg = f.replace("_icon.png", "")
            under_pkg = pkg.replace(".", "_")
            raw_path = os.path.join(EXTRACTED_ICONS_DIR, f)

            with Image.open(raw_path) as im:
                glyph = im.convert("RGBA")
                icon = composite_glyph(glyph, target_size=155)

                for name_variant in [pkg, under_pkg]:
                    icon.save(os.path.join(icons_dir, f"{name_variant}.png"), "PNG")
                    icon.save(os.path.join(icons_dir, f"{name_variant}.webp"), "WEBP", quality=100, lossless=True, method=0)
                    yamis_handled_keys.add(name_variant)

    print(f" -> Generated {len(yamis_handled_keys)} YAMIS dark glass base icons.")
    return yamis_handled_keys


def import_fallback_dark_glass_icons(icons_dir, yamis_handled_keys):
    """
    Imports INDIVIDUAL icons from Last Dark Glass Theme ONLY IF no YAMIS monochrome
    version exists for that app. Does NOT bulk import the 500+ Dark Glass pack.
    """
    print("Checking individual Dark Glass fallback icons for non-YAMIS apps...")
    if not os.path.exists(LAST_DARK_GLASS_ZTH):
        print("[-] Last Dark Glass Theme.zth not found, skipping fallbacks.")
        return

    imported_count = 0
    with zipfile.ZipFile(LAST_DARK_GLASS_ZTH, "r") as z:
        dark_glass_files = {os.path.basename(f): f for f in z.namelist() if f.startswith("icons/") and f.endswith(".png")}

        for app_key in DARK_GLASS_INDIVIDUAL_FALLBACK_APPS:
            dot_key = app_key.replace("_", ".")
            # Only import if NOT already handled by YAMIS
            if app_key in yamis_handled_keys or dot_key in yamis_handled_keys:
                continue

            # Look for matching icon in Dark Glass archive
            source_entry = None
            for candidate in [f"{app_key}.png", f"{dot_key}.png"]:
                if candidate in dark_glass_files:
                    source_entry = dark_glass_files[candidate]
                    break

            # Special case for Gemini / Bard
            if not source_entry and "bard" in app_key:
                if "bard.png" in dark_glass_files:
                    source_entry = dark_glass_files["bard.png"]

            if source_entry:
                dest_png = os.path.join(icons_dir, f"{app_key}.png")
                with open(dest_png, "wb") as out:
                    out.write(z.read(source_entry))

                # Save matching lossless WebP
                dest_webp = os.path.join(icons_dir, f"{app_key}.webp")
                try:
                    with Image.open(dest_png) as im:
                        im.save(dest_webp, "WEBP", quality=100, lossless=True, method=0)
                except Exception:
                    pass

                imported_count += 1
                print(f"  [Fallback Added] {app_key} from {source_entry}")

    print(f" -> Imported {imported_count} individual Dark Glass fallback icons.")


def cross_bind_aliases(icons_dir, yamis_handled_keys):
    """
    Binds all friendly component names, dot packages, underscore packages,
    and exact launcher activity aliases to their respective master icon.
    Prioritizes YAMIS monochrome master icons above all else.
    """
    print("Cross-binding Transsion friendly names, underscore & dot packages, and launcher activities...")
    existing_files = set(os.listdir(icons_dir))

    for key, aliases in PACKAGE_COMPONENT_ALIASES.items():
        candidates = [key] + aliases

        # 1. Identify source file (prefer YAMIS monochrome version if present)
        source_base = None
        for c in candidates:
            if c in yamis_handled_keys and f"{c}.png" in existing_files:
                source_base = c
                break

        # Fallback to any existing candidate
        if not source_base:
            for c in candidates:
                if f"{c}.png" in existing_files:
                    source_base = c
                    break

        if not source_base:
            continue

        src_png_path = os.path.join(icons_dir, f"{source_base}.png")
        if not os.path.exists(src_png_path):
            continue

        # Load master image once
        with Image.open(src_png_path) as master_im:
            master_rgba = master_im.convert("RGBA")

            for target in candidates:
                tgt_png = f"{target}.png"
                tgt_webp = f"{target}.webp"
                tgt_png_path = os.path.join(icons_dir, tgt_png)
                tgt_webp_path = os.path.join(icons_dir, tgt_webp)

                # Overwrite or create PNG
                master_rgba.save(tgt_png_path, "PNG")
                existing_files.add(tgt_png)

                # Overwrite or create WebP
                master_rgba.save(tgt_webp_path, "WEBP", quality=100, lossless=True, method=0)
                existing_files.add(tgt_webp)

    print(f"Total icon files in Space Neon build: {len(os.listdir(icons_dir))}")


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
  "description": "Premium Dark Glass Theme with cyber neon nebula wallpapers and crisp YAMIS white monochrome icons.",
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
    <description>Premium Dark Glass Theme with cyber neon nebula wallpapers and crisp YAMIS white monochrome icons.</description>
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


def main():
    print("=" * 60)
    print("Space Neon HiOS Theme Builder - Pure YAMIS Edition")
    print("=" * 60)

    # Clean and re-create theme_src structure
    if os.path.exists(THEME_SRC_DIR):
        shutil.rmtree(THEME_SRC_DIR)
    os.makedirs(THEME_SRC_DIR, exist_ok=True)

    icons_dir = os.path.join(THEME_SRC_DIR, "icons")
    os.makedirs(icons_dir, exist_ok=True)

    # 0. Synchronize / generate all high-res official vector glyphs
    if generate_fixed_icons:
        generate_fixed_icons.create_all_icons()

    # 1. Deploy Dark Glass plates and masks
    dark_bg = prepare_dark_glass_base_assets(icons_dir)

    # 2. Composite YAMIS monochrome white icons onto Dark Glass plates
    yamis_handled_keys = composite_raw_glyphs(icons_dir, dark_bg)

    # 3. Import individual Dark Glass fallback icons ONLY if no YAMIS icon exists
    import_fallback_dark_glass_icons(icons_dir, yamis_handled_keys)

    # 4. Cross-bind all aliases, component names, and launcher activities
    cross_bind_aliases(icons_dir, yamis_handled_keys)

    # 5. Standalone EasyDIY icons.zip
    package_icons_zip(icons_dir, os.path.join(BASE_DIR, "icons.zip"))

    # 6. Wallpapers
    process_wallpapers(THEME_SRC_DIR)

    # 7. Previews
    generate_previews(THEME_SRC_DIR)

    # 8. Manifests and App Overlays
    create_manifests_and_app_resources(THEME_SRC_DIR)

    # 9. Final Space Neon .zth and .xth bundles
    package_theme_archives(THEME_SRC_DIR)

    print("=" * 60)
    print("Compilation Complete! All packages verified.")
    print("=" * 60)


if __name__ == "__main__":
    main()
