"""The settlement, tick by tick, on the table of tbl_worked.png (P ticked once at a 30-degree dial and met the
fresh detector M): each book lays the four line lengths end to end on its own ruler, its unitdraw is a needle,
and it signs for the line the needle falls in; the same line in both books is a fact, otherwise a refusal.
Two lines are lit (0.87 and 0.50) and two are empty, so the ruler has two segments.
Unitdraws are the toy's own (table_logic.unitdraw, threads "P" and "M", ticks 1..). Output: ../assets/tbl_signing.png
"""
import os
import sys

sys.dont_write_bytecode = True
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

from table_logic import Table, unitdraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
INK, GREY, ORANGE, TEAL, RED, PALE = "#222", "#9a9a9a", "#c8781a", "#1a8a7a", "#c0392b", "#f6f1e7"
SEG = ["#e9d7b8", "#f3e6d0", "#d5e8e4", "#e8f2ef"]
NAMES = ["P = 0, M = 0", "P = 0, M = 1", "P = 1, M = 0", "P = 1, M = 1"]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})

p = Table([1, 0]); p.turn(0, np.pi / 6)
t = Table.meet(p, Table([1, 0]))
L = t.lengths((0, 1)).ravel(); share = L / L.sum(); cum = np.cumsum(share)
ticks = []
while True:
    rp, rm = unitdraw("P"), unitdraw("M")
    sp, sm = int(np.searchsorted(cum, rp)), int(np.searchsorted(cum, rm))
    ticks.append((rp, sp, rm, sm))
    if sp == sm:
        break

RW = 6.0                                                        # ruler width in axis units
fig, ax = plt.subplots(figsize=(11, 2.2 + 1.4 * len(ticks)), facecolor="white"); ax.axis("off")
ax.set_xlim(-2.0, 10.6); ax.set_ylim(-1.4 * len(ticks) - 0.6, 2.1)
ax.text(RW / 2, 1.9, "the settlement: two books, one ruler each, the lengths of the four lines laid end to end",
        ha="center", fontsize=12, color=INK)
ax.text(RW / 2, 1.4, "lengths 0.87, 0.00, 0.00, 0.50  give shares  "
        + ", ".join(f"{s:.2f}" for s in share) + "  (each length divided by their sum); the two empty lines get no room",
        ha="center", fontsize=10, color=GREY)
# the ruler's legend: one bar with the lit lines' names
x = 0.0
for k in range(4):
    w = share[k] * RW
    if w > 0:
        ax.add_patch(Rectangle((x, 0.45), w, 0.32, fc=SEG[k], ec=GREY, lw=0.8))
        ax.text(x + w / 2, 0.61, NAMES[k], ha="center", va="center", fontsize=8.5, color=INK)
    x += w
ax.text(-0.15, 0.61, "the lit lines", ha="right", va="center", fontsize=9.5, color=GREY)
ax.text(0, 0.3, "0", ha="center", va="top", fontsize=8.5, color=GREY); ax.text(RW, 0.3, "1", ha="center", va="top", fontsize=8.5, color=GREY)


def ruler(y, r, s, who, color):
    x = 0.0
    for k in range(4):
        w = share[k] * RW
        if w > 0:
            ax.add_patch(Rectangle((x, y - 0.16), w, 0.32, fc=SEG[k] if k != s else color, ec=GREY, lw=0.8, alpha=1 if k != s else 0.55))
        x += w
    ax.plot([r * RW, r * RW], [y - 0.32, y + 0.32], color=INK, lw=2)                    # the needle: the unitdraw
    above = who == "P"                                                                  # P's unitdraw above its ruler, M's below
    ha = "right" if r > 0.95 else ("left" if r < 0.05 else "center")                    # keep the label on the ruler
    ax.text(r * RW, y + 0.34 if above else y - 0.34, f"{r:.2f}", ha=ha, va="bottom" if above else "top", fontsize=8.5, color=INK)
    ax.text(-0.15, y, f"{who}'s book", ha="right", va="center", fontsize=9.5, color=color, fontweight="bold")
    ax.text(RW + 0.15, y, f"signs {NAMES[s]}", ha="left", va="center", fontsize=9.5, color=INK)


for n, (rp, sp, rm, sm) in enumerate(ticks):
    y0 = -0.35 - 1.4 * n
    fact = sp == sm
    ax.text(-1.95, y0 - 0.3, f"tick {n + 1}", ha="left", va="center", fontsize=10.5, color=INK, fontweight="bold")
    ruler(y0, rp, sp, "P", ORANGE)
    ruler(y0 - 0.6, rm, sm, "M", TEAL)
    verdict = "a fact: posted in both books" if fact else "a refusal: nothing posted, sign again"
    ax.text(RW + 0.15, y0 - 0.98, verdict, ha="left", va="center", fontsize=9.5, color=RED if fact else GREY, fontweight="bold" if fact else "normal")
    if fact:
        ax.add_patch(Rectangle((-2.0, y0 - 1.15), 12.5, 1.5, fc="none", ec=RED, lw=1.2))

path = os.path.join(OUT, "tbl_signing.png")
fig.savefig(path, dpi=170, bbox_inches="tight", facecolor="white"); plt.close(fig)
print("saved", path, "ticks", len(ticks), "fact", NAMES[ticks[-1][1]])
