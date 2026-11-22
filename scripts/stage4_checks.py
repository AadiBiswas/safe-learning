"""Stage 4 checks for aligned safety and sensing (ledger E008).

    .venv/bin/python scripts/stage4_checks.py   ->  results/stage4_checks.txt

research/aligned_identifiability.md. Exact arithmetic. Not proofs.
"""

import random
import sys
from fractions import Fraction as Fr
from pathlib import Path

from boolean import find_trap_boolean
from linear import aligned, aligned_2sat_trap, aligned_sat_u2, dot, global_conflicts, to_instance
from traps import satisfiable

OUT = Path(__file__).resolve().parents[1] / "results" / "stage4_checks.txt"
SEED = 20261124
lines, failures = [], []


def log(s=""):
    lines.append(s)
    print(s)


def check(name, ok, detail=""):
    log(f"  [{'ok' if ok else 'FAIL'}] {name}{': ' + detail if detail else ''}")
    if not ok:
        failures.append(name)


def rvec(rng, d, lo=-4, hi=4):
    return tuple(Fr(rng.randint(lo, hi)) for _ in range(d))


def aligned_family_instance(rng, n, m, d):
    """Random aligned experiments whose global conflict graph is empty, complete or one pair,
    with |unsafe set| <= 2 for complete ones (the AL2 family). Returns None if a draw is unusable."""
    pts = [rvec(rng, d) for _ in range(n)]
    if len(set(pts)) < n:
        return None
    exps = []
    for _ in range(m):
        c = rvec(rng, d, -3, 3)
        if not any(c):
            continue
        lam = rng.choice([Fr(1), Fr(2), Fr(-1), Fr(-1, 2)])        # positive and negative alignment
        a = tuple(lam * x for x in c)
        v = sorted({dot(a, p) for p in pts}, reverse=True)
        k = rng.choice([0, 1, 2])                                  # number of distinct top values unsafe
        b = (v[k - 1] + v[k]) / 2 if 0 < k < len(v) else v[0] + 1
        q = [dot(c, p) for p in pts]
        kind = rng.choice(["all", "pair", "blind"])
        if kind == "all":
            gaps = [y - x for x, y in zip(sorted(q), sorted(q)[1:])]
            if min(gaps) == 0:
                continue
            dl = min(gaps) / 3
        elif kind == "pair":
            lo, hi = min(q), max(q)
            if q.count(lo) > 1 or q.count(hi) > 1 or n < 3:
                continue
            others = [x for x in q if x not in (lo, hi)]
            M = max(hi - min(others), max(others) - lo)
            dl = (M + hi - lo) / 4
        else:
            dl = (max(q) - min(q)) / 2 + 1
        e = (a, b, c, dl)
        B = [i for i, p in enumerate(pts) if dot(a, p) > b]
        if kind == "all" and len(B) > 2:
            continue
        exps.append(e)
    return pts, exps


def main():
    rng = random.Random(SEED)

    log("A. Lemma AL1: an aligned lone pair is never disjoint from a nonempty unsafe set")
    ok, seen = True, 0
    for _ in range(400):
        d = rng.choice([1, 2, 3])
        pts = [rvec(rng, d) for _ in range(rng.randint(3, 7))]
        for _ in range(15):
            c = rvec(rng, d, -3, 3)
            if not any(c):
                continue
            lam = rng.choice([Fr(1), Fr(-2), Fr(1, 3)])
            a = tuple(lam * x for x in c)
            q = [dot(c, p) for p in pts]
            for dl in {abs(x - y) / 2 for x in q for y in q}:
                for b in {dot(a, p) for p in pts}:
                    P = global_conflicts(pts, (a, b, c, dl))
                    if len(P) == 1:
                        seen += 1
                        i, j = tuple(next(iter(P)))
                        B = {t for t, p in enumerate(pts) if dot(a, p) > b}
                        ok &= not B or i in B or j in B
    check("lone pair meets every nonempty aligned unsafe set", ok, f"{seen} (experiment, threshold) cases")

    log("\nB. Theorem AL2: the aligned D2 family reduces to 2-SAT (compared with exhaustive search)")
    ag = tot = traps_found = 0
    while tot < 600:
        d = rng.choice([1, 2, 3])
        r = aligned_family_instance(rng, rng.randint(2, 7), rng.randint(1, 8), d)
        if r is None:
            continue
        pts, exps = r
        assert aligned(exps) or not exps
        inst = to_instance(pts, exps)
        got = aligned_2sat_trap(pts, exps)
        tot += 1
        traps_found += got is not None
        ag += (got is None) == (inst.value(inst.full) is not None)
    check("2-SAT decision = exhaustive (exact identification)", ag == tot, f"{ag}/{tot}, {traps_found} with a trap")

    log("\nC. Aligned functionals are still NP-hard in unbounded dimension (aligned sat_u2)")
    cases = [(1, [(1,)]), (1, [(1,), (-1,)]), (2, []), (2, [()]), (2, [(1, 1)]), (2, [(1, -1, 2)]),
             (2, [(1, -2), (-1, 2), (1, 2), (-1, -2)])]
    for _ in range(40):
        nv = rng.randint(1, 3)
        cases.append((nv, [tuple(rng.choice([-1, 1]) * rng.randint(1, nv) for _ in range(rng.randint(1, 3)))
                           for _ in range(rng.randint(1, 5))]))
    ag = sat = 0
    for nv, cl in cases:
        pts, exps = aligned_sat_u2(nv, cl)
        inst = to_instance(pts, exps)
        s = satisfiable(nv, cl)
        sat += s
        ag += aligned(exps) and inst.unsafe_size() <= 2 and s == (find_trap_boolean(inst, pairwise=True) is not None)
    check("every experiment aligned (a = c); |B| <= 2; SAT <=> trap", ag == len(cases),
          f"{ag}/{len(cases)}, {sat} satisfiable")

    log("\nD. W5': sigma on the moment curve in Q^4 equals minimum vertex cover")
    from itertools import combinations
    from traps import safety_witness_number
    ag = tot = 0
    for _ in range(200):
        nv = rng.randint(2, 8)
        E = [e for e in combinations(range(nv), 2) if rng.random() < 0.4]
        pts = [tuple(Fr(t) ** k for k in (1, 2, 3, 4)) for t in range(nv)]
        exps = []
        for i, j in E:
            # -(t-i)^2 (t-j)^2 > -1/2 as a linear functional of (t, t^2, t^3, t^4) plus a constant
            c0, c1, c2, c3 = i * i * j * j, -2 * i * j * (i + j), i * i + j * j + 4 * i * j, -2 * (i + j)
            a = (Fr(-c1), Fr(-c2), Fr(-c3), Fr(-1))
            exps.append((a, Fr(c0) - Fr(1, 2), a, Fr(10 ** 9)))
        inst = to_instance(pts, exps)
        ok = all(inst.actions[u][0] == (1 << i | 1 << j) for u, (i, j) in enumerate(E))
        vc = min((k for k in range(nv + 1) for S in combinations(range(nv), k)
                  if all(i in S or j in S for i, j in E)), default=0)
        tot += 1
        ag += ok and safety_witness_number(inst, inst.full) == vc
    check("every edge is exactly a halfspace trace; sigma = minimum vertex cover", ag == tot, f"{ag}/{tot} graphs")

    text = "\n".join(lines) + "\n"
    OUT.write_text(text)
    log(f"\n{len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
