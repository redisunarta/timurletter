#!/usr/bin/env python3
"""
Generate the Open Graph card — assets/og.png (1200x630).

    python3 tools/make-og.py            # photo variant (default)
    python3 tools/make-og.py --logo     # Timur logo variant
    python3 tools/make-og.py --both     # writes og-photo.png and og-logo.png to preview

This is the image LinkedIn, X, WhatsApp and Slack show when someone pastes
your URL. It is a real image file, NOT rendered from the page, so it does
NOT update when you edit the site copy. Rerun this script whenever the
name, tagline, subtitle or domain changes.

Everything you would want to edit is in the CONFIG block below.
"""

import os
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---------------------------------------------------------------- CONFIG ----
# Edit these. They must match the site copy.
NAME     = "Redi Sunarta"
TAGLINE  = "Analytics for consumer tech"
SUBTITLE = ("I help consumer tech companies make promotional "
            "and incentive spend actually profitable.")
DOMAIN   = "timurletter.com"
PLACE    = "Jakarta, Indonesia"

PHOTO = "assets/redi-440.jpg"
LOGO  = "assets/timur-logo.png"

# Design tokens — same values as css/style.css
INK    = (26, 26, 26)        # --ink      #1A1A1A
MUTED  = (90, 90, 90)        # body grey
PAPER  = (250, 250, 248)     # --paper    #FAFAF8
ACCENT = (11, 95, 255)       # --accent   #0B5FFF
HAIR   = (223, 223, 218)     # hairline rule
LOGO_INK = (21, 47, 40)      # Timur mark  #152F28

W, H = 1200, 630             # the size every platform expects
LOGO_SIZE = 216              # logo drawn smaller than the 264px photo box,
                             # so a mark gets breathing room a portrait doesn't need
# ---------------------------------------------------------------------------

FONT_DIR = "/usr/share/fonts/truetype/liberation2"
if not os.path.isdir(FONT_DIR):
    FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(weight, size):
    path = os.path.join(FONT_DIR, f"LiberationSans-{weight}.ttf")
    if not os.path.exists(path):
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy wrap by measured pixel width, not character count."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def rounded(img, size, radius):
    """Square-crop, resize, and round the corners of an image."""
    side = min(img.size)
    left, top = (img.width - side) // 2, (img.height - side) // 2
    img = img.crop((left, top, left + side, top + side))
    img = img.resize((size, size), Image.LANCZOS).convert("RGB")
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1],
                                           radius=radius, fill=255)
    img.putalpha(mask)
    return img


def build(art_path, out_path, contain=False):
    card = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(card)

    X = 80                     # left margin
    ART = 264                  # artwork box
    ART_X = W - X - ART        # right-aligned artwork
    TEXT_W = ART_X - X - 56    # text column, 56px gutter before the artwork

    # accent rule — the same visual signature as the site header
    d.rounded_rectangle([X, 74, X + 66, 82], radius=4, fill=ACCENT)

    y = 128
    f_name = font("Bold", 70)
    d.text((X, y), NAME, font=f_name, fill=INK)
    y += 96

    f_tag = font("Regular", 40)
    for line in wrap(d, TAGLINE, f_tag, TEXT_W):
        d.text((X, y), line, font=f_tag, fill=INK)
        y += 52

    y += 30
    d.line([X, y, ART_X - 56, y], fill=HAIR, width=1)
    y += 34

    f_sub = font("Regular", 27)
    for line in wrap(d, SUBTITLE, f_sub, TEXT_W):
        d.text((X, y), line, font=f_sub, fill=MUTED)
        y += 38

    # domain and place, baseline-anchored to the bottom margin
    f_dom = font("Bold", 27)
    f_place = font("Regular", 22)
    d.text((X, H - 122), DOMAIN, font=f_dom, fill=ACCENT)
    d.text((X, H - 78), PLACE, font=f_place, fill=MUTED)

    # artwork, vertically centred against the name + tagline block
    art = Image.open(art_path)
    if contain:
        # The logo ships as dark-on-white with anti-aliased edges, so pasting
        # it as a block leaves a visible rectangle: its background is
        # #FCFDFD-#FFFFFF with a slight horizontal gradient, while the paper
        # is the warmer #FAFAF8.
        #
        # Multiply-blending gets close but cannot cancel the gradient — one
        # white point leaves one edge two levels off, which is still faintly
        # visible. A hard cutout would leave a pale halo on the anti-aliased
        # spokes.
        #
        # The mark is monochrome (#152F28 throughout), so the reliable move is
        # to treat luminance as an ink-coverage matte and repaint it: every
        # background pixel resolves to *exactly* the paper colour whatever the
        # gradient does, solid pixels to exactly the logo green, and the
        # anti-aliased spoke edges to a correct blend of the two.
        art = art.convert("RGB")
        art.thumbnail((LOGO_SIZE, LOGO_SIZE), Image.LANCZOS)
        lw, lh = art.size
        px = art.load()

        lum = [[(299 * px[ix, iy][0] + 587 * px[ix, iy][1]
                 + 114 * px[ix, iy][2]) // 1000
                for ix in range(lw)] for iy in range(lh)]
        flat = sorted(v for row in lum for v in row)
        # a high percentile, not max, so gradient noise clamps to zero coverage
        white = max(1, flat[int(len(flat) * 0.995)])
        black = flat[int(len(flat) * 0.002)]
        span = max(1, white - black)

        # Background pixels sit a shade below the white point, which would
        # leave them at ~1% coverage — enough to still read as a faint box.
        # Anything under 4% coverage is background noise, not artwork: a real
        # anti-aliased spoke edge ramps through that range in well under a
        # pixel, so snapping it to zero costs nothing visible.
        DEADBAND = 0.04

        for iy in range(lh):
            for ix in range(lw):
                a = (white - lum[iy][ix]) / span
                a = 0.0 if a < DEADBAND else (1.0 if a > 1.0 else a)
                px[ix, iy] = tuple(
                    round(PAPER[i] + a * (LOGO_INK[i] - PAPER[i]))
                    for i in range(3)
                )
        # centre the logo inside the same 264px box the portrait occupies,
        # so the two variants share one layout
        card.paste(art, (ART_X + (ART - lw) // 2, 136 + (ART - lh) // 2))
    else:
        art = rounded(art, ART, 10)
        card.paste(art, (ART_X, 136), art)

    card.save(out_path, "PNG", optimize=True)
    kb = os.path.getsize(out_path) / 1024
    print(f"  wrote {out_path}  {W}x{H}  {kb:.0f} KB")


if __name__ == "__main__":
    if "--both" in sys.argv:
        # underscore prefix: assets/_* is gitignored, so throwaway previews
        # can never be committed by accident
        build(PHOTO, "assets/_og-photo.png")
        build(LOGO, "assets/_og-logo.png", contain=True)
        print("\npreview both, then rerun without --both (or with --logo) "
              "to write assets/og.png")
    elif "--logo" in sys.argv:
        build(LOGO, "assets/og.png", contain=True)
    else:
        build(PHOTO, "assets/og.png")
