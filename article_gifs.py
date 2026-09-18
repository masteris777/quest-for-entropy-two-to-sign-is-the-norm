"""Two short animations for the article, light-themed, every number from table_logic.py.
  gif_one_ticks.gif   one particle P ticking on its own: the arrows turn, the book grows, each record carries a unitdraw
  gif_two_ticks.gif   P and M entangled, each ticking on its own clock (P every 3 s, M every 2 s); the receipt never moves
Keyframes are rendered with matplotlib and assembled with Pillow, one duration per frame. Output: ../assets/
"""
import os
import sys

sys.dont_write_bytecode = True
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
from PIL import Image

import table_logic
from table_logic import Table, unitdraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
INK, GREY, ORANGE, TEAL, RED, GREEN, BLUE = "#222", "#9a9a9a", "#c8781a", "#1a8a7a", "#c0392b", "#2e8b57", "#3b6ea5"
CELL, CELL_DIM, PALE = "#f1e6d2", "#faf7f1", "#f6f1e7"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
TWEEN = 6            # frames per turn
TWEEN_MS = 70
DPI = 100


# ---------------------------------------------------------------- drawing helpers
def render(fig):
    fig.canvas.draw()
    img = Image.fromarray(np.asarray(fig.canvas.buffer_rgba())).convert("RGB")
    plt.close(fig)
    return img


def save_gif(name, frames, durations):
    pal = [f.convert("P", palette=Image.ADAPTIVE, colors=128) for f in frames]
    path = os.path.join(OUT, name)
    pal[0].save(path, save_all=True, append_images=pal[1:], duration=durations, loop=0, optimize=True)
    print(f"saved {name}: {len(frames)} frames, {sum(durations)/1000:.1f} s, {os.path.getsize(path)/1e6:.2f} MB")


def ztext(zc):
    re_, im = round(zc.real, 2), round(zc.imag, 2)
    if abs(im) < 0.005: return f"{re_:.2f}".replace("-0.00", "0.00")
    if abs(re_) < 0.005: return f"{im:.2f}i"
    return f"{re_:.2f}{'+' if im > 0 else '-'}{abs(im):.2f}i"


def cell(ax, x, y, w, h, zc, dim=False):
    """One cell: tinted square, the arrow in a circle, the number, a length bar."""
    L = abs(zc)
    ax.add_patch(Rectangle((x, y), w, h, fc=CELL_DIM if (dim or L < 1e-9) else CELL, ec="#ddd", lw=1))
    cx, cy, r = x + w / 2, y + h * 0.62, min(w, h) * 0.24
    ax.add_patch(Circle((cx, cy), r, fc="white", ec="#e2e2e2", lw=1))
    if L > 1e-9:
        ax.annotate("", xy=(cx + r * 0.92 * zc.real, cy + r * 0.92 * zc.imag), xytext=(cx, cy),
                    arrowprops=dict(arrowstyle="-|>,head_width=0.18,head_length=0.3", color=INK, lw=1.8,
                                    mutation_scale=8, shrinkA=0, shrinkB=0))
    else:
        ax.plot([cx], [cy], "o", color="#c8c8c8", ms=2.5)
    label = ztext(zc)
    ax.text(cx, y + h * 0.26, label, ha="center", va="center", fontsize=9.5 if len(label) <= 5 else 7.5, color=INK, fontweight="bold")
    bw = w * 0.7
    ax.add_patch(Rectangle((cx - bw / 2, y + h * 0.1), bw, h * 0.05, fc="#e6e0d4", ec="none"))
    ax.add_patch(Rectangle((cx - bw / 2, y + h * 0.1), bw * L, h * 0.05, fc="#777", ec="none"))


def book(ax, x, y, w, h, name, color, records, keep=5):
    """A book: its name, then its newest records, newest at the bottom and highlighted."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02", fc="white", ec=color, lw=1.4))
    ax.text(x + 0.12, y + h - 0.22, f"{name}'s book", fontsize=10, color=color, fontweight="bold")
    ax.text(x + w - 0.12, y + h - 0.22, "tick · unitdraw", fontsize=8, color=GREY, ha="right")
    shown = records[-keep:]
    for i, (n, u) in enumerate(shown):
        yy = y + h - 0.52 - i * 0.30
        last = i == len(shown) - 1
        if last:
            ax.add_patch(Rectangle((x + 0.06, yy - 0.12), w - 0.12, 0.27, fc=PALE, ec="none"))
        ax.text(x + 0.18, yy, f"{n:>2}", fontsize=9.5, color=INK, va="center", family="DejaVu Sans Mono")
        ax.text(x + w - 0.18, yy, f"{u:.2f}", fontsize=9.5, color=INK if last else GREY, va="center",
                ha="right", family="DejaVu Sans Mono", fontweight="bold" if last else "normal")
    if len(records) > keep:
        ax.text(x + 0.18, y + h - 0.36, "…", fontsize=9, color=GREY, va="center")


def new_fig(w=7.2, h=3.6):
    fig, ax = plt.subplots(figsize=(w, h), dpi=DPI, facecolor="white")
    ax.axis("off"); ax.set_xlim(0, w); ax.set_ylim(0, h)
    return fig, ax


# ---------------------------------------------------------------- GIF 1: one particle ticking
def gif_one():
    table_logic.reset()
    theta = np.pi / 6
    t = Table([1, 0])
    records = []

    def frame(arrows, ticks, records, turning=False):
        fig, ax = new_fig(7.2, 3.0)
        cw, ch, x0, y0 = 1.15, 1.3, 0.55, 1.05
        ax.annotate("", xy=(x0 + 2 * cw + 0.2, y0 + ch + 0.32), xytext=(x0, y0 + ch + 0.32),
                    arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.3))
        ax.text(x0, y0 + ch + 0.42, "P's axis", color=TEAL, fontsize=9, va="bottom")
        for j in range(2):
            ax.text(x0 + j * cw + cw / 2, y0 + ch + 0.12, f"P = {j}", ha="center", fontsize=9.5, color=INK)
            cell(ax, x0 + j * cw, y0, cw, ch, arrows[j])
        ax.text(x0 + cw, y0 - 0.3, f"tick {ticks}" + ("  · turning" if turning else ""), ha="center",
                fontsize=10, color=ORANGE if turning else INK, fontweight="bold")
        book(ax, 3.75, 0.5, 3.0, 2.3, "P", TEAL, records)
        return render(fig)

    frames, durs = [frame(t.arrows, 0, records)], [1200]
    for n in range(1, 11):
        base = t.arrows.copy()
        for k in range(1, TWEEN + 1):
            tw = Table(base.copy()); tw.turn(0, theta * k / TWEEN)
            frames.append(frame(tw.arrows, n - 1, records, turning=True)); durs.append(TWEEN_MS)
        t.turn(0, theta)
        records.append((n, unitdraw("P")))
        frames.append(frame(t.arrows, n, records)); durs.append(1400)
    durs[-1] = 2200
    save_gif("gif_one_ticks.gif", frames, durs)


# ---------------------------------------------------------------- GIF 2: two entangled particles, two clocks
def build_pair():
    p = Table([1, 0]); p.turn(0, np.pi / 6)
    return Table.meet(p, Table([1, 0]))          # axes (P, M): rows P, columns M


def draw_pair(ax, arrows, x0, y0, cw, ch, title=None):
    ax.annotate("", xy=(x0 + 2 * cw + 0.15, y0 + 2 * ch + 0.42), xytext=(x0, y0 + 2 * ch + 0.42),
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.3))
    ax.text(x0, y0 + 2 * ch + 0.52, "M's axis", color=TEAL, fontsize=9, va="bottom")
    ax.annotate("", xy=(x0 - 0.42, y0 - 0.1), xytext=(x0 - 0.42, y0 + 2 * ch),
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.3))
    ax.text(x0 - 0.5, y0 + ch, "P's axis", color=ORANGE, fontsize=9, rotation=90, va="center", ha="right")
    for j in range(2):
        ax.text(x0 + j * cw + cw / 2, y0 + 2 * ch + 0.12, f"M = {j}", ha="center", fontsize=9, color=INK)
    for i in range(2):
        ax.text(x0 - 0.1, y0 + (1 - i) * ch + ch / 2, f"P = {i}", ha="right", va="center", fontsize=9, color=INK)
        for j in range(2):
            cell(ax, x0 + j * cw, y0 + (1 - i) * ch, cw, ch, arrows[i, j])


def gif_two():
    table_logic.reset()
    theta = np.pi / 6
    t = build_pair()
    rec = {"P": [], "M": []}
    axis = {"P": 0, "M": 1}
    col = {"P": ORANGE, "M": TEAL}
    events = sorted([(s, "M") for s in range(2, 13, 2)] + [(s, "P") for s in range(3, 13, 3)])
    receipt = t.receipt()

    def frame(arrows, who=None, clock=0.0):
        fig, ax = new_fig(7.2, 4.0)
        draw_pair(ax, arrows, 1.0, 0.8, 1.05, 1.15)
        ax.text(2.05, 0.5, f"receipt {receipt:.2f}", ha="center", fontsize=9.5, color=RED, fontweight="bold")
        if who:
            ax.text(2.05, 0.2, f"{who} turning", ha="center", fontsize=10, color=col[who], fontweight="bold")
        ax.text(6.95, 3.7, f"{clock:4.1f} s", ha="right", fontsize=10, color=GREY, family="DejaVu Sans Mono")
        book(ax, 3.95, 1.85, 3.0, 1.55, "P", ORANGE, rec["P"], keep=3)
        book(ax, 3.95, 0.15, 3.0, 1.55, "M", TEAL, rec["M"], keep=3)
        return render(fig)

    frames, durs = [frame(t.arrows, clock=0.0)], [1000]
    clock = 0.0
    for s, who in events:
        if s > clock:
            durs[-1] = int((s - clock) * 1000) - TWEEN * TWEEN_MS if len(frames) > 1 else durs[-1]
            durs[-1] = max(durs[-1], 400)
        base = t.arrows.copy()
        for k in range(1, TWEEN + 1):
            tw = Table(base.copy()); tw.turn(axis[who], theta * k / TWEEN)
            frames.append(frame(tw.arrows, who, s)); durs.append(TWEEN_MS)
        t.turn(axis[who], theta)
        rec[who].append((len(rec[who]) + 1, unitdraw(who)))
        frames.append(frame(t.arrows, clock=s)); durs.append(600)
        clock = s
    durs[-1] = 2200
    assert abs(t.receipt() - receipt) < 1e-9
    save_gif("gif_two_ticks.gif", frames, durs)
    return t


if __name__ == "__main__":
    gif_one()
    gif_two()
