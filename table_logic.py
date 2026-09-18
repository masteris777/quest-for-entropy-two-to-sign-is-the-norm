"""Two Books, One Fact - the table logic, as small as it goes (terms per ../terminology.md).

The TABLE is the state: one axis per thread, two candidates per axis, one ARROW per cell.
  turn(axis, theta)   - a thread's move at a tick: every pair of cells along its axis is rotated
  meet(a, b)          - two threads start sharing one table: the product, then one swap
  settle(p, m)        - the double entry: each of the two books signs for a LINE of the pair
                        (P = p and M = m), in proportion to the line's length, from its own unitdraw;
                        the same line twice is a FACT (posted, table narrowed); different lines are
                        a REFUSAL (nothing posted, sign again at the next tick)
No dice: a unitdraw is the hash of the thread's previous unitdraw (the first hashes its name).

Four exams, four table sizes:
  1 axis : the Born ladder     - only two books land on cos^2; one gives lengths, three give cubes
  2 axes : the Bell exam       - the table after a meeting reaches 2*sqrt(2); a product table cannot pass 2
  3 axes : no-signalling       - a detector meeting P leaves B's odds untouched, B's correlations not
  N axes : the chain           - many entangled threads settle one pair at a time and the joint line lands
                                 on |arrow|^2 for any N and any order; one fact signed by three books does not
Run:  python table_logic.py   (numpy only)
"""
import hashlib
from collections import defaultdict

import numpy as np

# ---------------------------------------------------------------- unitdraws (one per record, a hash chain)
_ticks = defaultdict(int)
_last = {}


def unitdraw(thread: str) -> float:
    """The number carried by a thread's next record: the hash of its previous unitdraw.
    The first record hashes the thread's name, so every book is a hash chain of its own."""
    _ticks[thread] += 1
    prev = _last.get(thread) or hashlib.sha256(thread.encode()).digest()
    h = hashlib.sha256(prev).digest()
    _last[thread] = h
    return int.from_bytes(h[:8], "big") / 2**64


def reset() -> None:
    """Forget every book (fresh threads, fresh chains)."""
    _ticks.clear(); _last.clear()


# ---------------------------------------------------------------- the table
def turn_rule(theta: float) -> np.ndarray:
    """The turn: new z0 = cos t * z0 + i sin t * z1 ; new z1 = i sin t * z0 + cos t * z1."""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, 1j * s], [1j * s, c]])


class Table:
    """arrows[c1, c2, ..., cn] is the arrow of the cell with candidates (c1..cn), one per axis."""

    def __init__(self, arrows):
        self.arrows = np.asarray(arrows, dtype=complex)

    @property
    def axes(self) -> int:
        return self.arrows.ndim

    # -- turn: one thread rotates every pair of cells along ITS axis ------------------------
    def turn(self, axis: int, theta: float) -> None:
        self.arrows = np.moveaxis(np.tensordot(turn_rule(theta), np.moveaxis(self.arrows, axis, 0), axes=(1, 0)), 0, axis)

    # -- the meeting: product of two tables, then one swap ----------------------------------
    @staticmethod
    def meet(a: "Table", b: "Table", swap: bool = True) -> "Table":
        joint = Table(np.multiply.outer(a.arrows, b.arrows))          # product: not entangled yet
        if swap:                                                       # the swap: where a's last axis reads 1,
            ia = a.axes - 1                                            # b's first axis trades its two cells
            sl1 = [slice(None)] * joint.axes; sl1[ia] = 1
            joint.arrows[tuple(sl1)] = np.flip(joint.arrows[tuple(sl1)], axis=ia)
        return joint

    # -- a quarter turn of the phase on candidate 1 (the Bell settings need it; not a term) ---
    def shift(self, axis: int, quarter_turns: int = 1) -> None:
        sl = [slice(None)] * self.axes; sl[axis] = 1
        self.arrows[tuple(sl)] *= 1j ** quarter_turns

    # -- lengths of the slices with the given axes fixed -----------------------------------
    def lengths(self, axes) -> np.ndarray:
        axes = tuple(axes)
        other = tuple(i for i in range(self.axes) if i not in axes)
        sq = np.sum(np.abs(self.arrows) ** 2, axis=other) if other else np.abs(self.arrows) ** 2
        sq = np.moveaxis(sq, [sorted(axes).index(a) for a in axes], range(len(axes)))
        return np.sqrt(sq / sq.sum())

    def odds(self, axes, books: int = 2) -> np.ndarray:
        """Exact odds of the settlement loop with the given number of books (shares to the power)."""
        L = self.lengths(axes); w = (L / L.sum()) ** books
        return w / w.sum()

    def receipt(self) -> float:
        """Two axes only: |z00 z11 - z01 z10|, zero exactly when the table is not entangled."""
        Z = self.arrows
        return abs(Z[0, 0] * Z[1, 1] - Z[0, 1] * Z[1, 0])

    # -- settle: DOUBLE ENTRY - the only place a fact is written ----------------------------
    def settle(self, p: int, m: int = None, books: int = 2):
        """Two books sign for a line of the pair (p, m); the same line twice is a fact.
        m = None: the counterparty is off the table (its book signs, its axis is not drawn)."""
        axes = (p,) if m is None else (p, m)
        L = self.lengths(axes).ravel()
        cum = np.cumsum(L / L.sum())                                   # the lengths laid end to end
        names = [f"axis{p}", "counterparty" if m is None else f"axis{m}"] + [f"book{k}" for k in range(2, books)]
        ticks = 0
        while True:
            ticks += 1
            signatures = [int(np.searchsorted(cum, unitdraw(n))) for n in names[:books]]
            if len(set(signatures)) == 1:                              # the same line in every book: a fact
                break                                                  # otherwise a refusal: sign again
        line = np.unravel_index(signatures[0], (2,) * len(axes))
        mask = np.zeros(self.arrows.shape, dtype=bool)                 # narrowing: only the posted line stays
        sl = [slice(None)] * self.axes
        for ax, c in zip(axes, line):
            sl[ax] = c
        mask[tuple(sl)] = True
        self.arrows[~mask] = 0
        return line if m is not None else line[0], ticks


# ---------------------------------------------------------------- exam 1: one axis, the Born ladder
def exam_born(n_per_angle: int = 3000) -> None:
    print("\nEXAM 1 - one axis. Counted frequency of candidate 0 vs the answer key cos^2(t)")
    print("  books:        1        2        3      (rms deviation from cos^2 over 13 angles)")
    devs = {k: [] for k in (1, 2, 3)}; waits = {k: [] for k in (1, 2, 3)}
    for t in np.linspace(0, np.pi / 2, 13):
        key = np.cos(t) ** 2
        for k in (1, 2, 3):
            hits = 0
            for _ in range(n_per_angle):
                tb = Table([1, 0]); tb.turn(0, t)                    # a fresh table, turned by the dial
                c, ticks = tb.settle(0, None, books=k); hits += c == 0; waits[k].append(ticks)
            devs[k].append(hits / n_per_angle - key)
    print("  rms:        " + "  ".join(f"{np.sqrt(np.mean(np.square(devs[k]))):.3f}   " for k in (1, 2, 3)))
    print("  mean ticks: " + "  ".join(f"{np.mean(waits[k]):.2f}    " for k in (1, 2, 3)))
    t30 = Table([np.cos(np.pi / 6), 1j * np.sin(np.pi / 6)])
    print("  exact loop odds at 30 deg (answer key 0.750): " + ", ".join(
        f"{k} book(s) -> {t30.odds((0,), k)[0]:.3f}" for k in (1, 2, 3)))


# ---------------------------------------------------------------- exam 2: two axes, the Bell exam
def correlation(table: Table, ta: float, tb: float) -> float:
    """E(ta, tb): each thread sets its own dial (one quarter turn of the phase, then its turn); exact odds."""
    t = Table(table.arrows.copy()); t.shift(0, 1); t.turn(0, ta); t.turn(1, tb)
    p = np.abs(t.arrows) ** 2; p /= p.sum()
    return p[0, 0] + p[1, 1] - p[0, 1] - p[1, 0]


def exam_bell() -> None:
    print("\nEXAM 2 - two axes. CHSH S = |E(a,b) - E(a,b') + E(a',b) + E(a',b')| (exact odds)")
    a = Table([1, 0]); a.turn(0, np.pi / 4)
    b = Table([1, 0])
    met = Table.meet(a, b, swap=True)                                # the meeting
    a2 = Table([1, 0]); a2.turn(0, np.pi / 8)                       # a control: two turned threads, product only
    b2 = Table([1, 0]); b2.turn(0, np.pi / 6)
    product = Table.meet(a2, b2, swap=False)
    for joint, label in ((product, "product table (no swap) "), (met, "table after the meeting")):
        best = 0.0
        for off in np.linspace(0, np.pi, 181):
            A, Ap, B, Bp = off, off + np.pi / 4, off + np.pi / 8, off + 3 * np.pi / 8
            S = abs(correlation(joint, A, B) - correlation(joint, A, Bp) + correlation(joint, Ap, B) + correlation(joint, Ap, Bp))
            best = max(best, S)
        print(f"  {label}: max S = {best:.4f}   receipt = {joint.receipt():.3f}   (classical bound 2, quantum 2*sqrt2 = 2.8284)")


# ---------------------------------------------------------------- exam 3: three axes, no-signalling
def exam_no_signalling(n: int = 4000) -> None:
    print("\nEXAM 3 - three axes. B's odds before and after a detector M meets P; the pair (P, M) settles")
    a = Table([1, 0]); a.turn(0, np.pi / 4)
    b = Table([1, 0])
    ab = Table.meet(a, b)                                            # the pair, axes (P, B)
    m = Table([1, 0])
    # meet() swaps on the LAST axis of the first table; to let M meet P, put P last, then restore the order
    abm = Table(np.moveaxis(Table.meet(Table(np.moveaxis(ab.arrows, 0, 1)), m).arrows, 1, 0))  # axes (P, B, M)
    for tb in (0.0, np.pi / 8, np.pi / 4):
        t2 = Table(ab.arrows.copy()); t2.turn(1, tb)
        t3 = Table(abm.arrows.copy()); t3.turn(1, tb)
        print(f"  B turned by {np.degrees(tb):5.1f} deg: odds(B=0) pair only = {t2.odds((1,))[0]:.4f}, "
              f"after M met P = {t3.odds((1,))[0]:.4f}")
    counts = np.zeros((2, 2))
    for _ in range(n):
        t = Table(abm.arrows.copy()); line, _ = t.settle(0, 2); counts[line] += 1
    print("  counted facts of the pair (P, M), lines 00 01 10 11:", np.round(counts.ravel() / n, 3),
          " key:", np.round((abm.lengths((0, 2)) ** 2).ravel(), 3))
    p = np.abs(abm.arrows) ** 2; p /= p.sum()
    E_ab = sum(p[i, j, k] * (1 - 2 * i) * (1 - 2 * j) for i in range(2) for j in range(2) for k in range(2))
    E_bm = sum(p[i, j, k] * (1 - 2 * j) * (1 - 2 * k) for i in range(2) for j in range(2) for k in range(2))
    print(f"  correlations in the 3-axis table: E(P,B) = {E_ab:+.3f}, E(B,M) = {E_bm:+.3f}")
    print("  B's odds did not move; whom B agrees with did.")


# ---------------------------------------------------------------- exam 4: many axes, the chain
def exam_chain(n: int = 6000) -> None:
    """Many threads share one table. The toy settles it one pairwise fact at a time (each thread with
    its own counterparty, two books per fact) and the joint line is counted against |arrow|^2.
    The signer count per fact stays two however many threads are on the table."""
    print("\nEXAM 4 - many axes. Threads settle one pair at a time; the joint line counted against |arrow|^2")
    rng = np.random.default_rng(7)

    def ghz(k):
        z = np.zeros((2,) * k, complex); z[(0,) * k] = z[(1,) * k] = 1; return z / np.sqrt(2)

    def w(k):
        z = np.zeros((2,) * k, complex)
        for i in range(k):
            idx = [0] * k; idx[i] = 1; z[tuple(idx)] = 1
        return z / np.sqrt(k)

    def rand(k):
        z = rng.normal(size=(2,) * k) + 1j * rng.normal(size=(2,) * k); return z / np.linalg.norm(z)

    def chain(z, order):
        counts = np.zeros(z.shape); ticks = []
        for _ in range(n):
            t = Table(z.copy()); line = [0] * z.ndim
            for p in order:
                line[p], tk = t.settle(p, None); ticks.append(tk)
            counts[tuple(line)] += 1
        return counts / n, np.mean(ticks)

    tables = [("GHZ", ghz(3)), ("W", w(3)), ("random", rand(3)), ("GHZ", ghz(4)), ("random", rand(4)), ("random", rand(5))]
    for label, z in tables:
        freq, mean_ticks = chain(z, range(z.ndim))
        print(f"  {label:6} {z.ndim} threads: rms from the key {np.sqrt(np.mean((freq - np.abs(z) ** 2) ** 2)):.4f}, "
              f"mean ticks per fact {mean_ticks:.2f}")
    z = tables[2][1]
    rev, _ = chain(z, range(2, -1, -1))
    print(f"  random 3 threads settled in the opposite order: rms from the key {np.sqrt(np.mean((rev - np.abs(z) ** 2) ** 2)):.4f}")
    key = (np.abs(z) ** 2).ravel()
    print("  one fact on all three threads at once, signed by k books (exact odds), rms from the key: " + ", ".join(
        f"{k} -> {np.sqrt(np.mean((Table(z.copy()).odds((0, 1, 2), k).ravel() - key) ** 2)):.3f}" for k in (1, 2, 3, 4)))
    t30 = Table([np.cos(np.pi / 6), 1j * np.sin(np.pi / 6)])
    print("  the whole ladder, exact odds of 0 at 30 deg (key 0.750): " + ", ".join(
        f"{k} -> {t30.odds((0,), k)[0]:.3f}" for k in range(1, 9)))
    print("  more threads add links to the chain, never signatures to a fact.")


if __name__ == "__main__":
    exam_born()
    exam_bell()
    exam_no_signalling()
    exam_chain()
