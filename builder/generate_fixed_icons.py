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
    # 1. Anytype
    "anytype.svg": [
        "io.anytype.app.png",
        "io.anytype.mobile.png",
        "com.anytypeio.anytype.png",
    ],
    # 2. Calendar (System & Google & Transsion)
    "calendar.svg": [
        "com.android.calendar.png",
        "com.google.android.calendar.png",
        "com.transsion.calendar.png",
    ],
    # 3. Claude
    "claude.svg": [
        "com.anthropic.claude.png",
    ],
    # 4. Compass
    "compass.svg": [
        "com.transsion.compass.png",
    ],
    # 5. Duolingo
    "duolingo.svg": [
        "com.duolingo.png",
    ],
    # 6. Free Download Manager
    "fdm.svg": [
        "org.freedownloadmanager.fdm.png",
    ],
    # 7. FileZilla
    "filezilla.svg": [
        "org.filezilla.png",
    ],
    # 8. Firefox
    "firefox.svg": [
        "org.mozilla.firefox.png",
    ],
    # 9. Gmail
    "gmail.svg": [
        "com.google.android.gm.png",
    ],
    # 10. Google Maps
    "googlemaps.svg": [
        "com.google.android.apps.maps.png",
    ],
    # 11. Google Play Store
    "googleplay.svg": [
        "com.android.vending.png",
    ],
    # 12. Luanti / Minetest
    "luanti.svg": [
        "net.minetest.minetest.png",
    ],
    # 13. Messages / SMS
    "messages.svg": [
        "com.google.android.apps.messaging.png",
        "com.android.mms.png",
    ],
    # 14. Microsoft Edge
    "microsoft-edge.svg": [
        "com.microsoft.emmx.png",
    ],
    # 15. Minecraft
    "minecraft.svg": [
        "com.mojang.minecraftpe.png",
    ],
    # 16. Notepad / Notes
    "notepad.svg": [
        "com.transsion.notebook.png",
    ],
    # 17. Phone / Dialer
    "phone.svg": [
        "com.sh.smart.caller.png",
        "com.android.dialer.png",
        "com.google.android.dialer.png",
    ],
    # 18. Pinta
    "pinta.svg": [
        "com.pinta.png",
    ],
    # 19. Proton Mail
    "protonmail.svg": [
        "ch.protonmail.android.png",
    ],
    # 20. Proton VPN
    "protonvpn-logo.svg": [
        "ch.protonvpn.android.png",
    ],
    # 21. Slack
    "slack.svg": [
        "com.Slack.png",
        "com.slack.png",
    ],
    # 22. Tor Browser
    "tor.svg": [
        "org.torproject.torbrowser.png",
    ],
    # 23. Weather
    "weather.svg": [
        "com.rlk.weathers.png",
        "com.transsion.weather.png",
        "com.google.android.apps.weather.png",
    ],
    # 24. WhatsApp & WhatsApp Business
    "whatsapp.svg": [
        "com.whatsapp.png",
        "com.whatsapp.w4b.png",
    ],
    # 25. Zoom
    "Zoom.svg": [
        "us.zoom.videomeetings.png",
    ],
    # 26. Binance (Fix: dedicated crisp vector)
    "binance.svg": [
        "com.binance.dev.png",
    ],
    # 27. Discord
    "discord.svg": [
        "com.discord.png",
    ],
    # 28. Expo Go
    "expo.svg": [
        "host.exp.exponent.png",
    ],
    # 29. Facebook
    "facebook.svg": [
        "com.facebook.katana.png",
    ],
    # 30. F-Droid
    "fdroid.svg": [
        "org.fdroid.fdroid.png",
    ],
    # 31. Figma
    "figma.svg": [
        "com.figma.mirror.png",
    ],
    # 32. Google Assistant
    "googleassistant.svg": [
        "com.google.android.apps.googleassistant.png",
    ],
    # 33. Google Authenticator (ONLY Google Authenticator, not Azure!)
    "googleauthenticator.svg": [
        "com.google.android.apps.authenticator2.png",
    ],
    # 34. Microsoft Authenticator (NEW: dedicated official shield+lock icon)
    "microsoftauthenticator.svg": [
        "com.azure.authenticator.png",
    ],
    # 35. Google Search / Google App (NEW: official monochrome 'G')
    "google.svg": [
        "com.google.android.googlequicksearchbox.png",
    ],
    # 36. NetGuard (NEW: official firewall shield icon)
    "netguard.svg": [
        "eu.faircode.netguard.png",
    ],
    # 37. HiTheme (NEW: YAMIS official theme paintbrush icon)
    "theme.svg": [
        "com.transsion.theme.png",
        "Theme.png",
        "Themes.png",
        "com.transsion.xtheme.png",
    ],
    # 38. LinkedIn (NEW: official vector)
    "linkedin.svg": [
        "com.linkedin.android.png",
    ],
    # 39. Snapchat (NEW)
    "snapchat.svg": [
        "com.snapchat.android.png",
    ],
    # 40. Pinterest (NEW)
    "pinterest.svg": [
        "com.pinterest.png",
    ],
    # 41. SoloLearn (NEW)
    "sololearn.svg": [
        "com.sololearn.png",
    ],
    # 42. Chess.com (NEW)
    "chessdotcom.svg": [
        "com.chess.png",
    ],
    # 43. Google Docs Suite
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
    # 44. WPS Office (NEW: official folding W icon)
    "wpsoffice.svg": [
        "cn.wps.moffice_eng.png",
    ],
    # 45. DeepSeek (NEW)
    "deepseek.svg": [
        "com.deepseek.chat.png",
    ],
    # 46. Kimi (NEW)
    "kimi.svg": [
        "com.moonshot.kimichat.png",
    ],
    # 47. Meta AI (NEW)
    "metaai.svg": [
        "com.facebook.metaai.png",
    ],
    # 48. Microsoft Outlook (NEW: official monochrome vector)
    "outlook.svg": [
        "com.microsoft.office.outlook.png",
    ],
    # 49. Luma (NEW: official mobile APK mathematical astroid star)
    "luma.svg": [
        "com.luma.mobile.png",
    ],
    # 50. Meetup & Social
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
    # 51. Uber & Lyft
    "uber.svg": [
        "com.ubercab.png",
    ],
    "lyft.svg": [
        "me.lyft.android.png",
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

    # Safely handle fill: keep fill="none" intact so stroke-only vector glyphs do not turn into solid shapes!
    def replace_fill(m):
        val = m.group(1).strip().lower()
        if val == "none":
            return 'fill="none"'
        return 'fill="#ffffff"'

    svg_content = re.sub(r'fill=["\']([^"\']+)["\']', replace_fill, svg_content, flags=re.IGNORECASE)

    # Convert dark / black / currentColor stroke to pure white
    def replace_stroke(m):
        val = m.group(1).strip().lower()
        if val == "none":
            return 'stroke="none"'
        return 'stroke="#ffffff"'

    svg_content = re.sub(r'stroke=["\']([^"\']+)["\']', replace_stroke, svg_content, flags=re.IGNORECASE)

    # If SVG has no fill attribute and no stroke, add fill="#ffffff" as default
    if "fill=" not in svg_content and "stroke=" not in svg_content:
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
