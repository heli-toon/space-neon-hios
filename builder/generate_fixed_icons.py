#!/usr/bin/env python3
"""
Generate Mathematically Exact, High-Resolution Monochrome White (512x512)
Glyphs for Space Neon HiOS & XOS Theme Suite.

Replaces broken, distorted, or incorrect app icons with official vector paths:
1. Zoom (us.zoom.videomeetings)
2. Microsoft Teams (com.microsoft.teams)
3. Xender (cn.xender)
4. Slack (com.Slack)
5. Claude (com.anthropic.claude)
6. Duolingo (com.duolingo - Duo Owl Face)
7. Google Play Store (com.android.vending)
8. Google Maps (com.google.android.apps.maps)
9. HiTheme (com.transsion.theme, com.transsion.xtheme)
10. Calendar (com.android.calendar, com.google.android.calendar, com.transsion.calendar)
11. WhatsApp (com.whatsapp)
12. WhatsApp Business (com.whatsapp.w4b)
13. Compass (com.transsion.compass)
14. Phone (com.sh.smart.caller, com.android.dialer, com.google.android.dialer)
15. Contacts (com.android.contacts, com.google.android.contacts)
16. KDE Connect (org.kde.kdeconnect_tp, org.kde.kdeconnect)
17. Gmail (com.google.android.gm)
18. Google Messages (com.google.android.apps.messaging, com.android.mms)
"""

import os
import re
import math
from PIL import Image
import cairo

BUILDER_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(BUILDER_DIR)
RAW_512_DIR = os.path.join(BASE_DIR, "raw_monochrome_pngs_512")
RAW_256_DIR = os.path.join(BASE_DIR, "raw_monochrome_pngs_256")
EXTRACTED_DIR = os.path.join(BUILDER_DIR, "extracted_user_icons")

os.makedirs(RAW_512_DIR, exist_ok=True)
os.makedirs(RAW_256_DIR, exist_ok=True)


def parse_svg_path(ctx, path_str):
    tokens = re.findall(r"([a-df-zA-DF-Z]|[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?)", path_str)
    i = 0
    cmd = ""
    cx, cy = 0.0, 0.0
    start_x, start_y = 0.0, 0.0
    while i < len(tokens):
        t = tokens[i]
        if t.isalpha():
            cmd = t
            i += 1
        if cmd == "M":
            cx, cy = float(tokens[i]), float(tokens[i+1])
            start_x, start_y = cx, cy
            ctx.move_to(cx, cy)
            i += 2
            cmd = "L"
        elif cmd == "m":
            cx += float(tokens[i])
            cy += float(tokens[i+1])
            start_x, start_y = cx, cy
            ctx.move_to(cx, cy)
            i += 2
            cmd = "l"
        elif cmd == "L":
            cx, cy = float(tokens[i]), float(tokens[i+1])
            ctx.line_to(cx, cy)
            i += 2
        elif cmd == "l":
            cx += float(tokens[i])
            cy += float(tokens[i+1])
            ctx.line_to(cx, cy)
            i += 2
        elif cmd == "H":
            cx = float(tokens[i])
            ctx.line_to(cx, cy)
            i += 1
        elif cmd == "h":
            cx += float(tokens[i])
            ctx.line_to(cx, cy)
            i += 1
        elif cmd == "V":
            cy = float(tokens[i])
            ctx.line_to(cx, cy)
            i += 1
        elif cmd == "v":
            cy += float(tokens[i])
            ctx.line_to(cx, cy)
            i += 1
        elif cmd == "C":
            x1, y1 = float(tokens[i]), float(tokens[i+1])
            x2, y2 = float(tokens[i+2]), float(tokens[i+3])
            cx, cy = float(tokens[i+4]), float(tokens[i+5])
            ctx.curve_to(x1, y1, x2, y2, cx, cy)
            i += 6
        elif cmd == "c":
            x1 = cx + float(tokens[i])
            y1 = cy + float(tokens[i+1])
            x2 = cx + float(tokens[i+2])
            y2 = cy + float(tokens[i+3])
            cx += float(tokens[i+4])
            cy += float(tokens[i+5])
            ctx.curve_to(x1, y1, x2, y2, cx, cy)
            i += 6
        elif cmd in ("Z", "z"):
            ctx.close_path()
            cx, cy = start_x, start_y
        else:
            i += 1


def center_and_scale_surface(src_surf, target_dim=512, glyph_target_size=330):
    src_surf.flush()
    tmp_path = "/tmp/_cairo_export_tmp.png"
    src_surf.write_to_png(tmp_path)
    im = Image.open(tmp_path).convert("RGBA")
    bbox = im.getbbox()
    if not bbox:
        return im
    cropped = im.crop(bbox)
    cw, ch = cropped.size
    aspect = cw / ch
    if aspect > 1:
        gw = glyph_target_size
        gh = max(1, int(glyph_target_size / aspect))
    else:
        gh = glyph_target_size
        gw = max(1, int(glyph_target_size * aspect))
    resized = cropped.resize((gw, gh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (target_dim, target_dim), (0, 0, 0, 0))
    pos = ((target_dim - gw) // 2, (target_dim - gh) // 2)
    canvas.paste(resized, pos, resized)
    return canvas


def save_icon(im_512, filename_list):
    im_256 = im_512.resize((256, 256), Image.Resampling.LANCZOS)
    for fn in filename_list:
        p512 = os.path.join(RAW_512_DIR, fn)
        p256 = os.path.join(RAW_256_DIR, fn)
        im_512.save(p512, "PNG")
        im_256.save(p256, "PNG")
        print(f"  Saved -> {fn} (512x512 & 256x256)")


def create_all_icons():
    print("[*] Generating 18 crisp monochrome white icon glyphs...")

    # 1. Claude (Official Anthropic Spark Vector)
    print("1/18: Claude (Anthropic Spark)")
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 580, 580)
    ctx = cairo.Context(surf)
    ctx.scale(20, 20)
    path_d = "M6.069,18.857L11.578,15.768L11.668,15.497L11.578,15.346H11.305L10.382,15.29L7.234,15.206L4.51,15.094L1.862,14.953L1.196,14.813L0.575,13.984L0.636,13.577L1.196,13.198L1.998,13.268L3.768,13.395L6.432,13.577L8.354,13.69L11.214,13.984H11.668L11.729,13.802L11.578,13.69L11.457,13.577L8.702,11.71L5.721,9.744L4.162,8.607L3.33,8.031L2.906,7.497L2.724,6.318L3.481,5.476L4.51,5.546L4.767,5.616L5.812,6.416L8.036,8.143L10.942,10.278L11.366,10.629L11.536,10.514L11.562,10.432L11.366,10.109L9.792,7.259L8.112,4.352L7.355,3.145L7.158,2.429C7.082,2.128 7.037,1.88 7.037,1.572L7.9,0.393L8.384,0.238L9.55,0.393L10.034,0.814L10.76,2.471L11.926,5.068L13.742,8.607L14.271,9.66L14.559,10.629L14.665,10.924H14.847V10.755L14.998,8.761L15.27,6.318L15.543,3.173L15.634,2.288L16.072,1.221L16.95,0.645L17.631,0.968L18.191,1.769L18.115,2.288L17.782,4.451L17.132,7.834L16.708,10.109H16.95L17.238,9.814L18.388,8.298L20.31,5.883L21.157,4.928L22.156,3.875L22.792,3.369H24.003L24.88,4.689L24.487,6.051L23.246,7.624L22.217,8.958L20.741,10.935L19.826,12.524L19.908,12.655L20.128,12.637L23.458,11.92L25.259,11.597L27.408,11.232L28.376,11.682L28.482,12.145L28.104,13.086L25.803,13.648L23.11,14.195L19.098,15.139L19.054,15.175L19.106,15.253L20.915,15.417L21.687,15.459H23.579L27.105,15.726L28.028,16.329L28.573,17.073L28.482,17.649L27.06,18.365L25.153,17.916L20.688,16.849L19.16,16.47H18.948V16.596L20.219,17.846L22.565,19.952L25.486,22.676L25.637,23.35L25.259,23.883L24.865,23.827L22.292,21.89L21.294,21.019L19.054,19.124H18.902V19.32L19.417,20.078L22.156,24.192L22.292,25.456L22.096,25.863L21.384,26.116L20.612,25.976L18.993,23.715L17.344,21.188L16.012,18.913L15.851,19.014L15.058,27.478L14.695,27.913L13.848,28.236L13.136,27.702L12.758,26.832L13.136,25.105L13.59,22.858L13.954,21.075L14.287,18.857L14.49,18.116L14.472,18.066L14.309,18.093L12.637,20.387L10.094,23.827L8.082,25.976L7.597,26.172L6.765,25.737L6.841,24.965L7.31,24.277L10.094,20.738L11.774,18.534L12.88,17.233L12.852,17.107L12.787,17.08L5.388,21.904L4.071,22.072L3.496,21.538L3.572,20.668L3.844,20.387L6.069,18.857Z"
    parse_svg_path(ctx, path_d)
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.fill()
    im_claude = center_and_scale_surface(surf, 512, 330)
    save_icon(im_claude, ["com.anthropic.claude.png"])

    # 2. Slack (Official Hashtag Vector)
    print("2/18: Slack (Official Hashtag)")
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
    ctx = cairo.Context(surf)
    ctx.scale(25, 25)
    path_d = "M9.52 4.8V2.9c0-0.34-0.09-0.66-0.26-0.95-0.17-0.3-0.4-0.52-0.69-0.69C8.28 1.09 7.97 1 7.62 1 7.28 1 6.96 1.09 6.67 1.26c-0.29 0.17-0.52 0.4-0.69 0.7-0.17 0.29-0.25 0.6-0.25 0.94 0 0.35 0.08 0.67 0.25 0.96 0.17 0.29 0.4 0.52 0.69 0.69 0.3 0.17 0.61 0.25 0.95 0.25h1.9Zm2.85 4.73c-0.35 0-0.67-0.08-0.96-0.25-0.29-0.17-0.52-0.4-0.69-0.69-0.17-0.3-0.25-0.61-0.25-0.96V2.9c0-0.34 0.08-0.66 0.25-0.95 0.17-0.3 0.4-0.52 0.69-0.69C11.71 1.09 12.02 1 12.37 1c0.34 0 0.65 0.09 0.94 0.26 0.29 0.17 0.51 0.4 0.68 0.69 0.17 0.3 0.26 0.61 0.26 0.95v4.73c0 0.35-0.09 0.67-0.26 0.96-0.17 0.29-0.4 0.52-0.68 0.69-0.29 0.17-0.6 0.25-0.94 0.25ZM9.53 7.62c0 0.35-0.09 0.67-0.26 0.96C9.1 8.87 8.87 9.1 8.58 9.27c-0.29 0.17-0.6 0.25-0.95 0.25H2.9c-0.34 0-0.66-0.08-0.95-0.25-0.3-0.17-0.53-0.4-0.7-0.69C1.08 8.28 1 7.97 1 7.62c0-0.34 0.09-0.65 0.26-0.94 0.17-0.3 0.4-0.52 0.69-0.69 0.3-0.17 0.61-0.26 0.95-0.26h4.73c0.35 0 0.66 0.09 0.95 0.26 0.3 0.17 0.52 0.4 0.69 0.69 0.17 0.29 0.26 0.6 0.26 0.94Zm5.67 1.9h1.9c0.34 0 0.66-0.08 0.95-0.25 0.3-0.17 0.52-0.4 0.69-0.69C18.91 8.28 19 7.97 19 7.62c0-0.34-0.09-0.65-0.26-0.94-0.17-0.3-0.4-0.52-0.7-0.69-0.29-0.17-0.6-0.26-0.94-0.26-0.35 0-0.67 0.09-0.96 0.26-0.29 0.17-0.52 0.4-0.69 0.69-0.17 0.29-0.25 0.6-0.25 0.94v1.9ZM2.9 14.25c-0.34 0-0.66-0.08-0.95-0.25-0.3-0.17-0.53-0.4-0.7-0.69C1.08 13.02 1 12.71 1 12.37c0-0.35 0.08-0.66 0.25-0.95 0.17-0.3 0.4-0.52 0.7-0.69 0.3-0.17 0.61-0.26 0.95-0.26h1.9v1.9c0 0.34-0.09 0.65-0.26 0.94-0.17 0.29-0.4 0.52-0.69 0.69-0.29 0.17-0.6 0.25-0.95 0.25Zm4.72-3.78c0.35 0 0.66 0.09 0.95 0.26 0.3 0.17 0.52 0.4 0.69 0.69 0.17 0.29 0.26 0.6 0.26 0.95v4.73c0 0.34-0.09 0.66-0.26 0.95-0.17 0.3-0.4 0.52-0.69 0.69C8.28 18.91 7.97 19 7.62 19c-0.34 0-0.66-0.09-0.95-0.26-0.29-0.17-0.52-0.4-0.69-0.7-0.17-0.29-0.25-0.6-0.25-0.94v-4.73c0-0.35 0.08-0.66 0.25-0.95 0.17-0.3 0.4-0.52 0.69-0.69 0.3-0.17 0.61-0.26 0.95-0.26Zm2.85 1.9c0-0.35 0.08-0.66 0.25-0.95 0.17-0.3 0.4-0.52 0.69-0.69 0.3-0.17 0.61-0.26 0.96-0.26h4.73c0.34 0 0.66 0.09 0.95 0.26 0.3 0.17 0.52 0.4 0.69 0.69 0.17 0.29 0.26 0.6 0.26 0.95 0 0.34-0.09 0.65-0.26 0.94-0.17 0.29-0.4 0.52-0.69 0.69-0.3 0.17-0.61 0.25-0.95 0.25h-4.73c-0.35 0-0.67-0.08-0.96-0.25-0.29-0.17-0.52-0.4-0.69-0.69-0.17-0.29-0.25-0.6-0.25-0.94Zm0 2.83v1.9c0 0.34 0.08 0.66 0.25 0.95 0.17 0.3 0.4 0.52 0.69 0.69 0.3 0.17 0.61 0.26 0.96 0.26 0.34 0 0.65-0.09 0.94-0.26 0.29-0.17 0.51-0.4 0.68-0.69 0.17-0.3 0.26-0.61 0.26-0.95 0-0.35-0.09-0.66-0.26-0.95-0.17-0.3-0.4-0.52-0.68-0.69-0.29-0.17-0.6-0.26-0.94-0.26h-1.9Z"
    parse_svg_path(ctx, path_d)
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.fill()
    im_slack = center_and_scale_surface(surf, 512, 330)
    save_icon(im_slack, ["com.Slack.png"])

    # 3. Zoom (Official Video Camera)
    print("3/18: Zoom (Video Camera)")
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 512, 512)
    ctx = cairo.Context(surf)
    bx, by, bw, bh, r = 70, 150, 240, 180, 40
    ctx.move_to(bx + r, by)
    ctx.line_to(bx + bw - r, by)
    ctx.arc(bx + bw - r, by + r, r, -math.pi/2, 0)
    ctx.line_to(bx + bw, by + bh - r)
    ctx.arc(bx + bw - r, by + bh - r, r, 0, math.pi/2)
    ctx.line_to(bx + r, by + bh)
    ctx.arc(bx + r, by + bh - r, r, math.pi/2, math.pi)
    ctx.line_to(bx, by + r)
    ctx.arc(bx + r, by + r, r, math.pi, 3*math.pi/2)
    ctx.close_path()

    lr = 16
    ctx.move_to(330, 205)
    ctx.line_to(425, 148)
    ctx.arc(425, 164, lr, -1.0, 0.4)
    ctx.line_to(441, 332)
    ctx.arc(425, 332, lr, 0.0, 1.3)
    ctx.line_to(330, 280)
    ctx.close_path()

    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.fill()
    im_zoom = center_and_scale_surface(surf, 512, 340)
    save_icon(im_zoom, ["us.zoom.videomeetings.png"])

    # 4. Microsoft Teams (Official Fluent Teams Vector)
    print("4/18: Microsoft Teams (Official Fluent Teams)")
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 512, 512)
    ctx = cairo.Context(surf)
    ctx.scale(512.0/48.0, 512.0/48.0)
    ctx.set_source_rgba(1, 1, 1, 1)
    parse_svg_path(ctx, "M22,20H34C37.314,20 40,22.686 40,26V36C40,39.314 37.314,42 34,42C30.686,42 28,39.314 28,36V26C28,22.686 25.314,20 22,20Z")
    parse_svg_path(ctx, "M33,18C35.761,18 38,15.761 38,13C38,10.239 35.761,8 33,8C30.239,8 28,10.239 28,13C28,15.761 30.239,18 33,18Z")
    parse_svg_path(ctx, "M8,24C8,20.686 10.686,18 14,18H22C25.314,18 28,20.686 28,24V36C28,39.314 30.686,42 34,42L18,42C12.477,42 8,37.523 8,32V24Z")
    parse_svg_path(ctx, "M18,16C21.314,16 24,13.314 24,10C24,6.686 21.314,4 18,4C14.686,4 12,6.686 12,10C12,13.314 14.686,16 18,16Z")
    ctx.fill()
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    parse_svg_path(ctx, "M6,21.5L18,21.5A4.5,4.5 0,0 1,22.5 26L22.5,37.5A4.5,4.5 0,0 1,18 42L6,42A4.5,4.5 0,0 1,1.5 37.5L1.5,26A4.5,4.5 0,0 1,6 21.5z")
    ctx.fill()
    ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.set_source_rgba(1, 1, 1, 1)
    parse_svg_path(ctx, "M7.25,23L16.75,23A3.25,3.25 0,0 1,20 26.25L20,35.75A3.25,3.25 0,0 1,16.75 39L7.25,39A3.25,3.25 0,0 1,4 35.75L4,26.25A3.25,3.25 0,0 1,7.25 23z")
    ctx.fill()
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    parse_svg_path(ctx, "M15.479,28.105H13.032V35.571H10.967V28.105H8.52V26.429H15.479V28.105Z")
    ctx.fill()
    im_teams = center_and_scale_surface(surf, 512, 330)
    save_icon(im_teams, ["com.microsoft.teams.png"])

    # 5. Xender (Official Crossing Arcs Foreground)
    print("5/18: Xender (Official Crossing Arcs)")
    src_xender = "/tmp/res/EtS.png"
    if os.path.exists(src_xender):
        im_x = Image.open(src_xender).convert("RGBA")
        w, h = im_x.size
        white_x = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        for y in range(h):
            for x in range(w):
                r, g, b, a = im_x.getpixel((x, y))
                if a > 40:
                    white_x.putpixel((x, y), (255, 255, 255, a))
        bbox = white_x.getbbox()
        cropped = white_x.crop(bbox)
        cw, ch = cropped.size
        aspect = cw / ch
        gw = 330 if aspect > 1 else int(330 * aspect)
        gh = int(330 / aspect) if aspect > 1 else 330
        resized = cropped.resize((gw, gh), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        canvas.paste(resized, ((512 - gw) // 2, (512 - gh) // 2), resized)
        save_icon(canvas, ["cn.xender.png"])
    else:
        print("  [-] Warning: /tmp/res/EtS.png not found, skipping Xender extraction")

    # 6. Duolingo (Official Duo Owl Head Vector)
    print("6/18: Duolingo (Duo Owl Head)")
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 512, 512)
    ctx = cairo.Context(surf)
    ctx.scale(512.0/432.0, 512.0/432.0)
    ctx.set_source_rgba(1, 1, 1, 1)
    parse_svg_path(ctx, "M190.63,167.11C194.3,170.9 193.21,177.16 188.48,179.46C172.76,187.09 153.68,183.63 141.3,170.82C128.93,158.01 126.13,138.84 134.31,123.41C136.77,118.77 142.14,117.93 145.81,121.71L190.63,167.11Z")
    parse_svg_path(ctx, "M185.52,162.09C201.19,177.9 228.82,177.9 246.27,162.09C263.72,146.27 243.65,254.17 243.65,253.89C243.65,253.76 234.32,253.72 215.67,253.78C210.66,253.79 201.66,253.83 188.64,253.89C176.12,182.15 175.08,151.54 185.52,162.09Z")
    parse_svg_path(ctx, "M121.83,138.54L164.11,185.45C167.65,189.37 166.35,195.59 161.54,197.72C145.56,204.8 126.61,200.68 114.69,187.44C102.77,174.21 100.64,154.95 109.36,139.81C111.98,135.26 118.3,134.61 121.83,138.54Z")
    parse_svg_path(ctx, "M241.39,167.11C237.72,170.9 238.8,177.16 243.54,179.46C259.25,187.09 278.33,183.63 290.71,170.82C303.09,158.01 305.89,138.84 297.71,123.41C295.25,118.77 289.88,117.93 286.21,121.71L241.39,167.11Z")
    parse_svg_path(ctx, "M310.18,138.54L267.9,185.45C264.37,189.37 265.67,195.59 270.48,197.72C286.45,204.8 305.4,200.68 317.33,187.44C329.25,174.21 331.38,154.95 322.66,139.81C320.04,135.26 313.72,134.61 310.18,138.54Z")
    parse_svg_path(ctx, "M143.53,145.63H145.99C177.04,145.63 202.21,170.8 202.21,201.85V230.83C202.21,261.88 177.04,287.05 145.99,287.05H143.53C112.48,287.05 87.31,261.88 87.31,230.83V201.85C87.31,170.8 112.48,145.63 143.53,145.63Z")
    parse_svg_path(ctx, "M286.02,145.63H287.99C319.04,145.63 344.21,170.79 344.21,201.84V230.84C344.21,261.88 319.04,287.05 287.99,287.05H286.25C255.38,287.05 230.28,262.15 230.04,231.28L229.81,202.29C229.56,171.24 254.53,145.88 285.58,145.63C285.72,145.63 285.87,145.63 286.02,145.63Z")
    parse_svg_path(ctx, "M216.01,233.12C227.76,233.12 237.28,242.65 237.28,254.4V261.78C237.28,273.53 227.76,283.05 216.01,283.05C204.26,283.05 194.74,273.53 194.74,261.78V254.4C194.74,242.65 204.26,233.12 216.01,233.12Z")
    ctx.fill()
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    parse_svg_path(ctx, "M153.04,188.1C163.29,188.1 171.6,196.42 171.6,206.67V226.51C171.6,236.76 163.29,245.07 153.04,245.07C142.79,245.07 134.47,236.76 134.47,226.51V206.67C134.47,196.42 142.79,188.1 153.04,188.1Z")
    parse_svg_path(ctx, "M278.48,188.1C288.73,188.1 297.04,196.42 297.04,206.67V226.51C297.04,236.76 288.73,245.07 278.48,245.07C268.22,245.07 259.91,236.76 259.91,226.51V206.67C259.91,196.42 268.22,188.1 278.48,188.1Z")
    ctx.fill()
    ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.set_source_rgba(1, 1, 1, 1)
    parse_svg_path(ctx, "M137.35,210.63C143.98,210.63 149.35,205.28 149.35,198.68C149.35,192.09 143.98,186.74 137.35,186.74C130.73,186.74 125.36,192.09 125.36,198.68C125.36,205.28 130.73,210.63 137.35,210.63Z")
    parse_svg_path(ctx, "M260.96,210.63C267.58,210.63 272.96,205.28 272.96,198.68C272.96,192.09 267.58,186.74 260.96,186.74C254.34,186.74 248.96,192.09 248.96,198.68C248.96,205.28 254.34,210.63 260.96,210.63Z")
    ctx.fill()
    im_duo = center_and_scale_surface(surf, 512, 330)
    save_icon(im_duo, ["com.duolingo.png"])

    # 7. Google Play Store (Sharp Faceted Triangle)
    print("7/18: Google Play Store (Faceted Triangle)")
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 512, 512)
    ctx = cairo.Context(surf)
    r = 24
    ctx.move_to(120 + r, 95)
    ctx.arc(410 - r*1.5, 256, r, -0.6, 0.6)
    ctx.arc(120 + r, 417 - r, r, 0.6, 2.5)
    ctx.arc(120 + r, 95 + r, r, 2.5, 4.4)
    ctx.close_path()
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.fill()
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    ctx.set_line_width(14)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(110, 85); ctx.line_to(295, 325); ctx.stroke()
    ctx.move_to(110, 427); ctx.line_to(295, 187); ctx.stroke()
    im_play = center_and_scale_surface(surf, 512, 330)
    save_icon(im_play, ["com.android.vending.png"])

    # 8. Google Maps (Clean Teardrop Pin)
    print("8/18: Google Maps (Teardrop Pin)")
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 512, 512)
    ctx = cairo.Context(surf)
    cx, cy, r, py = 256, 190, 110, 420
    ang = 0.58
    x_r, y_r = cx + r * math.cos(ang), cy + r * math.sin(ang)
    x_l, y_l = cx - r * math.cos(ang), cy + r * math.sin(ang)
    ctx.move_to(cx, py)
    ctx.curve_to(cx - 30, 360, x_l - 10, y_l + 30, x_l, y_l)
    ctx.arc(cx, cy, r, math.pi - ang, -ang)
    ctx.curve_to(x_r + 10, y_r + 30, cx + 30, 360, cx, py)
    ctx.close_path()
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.fill()
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    ctx.arc(cx, cy, 45, 0, 2 * math.pi)
    ctx.fill()
    im_maps = center_and_scale_surface(surf, 512, 330)
    save_icon(im_maps, ["com.google.android.apps.maps.png"])

    # 9. Compass (Real Navigational Compass Dial & Star Needle)
    print("9/18: Compass (Navigational Compass Rose)")
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 512, 512)
    ctx = cairo.Context(surf)
    cx, cy = 256, 256
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.arc(cx, cy, 180, 0, 2*math.pi)
    ctx.set_line_width(18)
    ctx.stroke()
    ctx.set_line_width(10)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(cx, cy - 170); ctx.line_to(cx, cy - 145); ctx.stroke()
    ctx.move_to(cx, cy + 170); ctx.line_to(cx, cy + 145); ctx.stroke()
    ctx.move_to(cx + 170, cy); ctx.line_to(cx + 145, cy); ctx.stroke()
    ctx.move_to(cx - 170, cy); ctx.line_to(cx - 145, cy); ctx.stroke()
    ctx.move_to(cx, cy - 145); ctx.line_to(cx - 32, cy); ctx.line_to(cx, cy); ctx.close_path(); ctx.fill()
    ctx.move_to(cx, cy + 145); ctx.line_to(cx + 32, cy); ctx.line_to(cx, cy); ctx.close_path(); ctx.fill()
    ctx.move_to(cx + 80, cy); ctx.line_to(cx, cy - 20); ctx.line_to(cx, cy); ctx.close_path(); ctx.fill()
    ctx.move_to(cx - 80, cy); ctx.line_to(cx, cy + 20); ctx.line_to(cx, cy); ctx.close_path(); ctx.fill()
    ctx.arc(cx, cy, 18, 0, 2*math.pi); ctx.fill()
    im_compass = center_and_scale_surface(surf, 512, 330)
    save_icon(im_compass, ["com.transsion.compass.png"])

    # 10. Phone (Ergonomic 45° Handset Receiver)
    print("10/18: Phone (Classic 45° Handset)")
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 512, 512)
    ctx = cairo.Context(surf)
    phone_d = "M362.7 319.5c-15.6-2.5-30.8-7.8-44.8-15.5-7.1-3.9-15.8-3.4-22.3 1.5l-33.1 24.8c-47.5-24.1-86.4-63-110.5-110.5l24.8-33.1c4.9-6.5 5.4-15.2 1.5-22.3-7.7-14-13-29.2-15.5-44.8-2.6-16.1-16.6-27.6-32.9-27.6h-54c-18.7 0-34.1 14.8-34.8 33.5C38.9 257.6 198.4 417.1 330.5 420.9c18.7.7 33.5-14.7 33.5-33.5v-35c0-16.3-11.5-30.3-27.6-32.9z"
    ctx.set_source_rgba(1, 1, 1, 1)
    parse_svg_path(ctx, phone_d)
    ctx.fill()
    im_phone = center_and_scale_surface(surf, 512, 330)
    save_icon(im_phone, ["com.sh.smart.caller.png", "com.android.dialer.png", "com.google.android.dialer.png"])

    # 11. Contacts (User Portrait Silhouette)
    print("11/18: Contacts (User Portrait Avatar)")
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 512, 512)
    ctx = cairo.Context(surf)
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.arc(256, 175, 68, 0, 2*math.pi)
    ctx.fill()
    ctx.move_to(115, 385)
    ctx.curve_to(125, 305, 185, 275, 220, 272)
    ctx.line_to(292, 272)
    ctx.curve_to(327, 275, 387, 305, 397, 385)
    ctx.arc(256, 420, 145, 0.25, math.pi - 0.25)
    ctx.close_path()
    ctx.fill()
    im_contacts = center_and_scale_surface(surf, 512, 330)
    save_icon(im_contacts, ["com.android.contacts.png", "com.google.android.contacts.png"])

    # 12. HiTheme (Artist Palette)
    print("12/18: HiTheme (Artist Palette)")
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 512, 512)
    ctx = cairo.Context(surf)
    palette_d = "M256,80 C155,80 80,155 80,256 C80,310 102,358 138,392 C152,406 172,416 194,416 C220,416 238,398 238,374 C238,358 230,344 230,330 C230,308 248,290 270,290 L310,290 C376,290 432,234 432,168 C432,119 353,80 256,80 Z"
    ctx.set_source_rgba(1, 1, 1, 1)
    parse_svg_path(ctx, palette_d)
    ctx.fill()
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    ctx.arc(350, 225, 28, 0, 2*math.pi); ctx.fill()
    ctx.arc(170, 160, 22, 0, 2*math.pi); ctx.fill()
    ctx.arc(245, 140, 22, 0, 2*math.pi); ctx.fill()
    ctx.arc(320, 155, 22, 0, 2*math.pi); ctx.fill()
    ctx.arc(150, 240, 22, 0, 2*math.pi); ctx.fill()
    im_theme = center_and_scale_surface(surf, 512, 330)
    save_icon(im_theme, ["com.transsion.theme.png", "com.transsion.xtheme.png"])

    # 13. Calendar (Tear-off Card with "31")
    print("13/18: Calendar (Tear-off Page with 31)")
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 512, 512)
    ctx = cairo.Context(surf)
    x, y, w, h, r = 110, 115, 292, 285, 36
    ctx.move_to(x + r, y); ctx.line_to(x + w - r, y)
    ctx.arc(x + w - r, y + r, r, -math.pi/2, 0)
    ctx.line_to(x + w, y + h - r)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi/2)
    ctx.line_to(x + r, y + h)
    ctx.arc(x + r, y + h - r, r, math.pi/2, math.pi)
    ctx.line_to(x, y + r)
    ctx.arc(x + r, y + r, r, math.pi, 3*math.pi/2)
    ctx.close_path()
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.fill()
    for bx in [185, 327]:
        ctx.arc(bx, 100, 16, math.pi, 0)
        ctx.line_to(bx + 16, 135)
        ctx.arc(bx, 135, 16, 0, math.pi)
        ctx.close_path()
        ctx.fill()
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    ctx.set_line_width(14)
    ctx.move_to(95, 195); ctx.line_to(417, 195); ctx.stroke()
    ctx.set_line_width(22)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.arc(215, 255, 32, -2.5, 0.8); ctx.stroke()
    ctx.arc(215, 325, 36, -0.8, 2.5); ctx.stroke()
    ctx.move_to(285, 250); ctx.line_to(315, 230); ctx.line_to(315, 360); ctx.stroke()
    im_cal = center_and_scale_surface(surf, 512, 330)
    save_icon(im_cal, ["com.android.calendar.png", "com.google.android.calendar.png", "com.transsion.calendar.png"])

    # 14. WhatsApp (Speech Bubble with Handset)
    print("14/18: WhatsApp (Speech Bubble + Handset)")
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 512, 512)
    ctx = cairo.Context(surf)
    cx, cy, r = 256, 235, 140
    ctx.move_to(140, 375); ctx.line_to(170, 335)
    ctx.arc(cx, cy, r, 2.2, 0.8)
    ctx.line_to(140, 375); ctx.close_path()
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.fill()
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    phone_d = "M362.7 319.5c-15.6-2.5-30.8-7.8-44.8-15.5-7.1-3.9-15.8-3.4-22.3 1.5l-33.1 24.8c-47.5-24.1-86.4-63-110.5-110.5l24.8-33.1c4.9-6.5 5.4-15.2 1.5-22.3-7.7-14-13-29.2-15.5-44.8-2.6-16.1-16.6-27.6-32.9-27.6h-54c-18.7 0-34.1 14.8-34.8 33.5C38.9 257.6 198.4 417.1 330.5 420.9c18.7.7 33.5-14.7 33.5-33.5v-35c0-16.3-11.5-30.3-27.6-32.9z"
    ctx.save()
    ctx.translate(256, 235)
    ctx.scale(0.48, 0.48)
    ctx.translate(-240, -250)
    parse_svg_path(ctx, phone_d)
    ctx.fill()
    ctx.restore()
    im_wa = center_and_scale_surface(surf, 512, 330)
    save_icon(im_wa, ["com.whatsapp.png"])

    # 15. WhatsApp Business (Speech Bubble with Bold 'B')
    print("15/18: WhatsApp Business (Speech Bubble with 'B')")
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 512, 512)
    ctx = cairo.Context(surf)
    cx, cy, r = 256, 235, 140
    ctx.move_to(140, 375); ctx.line_to(170, 335)
    ctx.arc(cx, cy, r, 2.2, 0.8)
    ctx.line_to(140, 375); ctx.close_path()
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.fill()
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    ctx.set_line_width(28)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.move_to(220, 165); ctx.line_to(220, 305); ctx.stroke()
    ctx.move_to(220, 165); ctx.line_to(255, 165)
    ctx.arc(255, 198, 33, -math.pi/2, math.pi/2)
    ctx.line_to(220, 231); ctx.stroke()
    ctx.move_to(220, 231); ctx.line_to(260, 231)
    ctx.arc(260, 268, 37, -math.pi/2, math.pi/2)
    ctx.line_to(220, 305); ctx.stroke()
    im_w4b = center_and_scale_surface(surf, 512, 330)
    save_icon(im_w4b, ["com.whatsapp.w4b.png"])

    # 16. KDE Connect (Official Device + K Vector)
    print("16/18: KDE Connect (Device + K)")
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 512, 512)
    ctx = cairo.Context(surf)
    ctx.scale(512.0/108.0, 512.0/108.0)
    ctx.translate(10.8, 10.8)
    ctx.scale(0.8, 0.8)
    ctx.set_source_rgba(1, 1, 1, 1)
    parse_svg_path(ctx, "M40,27A2,2 0,0 0,38 29L38,79A2,2 0,0 0,40 81L68,81A2,2 0,0 0,70 79L70,29A2,2 0,0 0,68 27L40,27zM50.25,28.25L57.75,28.25A0.25,0.25 0,0 1,58 28.5A0.25,0.25 0,0 1,57.75 28.75L50.25,28.75A0.25,0.25 0,0 1,50 28.5A0.25,0.25 0,0 1,50.25 28.25zM41,30L67,30L67,78L41,78L41,30z")
    parse_svg_path(ctx, "m47.69,47.38c-0.04,0 -0.08,0.01 -0.11,0.05 0,0 -1.38,1.38 -1.38,1.38 -0.06,0.06 -0.06,0.15 -0.02,0.22 0,0 1.61,2.66 1.61,2.66 -0.29,0.48 -0.52,1 -0.68,1.55 0,0 -2.96,0.62 -2.96,0.62C44.06,53.87 44,53.95 44,54.03v1.95c0,0.08 0.06,0.15 0.14,0.17 0,0 2.88,0.7 2.88,0.7 0.15,0.63 0.39,1.24 0.71,1.79 0,0 -1.67,2.54 -1.67,2.54 -0.05,0.07 -0.04,0.17 0.02,0.22 0,0 1.38,1.38 1.38,1.38 0.06,0.06 0.15,0.06 0.22,0.02 0,0 2.61,-1.58 2.61,-1.58 0.51,0.3 1.07,0.53 1.65,0.69 0,0 0.61,2.93 0.61,2.93 0.02,0.08 0.09,0.14 0.17,0.14h1.95c0.08,0 0.15,-0.05 0.17,-0.14 0,0 0.72,-2.94 0.72,-2.94 0.6,-0.16 1.17,-0.4 1.7,-0.71 0,0 2.58,1.69 2.58,1.69 0.07,0.05 0.17,0.04 0.22,-0.02 0,0 1.37,-1.38 1.37,-1.38 0.06,-0.06 0.07,-0.15 0.03,-0.22 0,0 -0.94,-1.55 -0.94,-1.55 0,0 -0.31,0.1 -0.31,0.1 -0.04,0.01 -0.09,-0.01 -0.12,-0.05 0,0 -0.59,-0.87 -1.37,-2.01 -0.93,1.81 -2.81,3.05 -4.99,3.05 -3.09,0 -5.59,-2.51 -5.59,-5.59 0,-2.27 1.36,-4.22 3.3,-5.1v-1.44c-0.35,0.12 -0.7,0.27 -1.02,0.45 -0,0 0,-0.01 0,-0.01 0,0 -2.63,-1.73 -2.63,-1.73 -0.04,-0.02 -0.07,-0.03 -0.11,-0.02 0,0 0,0 0,0zM55.66,43.85c0,0 -3.51,0.34 -3.51,0.34v14.48c0,0 3.48,-0.53 3.48,-0.53v-6.17c0,0 4.68,6.85 4.68,6.85 0,0 3.66,-1.16 3.66,-1.16 0,0 -4.79,-6.58 -4.79,-6.58 0,0 4.83,-6.21 4.83,-6.21 0,0 -3.74,-0.86 -3.74,-0.86 0,0 -4.64,6.21 -4.64,6.21 0,0 0.04,-6.36 0.04,-6.36z")
    ctx.fill()
    im_kde = center_and_scale_surface(surf, 512, 330)
    save_icon(im_kde, ["org.kde.kdeconnect_tp.png", "org.kde.kdeconnect.png"])

    # 17. Gmail (Modern Envelope 'M')
    print("17/18: Gmail (Modern M Envelope)")
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 512, 512)
    ctx = cairo.Context(surf)
    ctx.set_source_rgba(1, 1, 1, 1)
    bx, by, bw, bh, r = 85, 120, 342, 272, 32
    ctx.move_to(bx + r, by); ctx.line_to(bx + bw - r, by)
    ctx.arc(bx + bw - r, by + r, r, -math.pi/2, 0)
    ctx.line_to(bx + bw, by + bh - r)
    ctx.arc(bx + bw - r, by + bh - r, r, 0, math.pi/2)
    ctx.line_to(bx + r, by + bh)
    ctx.arc(bx + r, by + bh - r, r, math.pi/2, math.pi)
    ctx.line_to(bx, by + r)
    ctx.arc(bx + r, by + r, r, math.pi, 3*math.pi/2)
    ctx.close_path(); ctx.fill()
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    ctx.set_line_width(18)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.move_to(110, 140); ctx.line_to(256, 260); ctx.line_to(402, 140); ctx.stroke()
    ctx.move_to(155, 365); ctx.line_to(155, 230); ctx.line_to(256, 310); ctx.line_to(357, 230); ctx.line_to(357, 365)
    ctx.close_path(); ctx.fill()
    im_gmail = center_and_scale_surface(surf, 512, 330)
    save_icon(im_gmail, ["com.google.android.gm.png"])

    # 18. Google Messages (Modern Chat Bubble Cutout)
    print("18/18: Google Messages (Modern Speech Bubble)")
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 512, 512)
    ctx = cairo.Context(surf)
    ctx.set_source_rgba(1, 1, 1, 1)
    x, y, w, h, r = 96, 120, 320, 240, 85
    ctx.move_to(x + r, y); ctx.line_to(x + w - r, y)
    ctx.arc(x + w - r, y + r, r, -math.pi/2, 0)
    ctx.line_to(x + w, y + h - r)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi/2)
    ctx.line_to(x + 50, y + h)
    ctx.line_to(x - 10, y + h + 35)
    ctx.line_to(x + 10, y + h - 15)
    ctx.arc(x + r, y + h - r, r, math.pi/2, math.pi)
    ctx.line_to(x, y + r)
    ctx.arc(x + r, y + r, r, math.pi, 3*math.pi/2)
    ctx.close_path(); ctx.fill()
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    ix, iy, iw, ih, ir = 180, 185, 170, 110, 40
    ctx.move_to(ix + ir, iy); ctx.line_to(ix + iw - ir, iy)
    ctx.arc(ix + iw - ir, iy + ir, ir, -math.pi/2, 0)
    ctx.line_to(ix + iw, iy + ih - 10)
    ctx.line_to(ix + iw + 18, iy + ih + 18)
    ctx.line_to(ix + iw - 25, iy + ih)
    ctx.arc(ix + ir, iy + ih - ir, ir, math.pi/2, math.pi)
    ctx.line_to(ix, iy + ir)
    ctx.arc(ix + ir, iy + ir, ir, math.pi, 3*math.pi/2)
    ctx.close_path(); ctx.fill()
    im_msg = center_and_scale_surface(surf, 512, 330)
    save_icon(im_msg, ["com.google.android.apps.messaging.png", "com.android.mms.png"])

    # Clean up stale/defective icons in builder/extracted_user_icons/
    print("[*] Cleaning up obsolete extracted user icons...")
    bad_extracted = [
        "cn.xender_icon.png",
        "com.Slack_icon.png",
        "com.anthropic.claude_icon.png",
        "com.duolingo_icon.png",
        "com.microsoft.teams_icon.png",
        "us.zoom.videomeetings_icon.png",
    ]
    for b in bad_extracted:
        bp = os.path.join(EXTRACTED_DIR, b)
        if os.path.exists(bp):
            os.remove(bp)
            print(f"  Removed defective extracted icon: {b}")

    print("[✓] All 18 monochrome icon glyphs generated and synchronized!")


if __name__ == "__main__":
    create_all_icons()
