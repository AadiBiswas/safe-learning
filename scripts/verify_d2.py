"""Standalone exact verifier for the planar reduction D2 (research/planar_hardness_audit.md).

    .venv/bin/python scripts/verify_d2.py   ->  results/verify_d2.txt   (ledger E007)

Independent of the construction's own checks: the intended experiments are re-derived here
from the formula alone (as labelled unsafe sets and separated pairs), and every geometric
quantity is recomputed with local exact arithmetic. The only interface to the builder is
its output (points, experiments) and the label of each point. It does not import
scripts/linear.py or the builder's verify().
"""

import itertools
import random
from collections import Counter
import sys
from fractions import Fraction as Fr
from pathlib import Path

from planar_hardness import build

OUT = Path(__file__).resolve().parents[1] / "results" / "verify_d2.txt"


def ip(a, x):
    return a[0] * x[0] + a[1] * x[1]


def intended(nvars, clauses):
    """Multiset of (unsafe labels, separated-pair labels or 'all') demanded by the proof."""
    want = []
    lit = lambda l: ("T" if l > 0 else "F", abs(l) - 1)  # noqa: E731
    helper = lambda x: ("w" + x[0], x[1]) if x[0] not in ("T", "F") else (("wT" if x[0] == "T" else "wF"), x[1])  # noqa: E731
    for v in range(nvars):
        for x in (("T", v), ("F", v)):
            want.append((frozenset([helper(x)]), "all"))                    # force helper
        want.append((frozenset([("Tp", v)]), frozenset([("T", v), ("wT", v)])))
        want.append((frozenset([("Fp", v)]), frozenset([("F", v), ("wF", v)])))
        want.append((frozenset(), frozenset([("Tp", v), ("Fp", v)])))
    for j, c in enumerate(clauses):
        if not c:
            want.append((frozenset(), "all"))
            continue
        l = list(c) + [c[-1]] * (3 - len(c))
        for nm in ("s", "sp", "k1", "k2", "k3"):
            want.append((frozenset([("w" + nm, j)]), "all"))
        want.append((frozenset([("s", j), ("sp", j)]), "all"))
        want.append((frozenset([("k1", j), ("k2", j)]), frozenset([("sp", j), ("wsp", j)])))
        want.append((frozenset([("k3", j)]), frozenset([("s", j), ("ws", j)])))
        for nm, li in zip(("k1", "k2", "k3"), l):
            want.append((frozenset([lit(li)]), frozenset([(nm, j), ("w" + nm, j)])))
    return Counter(want)


def cyclic_order(pts):
    """Exact angular order on the unit circle: upper half (y > 0) by decreasing x, then lower half by increasing x."""
    return sorted(range(len(pts)), key=lambda i: (0, -pts[i][0]) if pts[i][1] > 0 else (1, pts[i][0]))


def bits(q):
    return max(abs(q.numerator).bit_length(), q.denominator.bit_length())


def check(nvars, clauses):
    pts, exps, meta = build(nvars, clauses)
    names = meta["names"]
    n = len(pts)
    rep = {}
    rep["on_circle"] = all(x * x + y * y == 1 for x, y in pts)
    rep["distinct"] = len(set(pts)) == n
    order = cyclic_order(pts)
    adj = {frozenset((order[t], order[(t + 1) % n])) for t in range(n)}
    got, deltas, maxbits = [], set(), 0
    struct = True
    for a, b, c, dl in exps:
        U = frozenset(i for i in range(n) if ip(a, pts[i]) > b)
        v = [ip(c, p) for p in pts]
        far = {frozenset((i, j)) for i, j in itertools.combinations(range(n), 2) if abs(v[i] - v[j]) > 2 * dl}
        if len(far) == n * (n - 1) // 2:
            sep = "all"
        else:
            sep = frozenset(names[i] for i in next(iter(far))) if len(far) == 1 else ("other", len(far))
            if len(far) == 1:
                i, j = tuple(next(iter(far)))
                struct &= pts[i] == (-pts[j][0], -pts[j][1])                 # antipodal
                # strict margins: i, j are strict extremes of the observation functional
                others = [v[t] for t in range(n) if t not in (i, j)]
                struct &= max(v[i], v[j]) > max(others) and min(v[i], v[j]) < min(others)
        struct &= len(U) <= 2 and (len(U) < 2 or frozenset(U) in adj)
        # strict safety margin: no parameter sits exactly on the threshold
        struct &= all(ip(a, p) != b for p in pts)
        got.append((frozenset(names[i] for i in U), sep))
        deltas.add(dl)
        maxbits = max([maxbits] + [bits(x) for x in (*a, b, *c, dl)])
    maxbits = max([maxbits] + [bits(x) for p in pts for x in p])
    traces = {U for U, _ in got if U}
    rep["laminar"] = all(not (s & t) or s <= t or t <= s for s, t in itertools.combinations(traces, 2))
    rep["structure"] = struct
    rep["matches_intent"] = Counter(got) == intended(nvars, clauses)
    # a common noise radius: dividing c by delta keeps every comparison, so delta = 1 for all
    rep["common_delta_possible"] = all(d > 0 for d in deltas)
    rep["params"], rep["exps"], rep["maxbits"] = n, len(exps), maxbits
    return rep


def main():
    rng = random.Random(20261124)
    cases = [(1, [(1,)]), (1, [(1,), (-1,)]), (1, []), (2, [()]), (2, [(1, 1, -2)]), (2, [(1, -1)]),
             (2, [(1, 2), (-1, 2), (1, -2), (-1, -2)]), (3, [(1, 2, 3), (-1, -2), (-3, 1)])]
    for _ in range(40):
        nv = rng.randint(1, 6)
        cases.append((nv, [tuple(rng.choice([-1, 1]) * rng.randint(1, nv) for _ in range(rng.randint(1, 3)))
                           for _ in range(rng.randint(1, 4 * nv))]))
    lines, ok_all = [], True
    worst = 0.0
    for nv, cl in cases:
        r = check(nv, cl)
        ok = all(r[k] for k in ("on_circle", "distinct", "laminar", "structure", "matches_intent", "common_delta_possible"))
        ok_all &= ok
        N = r["params"]
        worst = max(worst, r["maxbits"] / max(1, (N + 1).bit_length()))
        lines.append(f"n={nv} m={len(cl)}: {N} parameters, {r['exps']} experiments, max {r['maxbits']} bits; "
                     + ("ok" if ok else f"FAIL {r}"))
    lines.append(f"\n{len(cases)} formulas; all checks pass: {ok_all}; "
                 f"max bits / log2(parameters) = {worst:.2f}")
    text = "\n".join(lines) + "\n"
    OUT.write_text(text)
    print(text, end="")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
