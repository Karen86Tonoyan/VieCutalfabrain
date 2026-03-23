#!/usr/bin/env python3
"""Generate the GitHub social preview image (1280x640) for VieCut."""

from PIL import Image, ImageDraw, ImageFont
import math
import os

W, H = 1280, 640
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "social-preview.png")

canvas = Image.new("RGB", (W, H), (26, 26, 46))
draw = ImageDraw.Draw(canvas)

# Gradient background (dark navy)
cx, cy = W // 2, H // 2
for r in range(500, 0, -2):
    frac = r / 500
    c1 = int(26 + (22 - 26) * (1 - frac))
    c2 = int(26 + (33 - 26) * (1 - frac))
    c3 = int(46 + (62 - 46) * (1 - frac))
    draw.ellipse([cx - r * 1.6, cy - r, cx + r * 1.6, cy + r], fill=(c1, c2, c3))

# Colors matching VieCut banner
blue = (66, 165, 245)       # #42a5f5 - S partition
orange = (255, 138, 101)    # #ff8a65 - T partition
red_cut = (239, 83, 80)     # #ef5350 - cut line
bg = (26, 26, 46)

# S partition nodes (left side, densely connected)
s_nodes = [
    (660, 100), (730, 140), (680, 210), (750, 250),
    (640, 300), (720, 340), (660, 400), (740, 430),
    (690, 480), (770, 180),
]

# T partition nodes (right side, densely connected)
t_nodes = [
    (1010, 100), (1080, 140), (1030, 210), (1100, 250),
    (990, 300), (1070, 340), (1020, 400), (1090, 430),
    (1040, 480), (960, 180),
]

# Intra-partition edges (S) - well connected
s_edges = [
    (0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4),
    (3, 5), (4, 5), (4, 6), (5, 6), (5, 7), (6, 7),
    (6, 8), (7, 8), (0, 9), (1, 9), (3, 9), (9, 5),
]

# Intra-partition edges (T) - well connected
t_edges = [
    (0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4),
    (3, 5), (4, 5), (4, 6), (5, 6), (5, 7), (6, 7),
    (6, 8), (7, 8), (0, 9), (9, 2), (9, 4), (1, 3),
]

# Cut edges - only 2 edges cross, making it a clear minimum cut
cut_edges = [
    (3, 9),  # S[3] to T[9]
    (5, 4),  # S[5] to T[4]
]

# Draw intra-S edges
for i, j in s_edges:
    x1, y1 = s_nodes[i]
    x2, y2 = s_nodes[j]
    draw.line([(x1, y1), (x2, y2)], fill=(blue[0] // 2, blue[1] // 2, blue[2] // 2), width=2)

# Draw intra-T edges
for i, j in t_edges:
    x1, y1 = t_nodes[i]
    x2, y2 = t_nodes[j]
    draw.line([(x1, y1), (x2, y2)], fill=(orange[0] // 2, orange[1] // 2, orange[2] // 2), width=2)

# Draw cut edges (red, semi-transparent)
for si, ti in cut_edges:
    x1, y1 = s_nodes[si]
    x2, y2 = t_nodes[ti]
    cut_c = (red_cut[0] // 2, red_cut[1] // 2, red_cut[2] // 2)
    draw.line([(x1, y1), (x2, y2)], fill=cut_c, width=2)

# Draw the cut line (dashed, curved vertical line between partitions)
cut_x = 870
for y in range(40, H - 40, 12):
    offset = int(15 * math.sin(y * 0.015))
    x = cut_x + offset
    draw.line([(x, y), (x, y + 6)], fill=red_cut, width=3)

# Glow for S nodes
for x, y in s_nodes:
    for r in range(22, 5, -1):
        alpha_frac = 1 - (r - 5) / 17
        gc = tuple(int(blue[k] * 0.15 * alpha_frac + (1 - 0.15 * alpha_frac) * bg[k]) for k in range(3))
        draw.ellipse([x - r, y - r, x + r, y + r], fill=gc)

# Glow for T nodes
for x, y in t_nodes:
    for r in range(22, 5, -1):
        alpha_frac = 1 - (r - 5) / 17
        gc = tuple(int(orange[k] * 0.15 * alpha_frac + (1 - 0.15 * alpha_frac) * bg[k]) for k in range(3))
        draw.ellipse([x - r, y - r, x + r, y + r], fill=gc)

# Draw S nodes
for x, y in s_nodes:
    r = 9
    bright = tuple(min(255, int(v * 1.2)) for v in blue)
    draw.ellipse([x - r, y - r, x + r, y + r], fill=blue, outline=bright, width=2)

# Draw T nodes
for x, y in t_nodes:
    r = 9
    bright = tuple(min(255, int(v * 1.2)) for v in orange)
    draw.ellipse([x - r, y - r, x + r, y + r], fill=orange, outline=bright, width=2)

# Fonts
try:
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    font_tag = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    font_legend = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
except OSError:
    font_title = font_sub = font_tag = font_legend = ImageFont.load_default()

text_x = 60

# Title: "Vie" in red, "Cut" in white
draw.text((text_x, 140), "Vie", fill=red_cut, font=font_title)
vie_bbox = draw.textbbox((text_x, 140), "Vie", font=font_title)
draw.text((vie_bbox[2], 140), "Cut", fill=(224, 224, 224), font=font_title)

# Separator
draw.line([(text_x, 245), (text_x + 480, 245)], fill=(60, 80, 110), width=2)

# Subtitle
draw.text((text_x, 265), "Shared-Memory Minimum Cuts", fill=(144, 164, 174), font=font_sub)

# Tagline
draw.text((text_x, 325), "Inexact, Exact, Cactus, Multiterminal", fill=(96, 125, 139), font=font_tag)

# Badge: Part of KaHIP
badge_y = 400
badge_text = "Part of KaHIP"
badge_bbox = draw.textbbox((0, 0), badge_text, font=font_legend)
bw = badge_bbox[2] - badge_bbox[0]
draw.rounded_rectangle(
    [text_x, badge_y, text_x + bw + 24, badge_y + 32],
    radius=16, fill=(38, 50, 56)
)
draw.text((text_x + 12, badge_y + 5), badge_text, fill=(128, 203, 196), font=font_legend)

# Legend (bottom-left)
legend_y = 480
# S
draw.line([(text_x, legend_y), (text_x + 30, legend_y)], fill=blue, width=3)
draw.text((text_x + 40, legend_y - 10), "S partition", fill=(160, 160, 160), font=font_legend)
# T
draw.line([(text_x, legend_y + 30), (text_x + 30, legend_y + 30)], fill=orange, width=3)
draw.text((text_x + 40, legend_y + 20), "T partition", fill=(160, 160, 160), font=font_legend)
# Cut
for dx in range(0, 30, 10):
    draw.line([(text_x + dx, legend_y + 60), (text_x + dx + 5, legend_y + 60)], fill=red_cut, width=3)
draw.text((text_x + 40, legend_y + 50), "Minimum cut", fill=(160, 160, 160), font=font_legend)

# Bottom tagline
bottom_text = "shared-memory parallel minimum cut algorithms"
bt_bbox = draw.textbbox((0, 0), bottom_text, font=font_legend)
bt_w = bt_bbox[2] - bt_bbox[0]
draw.text(((W - bt_w) // 2 + 200, H - 40), bottom_text, fill=(84, 110, 122), font=font_legend)

canvas.save(OUT_PATH, "PNG", quality=95)
print(f"Saved {OUT_PATH}")
