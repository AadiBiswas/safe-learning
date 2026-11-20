"""Finite safe-identification game, solved by brute force, against the trap characterization.

Parameters are points on a line (diam = max - min), actions are indices, observations
are h(theta, u) + [-delta, delta], and safe[theta][u] says whether u is safe for theta.
The agent may only play actions safe for every parameter still consistent.

    .venv/bin/python scripts/finite_game.py   ->  results/finite_game.txt
"""

import itertools
import random
import sys
from functools import lru_cache
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "results" / "finite_game.txt"
SEED = 20261120


class Game:
    def __init__(self, points, h, safe, delta, eps):
        self.points, self.h, self.safe, self.delta, self.eps = points, h, safe, delta, eps
        self.n, self.m = len(points), len(h[0])
        self.win = lru_cache(maxsize=None)(self._win)

    def members(self, K):
        return [i for i in range(self.n) if K >> i & 1]

    def diam(self, K):
        vals = [self.points[i] for i in self.members(K)]
        return max(vals) - min(vals) if vals else 0.0

    def safe_actions(self, K):
        idx = self.members(K)
        return [u for u in range(self.m) if all(self.safe[i][u] for i in idx)]

    def responses(self, K, u):
        """Every nonempty consistent subset the adversary can produce with one observation."""
        idx = self.members(K)
        hs = sorted({self.h[i][u] for i in idx})
        cands = {v + s * self.delta for v in hs for s in (-1, 1)}
        cs = sorted(cands)
        cands |= {(a + b) / 2 for a, b in zip(cs, cs[1:])}
        out = set()
        for y in cands:
            K2 = sum(1 << i for i in idx if abs(y - self.h[i][u]) <= self.delta + 1e-12)
            if K2:
                out.add(K2)
        return out

    def _win(self, K):
        """Least number of experiments that guarantees diam <= eps from K, or None."""
        if self.diam(K) <= self.eps:
            return 0
        best = None
        for u in self.safe_actions(K):
            worst = 0
            for K2 in self.responses(K, u):
                r = None if K2 == K else self.win(K2)
                if r is None:
                    worst = None
                    break
                worst = max(worst, r)
            if worst is not None and (best is None or worst + 1 < best):
                best = worst + 1
        return best

    def self_preserving(self, K):
        """Every action safe for all of K has an observation compatible with all of K."""
        idx = self.members(K)
        for u in self.safe_actions(K):
            hv = [self.h[i][u] for i in idx]
            if max(hv) - min(hv) > 2 * self.delta + 1e-12:  # 1D intervals: Helly makes this pairwise
                return False
        return True

    def traps(self, K0):
        return [K for K in range(1, K0 + 1) if K & K0 == K and self.diam(K) > self.eps and self.self_preserving(K)]


def random_game(rng):
    n, m = rng.randint(2, 7), rng.randint(1, 5)
    points = sorted(rng.sample(range(20), n))
    h = [[rng.randint(0, 6) for _ in range(m)] for _ in range(n)]
    psafe = rng.choice([0.4, 0.6, 0.8, 1.0])
    safe = [[rng.random() < psafe for _ in range(m)] for _ in range(n)]
    delta = rng.choice([0.0, 0.5, 1.0, 1.5])
    eps = rng.choice([0, 0, 3, 6])
    return Game(points, h, safe, delta, eps)


def minimal_traps(g, K0):
    T = set(g.traps(K0))
    return [K for K in T if not any(K2 != K and K2 & K == K2 for K2 in T)]


def nonlocal_example(n):
    """Action a_k is safe for every parameter except k and separates everything.
    Theta is a trap; every proper subset is identified by one experiment."""
    points = list(range(n))
    h = [[float(i) for _ in range(n)] for i in range(n)]
    safe = [[i != k for k in range(n)] for i in range(n)]
    return Game(points, h, safe, delta=0.25, eps=0)


def sat_game(nvars, clauses):
    """3-SAT -> trap existence. Parameters T_i = 2i, F_i = 2i + 1. A trap is exactly
    the set of true literals of a satisfying assignment (research/finite_analysis.md, Prop. F4)."""
    n = 2 * nvars
    lit = lambda v: 2 * (abs(v) - 1) + (0 if v > 0 else 1)  # noqa: E731
    h, safe = [[] for _ in range(n)], [[] for _ in range(n)]

    def action(unsafe_for, values):
        for i in range(n):
            safe[i].append(i not in unsafe_for)
            h[i].append(values(i))

    spread = lambda i: 10.0 * i  # noqa: E731  -- separates any two parameters
    for v in range(nvars):
        T, F = 2 * v, 2 * v + 1
        # b_v: always safe, separates only T from F (gaps of 1 vs 2 delta = 1.2)
        action(set(), lambda i, T=T, F=F: 1.0 if i == T else -1.0 if i == F else 0.0)
        # a_v: blocked iff K meets {T, F}; otherwise separates everything
        action({T, F}, spread)
    for c in clauses:
        action({lit(v) for v in c}, spread)
    return Game(list(range(n)), h, safe, delta=0.6, eps=0)


def satisfiable(nvars, clauses):
    return any(all(any((v > 0) == bits[abs(v) - 1] for v in c) for c in clauses)
               for bits in itertools.product([False, True], repeat=nvars))


def main():
    rng = random.Random(SEED)
    lines = []
    agree = total = 0
    max_ratio = 0.0
    sizes = {}
    pair_ok_but_stuck = 0
    for _ in range(3000):
        g = random_game(rng)
        K0 = (1 << g.n) - 1
        w = g.win(K0)
        has_trap = bool(g.traps(K0))
        total += 1
        agree += (w is None) == has_trap
        if w is not None and g.n > 1:
            max_ratio = max(max_ratio, w / (g.n - 1))
        if has_trap:
            for K in minimal_traps(g, K0):
                s = bin(K).count("1")
                sizes[s] = sizes.get(s, 0) + 1
            # identifiable pairs: every far-apart pair can be resolved on its own
            pairs = [(1 << i) | (1 << j) for i, j in itertools.combinations(range(g.n), 2)]
            if all(g.win(P) is not None for P in pairs):
                pair_ok_but_stuck += 1
    lines.append(f"random instances: {total}; game value agrees with 'no trap of diameter > eps': {agree}/{total}")
    lines.append(f"max (experiments used by an optimal strategy) / (|Theta| - 1): {max_ratio:.3f}  (bound: 1)")
    lines.append(f"minimal trap sizes among non-identifiable instances: {dict(sorted(sizes.items()))}")
    lines.append(f"non-identifiable although every pair is identifiable on its own: {pair_ok_but_stuck}")
    for n in (3, 4, 5, 6, 7):
        g = nonlocal_example(n)
        K0 = (1 << n) - 1
        proper = [K for K in range(1, K0) if bin(K).count("1") >= 2]
        lines.append(
            f"non-local example n={n}: Theta identifiable: {g.win(K0) is not None}; "
            f"proper subsets identifiable: {sum(g.win(K) is not None for K in proper)}/{len(proper)}, "
            f"max experiments {max(g.win(K) for K in proper)}; minimal traps {[bin(K).count('1') for K in minimal_traps(g, K0)]}"
        )
    sat_agree = sat_total = sat_yes = 0
    for _ in range(400):
        nv = rng.randint(2, 5)
        cl = [tuple(rng.choice([-1, 1]) * v for v in rng.sample(range(1, nv + 1), min(3, nv)))
              for _ in range(rng.randint(1, 4 * nv) if rng.random() < 0.5 else rng.randint(5 * nv, 10 * nv))]
        g = sat_game(nv, cl)
        K0 = (1 << g.n) - 1
        s = satisfiable(nv, cl)
        traps = g.traps(K0)
        sat_total += 1
        sat_yes += s
        sat_agree += (s == bool(traps)) and (s == (g.win(K0) is None))
    lines.append(f"3-SAT reduction: {sat_agree}/{sat_total} agree (satisfiable <=> trap <=> not identifiable); "
                 f"{sat_yes} satisfiable")
    text = "\n".join(lines) + "\n"
    print(text, end="")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(text)
    return 0 if agree == total and sat_agree == sat_total else 1


if __name__ == "__main__":
    sys.exit(main())
