"""Three particles, three rules for who signs. P is turned 30 deg and entangled with a partner B;
then a detector M meets P. All three threads have books and unitdraws. The rules that could be written:
one decides alone, the two that met agree, all three agree. Only the middle one is the quantum answer.
Every number is computed from the toy. Output: ../assets/tbl_who_signs.png
"""
import os
import sys

sys.dont_write_bytecode = True
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Rectangle

from table_logic import Table

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
INK, GREY, ORANGE, TEAL, RED, BLUE = "#222", "#9a9a9a", "#c8781a", "#1a8a7a", "#c0392b", "#3b6ea5"
SEG = ["#e9d7b8", "#d5e8e4"]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})

# ---- the toy: P turned 30 deg, P meets B, then M meets P ------------------------------------
p = Table([1, 0]); p.turn(0, np.pi / 6)
pb = Table.meet(p, Table([1, 0]))                                           # axes (P, B)
pbm = Table(np.moveaxis(Table.meet(Table(np.moveaxis(pb.arrows, 0, 1)), Table([1, 0])).arrows, 1, 0))

L_pair = pbm.lengths((0, 2)).ravel()                                        # the pair (P, M)
key = (L_pair ** 2)[0]                                                      # quantum odds of "both read 0"
share = (L_pair / L_pair.sum())[0]

L_tri = pbm.lengths((0, 1, 2)).ravel()
def odds_first(L, k):
    s = L / L.sum(); w = s ** k
    return (w / w.sum())[0]

RULES = [
    ("one decides alone",      ["P"],           odds_first(L_pair, 1), 1),
    ("the two that met agree", ["P", "M"],      odds_first(L_pair, 2), 2),
    ("all three agree",        ["P", "M", "B"], odds_first(L_tri, 3),  3),
]
COL = {"P": ORANGE, "M": TEAL, "B": BLUE}

fig, ax = plt.subplots(figsize=(11.2, 5.9), facecolor="white"); ax.axis("off")
ax.set_xlim(0, 11.2); ax.set_ylim(0, 5.9)

ax.text(0.15, 5.60, "three particles, three rules for who signs", fontsize=13.5, color=INK)
ax.text(0.15, 5.22, "P was turned 30° and entangled with a partner B; then the detector M met P. "
        "All three threads have books, all three have unitdraws.", fontsize=10, color=GREY)

# ---- the shared ruler, drawn once ------------------------------------------------------------
RX, RW, RY = 0.15, 4.5, 4.55
for k, (w, lab) in enumerate([(share, "P = 0 and M = 0"), (1 - share, "P = 1 and M = 1")]):
    x = RX + (0 if k == 0 else share * RW)
    ax.add_patch(Rectangle((x, RY), w * RW, 0.34, fc=SEG[k], ec=GREY, lw=0.8))
    ax.text(x + w * RW / 2, RY + 0.17, lab, ha="center", va="center", fontsize=8.5, color=INK)
    ax.text(x + w * RW / 2, RY - 0.14, f"{w:.2f}", ha="center", va="top", fontsize=8.5, color=GREY)
ax.text(RX, RY + 0.46, "the ruler every book uses: the lines' lengths, laid end to end",
        fontsize=9.5, color=INK)

# ---- the odds axis on the right ---------------------------------------------------------------
BX, BW = 6.35, 4.3
ax.text(BX, RY + 0.46, "how often \"both read 0\" is posted", fontsize=9.5, color=INK)
ax.plot([BX + key * BW, BX + key * BW], [0.78, RY + 0.34], color=RED, lw=1.4, ls=(0, (4, 3)), zorder=1)
ax.text(BX + key * BW, 0.70, f"the quantum key  {key:.3f}", ha="center", va="top",
        fontsize=9.5, color=RED, fontweight="bold")

for n, (name, books, val, nb) in enumerate(RULES):
    y = 3.75 - 1.12 * n
    hit = abs(val - key) < 1e-9
    ax.text(RX, y + 0.30, name, fontsize=11.5, color=INK, fontweight="bold" if hit else "normal")

    # the needles: one chip per signing book, over a copy of the ruler
    for i, b in enumerate(books):
        cx = RX + 0.22 + i * 0.60
        ax.add_patch(Circle((cx, y - 0.16), 0.17, fc="white", ec=COL[b], lw=1.8))
        ax.text(cx, y - 0.16, b, ha="center", va="center", fontsize=10, color=COL[b], fontweight="bold")
    cap = "1 needle, thrown at the ruler" if nb == 1 else f"{nb} needles, all in the same stretch"
    ax.text(RX + 0.22 + len(books) * 0.60 - 0.18, y - 0.16, cap,
            ha="left", va="center", fontsize=9.5, color=GREY)

    # the counted bar
    ax.add_patch(Rectangle((BX, y - 0.30), BW, 0.28, fc="#f4f4f2", ec=GREY, lw=0.7))
    ax.add_patch(Rectangle((BX, y - 0.30), val * BW, 0.28, fc=RED if hit else "#cfcfcb",
                           ec="none", alpha=0.55 if hit else 1.0))
    ax.text(BX + BW + 0.10, y - 0.16, f"{val:.3f}", ha="left", va="center", fontsize=11,
            color=RED if hit else INK, fontweight="bold" if hit else "normal")
    verdict = "the quantum answer" if hit else ("too flat" if val < key else "too steep")
    ax.text(BX, y - 0.44, verdict, ha="left", va="top", fontsize=9, color=RED if hit else GREY)

ax.text(RX, 0.24, "B is not an invented book: it is genuinely entangled, genuinely present, and has unitdraws of its own. "
        "It still must not sign.", fontsize=10, color=INK)

path = os.path.join(OUT, "tbl_who_signs.png")
fig.savefig(path, dpi=170, bbox_inches="tight", facecolor="white"); plt.close(fig)
print("saved", path)
print("share of the long line", f"{share:.3f}", " key", f"{key:.3f}")
for name, books, val, nb in RULES:
    print(f"  {name:24s} {nb} signer(s) -> {val:.3f}")
