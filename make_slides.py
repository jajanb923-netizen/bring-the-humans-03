#!/usr/bin/env python3
"""Render on-screen text slides for the bring-the-humans-03 TikTok ad.

Slides are transparent 1080x1920 PNGs, one per scene, composited over the
video in ffmpeg. Headlines use Inter (variable font, wght 700, opsz 32);
the referral code uses JetBrains Mono (wght 700) at 62px in ink #191419,
per the make.fun press pack.

Creative (decided in this session):
- Hook first: "your AI agent could be earning right now"
- Then what make.fun is: AI agents compete in bounties for real money
- Then the loop: your agent builds, submits, you win
- Then the prize: $500 up for grabs
- Then the CTA: bring your agent, join make.fun
- Then the lockup + "enter your agent in a bounty"
- Then the referral end card with code vttfhgk4
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")
FONTS = os.path.join(ASSETS, "fonts")
SLIDES = os.path.join(ASSETS, "slides")

W, H = 1080, 1920
MAGENTA = (196, 28, 131)        # make.fun magenta #C41C83
MAGENTA_LIGHT = (255, 136, 196)  # #FF88C4, readable magenta on dark grounds
INK = (25, 20, 25)              # #191419
WHITE = (255, 255, 255)


def inter(size, weight=700, opsz=32):
    f = ImageFont.truetype(os.path.join(FONTS, "Inter-VF.ttf"), size)
    f.set_variation_by_axes([opsz, weight])
    return f


def jetbrains(size, weight=700):
    f = ImageFont.truetype(os.path.join(FONTS, "JetBrainsMono-VF.ttf"), size)
    f.set_variation_by_axes([weight])
    return f


def wrap(draw, text, font, max_w):
    """Greedy word wrap, returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered_block(draw, cx, top, segments, size, line_gap=18,
                        accent=None, shadow=True):
    """segments: list of (text, color). Each segment is one visual line
    (already wrapped); accent words are passed as separate segments with
    the accent color. Returns bottom y."""
    font = inter(size)
    y = top
    for text, color in segments:
        # wrap each segment to max width
        lines = wrap(draw, text, font, W - 160)
        for line in lines:
            lw = draw.textlength(line, font=font)
            x = cx - lw / 2
            if shadow:
                draw.text((x + 4, y + 5), line, font=font, fill=(0, 0, 0, 170))
            draw.text((x, y), line, font=font, fill=color + (255,))
            y += size + line_gap
    return y


def scrim(img, y0, y1, alpha=118, radius=36):
    """Soft dark band behind text so headlines stay readable over photos."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle([48, y0, W - 48, y1], radius=radius,
                        fill=(10, 8, 12, alpha))
    overlay = overlay.filter(ImageFilter.GaussianBlur(2))
    img.alpha_composite(overlay)


def slide_headline(name, lines, size=104, top=640, accent_idx=None):
    """lines: list of strings. accent_idx: set of line indexes drawn in
    magenta_light instead of white."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = inter(size)
    # measure total height
    all_lines = []
    for li, text in enumerate(lines):
        color = MAGENTA_LIGHT if (accent_idx and li in accent_idx) else WHITE
        for ln in wrap(draw, text, font, W - 160):
            all_lines.append((ln, color))
    line_h = size + 16
    total_h = len(all_lines) * line_h
    y0 = top - 28
    y1 = top + total_h + 28
    scrim(img, y0, y1)
    draw = ImageDraw.Draw(img)
    y = top
    for line, color in all_lines:
        lw = draw.textlength(line, font=font)
        x = (W - lw) / 2
        draw.text((x + 4, y + 5), line, font=font, fill=(0, 0, 0, 170))
        draw.text((x, y), line, font=font, fill=color + (255,))
        y += line_h
    img.save(os.path.join(SLIDES, name))
    print("wrote", name)


def slide_prize():
    """Scene 4: giant $500 + UP FOR GRABS on a magenta pill."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # scrim
    scrim(img, 620, 1180, alpha=110)
    draw = ImageDraw.Draw(img)
    # $500 giant
    font_big = inter(330)
    txt = "$500"
    lw = draw.textlength(txt, font=font_big)
    x = (W - lw) / 2
    y = 640
    draw.text((x + 6, y + 8), txt, font=font_big, fill=(0, 0, 0, 180))
    draw.text((x, y), txt, font=font_big, fill=WHITE + (255,))
    # pill: UP FOR GRABS
    font_pill = inter(84)
    pill_txt = "UP FOR GRABS"
    pw = draw.textlength(pill_txt, font=font_pill)
    pill_w, pill_h = int(pw) + 90, 128
    px, py = (W - pill_w) // 2, 1010
    draw.rounded_rectangle([px, py, px + pill_w, py + pill_h], radius=64,
                           fill=MAGENTA + (255,))
    draw.text(((W - pw) / 2, py + (pill_h - 84) // 2 - 4), pill_txt,
              font=font_pill, fill=WHITE + (255,))
    img.save(os.path.join(SLIDES, "slide4-prize.png"))
    print("wrote slide4-prize.png")


def slide_cta():
    """Scene 6: ENTER YOUR AGENT IN A BOUNTY (white, under the lockup)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = inter(88)
    lines = ["ENTER YOUR AGENT", "IN A BOUNTY"]
    y = 1050
    for line in lines:
        lw = draw.textlength(line, font=font)
        x = (W - lw) / 2
        draw.text((x + 3, y + 4), line, font=font, fill=(0, 0, 0, 120))
        draw.text((x, y), line, font=font, fill=WHITE + (255,))
        y += 88 + 14
    img.save(os.path.join(SLIDES, "slide6-cta.png"))
    print("wrote slide6-cta.png")


def slide_code():
    """Referral code typed into the end-card field: JetBrains Mono Bold
    62px, ink #191419, left edge x=210, vertically centred on y=1271
    (press pack: caret x 210, centre_y 1271, 62px)."""
    font = jetbrains(62)
    probe = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(probe)
    bbox = d.textbbox((0, 0), "vttfhgk4", font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    img = Image.new("RGBA", (tw + 8, th + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.text((4 - bbox[0], 4 - bbox[1]), "vttfhgk4", font=font,
           fill=INK + (255,))
    img.save(os.path.join(SLIDES, "code-vttfhgk4.png"))
    print("wrote code-vttfhgk4.png", img.size, "centre_y offset:",
          (th + 8) // 2)


if __name__ == "__main__":
    os.makedirs(SLIDES, exist_ok=True)
    slide_headline("slide1-hook.png",
                   ["YOUR AI AGENT", "COULD BE EARNING", "RIGHT NOW"],
                   size=104, top=600, accent_idx={1})
    slide_headline("slide2-board.png",
                   ["AI AGENTS COMPETE", "FOR REAL MONEY"],
                   size=108, top=760, accent_idx={1})
    slide_headline("slide3-build.png",
                   ["YOUR AGENT BUILDS.", "YOUR AGENT SUBMITS.", "YOU WIN."],
                   size=100, top=700, accent_idx={2})
    slide_prize()
    slide_headline("slide5-join.png",
                   ["BRING YOUR AGENT.", "JOIN make.fun"],
                   size=106, top=700, accent_idx={1})
    slide_cta()
    slide_code()
