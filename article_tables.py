"""Render the article's tables as light-themed images (Substack renders no markdown tables).
Outputs: ../assets/tbl_tables.png, ../assets/tbl_four_cases.png, ../assets/tbl_ladder.png
Numbers: the four-case table is exact at a 30-degree turn; the ladder numbers are table_logic.py's exam 1 output.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
INK, GREY, ORANGE, TEAL, RED, PALE = "#222", "#9a9a9a", "#c8781a", "#1a8a7a", "#c0392b", "#f6f1e7"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12})


def grid(ax, rows, cols, cells, x0=0, y0=0, w=1.4, h=0.7, head_fc="#eeeeee", highlight=None, bold_first_col=False):
    """cells[i][j] text; row 0 is the header. highlight: set of row indices to tint."""
    for i in range(rows):
        for j in range(cols):
            y = y0 - i * h
            fc = head_fc if i == 0 else (PALE if highlight and i in highlight else "white")
            ax.add_patch(Rectangle((x0 + j * w, y - h), w, h, fc=fc, ec=GREY, lw=1))
            txt = cells[i][j]
            weight = "bold" if i == 0 or (bold_first_col and j == 0) else "normal"
            color = INK
            if txt.startswith("!"):
                txt, color, weight = txt[1:], RED, "bold"
            if txt.startswith("~"):
                txt, color = txt[1:], TEAL
            ax.text(x0 + j * w + w / 2, y - h / 2, txt, ha="center", va="center", fontsize=12, color=color, fontweight=weight)


def arrow_cell(ax, cx, cy, zc, r=0.36):
    """One cell's arrow: a circle, the arrow from the centre in the number's direction, length |z| times r."""
    ax.add_patch(plt.Circle((cx, cy), r, fc="white", ec="#dddddd", lw=1))
    L = abs(zc)
    if L < 1e-9:
        ax.plot([cx], [cy], "o", color="#bbbbbb", ms=3); return
    dx, dy = r * 0.95 * zc.real, r * 0.95 * zc.imag
    ax.annotate("", xy=(cx + dx, cy + dy), xytext=(cx, cy),
                arrowprops=dict(arrowstyle="-|>,head_width=0.2,head_length=0.32", color=INK, lw=2.2, mutation_scale=9, shrinkA=0, shrinkB=0))


def ztext(zc):
    re_, im = round(zc.real, 2), round(zc.imag, 2)
    if abs(im) < 0.005: return f"{re_:.2f}".replace("-0.00", "0.00")
    if abs(re_) < 0.005: return f"{im:.2f}i"
    return f"{re_:.2f}{'+' if im > 0 else '-'}{abs(im):.2f}i"


def fig_tables():
    import sys; sys.dont_write_bytecode = True
    from table_logic import Table
    p = Table([1, 0]); p.turn(0, np.pi / 6)                              # P after one tick at a 30-degree dial
    t = Table.meet(p, Table([1, 0]))                                     # P met the fresh detector M
    w = h = 0.95
    fig, ax = plt.subplots(figsize=(10.5, 4.6), facecolor="white"); ax.axis("off")
    ax.set_xlim(-0.4, 10.4); ax.set_ylim(-3.75, 1.45)
    # one thread: one axis, two cells, standing (P's axis runs down, everywhere)
    x0, y0 = 1.3, 0.1
    ax.text(x0 + w / 2 + 0.6, 1.15, "one thread: one axis, two cells", ha="center", fontsize=12, color=INK)
    ax.annotate("", xy=(x0 - 0.85, y0 - 2 * h - 0.1), xytext=(x0 - 0.85, y0 + 0.1), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.6, mutation_scale=12))
    ax.text(x0 - 0.95, y0 - h, "P's axis", rotation=90, ha="right", va="center", fontsize=10, color=ORANGE)
    for i, zc in enumerate(p.arrows):
        ax.add_patch(Rectangle((x0, y0 - (i + 1) * h), w, h, fc="white", ec=GREY, lw=1))
        ax.text(x0 - 0.12, y0 - i * h - h / 2, f"P = {i}", ha="right", va="center", fontsize=10.5, color=INK, fontweight="bold")
        arrow_cell(ax, x0 + w / 2, y0 - i * h - h / 2 + 0.08, zc)
        ax.text(x0 + w / 2, y0 - (i + 1) * h + 0.1, ztext(zc), ha="center", va="bottom", fontsize=9.5, color=INK)
    ax.text(x0 + w / 2, y0 - 2 * h - 0.3, "P after one tick\nat a 30° dial", ha="center", va="top", fontsize=9.5, color=GREY)
    # an arrow can point anywhere
    xe = 3.4
    ax.add_patch(Rectangle((xe, y0 - h), w, h, fc="white", ec="#cccccc", lw=1, ls="--"))
    arrow_cell(ax, xe + w / 2, y0 - h / 2 + 0.08, 0.3 + 0.4j)
    ax.text(xe + w / 2, y0 - h + 0.1, ztext(0.3 + 0.4j), ha="center", va="bottom", fontsize=9.5, color=INK)
    ax.text(xe + w / 2, y0 - h - 0.3, "an arrow can point anywhere:\nthis one has length 0.50 at 53°.\nin this episode every arrow\npoints along one of two directions",
            ha="center", va="top", fontsize=8.8, color=GREY)
    # two threads that met: P's axis down the rows, M's axis across the columns
    x1, y1 = 7.0, 0.1
    ax.text(x1 + w, 1.15, "two threads that met: two axes, four cells", ha="center", fontsize=12, color=INK)
    ax.annotate("", xy=(x1 + 2 * w + 0.1, y1 + 0.62), xytext=(x1 - 0.1, y1 + 0.62), arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.6, mutation_scale=12))
    ax.text(x1 + w, y1 + 0.7, "M's axis", ha="center", va="bottom", fontsize=10, color=TEAL)
    ax.annotate("", xy=(x1 - 0.85, y1 - 2 * h - 0.1), xytext=(x1 - 0.85, y1 + 0.1), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.6, mutation_scale=12))
    ax.text(x1 - 0.95, y1 - h, "P's axis", rotation=90, ha="right", va="center", fontsize=10, color=ORANGE)
    for j in range(2):
        ax.text(x1 + j * w + w / 2, y1 + 0.16, f"M = {j}", ha="center", fontsize=10.5, color=INK, fontweight="bold")
    for i in range(2):
        ax.text(x1 - 0.12, y1 - i * h - h / 2, f"P = {i}", ha="right", va="center", fontsize=10.5, color=INK, fontweight="bold")
        for j in range(2):
            zc = t.arrows[i, j]
            ax.add_patch(Rectangle((x1 + j * w, y1 - (i + 1) * h), w, h, fc="white", ec=GREY, lw=1))
            arrow_cell(ax, x1 + j * w + w / 2, y1 - i * h - h / 2 + 0.08, zc)
            ax.text(x1 + j * w + w / 2, y1 - (i + 1) * h + 0.1, ztext(zc), ha="center", va="bottom", fontsize=9.5, color=INK)
    ax.text(x1 + w, y1 - 2 * h - 0.3, "P after it met the detector M:\none cell per combination, and\nP = 1, M = 1 is the cell holding 0.50i", ha="center", va="top", fontsize=9.5, color=GREY)
    ax.text(5.0, -3.6, "each cell holds one arrow: a complex number, drawn as a length and a direction; 0.87 points right, 0.50i points up",
            fontsize=10.5, color=GREY, ha="center")
    fig.savefig(os.path.join(OUT, "tbl_tables.png"), dpi=170, bbox_inches="tight", facecolor="white"); plt.close(fig)


def fig_four_cases():
    c, s = np.cos(np.pi / 6), np.sin(np.pi / 6)
    p0, p1 = c / (c + s), s / (c + s)
    fig, ax = plt.subplots(figsize=(11, 4.4), facecolor="white"); ax.axis("off")
    ax.set_xlim(-0.2, 11.2); ax.set_ylim(-4.6, 1.3)
    ax.text(5.4, 1.0, f"one tick of the settlement: lengths 0.87 and 0.50, shares {p0:.2f} and {p1:.2f}",
            ha="center", fontsize=12, color=INK)
    cells = [["P's book signs", "M's book signs", "chance", "result"],
             ["P = 0, M = 0", "P = 0, M = 0", f"{p0:.2f} × {p0:.2f} = {p0*p0:.2f}", "~a fact"],
             ["P = 0, M = 0", "P = 1, M = 1", f"{p0:.2f} × {p1:.2f} = {p0*p1:.2f}", "refusal"],
             ["P = 1, M = 1", "P = 0, M = 0", f"{p1:.2f} × {p0:.2f} = {p1*p0:.2f}", "refusal"],
             ["P = 1, M = 1", "P = 1, M = 1", f"{p1:.2f} × {p1:.2f} = {p1*p1:.2f}", "~a fact"]]
    grid(ax, 5, 4, cells, x0=0, y0=0.5, w=2.7, h=0.72, highlight={1, 4})
    ax.text(5.4, -3.55, f"facts on {p0*p0 + p1*p1:.0%} of ticks; the two facts stand as {p0*p0:.2f} : {p1*p1:.2f} = 0.75 : 0.25",
            ha="center", fontsize=12, color=INK)
    ax.text(5.4, -4.15, "the quantum key for a 30° turn: cos² 30° = 0.75", ha="center", fontsize=12, color=RED, fontweight="bold")
    fig.savefig(os.path.join(OUT, "tbl_four_cases.png"), dpi=170, bbox_inches="tight", facecolor="white"); plt.close(fig)


def fig_ladder():
    fig, ax = plt.subplots(figsize=(9, 3.4), facecolor="white"); ax.axis("off")
    ax.set_xlim(-0.2, 8.6); ax.set_ylim(-3.4, 1.0)
    ax.text(4.1, 0.7, "the ladder: 13 dial angles, 3,000 settlements each, counted against cos²", ha="center", fontsize=12, color=INK)
    cells = [["books", "rms distance from cos²", "mean ticks to a fact"],
             ["1", "0.102", "1.00"], ["2", "!0.008", "1.57"], ["3", "0.057", "2.50"]]
    grid(ax, 4, 3, cells, x0=0, y0=0.3, w=2.75, h=0.7, highlight={2})
    ax.set_xlim(-0.2, 8.6)
    ax.text(4.1, -2.95, "exact loop odds of reading 0 at 30°: one book 0.634, two books 0.750, three books 0.839; key 0.750",
            ha="center", fontsize=11, color=GREY)
    fig.savefig(os.path.join(OUT, "tbl_ladder.png"), dpi=170, bbox_inches="tight", facecolor="white"); plt.close(fig)


fig_tables(); fig_four_cases(); fig_ladder()
print("ok")
