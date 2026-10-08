"""Genera la imagen destacada del artículo de agencias (1200x630).

Datos: Leones de Cannes Lions 2026 por oficina mexicana, según InformaBTL.
Uso: python scripts/img_agencias_2026.py images/mejores-agencias-publicidad-digital-mexico.png
"""
import sys
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1] if len(sys.argv) > 1 else "out.png"
W, H = 1200, 630
S = 2  # supersampling para bordes suaves
F = "/usr/share/fonts/opentype/inter/"

INK = (15, 18, 34)
PANEL = (24, 28, 50)
TEXT = (245, 243, 238)
MUTED = (150, 155, 180)
ACCENT = (255, 90, 60)
BAR = (92, 99, 140)

DATA = [  # (agencia, leones)
    ("VML México", 10),
    ("Grey México", 5),
    ("LePub México", 5),
    ("Rainbow Lobster", 4),
    ("Wieden+Kennedy", 3),
    ("GUT México", 2),
    ("Ogilvy México", 1),
    ("Monks / Netflix", 1),
]


def font(name, size):
    return ImageFont.truetype(F + name, size * S)


img = Image.new("RGB", (W * S, H * S), INK)
d = ImageDraw.Draw(img)

# Columna izquierda: titular
x0 = 64
d.text((x0 * S, 64 * S), "PUBLIMERCA", font=font("InterDisplay-Black.otf", 22), fill=ACCENT)
title = ["Las mejores", "agencias de", "publicidad digital", "en México 2026"]
y = 118
for line in title:
    d.text((x0 * S, y * S), line, font=font("InterDisplay-ExtraBold.otf", 54), fill=TEXT)
    y += 62
d.text((x0 * S, (y + 18) * S), "Ranking por premios verificables:", font=font("Inter-Medium.otf", 22), fill=MUTED)
d.text((x0 * S, (y + 48) * S), "Cannes Lions, Effie e IAB MIXX", font=font("Inter-SemiBold.otf", 22), fill=TEXT)

# Columna derecha: panel con barras
px, py, pw, ph = 640, 56, 504, 518
d.rounded_rectangle([px * S, py * S, (px + pw) * S, (py + ph) * S], radius=20 * S, fill=PANEL)
d.text(((px + 28) * S, (py + 26) * S), "Leones en Cannes Lions 2026", font=font("Inter-SemiBold.otf", 21), fill=TEXT)
d.text(((px + 28) * S, (py + 56) * S), "por oficina mexicana", font=font("Inter-Regular.otf", 17), fill=MUTED)

label_w = 170
bx = px + 28 + label_w
bmax = pw - 28 - label_w - 56
row_y = py + 104
row_h = 48
vmax = max(v for _, v in DATA)
for i, (name, v) in enumerate(DATA):
    cy = row_y + i * row_h
    d.text(((px + 28) * S, (cy + 4) * S), name, font=font("Inter-Medium.otf", 17), fill=TEXT)
    bw = max(int(bmax * v / vmax), 10)
    color = ACCENT if i == 0 else BAR
    d.rounded_rectangle([bx * S, cy * S, (bx + bw) * S, (cy + 28) * S], radius=6 * S, fill=color)
    d.text(((bx + bw + 10) * S, (cy + 3) * S), str(v), font=font("Inter-Bold.otf", 18), fill=TEXT)

d.text(((px + 28) * S, (py + ph - 34) * S), "Fuente: InformaBTL, junio 2026", font=font("Inter-Regular.otf", 14), fill=MUTED)

img = img.resize((W, H), Image.LANCZOS)
img.save(OUT, "PNG", optimize=True)
print("ok", OUT)
