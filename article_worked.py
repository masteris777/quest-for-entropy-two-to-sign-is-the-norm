"""The arithmetic of one measurement, with real numbers: the particle P alone ticks (one turn of its dial), its
lengths, then P meets the detector M (product, swap), then the four lines' lengths. Every number from table_logic.
P's axis runs down (rows) and M's across (columns) in every picture; every number has two decimals.
Output: ../assets/tbl_worked.png  (light theme, white page)
"""
import os
import sys

sys.dont_write_bytecode = True
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle

from table_logic import Table

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
INK, GREY, ORANGE, TEAL, RED, PALE = "#222", "#9a9a9a", "#c8781a", "#1a8a7a", "#c0392b", "#f6f1e7"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
DIAL = np.pi / 6

fresh = Table([1, 0]).arrows
p = Table([1, 0]); p.turn(0, DIAL); once = p.arrows
q = Table(once.copy()); q.turn(0, DIAL); twice = q.arrows
m = Table([1, 0])
product = Table.meet(p, m, swap=False).arrows
met = Table.meet(p, m, swap=True).arrows
L = Table(met).lengths((0, 1)).ravel()


def z(c):
    """A complex number with two decimals: 0.87, 0.50i, -0.29, 0.30+0.40i."""
    re, im = round(c.real, 2), round(c.imag, 2)
    if abs(im) < 0.005: return f"{re:.2f}".replace("-0.00", "0.00")
    if abs(re) < 0.005: return f"{im:.2f}i"
    return f"{re:.2f}{'+' if im > 0 else '-'}{abs(im):.2f}i"


def strip(ax, x0, y0, Z, w=1.2, h=0.6, axis=True):
    """P's one-axis table, standing: P = 0 on top, P = 1 below; P's axis drawn down the left."""
    for i in range(2):
        ax.add_patch(Rectangle((x0, y0 - (i + 1) * h), w, h, fc="white", ec=GREY, lw=1))
        ax.text(x0 - 0.12, y0 - i * h - h / 2, f"P = {i}", ha="right", va="center", fontsize=10, color=INK)
        ax.text(x0 + w / 2, y0 - i * h - h / 2, z(Z[i]), ha="center", va="center", fontsize=11.5, color=INK)
    if axis:
        ax.add_patch(FancyArrowPatch((x0 - 0.75, y0 + 0.05), (x0 - 0.75, y0 - 2 * h - 0.05), arrowstyle="-|>", mutation_scale=12, color=ORANGE, lw=1.6))
        ax.text(x0 - 0.83, y0 - h, "P's axis", rotation=90, ha="right", va="center", fontsize=9.5, color=ORANGE)


def table(ax, x0, y0, Z, w=1.2, h=0.6, tint=None, tint_color=PALE, axes=True):
    """The two-axis table: P's axis down the rows, M's axis across the columns."""
    ax.text(x0 + 0.5 * w, y0 + 0.2, "M = 0", ha="center", fontsize=10, color=INK)
    ax.text(x0 + 1.5 * w, y0 + 0.2, "M = 1", ha="center", fontsize=10, color=INK)
    for i in range(2):
        ax.text(x0 - 0.12, y0 - i * h - h / 2, f"P = {i}", ha="right", va="center", fontsize=10, color=INK)
        for j in range(2):
            fc = tint_color if tint and (i, j) in tint else "white"
            ax.add_patch(Rectangle((x0 + j * w, y0 - (i + 1) * h), w, h, fc=fc, ec=GREY, lw=1))
            ax.text(x0 + j * w + w / 2, y0 - i * h - h / 2, z(Z[i, j]), ha="center", va="center", fontsize=11.5, color=INK)
    if axes:
        ax.add_patch(FancyArrowPatch((x0 - 0.75, y0 + 0.05), (x0 - 0.75, y0 - 2 * h - 0.05), arrowstyle="-|>", mutation_scale=12, color=ORANGE, lw=1.6))
        ax.text(x0 - 0.83, y0 - h, "P's axis", rotation=90, ha="right", va="center", fontsize=9.5, color=ORANGE)
        ax.add_patch(FancyArrowPatch((x0 - 0.05, y0 + 0.5), (x0 + 2 * w + 0.05, y0 + 0.5), arrowstyle="-|>", mutation_scale=12, color=TEAL, lw=1.6))
        ax.text(x0 + 2 * w + 0.15, y0 + 0.5, "M's axis", ha="left", va="center", fontsize=9.5, color=TEAL)


def mono(ax, x, y, text):
    ax.text(x, y, text, ha="left", va="top", fontsize=9.6, color=INK, family="DejaVu Sans Mono", linespacing=1.5)


def title(ax, x, y, text):
    ax.text(x, y, text, ha="left", va="bottom", fontsize=11, color=INK, fontweight="bold")


def arrow_between(ax, x0, x1, y, label):
    ax.annotate("", xy=(x1, y), xytext=(x0, y), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.4, mutation_scale=12))
    ax.text((x0 + x1) / 2, y + 0.1, label, ha="center", va="bottom", fontsize=9, color=GREY)


c, s = np.cos(DIAL), np.sin(DIAL)
W, H = 1.2, 0.6
fig, ax = plt.subplots(figsize=(10.5, 14.2), facecolor="white"); ax.axis("off")
ax.set_xlim(-0.2, 10.8); ax.set_ylim(-14.6, 0.3)
fig.text(0.5, 0.985, "one measurement, with the numbers: P ticks once at a 30° dial, then meets the detector M",
         ha="center", fontsize=12.5, color=INK)

# 1 the tick
y = -0.9
title(ax, 0.3, y + 0.75, "1  the tick: P turns the pair of cells along its axis by its dial, 30°")
strip(ax, 1.0, y, fresh)
arrow_between(ax, 2.35, 3.25, y - H, "one tick")
strip(ax, 3.4, y, once, axis=False)
mono(ax, 5.0, y + 0.05,
     "the rule, four numbers:\n"
     "  new top    = cos 30° · top + i sin 30° · bottom\n"
     "  new bottom = i sin 30° · top + cos 30° · bottom\n"
     "on the fresh table (1.00, 0.00):\n"
     f"  new top    = {c:.2f} · 1.00 + i {s:.2f} · 0.00 = {z(once[0])}\n"
     f"  new bottom = i {s:.2f} · 1.00 + {c:.2f} · 0.00 = {z(once[1])}\n"
     f"a second tick would give ({z(twice[0])}, {z(twice[1])}):\n"
     "the angle adds up, tick by tick")

# 2 the lengths of P's table
y = -4.6
title(ax, 0.3, y + 0.75, "2  the lengths: square, add, take the root")
strip(ax, 1.0, y, once)
sq1 = np.abs(once) ** 2
mono(ax, 2.9, y + 0.05,
     f"squared arrow lengths: {sq1[0]:.2f} and {sq1[1]:.2f}, they add to {sq1.sum():.2f}\n"
     f"length of cell P = 0 = √{sq1[0]:.2f} = {np.sqrt(sq1[0]):.2f}\n"
     f"length of cell P = 1 = √{sq1[1]:.2f} = {np.sqrt(sq1[1]):.2f}\n"
     f"{np.sqrt(sq1[0]):.2f}² + {np.sqrt(sq1[1]):.2f}² = 1.00: the two cells are the legs,\n"
     "the whole table the hypotenuse; a turn never changes that")

# 3 the meeting: product, then the swap
y = -7.6
title(ax, 0.3, y + 0.75, "3  the meeting: the product of the two tables, then the swap")
table(ax, 1.0, y, product)
arrow_between(ax, 3.55, 4.55, y - H, "the swap")
table(ax, 5.4, y, met, tint={(1, 0), (1, 1)}, tint_color="#fbeedd", axes=False)
ax.annotate("", xy=(5.4 + 1.5 * W, y - 2 * H + 0.1), xytext=(5.4 + 0.5 * W, y - 2 * H + 0.1),
            arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1.8))
r0 = abs(product[0, 0] * product[1, 1] - product[0, 1] * product[1, 0]); r1 = abs(met[0, 0] * met[1, 1] - met[0, 1] * met[1, 0])
mono(ax, 1.0, y - 2 * H - 0.35,
     "product: every cell = P's arrow × M's arrow, with M fresh at (1.00, 0.00):\n"
     f"  cell (0,0) = {z(once[0])} × 1.00 = {z(product[0,0])}    cell (0,1) = {z(once[0])} × 0.00 = {z(product[0,1])}\n"
     f"  cell (1,0) = {z(once[1])} × 1.00 = {z(product[1,0])}   cell (1,1) = {z(once[1])} × 0.00 = {z(product[1,1])}\n"
     "  not entangled: one strip times the other\n"
     "swap: where P reads 1, M's two cells trade places, so 0.50i moves from M = 0 to M = 1;\n"
     "  now P = 0 goes with M = 0 and P = 1 with M = 1: the detector has copied the particle.\n"
     f"  entangled: no two strips multiply to this table. receipt |z00·z11 − z01·z10|: {r0:.2f} before, {r1:.2f} after")

# 4 the four lines
y = -12.2
title(ax, 0.3, y + 0.75, "4  the four lines of the pair and their lengths")
table(ax, 1.0, y, met, tint={(0, 0), (1, 1)}, tint_color="#e3f2ef", axes=False)
sq = np.abs(met) ** 2
mono(ax, 4.0, y + 0.05,
     "a line is one cell of the pair, named by both parties:\n"
     f"  P = 0, M = 0  length √{sq[0,0]:.2f} = {L[0]:.2f}     P = 0, M = 1  length {L[1]:.2f}\n"
     f"  P = 1, M = 0  length {L[2]:.2f}             P = 1, M = 1  length √{sq[1,1]:.2f} = {L[3]:.2f}\n"
     f"squares {sq[0,0]:.2f} + {sq[0,1]:.2f} + {sq[1,0]:.2f} + {sq[1,1]:.2f} = 1.00\n"
     "two lines lit, two empty: the detector copied, it did not decide")

path = os.path.join(OUT, "tbl_worked.png")
fig.savefig(path, dpi=170, bbox_inches="tight", facecolor="white"); plt.close(fig)
print("saved", path)
