"""Generate the HASHFIT logo system as outlined SVGs (no font dependency)."""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/home/user/first/hashfit-brand/svg"
os.makedirs(OUT, exist_ok=True)

RED = "#E8312E"
BLACK = "#0A0A0A"
BONE = "#F4F1EC"
ASH = "#8A847C"
CHAR = "#1C1A19"

FONTS = {k: TTFont(os.path.join(os.environ.get("FONT_DIR", os.path.join(HERE, "fonts")), "", f"{k}.ttf")) for k in ("anton", "inter", "serif")}


def text(font_key, s, size, x, y, fill, tracking=0.0, anchor="start"):
    """Return (svg path element, width). y is the baseline. tracking in em."""
    f = FONTS[font_key]
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    upm = f["head"].unitsPerEm
    scale = size / upm
    hmtx = f["hmtx"]
    names = [cmap[ord(c)] for c in s]
    adv = [hmtx[n][0] for n in names]
    width_units = sum(adv) + tracking * upm * (len(s) - 1)
    width = width_units * scale
    if anchor == "middle":
        x -= width / 2
    elif anchor == "end":
        x -= width
    pen = SVGPathPen(gs)
    cx = 0
    for n, a in zip(names, adv):
        tp = TransformPen(pen, (scale, 0, 0, -scale, x + cx * scale, y))
        gs[n].draw(tp)
        cx += a + tracking * upm
    return f'<path fill="{fill}" d="{pen.getCommands()}"/>', width


def cap_height(font_key, size):
    f = FONTS[font_key]
    return f["OS/2"].sCapHeight * size / f["head"].unitsPerEm


def mark(x, y, s, fg, accent):
    """The hash-H mark: a '#' whose slanted uprights and crossbars also read as an H.
    Drawn in a 100x100 box, placed at (x, y) with size s."""
    k = s / 100
    def P(pts):
        return " ".join(f"{x + px * k:.2f},{y + py * k:.2f}" for px, py in pts)
    sk = 16  # horizontal slant across full height
    w = 19   # upright thickness
    def upright(bx):
        return [(bx, 100), (bx + w, 100), (bx + w + sk, 0), (bx + sk, 0)]
    def bar(y0, h, x0, x1):
        # crossbars follow the slant so they sit flush on the uprights
        t0, t1 = sk * (1 - y0 / 100), sk * (1 - (y0 + h) / 100)
        return [(x0 + t1, y0 + h), (x1 + t1, y0 + h), (x1 + t0, y0), (x0 + t0, y0)]
    parts = [
        f'<polygon fill="{fg}" points="{P(upright(8))}"/>',
        f'<polygon fill="{fg}" points="{P(upright(57))}"/>',
        f'<polygon fill="{fg}" points="{P(bar(27, 14, -2, 90))}"/>',
        f'<polygon fill="{accent}" points="{P(bar(59, 14, -8, 84))}"/>',
    ]
    return "".join(parts)


def svg(w, h, body, bg=None):
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{b}{body}</svg>'


def save(name, content):
    with open(os.path.join(OUT, name + ".svg"), "w") as fh:
        fh.write(content)


# ---------- 1. Mark ----------
for suffix, fg, bg in (("dark", BONE, BLACK), ("light", BLACK, BONE), ("transparent-white", "#FFFFFF", None), ("transparent-black", BLACK, None)):
    save(f"01-mark-{suffix}", svg(1000, 1000, mark(210, 210, 580, fg, RED), bg))

# ---------- 2. Horizontal lockup ----------
def horizontal(fg, bg, name):
    size = 300
    ch = cap_height("anton", size)
    msize = ch * 1.06
    body = mark(80, 110 + (ch - msize) / 2, msize, fg, RED)
    word, ww = text("anton", "HASHFIT", size, 80 + msize + 70, 110 + ch, fg, tracking=0.02)
    tag, tw = text("inter", "COACHING WITH AALIYAN", 44, 80 + msize + 74, 110 + ch + 100, RED, tracking=0.32)
    W = int(80 + msize + 70 + max(ww, tw) + 90)
    save(name, svg(W, int(110 + ch + 150), body + word + tag, bg))

horizontal(BONE, BLACK, "02-logo-horizontal-dark")
horizontal(BLACK, BONE, "02-logo-horizontal-light")
horizontal("#FFFFFF", None, "02-logo-horizontal-transparent-white")
horizontal(BLACK, None, "02-logo-horizontal-transparent-black")

# ---------- 3. Stacked lockup ----------
def stacked(fg, bg, name):
    W = 1400
    body = mark(W / 2 - 190, 120, 380, fg, RED)
    word, _ = text("anton", "HASHFIT", 260, W / 2, 120 + 380 + 90 + cap_height("anton", 260), fg, tracking=0.03, anchor="middle")
    ty = 120 + 380 + 90 + cap_height("anton", 260) + 110
    tag, tw = text("inter", "COACHING WITH AALIYAN", 46, W / 2, ty, RED, tracking=0.34, anchor="middle")
    save(name, svg(W, int(ty + 120), body + word + tag, bg))

stacked(BONE, BLACK, "03-logo-stacked-dark")
stacked(BLACK, BONE, "03-logo-stacked-light")
stacked("#FFFFFF", None, "03-logo-stacked-transparent-white")
stacked(BLACK, None, "03-logo-stacked-transparent-black")

# Themes: dark = black background / bone ink, light = bone background / black ink.
THEMES = {
    "dark":  dict(bg=BLACK, ink=BONE, sub=ASH, pill=BLACK, pill_ink=BONE, after=RED, after_ink="#FFFFFF", badge_mark_bar=BLACK),
    "light": dict(bg=BONE, ink=BLACK, sub="#6B655E", pill=BLACK, pill_ink=BONE, after=RED, after_ink="#FFFFFF", badge_mark_bar=BLACK),
}

# ---------- 4. Wordmark only ----------
for t, c in THEMES.items():
    ch = cap_height("anton", 300)
    wm, ww = text("anton", "HASHFIT", 300, 90, 90 + ch, c["ink"], tracking=0.02)
    save(f"04-wordmark-{t}", svg(int(ww + 180), int(ch + 180), wm, c["bg"]))
wm, ww = text("anton", "HASHFIT", 300, 60, 60 + cap_height("anton", 300), "#FFFFFF", tracking=0.02)
save("04-wordmark-transparent-white", svg(int(ww + 120), int(cap_height("anton", 300) + 120), wm))
wm, ww = text("anton", "HASHFIT", 300, 60, 60 + cap_height("anton", 300), BLACK, tracking=0.02)
save("04-wordmark-transparent-black", svg(int(ww + 120), int(cap_height("anton", 300) + 120), wm))

# ---------- 5. Transformation badge (watermark for results posts) ----------
def badge(t, c):
    H = 260
    red_w = H
    m = mark(46, 46, H - 92, BONE, BLACK)
    ch1 = cap_height("anton", 120)
    word, ww = text("anton", "HASHFIT", 120, red_w + 50, 48 + ch1, c["ink"], tracking=0.03)
    t2, tw = text("inter", "TRANSFORMATION", 38, red_w + 54, 48 + ch1 + 78, RED, tracking=0.30)
    W = int(red_w + 50 + max(ww, tw) + 60)
    body = (f'<rect width="{W}" height="{H}" rx="18" fill="{c["bg"]}"/>'
            f'<path d="M18 0H{red_w}V{H}H18a18 18 0 0 1-18-18V18A18 18 0 0 1 18 0Z" fill="{RED}"/>'
            + m + word + t2)
    save(f"05-transformation-badge-{t}", svg(W, H, body))

# ---------- 6. Before / After / Weeks tags ----------
def pill(label, fill, fg, name, stroke=None):
    size = 110
    ch = cap_height("anton", size)
    tx, tw = text("anton", label, size, 70, 55 + ch, fg, tracking=0.08)
    W, H = int(tw + 140), int(ch + 110)
    st = f' stroke="{stroke}" stroke-width="8"' if stroke else ""
    inset = 4 if stroke else 0
    rect = f'<rect x="{inset}" y="{inset}" width="{W - 2 * inset}" height="{H - 2 * inset}" rx="{H / 2 - inset}" fill="{fill}"{st}/>'
    save(name, svg(W, H, rect + tx))

def weeks(t, c):
    chn = cap_height("anton", 260)
    num, nw = text("anton", "12", 260, 60, 60 + chn, c["ink"])
    lab, lw = text("inter", "WEEKS", 58, 60 + nw + 34, 60 + chn, c["ink"], tracking=0.25)
    bar = f'<rect x="{60 + nw + 38}" y="{60 + chn - cap_height("inter", 58) - 44:.0f}" width="{lw * 0.35:.0f}" height="16" fill="{RED}"/>'
    W, H = int(60 + nw + 34 + lw + 70), int(chn + 120)
    save(f"06-tag-weeks-{t}", svg(W, H, f'<rect width="{W}" height="{H}" rx="24" fill="{c["bg"]}"/>' + num + lab + bar))

# ---------- 7. Transformation post overlay (1080x1350, photo windows are transparent) ----------
def post_overlay(t, c):
    W, H = 1080, 1350
    gap, top, side = 16, 290, 40
    pw = (W - side * 2 - gap) / 2
    ph = 860
    r = 14
    def rr(x, y, w, h):
        return (f"M{x + r} {y}H{x + w - r}A{r} {r} 0 0 1 {x + w} {y + r}V{y + h - r}A{r} {r} 0 0 1 {x + w - r} {y + h}"
                f"H{x + r}A{r} {r} 0 0 1 {x} {y + h - r}V{y + r}A{r} {r} 0 0 1 {x + r} {y}Z")
    frame = f'<path fill-rule="evenodd" fill="{c["bg"]}" d="M0 0H{W}V{H}H0Z {rr(side, top, pw, ph)} {rr(side + pw + gap, top, pw, ph)}"/>'
    head_m = mark(side, 44, 56, c["ink"], RED)
    head_w, _ = text("anton", "HASHFIT", 52, side + 56 + 20, 44 + 56, c["ink"], tracking=0.03)
    kicker, _ = text("inter", "CLIENT TRANSFORMATION", 24, W - side, 44 + 56, RED, tracking=0.28, anchor="end")
    headline, _ = text("anton", "-9KG IN 12 WEEKS", 100, side, 250, c["ink"], tracking=0.01)
    b_tag = f'<rect x="{side + 20}" y="{top + ph - 76}" width="170" height="56" rx="28" fill="{BLACK}"/>'
    b_txt, _ = text("anton", "BEFORE", 34, side + 20 + 85, top + ph - 76 + 43, BONE, tracking=0.08, anchor="middle")
    a_x = side + pw + gap + 20
    a_tag = f'<rect x="{a_x}" y="{top + ph - 76}" width="150" height="56" rx="28" fill="{RED}"/>'
    a_txt, _ = text("anton", "AFTER", 34, a_x + 75, top + ph - 76 + 43, "#FFFFFF", tracking=0.08, anchor="middle")
    foot_y = top + ph + 90
    name_t, _ = text("anton", "CLIENT NAME", 56, side, foot_y, c["ink"], tracking=0.03)
    sub_t, _ = text("inter", "COACHING WITH AALIYAN", 24, side, foot_y + 50, c["sub"], tracking=0.28)
    cta_t, _ = text("inter", "APPLY VIA LINK IN BIO", 24, W - side, foot_y + 50, RED, tracking=0.2, anchor="end")
    body = frame + head_m + head_w + kicker + headline + b_tag + b_txt + a_tag + a_txt + name_t + sub_t + cta_t
    save(f"07-transformation-post-overlay-{t}", svg(W, H, body))

for t, c in THEMES.items():
    badge(t, c)
    weeks(t, c)
    post_overlay(t, c)
    # ---------- 8. Profile picture ----------
    save(f"08-profile-picture-{t}", svg(1080, 1080, mark(290, 290, 500, c["ink"], RED), c["bg"]))

pill("BEFORE", BLACK, BONE, "06-tag-before-dark")
pill("BEFORE", BONE, BLACK, "06-tag-before-light", stroke=BLACK)
pill("AFTER", RED, "#FFFFFF", "06-tag-after-dark")
pill("AFTER", BONE, RED, "06-tag-after-light", stroke=RED)

print("done")

# ---------- 9. Coach Vault platform logos (backgrounds match its logo preview boxes) ----------
CV_LIGHT_BG, CV_DARK_BG = "#FFFFFF", "#111111"
save("09-coachvault-logo-light", svg(1000, 1000, mark(200, 200, 600, BLACK, RED), CV_LIGHT_BG))
save("09-coachvault-logo-dark", svg(1000, 1000, mark(200, 200, 600, BONE, RED), CV_DARK_BG))

# ---------- 10. Post logos: compact mark + wordmark, transparent, tight crop, no tagline ----------
def post_logo(fg, name):
    size, pad = 200, 24
    ch = cap_height("anton", size)
    word, ww = text("anton", "HASHFIT", size, pad + ch * 1.06 + 44, pad + ch, fg, tracking=0.03)
    body = mark(pad + ch * 0.04, pad, ch, fg, RED) + word
    save(name, svg(int(pad + ch * 1.06 + 44 + ww + pad), int(ch + pad * 2), body))

post_logo("#FFFFFF", "10-post-logo-white")
post_logo(BLACK, "10-post-logo-dark")
