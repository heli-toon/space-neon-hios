#!/usr/bin/env python3
"""
Generate Mathematically Exact, High-Resolution Monochrome White (512x512 and 256x256)
Glyphs for Space Neon HiOS & XOS Theme Suite.

Renders official vector SVGs from the `myicons` directory directly using cairosvg
to prevent any distortion, jagged strokes, or malformed icons.
"""

import os
import re
import cairosvg
from PIL import Image

BUILDER_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(BUILDER_DIR)
MYICONS_DIR = os.path.join(BASE_DIR, "myicons")
RAW_512_DIR = os.path.join(BASE_DIR, "raw_monochrome_pngs_512")
RAW_256_DIR = os.path.join(BASE_DIR, "raw_monochrome_pngs_256")

os.makedirs(RAW_512_DIR, exist_ok=True)
os.makedirs(RAW_256_DIR, exist_ok=True)

SVG_MAPPINGS = {
    "anytype.svg": [
        "io.anytype.app.png",
        "io.anytype.mobile.png",
        "com.anytypeio.anytype.png",
    ],
    "calendar.svg": [
        "com.android.calendar.png",
        "com.google.android.calendar.png",
        "com.transsion.calendar.png",
    ],
    "claude.svg": [
        "com.anthropic.claude.png",
    ],
    "compass.svg": [
        "com.transsion.compass.png",
    ],
    "duolingo.svg": [
        "com.duolingo.png",
    ],
    "fdm.svg": [
        "org.freedownloadmanager.fdm.png",
    ],
    "filezilla.svg": [
        "org.filezilla.png",
    ],
    "firefox.svg": [
        "org.mozilla.firefox.png",
    ],
    "gmail.svg": [
        "com.google.android.gm.png",
    ],
    "googlemaps.svg": [
        "com.google.android.apps.maps.png",
    ],
    "googleplay.svg": [
        "com.android.vending.png",
    ],
    "luanti.svg": [
        "net.minetest.minetest.png",
    ],
    "messages.svg": [
        "com.google.android.apps.messaging.png",
        "com.android.mms.png",
    ],
    "microsoft-edge.svg": [
        "com.microsoft.emmx.png",
    ],
    "minecraft.svg": [
        "com.mojang.minecraftpe.png",
    ],
    "notepad.svg": [
        "com.transsion.notebook.png",
    ],
    "phone.svg": [
        "com.sh.smart.caller.png",
        "com.android.dialer.png",
        "com.google.android.dialer.png",
    ],
    "pinta.svg": [
        "com.pinta.png",
    ],
    "protonmail.svg": [
        "ch.protonmail.android.png",
    ],
    "protonvpn-logo.svg": [
        "ch.protonvpn.android.png",
    ],
    "slack.svg": [
        "com.Slack.png",
        "com.slack.png",
    ],
    "tor.svg": [
        "org.torproject.torbrowser.png",
    ],
    "weather.svg": [
        "com.rlk.weathers.png",
        "com.transsion.weather.png",
        "com.google.android.apps.weather.png",
    ],
    "whatsapp.svg": [
        "com.whatsapp.png",
        "com.whatsapp.w4b.png",
    ],
    "Zoom.svg": [
        "us.zoom.videomeetings.png",
    ],
    "binance.svg": [
        "com.binance.dev.png",
    ],
    "discord.svg": [
        "com.discord.png",
    ],
    "expo.svg": [
        "host.exp.exponent.png",
    ],
    "facebook.svg": [
        "com.facebook.katana.png",
    ],
    "fdroid.svg": [
        "org.fdroid.fdroid.png",
    ],
    "figma.svg": [
        "com.figma.mirror.png",
    ],
    "googleassistant.svg": [
        "com.google.android.apps.googleassistant.png",
    ],
    "googleauthenticator.svg": [
        "com.google.android.apps.authenticator2.png",
        "com.azure.authenticator.png",
    ],
    "googlecalendar.svg": [
        "com.google.android.calendar.png",
        "com.android.calendar.png",
        "com.transsion.calendar.png",
    ],
    "googledocs.svg": [
        "com.google.android.apps.docs.editors.docs.png",
    ],
    "googledrive.svg": [
        "com.google.android.apps.docs.png",
    ],
    "googlegemini.svg": [
        "com.google.android.apps.bard.png",
    ],
    "googlemeet.svg": [
        "com.google.android.apps.tachyon.png",
    ],
    "googlemessages.svg": [
        "com.google.android.apps.messaging.png",
        "com.android.mms.png",
    ],
    "googlenews.svg": [
        "com.google.android.apps.magazines.png",
    ],
    "googlephotos.svg": [
        "com.google.android.apps.photos.png",
        "com.transsion.aigallery.png",
    ],
    "googlesheets.svg": [
        "com.google.android.apps.docs.editors.sheets.png",
    ],
    "googleslides.svg": [
        "com.google.android.apps.docs.editors.slides.png",
    ],
    "meetup.svg": [
        "com.meetup.png",
    ],
    "messenger.svg": [
        "com.facebook.orca.png",
    ],
    "moodle.svg": [
        "com.moodle.moodlemobile.png",
    ],
    "threads.svg": [
        "com.instagram.barcelona.png",
    ],
}


def process_vector_svg(svg_path, target_dim=330):
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()

    # Normalize off-white / Breeze palette colors to pure white
    svg_content = re.sub(r"#d8dee9", "#ffffff", svg_content, flags=re.IGNORECASE)
    svg_content = re.sub(
        r"\.ColorScheme-Text\s*\{[^}]*\}",
        ".ColorScheme-Text { color: #ffffff; fill: #ffffff; }",
        svg_content,
    )
    if "fill=" in svg_content:
        svg_content = re.sub(r'fill="[^"]+"', 'fill="#ffffff"', svg_content)
        svg_content = re.sub(r"fill='[^']+'", 'fill="#ffffff"', svg_content)
    else:
        svg_content = re.sub(r"<svg\b", '<svg fill="#ffffff"', svg_content, count=1)

    tmp_png = "/tmp/_vector_svg_render.png"
    cairosvg.svg2png(
        bytestring=svg_content.encode("utf-8"),
        write_to=tmp_png,
        output_width=512,
        output_height=512,
    )

    with Image.open(tmp_png) as im:
        im = im.convert("RGBA")
        bbox = im.getbbox()
        if not bbox:
            return None
        cropped = im.crop(bbox)
        cw, ch = cropped.size
        aspect = cw / ch
        if aspect > 1:
            gw = target_dim
            gh = max(1, int(target_dim / aspect))
        else:
            gh = target_dim
            gw = max(1, int(target_dim * aspect))
        resized = cropped.resize((gw, gh), Image.Resampling.LANCZOS)

        # Pure white RGB with preserved alpha channel
        _, _, _, a = resized.split()
        white_rgb = Image.new("RGB", (gw, gh), (255, 255, 255))
        clean_glyph = Image.merge("RGBA", (*white_rgb.split(), a))

        canvas512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        canvas512.paste(clean_glyph, ((512 - gw) // 2, (512 - gh) // 2), clean_glyph)
        return canvas512


def create_all_icons():
    print("[*] Synchronizing all crisp monochrome vector glyphs from myicons/...")
    success_count = 0

    for svg_file, targets in SVG_MAPPINGS.items():
        svg_path = os.path.join(MYICONS_DIR, svg_file)
        if not os.path.exists(svg_path):
            print(f"  [-] Warning: {svg_file} not found in myicons/, skipping.")
            continue

        im_512 = process_vector_svg(svg_path, target_dim=330)
        if not im_512:
            print(f"  [-] Failed to render {svg_file}")
            continue

        im_256 = im_512.resize((256, 256), Image.Resampling.LANCZOS)

        for target_fn in targets:
            p512 = os.path.join(RAW_512_DIR, target_fn)
            p256 = os.path.join(RAW_256_DIR, target_fn)
            im_512.save(p512, "PNG")
            im_256.save(p256, "PNG")
            success_count += 1

        print(f"  [✓] {svg_file} -> {', '.join(targets)}")

    print(f"[*] Successfully compiled {success_count} vector glyph targets.")


if __name__ == "__main__":
    create_all_icons()
