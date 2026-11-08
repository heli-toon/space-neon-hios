#!/usr/bin/env python3
"""
Space Neon HiOS Theme Builder
Compiles KDE Plasma "Space Neon Minimal" assets into a production-ready
Tecno HiOS (.zth) and Infinix XOS (.xth) theme package.

Features:
- Scales & renders monochrome vector glyphs into cyber-neon squircle icons
- Generates high-res 1080x2400 phone wallpapers from 4K Plasma wallpapers
- Creates HiTheme-compliant directory hierarchy (Icons, Wallpaper, Preview, Thumbnail)
- Builds description.xml and manifest.xml with proper Transsion tags
- Produces individual transparent monochrome PNGs for desktop Theme Creation Tools
- Assembles valid, flashable .zth and .xth archives
"""

import os
import io
import zipfile
import shutil
from PIL import Image, ImageDraw, ImageFont
import cairosvg

# Project root paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLASMA_DIR = os.path.join(os.path.dirname(BASE_DIR), "space-neon-plasma")
YAMIS_DIR = os.path.expanduser("~/.local/share/icons/YAMIS")
PAPIRUS_DIR = "/usr/share/icons/Papirus"

THEME_SRC_DIR = os.path.join(BASE_DIR, "theme_src")
ICONS_DIR = os.path.join(THEME_SRC_DIR, "Icons")
WALLPAPER_DIR = os.path.join(THEME_SRC_DIR, "Wallpaper")
PREVIEW_DIR = os.path.join(THEME_SRC_DIR, "Preview")
THUMBNAIL_DIR = os.path.join(THEME_SRC_DIR, "Thumbnail")

RAW_PNG_256_DIR = os.path.join(BASE_DIR, "raw_monochrome_pngs_256")
RAW_PNG_512_DIR = os.path.join(BASE_DIR, "raw_monochrome_pngs_512")
WALLPAPERS_OUT_DIR = os.path.join(BASE_DIR, "wallpapers")

# Color Palette (matches Space Neon Plasma colors)
COLOR_BG_BLACK = (10, 10, 11, 255)       # #0A0A0B (pitch deep space black)
COLOR_SURFACE = (14, 15, 19, 255)        # #0E0F13 (squircle body)
COLOR_NEON_ORANGE = (255, 107, 0, 255)   # #FF6B00 (neon accent)
COLOR_ORANGE_BORDER = (255, 107, 0, 220) # #FF6B00 border
COLOR_WHITE = (245, 245, 245, 255)       # crisp white glyph
HEX_ORANGE = "#FF6B00"
HEX_WHITE = "#FFFFFF"

# Custom inline vector SVG glyphs for icons not in local sets or needing precision styling
VECTOR_GLYPHS = {
    "message": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
        <path fill="#ffffff" d="M 10 14 C 6.7 14 4 16.7 4 20 L 4 42 C 4 45.3 6.7 48 10 48 L 18 48 L 18 56 L 28 48 L 54 48 C 57.3 48 60 45.3 60 42 L 60 20 C 60 16.7 57.3 14 54 14 Z M 20 28 A 3.2 3.2 0 1 1 20 34.4 A 3.2 3.2 0 1 1 20 28 Z M 32 28 A 3.2 3.2 0 1 1 32 34.4 A 3.2 3.2 0 1 1 32 28 Z M 44 28 A 3.2 3.2 0 1 1 44 34.4 A 3.2 3.2 0 1 1 44 28 Z"/>
    </svg>''',
    
    "whatsapp": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
        <path fill="#ffffff" d="M 32 6 C 17.6 6 6 17.6 6 32 C 6 37.1 7.5 41.8 10.1 45.8 L 6.5 57.5 L 18.7 54.1 C 22.6 56.4 27.1 57.8 32 57.8 C 46.4 57.8 58 46.2 58 31.8 C 58 17.4 46.4 6 32 6 Z M 44.8 41.2 C 44.2 42.8 41.8 44.3 40.1 44.6 C 38.4 44.9 36.3 45.1 29.8 42.4 C 21.6 39 16.3 30.5 15.9 29.9 C 15.5 29.3 12.6 25.5 12.6 21.5 C 12.6 17.5 14.6 15.6 15.4 14.7 C 16.2 13.8 17.2 13.6 17.9 13.6 C 18.6 13.6 19.3 13.6 19.8 13.6 C 20.4 13.6 21.1 13.3 21.7 14.8 C 22.4 16.5 23.9 20.2 24.1 20.6 C 24.3 21 24.5 21.6 24.1 22.3 C 23.7 23 23.4 23.4 22.8 24.1 C 22.2 24.8 21.6 25.3 22.3 26.5 C 23 27.7 25.4 31.6 28.9 34.7 C 33.4 38.7 37.1 40 38.3 40.5 C 39.5 41 40.2 40.9 40.8 40.2 C 41.4 39.5 43.4 37.2 44.1 36.2 C 44.8 35.2 45.5 35.4 46.5 35.8 C 47.5 36.2 52.8 38.8 53.6 39.2 C 54.4 39.6 55 39.8 55.2 40.2 C 55.4 40.6 55.4 42.5 44.8 41.2 Z"/>
    </svg>''',

    "contacts": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
        <path fill="#ffffff" d="M 32 10 C 25.4 10 20 15.4 20 22 C 20 28.6 25.4 34 32 34 C 38.6 34 44 28.6 44 22 C 44 15.4 38.6 10 32 10 Z M 16 46 C 16 40.7 26.7 38 32 38 C 37.3 38 48 40.7 48 46 L 48 52 L 16 52 Z"/>
    </svg>''',

    "calendar": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
        <path fill="#ffffff" d="M 12 12 C 8.7 12 6 14.7 6 18 L 6 48 C 6 51.3 8.7 54 12 54 L 52 54 C 55.3 54 58 51.3 58 48 L 58 18 C 58 14.7 55.3 12 52 12 L 46 12 L 46 8 L 40 8 L 40 12 L 24 12 L 24 8 L 18 8 L 18 12 Z M 12 24 L 52 24 L 52 48 L 12 48 Z M 18 30 L 26 30 L 26 36 L 18 36 Z M 30 30 L 38 30 L 38 36 L 30 36 Z M 42 30 L 48 30 L 48 36 L 42 36 Z M 18 40 L 26 40 L 26 46 L 18 46 Z M 30 40 L 38 40 L 38 46 L 30 46 Z"/>
    </svg>''',

    "gallery": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
        <path fill="#ffffff" d="M 10 12 C 6.7 12 4 14.7 4 18 L 4 46 C 4 49.3 6.7 52 10 52 L 54 52 C 57.3 52 60 49.3 60 46 L 60 18 C 60 14.7 57.3 12 54 12 Z M 18 20 A 4 4 0 1 1 18 28 A 4 4 0 1 1 18 20 Z M 10 46 L 24 28 L 34 40 L 42 32 L 54 46 Z"/>
    </svg>''',

    "playstore": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
        <path fill="#ffffff" d="M 12 8 C 11.3 8.3 10.7 9 10.7 9.9 L 10.7 54.1 C 10.7 55 11.3 55.7 12 56 L 36 32 Z M 16 11.5 L 43.5 26.5 L 39 30.5 Z M 48 30.2 L 41.5 33.7 L 48 40.2 C 49.4 39.3 50.3 37.8 50.3 36 C 50.3 34.2 49.4 32.7 48 30.2 Z M 16 52.5 L 39 33.5 L 43.5 37.5 Z"/>
    </svg>''',

    "youtube": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
        <path fill="#ffffff" d="M 32 14 C 18 14 10 14.8 6.5 16.5 C 4.5 17.5 3 20 2.5 23 C 2 26 2 32 2 32 C 2 32 2 38 2.5 41 C 3 44 4.5 46.5 6.5 47.5 C 10 49.2 18 50 32 50 C 46 50 54 49.2 57.5 47.5 C 59.5 46.5 61 44 61.5 41 C 62 38 62 32 62 32 C 62 32 62 26 61.5 23 C 61 20 59.5 17.5 57.5 16.5 C 54 14.8 46 14 32 14 Z M 26 23 L 42 32 L 26 41 Z"/>
    </svg>''',

    "instagram": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
        <path fill="#ffffff" d="M 20 8 C 13.4 8 8 13.4 8 20 L 8 44 C 8 50.6 13.4 56 20 56 L 44 56 C 50.6 56 56 50.6 56 44 L 56 20 C 56 13.4 50.6 8 44 8 Z M 20 13 L 44 13 C 47.9 13 51 16.1 51 20 L 51 44 C 51 47.9 47.9 51 44 51 L 20 51 C 16.1 51 13 47.9 13 44 L 13 20 C 13 16.1 16.1 13 20 13 Z M 44 17 A 3 3 0 1 0 44 23 A 3 3 0 1 0 44 17 Z M 32 20 C 25.4 20 20 25.4 20 32 C 20 38.6 25.4 44 32 44 C 38.6 44 44 38.6 44 32 C 44 25.4 38.6 20 32 20 Z M 32 25 C 35.9 25 39 28.1 39 32 C 39 35.9 35.9 39 32 39 C 28.1 39 25 35.9 25 32 C 25 28.1 28.1 25 32 25 Z"/>
    </svg>''',

    "twitter": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
        <path fill="#ffffff" d="M 12 10 L 26.5 30 L 11 48 L 16 48 L 29 33.5 L 40 48 L 54 48 L 38.5 26.5 L 53 10 L 48 10 L 36 23 L 26 10 Z M 19 14 L 24 14 L 46 44 L 41 44 Z"/>
    </svg>''',

    "weather": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
        <path fill="#ffffff" d="M 32 10 A 10 10 0 0 0 24 24.2 A 13 13 0 0 0 13 37 C 13 44.2 18.8 50 26 50 L 46 50 C 52.6 50 58 44.6 58 38 C 58 31.9 53.5 26.8 47.6 26.1 A 14 14 0 0 0 32 10 Z"/>
    </svg>''',

    "compass": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
        <path fill="#ffffff" d="M 32 6 C 17.6 6 6 17.6 6 32 C 6 46.4 17.6 58 32 58 C 46.4 58 58 46.4 58 32 C 58 17.6 46.4 6 32 6 Z M 32 12 C 43 12 52 21 52 32 C 52 43 43 52 32 52 C 21 52 12 43 12 32 C 12 21 21 12 32 12 Z M 44 20 L 35 30 L 20 44 L 29 34 Z"/>
    </svg>''',

    "theme": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
        <path fill="#ffffff" d="M 32 6 C 17.6 6 6 17.6 6 32 C 6 43 13.5 52.2 24 54.8 C 25.5 55.2 27 54 27 52.5 C 27 51.5 26.5 50.6 26.5 49.5 C 26.5 47 28.5 45 31 45 L 36 45 C 46 45 54 37 54 27 C 54 15.4 44.1 6 32 6 Z M 18 24 A 4 4 0 1 1 18 32 A 4 4 0 1 1 18 24 Z M 28 15 A 4 4 0 1 1 28 23 A 4 4 0 1 1 28 15 Z M 40 18 A 4 4 0 1 1 40 26 A 4 4 0 1 1 40 18 Z M 48 29 A 4 4 0 1 1 48 37 A 4 4 0 1 1 48 29 Z"/>
    </svg>''',

    "launcher": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
        <path fill="#ffffff" d="M 32 6 C 32 6 22 18 22 32 C 22 38 24.5 43.5 28 47 L 24 55 L 32 51 L 40 55 L 36 47 C 39.5 43.5 42 38 42 32 C 42 18 32 6 32 6 Z M 32 20 A 5 5 0 1 1 32 30 A 5 5 0 1 1 32 20 Z M 18 36 L 10 44 L 18 46 Z M 46 36 L 46 46 L 54 44 Z"/>
    </svg>''',

    "search": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
        <path fill="#ffffff" d="M 26 8 C 16.1 8 8 16.1 8 26 C 8 35.9 16.1 44 26 44 C 30.1 44 33.8 42.6 36.8 40.2 L 50.3 53.7 L 53.7 50.3 L 40.2 36.8 C 42.6 33.8 44 30.1 44 26 C 44 16.1 35.9 8 26 8 Z M 26 13 C 33.2 13 39 18.8 39 26 C 39 33.2 33.2 39 26 39 C 18.8 39 13 33.2 13 26 C 13 18.8 18.8 13 26 13 Z"/>
    </svg>'''
}

# Mapping: Package Name -> (Source Icon Type, File/Key, Glyph Accent Color, Description)
# All icons use uniform YAMIS-styled pure white monochrome glyphs (HEX_WHITE)
APP_MAPPINGS = [
    # Dialer / Phone
    ("com.sh.smart.caller", "yamis_device", "phone.svg", HEX_WHITE, "Tecno Smart Caller / Phone"),
    ("com.android.dialer", "yamis_device", "phone.svg", HEX_WHITE, "AOSP Dialer"),
    ("com.google.android.dialer", "yamis_device", "phone.svg", HEX_WHITE, "Google Phone"),

    # SMS / Messaging
    ("com.android.mms", "vector", "message", HEX_WHITE, "Tecno Messages"),
    ("com.google.android.apps.messaging", "vector", "message", HEX_WHITE, "Google Messages"),

    # Contacts
    ("com.android.contacts", "vector", "contacts", HEX_WHITE, "Tecno Contacts"),
    ("com.google.android.contacts", "vector", "contacts", HEX_WHITE, "Google Contacts"),

    # Settings
    ("com.android.settings", "yamis_app", "systemsettings.svg", HEX_WHITE, "System Settings"),
    ("com.transsion.settings", "yamis_app", "systemsettings.svg", HEX_WHITE, "Tecno Settings"),

    # Camera
    ("com.transsion.camera", "yamis_device", "camera-photo.svg", HEX_WHITE, "Tecno Camera"),
    ("com.android.camera", "yamis_device", "camera-photo.svg", HEX_WHITE, "AOSP Camera"),
    ("com.google.android.GoogleCamera", "yamis_device", "camera-photo.svg", HEX_WHITE, "Google Camera"),

    # Gallery / Photos
    ("com.transsion.aigallery", "vector", "gallery", HEX_WHITE, "Tecno AI Gallery"),
    ("com.android.gallery3d", "vector", "gallery", HEX_WHITE, "AOSP Gallery"),
    ("com.google.android.apps.photos", "vector", "gallery", HEX_WHITE, "Google Photos"),

    # File Manager
    ("com.transsion.filemanager", "yamis_app", "system-file-manager.svg", HEX_WHITE, "Tecno File Manager"),
    ("com.android.filemanager", "yamis_app", "system-file-manager.svg", HEX_WHITE, "AOSP File Manager"),
    ("com.google.android.apps.nbu.files", "yamis_app", "system-file-manager.svg", HEX_WHITE, "Google Files"),

    # Calculator
    ("com.transsion.calculator", "yamis_app", "accessories-calculator.svg", HEX_WHITE, "Tecno Calculator"),
    ("com.android.calculator2", "yamis_app", "accessories-calculator.svg", HEX_WHITE, "AOSP Calculator"),
    ("com.google.android.calculator", "yamis_app", "accessories-calculator.svg", HEX_WHITE, "Google Calculator"),

    # Clock
    ("com.android.deskclock", "yamis_app", "org.gnome.clocks.svg", HEX_WHITE, "Tecno Clock"),
    ("com.google.android.deskclock", "yamis_app", "org.gnome.clocks.svg", HEX_WHITE, "Google Clock"),

    # Calendar
    ("com.android.calendar", "vector", "calendar", HEX_WHITE, "Tecno Calendar"),
    ("com.google.android.calendar", "vector", "calendar", HEX_WHITE, "Google Calendar"),

    # HiTheme / XTheme
    ("com.transsion.theme", "vector", "theme", HEX_WHITE, "Tecno HiTheme Store"),
    ("com.transsion.xtheme", "vector", "theme", HEX_WHITE, "Infinix XTheme"),
    ("com.transsion.magicshow", "vector", "theme", HEX_WHITE, "Tecno Magic Show DIY"),

    # Launcher
    ("com.transsion.hilauncher", "vector", "launcher", HEX_WHITE, "HiOS Launcher"),

    # Weather
    ("com.transsion.weather", "vector", "weather", HEX_WHITE, "Tecno Weather"),
    ("com.google.android.apps.weather", "vector", "weather", HEX_WHITE, "Google Weather"),

    # Compass
    ("com.transsion.compass", "vector", "compass", HEX_WHITE, "Tecno Compass"),

    # Sound Recorder
    ("com.android.soundrecorder", "yamis_device", "audio-input-microphone.svg", HEX_WHITE, "Tecno Sound Recorder"),
    ("com.transsion.soundrecorder", "yamis_device", "audio-input-microphone.svg", HEX_WHITE, "Tecno Sound Recorder 2"),

    # Music / Audio
    ("com.google.android.apps.youtube.music", "yamis_app", "youtube-music.svg", HEX_WHITE, "YouTube Music"),

    # Browser
    ("com.android.chrome", "yamis_app", "google-chrome.svg", HEX_WHITE, "Google Chrome"),
    ("org.mozilla.firefox", "yamis_app", "google-chrome.svg", HEX_WHITE, "Firefox"),

    # App Store
    ("com.android.vending", "vector", "playstore", HEX_WHITE, "Google Play Store"),

    # Google Apps
    ("com.google.android.gm", "vector", "message", HEX_WHITE, "Gmail"),
    ("com.google.android.youtube", "vector", "youtube", HEX_WHITE, "YouTube"),
    ("com.google.android.googlequicksearchbox", "vector", "search", HEX_WHITE, "Google Search"),
    ("com.google.android.apps.maps", "vector", "compass", HEX_WHITE, "Google Maps"),

    # Messaging & Social
    ("com.whatsapp", "vector", "whatsapp", HEX_WHITE, "WhatsApp"),
    ("com.whatsapp.w4b", "vector", "whatsapp", HEX_WHITE, "WhatsApp Business"),
    ("org.telegram.messenger", "yamis_app", "telegram.svg", HEX_WHITE, "Telegram"),
    ("org.telegram.plus", "yamis_app", "telegram.svg", HEX_WHITE, "Telegram Plus"),
    ("com.instagram.android", "vector", "instagram", HEX_WHITE, "Instagram"),
    ("com.twitter.android", "vector", "twitter", HEX_WHITE, "Twitter / X"),

    # Productivity, Knowledge & Device Integration (from applist.md)
    ("io.anytype.app", "yamis_app", "anytype.svg", HEX_WHITE, "Anytype"),
    ("io.anytype.mobile", "yamis_app", "anytype.svg", HEX_WHITE, "Anytype Mobile"),
    ("org.kde.kdeconnect_tp", "yamis_app", "kdeconnect.svg", HEX_WHITE, "KDE Connect"),
    ("org.kde.kdeconnect", "yamis_app", "kdeconnect.svg", HEX_WHITE, "KDE Connect Alternate"),

    # Developer & Power Tools
    ("com.termux", "yamis_app", "utilities-terminal.svg", HEX_WHITE, "Termux Terminal"),
    ("com.github.android", "yamis_app", "appimagekit-github-desktop.svg", HEX_WHITE, "GitHub"),
    ("org.videolan.vlc", "yamis_app", "vlc.svg", HEX_WHITE, "VLC Media Player")
]


def resolve_svg_content(icon_type, filename_or_key, color_hex):
    """Loads SVG content and colors the glyph."""
    if icon_type == "vector":
        svg_str = VECTOR_GLYPHS[filename_or_key]
        return svg_str.replace("#ffffff", color_hex).replace("#FFFFFF", color_hex)
    
    path = None
    if icon_type == "yamis_app":
        path = os.path.join(YAMIS_DIR, "apps/scalable", filename_or_key)
    elif icon_type == "yamis_device":
        path = os.path.join(YAMIS_DIR, "devices/scalable", filename_or_key)
    elif icon_type == "plasma_icon":
        path = os.path.join(PLASMA_DIR, "icons", filename_or_key)

    if not path or not os.path.exists(path):
        # Fallback to search
        print(f"Warning: Icon file {path} not found directly, falling back...")
        return None

    with open(path, "r", errors="ignore") as f:
        content = f.read()

    # Normalize colors to target hex (replace stylesheet definitions and inline currentColor)
    content = (content
               .replace("currentColor", color_hex)
               .replace("#232629", color_hex)
               .replace("#d8dee9", color_hex)
               .replace("#ffffff", color_hex)
               .replace("#FFFFFF", color_hex))
    return content


def create_squircle_icon(svg_content, size=192, glyph_hex=HEX_WHITE, border_color=COLOR_ORANGE_BORDER):
    """Renders a deep space squircle icon with neon border and centered glyph."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    margin = 6
    radius = int(size * 0.24)  # standard Android squircle curvature
    box = [margin, margin, size - margin, size - margin]

    # Draw dark body with neon border
    draw.rounded_rectangle(box, radius=radius, fill=COLOR_SURFACE, outline=border_color, width=3)

    # Render vector glyph
    glyph_target = int(size * 0.54)
    png_bytes = cairosvg.svg2png(bytestring=svg_content.encode("utf-8"), output_width=glyph_target, output_height=glyph_target)
    glyph = Image.open(io.BytesIO(png_bytes)).convert("RGBA")

    # Force monochrome purity while respecting alpha anti-aliasing
    r, g, b, a = glyph.split()
    hex_clean = glyph_hex.lstrip("#")
    rgb = tuple(int(hex_clean[i:i+2], 16) for i in (0, 2, 4))
    colored_glyph = Image.new("RGBA", glyph.size, rgb + (255,))
    colored_glyph.putalpha(a)

    pos = ((size - glyph.width) // 2, (size - glyph.height) // 2)
    img.paste(colored_glyph, pos, colored_glyph)
    return img


def create_raw_transparent_icon(svg_content, size=256, glyph_hex=HEX_WHITE):
    """Renders a clean transparent PNG glyph for Theme Creation Tool imports."""
    glyph_target = int(size * 0.80)
    png_bytes = cairosvg.svg2png(bytestring=svg_content.encode("utf-8"), output_width=glyph_target, output_height=glyph_target)
    glyph = Image.open(io.BytesIO(png_bytes)).convert("RGBA")

    r, g, b, a = glyph.split()
    hex_clean = glyph_hex.lstrip("#")
    rgb = tuple(int(hex_clean[i:i+2], 16) for i in (0, 2, 4))
    colored_glyph = Image.new("RGBA", glyph.size, rgb + (255,))
    colored_glyph.putalpha(a)

    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    pos = ((size - glyph.width) // 2, (size - glyph.height) // 2)
    canvas.paste(colored_glyph, pos, colored_glyph)
    return canvas


def generate_all_icons():
    """Generates all themed HiOS package icons, fallbacks, and raw transparent PNGs."""
    print("Generating HiOS / XOS Themed Icons...")
    # Clean previous generated icons to prevent removed apps from persisting
    for d in [ICONS_DIR, RAW_PNG_256_DIR, RAW_PNG_512_DIR]:
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d, exist_ok=True)

    generated_count = 0
    for pkg, itype, key, hex_color, desc in APP_MAPPINGS:
        svg_data = resolve_svg_content(itype, key, hex_color)
        if not svg_data:
            continue

        # 1. Themed Squircle for .zth package
        icon_img = create_squircle_icon(svg_data, size=192, glyph_hex=hex_color)
        icon_out = os.path.join(ICONS_DIR, f"{pkg}.png")
        icon_img.save(icon_out, "PNG", optimize=True)

        # 2. Raw transparent PNGs (256x256 & 512x512) for Community Desktop Tool
        raw_256 = create_raw_transparent_icon(svg_data, size=256, glyph_hex=hex_color)
        raw_512 = create_raw_transparent_icon(svg_data, size=512, glyph_hex=hex_color)
        raw_256.save(os.path.join(RAW_PNG_256_DIR, f"{pkg}.png"), "PNG")
        raw_512.save(os.path.join(RAW_PNG_512_DIR, f"{pkg}.png"), "PNG")

        generated_count += 1

    # 3. Fallback mask, background, and border for third-party unthemed apps
    bg_mask = Image.new("RGBA", (192, 192), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bg_mask)
    draw.rounded_rectangle([6, 6, 186, 186], radius=46, fill=COLOR_SURFACE, outline=COLOR_ORANGE_BORDER, width=3)
    bg_mask.save(os.path.join(ICONS_DIR, "icon_background.png"), "PNG")
    bg_mask.save(os.path.join(ICONS_DIR, "icon_border.png"), "PNG")

    # Pure white mask for launchers supporting dynamic masking
    pure_mask = Image.new("L", (192, 192), 0)
    draw_mask = ImageDraw.Draw(pure_mask)
    draw_mask.rounded_rectangle([6, 6, 186, 186], radius=46, fill=255)
    pure_mask.save(os.path.join(ICONS_DIR, "icon_mask.png"), "PNG")

    print(f"Generated {generated_count} themed app icons + 3 system fallbacks.")


def process_wallpapers():
    """Crops and optimizes 4K Plasma wallpapers for tall Android mobile screens."""
    print("Processing Wallpapers for Tecno HiOS...")
    os.makedirs(WALLPAPER_DIR, exist_ok=True)
    os.makedirs(WALLPAPERS_OUT_DIR, exist_ok=True)

    target_w, target_h = 1080, 2400  # Modern 20:9 HiOS display resolution

    plasma_wallpapers = [
        "space-neon-orange-nebula.jpg",
        "neon-orange-blackhole.png",
        "127.0.0.1.png",
        "ubuntu-orange-fire.png",
        "orange_Flipper_Devices_wallpaper.png",
        "noplacelikelocalhost.jpg"
    ]

    for wp_name in plasma_wallpapers:
        src_path = os.path.join(PLASMA_DIR, "wallpapers", wp_name)
        if not os.path.exists(src_path):
            continue

        base_name, ext = os.path.splitext(wp_name)
        # 1. Copy desktop original
        shutil.copy(src_path, os.path.join(WALLPAPERS_OUT_DIR, f"{base_name}-desktop{ext}"))

        # 2. Crop centered vertical phone version
        try:
            with Image.open(src_path) as im:
                im_rgb = im.convert("RGB")
                w, h = im_rgb.size
                crop_w = int(h * (target_w / target_h))
                if crop_w > w:
                    crop_w = w
                left = (w - crop_w) // 2
                cropped = im_rgb.crop((left, 0, left + crop_w, h)).resize((target_w, target_h), Image.Resampling.LANCZOS)
                
                phone_out = os.path.join(WALLPAPERS_OUT_DIR, f"{base_name}-phone.jpg")
                cropped.save(phone_out, "JPEG", quality=95)

                # Use nebula as the primary theme wallpaper inside theme package
                if "space-neon-orange-nebula" in wp_name:
                    for name in ["default_wallpaper.jpg", "home_wallpaper.jpg", "lock_wallpaper.jpg", "wallpaper.jpg"]:
                        cropped.save(os.path.join(WALLPAPER_DIR, name), "JPEG", quality=95)
        except Exception as e:
            print(f"Error processing wallpaper {wp_name}: {e}")

    print("Mobile and desktop wallpapers generated.")


def generate_previews():
    """Generates realistic UI mockups for HiTheme preview cards and local DIY selector."""
    print("Generating Theme Previews & Showcase Mockups...")
    os.makedirs(PREVIEW_DIR, exist_ok=True)
    os.makedirs(THUMBNAIL_DIR, exist_ok=True)

    # Load base mobile wallpaper
    wp_path = os.path.join(WALLPAPER_DIR, "default_wallpaper.jpg")
    if not os.path.exists(wp_path):
        base_canvas = Image.new("RGB", (1080, 2400), (10, 10, 11))
    else:
        base_canvas = Image.open(wp_path).copy()

    # Homescreen Preview (preview_0.jpg)
    hs_preview = base_canvas.copy()
    draw = ImageDraw.Draw(hs_preview)

    # Font setup
    try:
        font_time = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/UbuntuSans[wdth,wght].ttf", 140)
        font_date = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/UbuntuSans[wdth,wght].ttf", 42)
        font_label = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/UbuntuSans[wdth,wght].ttf", 30)
    except:
        font_time = font_date = font_label = ImageFont.load_default()

    # Status Bar
    draw.text((60, 48), "21:45", fill=(240, 240, 240), font=font_label)
    draw.text((920, 48), "5G  98%", fill=(255, 107, 0), font=font_label)

    # Widget
    draw.text((100, 360), "21:45", fill=(255, 255, 255), font=font_time)
    draw.text((105, 520), "Friday, November 6  •  28°C Neon Cyber", fill=(255, 107, 0), font=font_date)

    # Minimal Search Bar
    draw.rounded_rectangle([80, 640, 1000, 720], radius=40, fill=(18, 19, 24, 230), outline=(255, 107, 0, 180), width=2)
    draw.text((130, 665), "Search apps, web, terminal...", fill=(160, 160, 160), font=font_label)

    # Render Homescreen Icon Grid (4 columns x 3 rows)
    grid_pkgs = [
        ("com.sh.smart.caller", "Phone"),
        ("com.android.mms", "Messages"),
        ("com.android.chrome", "Chrome"),
        ("com.transsion.camera", "Camera"),
        ("com.transsion.aigallery", "Gallery"),
        ("com.android.settings", "Settings"),
        ("com.android.vending", "Play Store"),
        ("com.google.android.youtube", "YouTube"),
        ("io.anytype.app", "Anytype"),
        ("org.kde.kdeconnect_tp", "KDE Connect"),
        ("com.termux", "Termux"),
        ("com.transsion.calculator", "Calculator")
    ]

    col_w = 1080 // 4
    start_y = 880
    row_h = 270

    for idx, (pkg, label) in enumerate(grid_pkgs):
        col = idx % 4
        row = idx // 4
        x = col * col_w + (col_w - 150) // 2
        y = start_y + row * row_h

        icon_f = os.path.join(ICONS_DIR, f"{pkg}.png")
        if os.path.exists(icon_f):
            ic = Image.open(icon_f).resize((150, 150), Image.Resampling.LANCZOS)
            hs_preview.paste(ic, (x, y), ic)
            # Label
            draw.text((x + 75, y + 165), label, fill=(240, 240, 240), font=font_label, anchor="mt")

    # Dock Bar
    draw.rounded_rectangle([60, 2060, 1020, 2260], radius=50, fill=(12, 13, 16, 220), outline=(255, 107, 0, 160), width=2)
    dock_pkgs = ["com.sh.smart.caller", "com.android.mms", "com.android.chrome", "com.android.settings"]
    dock_col_w = (1020 - 60) // 4
    for idx, pkg in enumerate(dock_pkgs):
        x = 60 + idx * dock_col_w + (dock_col_w - 130) // 2
        y = 2095
        icon_f = os.path.join(ICONS_DIR, f"{pkg}.png")
        if os.path.exists(icon_f):
            ic = Image.open(icon_f).resize((130, 130), Image.Resampling.LANCZOS)
            hs_preview.paste(ic, (x, y), ic)

    # Save Homescreen preview
    hs_preview.save(os.path.join(PREVIEW_DIR, "preview_0.jpg"), "JPEG", quality=90)

    # Lockscreen Preview (preview_1.jpg)
    ls_preview = base_canvas.copy()
    draw_ls = ImageDraw.Draw(ls_preview)
    draw_ls.text((540, 480), "21:45", fill=(255, 255, 255), font=font_time, anchor="mt")
    draw_ls.text((540, 660), "Friday, November 6", fill=(255, 107, 0), font=font_date, anchor="mt")

    # Minimal notification card
    draw_ls.rounded_rectangle([100, 950, 980, 1150], radius=40, fill=(14, 15, 20, 220), outline=(255, 107, 0, 140), width=2)
    kdec_icon_f = os.path.join(ICONS_DIR, "org.kde.kdeconnect_tp.png")
    if os.path.exists(kdec_icon_f):
        kdec_ic = Image.open(kdec_icon_f).resize((90, 90), Image.Resampling.LANCZOS)
        ls_preview.paste(kdec_ic, (140, 995), kdec_ic)
    draw_ls.text((260, 1005), "KDE Connect", fill=(255, 107, 0), font=font_date)
    draw_ls.text((260, 1065), "Device connected: Space Neon Minimal active.", fill=(200, 200, 200), font=font_label)

    ls_preview.save(os.path.join(PREVIEW_DIR, "preview_1.jpg"), "JPEG", quality=90)

    # Cover image
    hs_preview.save(os.path.join(PREVIEW_DIR, "cover.jpg"), "JPEG", quality=90)
    hs_preview.save(os.path.join(BASE_DIR, "preview.jpg"), "JPEG", quality=90)
    hs_preview.save(os.path.join(BASE_DIR, "preview_cover.jpg"), "JPEG", quality=90)

    # Thumbnail for local DIY picker (450x1000)
    thumb = hs_preview.resize((450, 1000), Image.Resampling.LANCZOS)
    thumb.save(os.path.join(THUMBNAIL_DIR, "thumbnail.jpg"), "JPEG", quality=90)
    thumb.save(os.path.join(PREVIEW_DIR, "thumbnail.jpg"), "JPEG", quality=90)

    print("Preview images generated.")


def create_manifests():
    """Generates description.xml, manifest.xml, and info.json."""
    print("Writing Theme Manifests...")

    desc_xml = """<?xml version="1.0" encoding="utf-8"?>
<theme>
    <title>Space Neon Minimal</title>
    <author>heli-toon</author>
    <designer>heli-toon</designer>
    <version>1.0.0</version>
    <formatVersion>1</formatVersion>
    <description>Ultra-minimal high-contrast cyber theme for Tecno HiOS and Infinix XOS. Deep space black (#0A0A0B), grayscale hierarchy, vibrant neon orange (#FF6B00) accents, and precision squircle monochrome icons.</description>
    <uiVersion>HiOS 8.0 - HiOS 15+</uiVersion>
    <compatibility>
        <minVersion>8.0</minVersion>
        <targetVersion>15.0</targetVersion>
    </compatibility>
</theme>
"""
    with open(os.path.join(THEME_SRC_DIR, "description.xml"), "w", encoding="utf-8") as f:
        f.write(desc_xml)

    manifest_xml = """<?xml version="1.0" encoding="utf-8"?>
<manifest>
    <theme-name>Space Neon Minimal</theme-name>
    <version>1.0.0</version>
    <author>heli-toon</author>
    <modules>
        <module name="com.transsion.hilauncher" />
        <module name="com.transsion.xoslauncher" />
        <module name="icons" />
        <module name="wallpaper" />
    </modules>
</manifest>
"""
    with open(os.path.join(THEME_SRC_DIR, "manifest.xml"), "w", encoding="utf-8") as f:
        f.write(manifest_xml)

    print("Manifest files created.")


def package_theme_archives():
    """Compresses theme_src into valid .zth and .xth bundles."""
    print("Packaging .zth and .xth Theme Files...")
    zth_path = os.path.join(BASE_DIR, "SpaceNeonMinimal.zth")
    xth_path = os.path.join(BASE_DIR, "SpaceNeonMinimal.xth")

    for archive_path in [zth_path, xth_path]:
        if os.path.exists(archive_path):
            os.remove(archive_path)

        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(THEME_SRC_DIR):
                for f in files:
                    full_p = os.path.join(root, f)
                    rel_p = os.path.relpath(full_p, THEME_SRC_DIR)
                    zipf.write(full_p, rel_p)

    print(f"Theme packaged successfully:")
    print(f" -> HiOS Package:    {zth_path} ({os.path.getsize(zth_path) // 1024} KB)")
    print(f" -> XOS Package:     {xth_path} ({os.path.getsize(xth_path) // 1024} KB)")


def main():
    print("=" * 60)
    print("Space Neon HiOS Theme Builder - Starting Compilation")
    print("=" * 60)
    generate_all_icons()
    process_wallpapers()
    generate_previews()
    create_manifests()
    package_theme_archives()
    print("=" * 60)
    print("Compilation Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
