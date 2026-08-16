#!/usr/bin/env python3
"""
Re-extract Timur cover images from the published LinkedIn PDFs.

Pulls the largest landscape image off page 1 of each "Part N ... LinkedIn.pdf"
and writes assets/covers/sw-NN.jpg at THUMB_W wide.

The site shows covers as small list thumbnails (~176px), so 480px is plenty
even on a Retina screen. Raise THUMB_W if you ever display them larger.

    python3 tools/extract-covers.py
"""
import glob, os, re, sys
import pikepdf
from pikepdf import PdfImage
from PIL import Image

SRC = os.path.expanduser(
    "~/Documents/personal-wiki/wiki/project/Timur Newsletter/Published Draft")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "assets", "covers")
THUMB_W = 480

def main():
    if not os.path.isdir(SRC):
        sys.exit(f"source folder not found: {SRC}")
    os.makedirs(OUT, exist_ok=True)
    files = [f for f in glob.glob(os.path.join(SRC, "Part *.pdf"))
             if not os.path.basename(f).startswith("Post")]
    files.sort(key=lambda f: int(re.match(r"Part (\d+)", os.path.basename(f)).group(1)))
    for f in files:
        n = int(re.match(r"Part (\d+)", os.path.basename(f)).group(1))
        pdf = pikepdf.open(f)
        best, best_px = None, 0
        for _, raw in pdf.pages[0].images.items():
            try:
                pi = PdfImage(raw)
                px = pi.width * pi.height
                if px > best_px and pi.width > 400 and pi.width > pi.height:
                    best, best_px = pi, px
            except Exception:
                pass
        if best is None:
            print(f"  part {n:2}: no cover found"); continue
        img = best.as_pil_image().convert("RGB")
        img = img.resize((THUMB_W, round(img.height * THUMB_W / img.width)),
                         Image.LANCZOS)
        p = os.path.join(OUT, f"sw-{n:02}.jpg")
        img.save(p, "JPEG", quality=84, optimize=True)
        print(f"  part {n:2}: {img.width}x{img.height}  {os.path.getsize(p)//1024} KB")

if __name__ == "__main__":
    main()
