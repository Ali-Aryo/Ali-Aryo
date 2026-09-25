"""Turns Profile_Pic.jpg into colored ASCII rows: [[(char, hex_color | None), ...], ...]."""
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

SRC = Path(__file__).resolve().parent.parent / 'Profile_Pic.jpg'
RAMP = '@%#*+=-:.'          # dark pixel -> dense glyph, so hair and suit carry the shape
BACKDROP = (215, 190, 150)  # photo's beige wall, dropped to blank space


def portrait(cols=54, rows=34, crop=(80, 20, 330, 330)):
    im = Image.open(SRC).convert('RGB').crop(crop)
    im = im.filter(ImageFilter.UnsharpMask(radius=3, percent=160, threshold=2))
    small = im.resize((cols, rows), Image.LANCZOS)
    lum = ImageOps.autocontrast(small.convert('L'), cutoff=2)
    color = ImageEnhance.Color(ImageEnhance.Brightness(small).enhance(1.35)).enhance(1.4)

    def lift(c):  # keep darks readable on a dark terminal; quantize so runs merge into fewer tspans
        return min(255, max(90, c) // 20 * 20 + 10)

    out = []
    for y in range(rows):
        row = []
        for x in range(cols):
            r, g, b = small.getpixel((x, y))
            if ((r - BACKDROP[0]) ** 2 + (g - BACKDROP[1]) ** 2 + (b - BACKDROP[2]) ** 2) ** 0.5 < 50:
                row.append((' ', None))
                continue
            v = lum.getpixel((x, y)) / 255
            R, G, B = color.getpixel((x, y))
            row.append((RAMP[min(len(RAMP) - 1, int(v * len(RAMP)))], f'#{lift(R):02x}{lift(G):02x}{lift(B):02x}'))
        out.append(row)
    return out
