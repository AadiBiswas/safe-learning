"""Stage 3 checks (ledger E006).

    .venv/bin/python scripts/stage3_checks.py   ->  results/stage3_checks.txt

research/boolean_trap_formulation.md, research/fixed_dimension_complexity.md,
research/geometric_realizations.md. Exact arithmetic throughout. Not proofs.
"""

import random
import sys
from fractions import Fraction as Fr
from pathlib import Path

from boolean import clauses, find_trap_boolean, is_horn
from linear import dot, find_trap_obsdirs, to_instance
from planar_hardness import build, verify
from traps import popcount, random_instance, satisfiable

OUT = Path(__file__).resolve().parents[1] / "results" / "stage3_checks.txt"
SEED = 20261123
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


def rand_linear(rng, n, m, d, obs_dirs=None):
    pts = [rvec(rng, d) for _ in range(n)]
    exps = []
    for _ in range(m):
        a = rvec(rng, d, -3, 3)
        b = Fr(rng.choice([dot(a, p) for p in pts])) - rng.choice([0, Fr(1, 2)])
        c = rng.choice(obs_dirs) if obs_dirs else rvec(rng, d, -3, 3)
        lam = rng.choice([1, 2, -1])                                  # one factor: same line
        c = tuple(lam * x for x in c)
        dl = Fr(rng.randint(0, 6), 2)
        exps.append((a, b, c, dl))
    return pts, exps


def main():
    rng = random.Random(SEED)

    log("A. Boolean formulation = trap enumeration")
    ag = tot = 0
    for _ in range(600):                      # general set-valued observations: hyperedge conflicts
        n = rng.randint(2, 6)
        inst = random_instance(rng, n, rng.randint(1, 5), alphabet=rng.choice([2, 3, 4]), p_unsafe=0.3)
        tot += 1
        ag += (find_trap_boolean(inst) is None) == (inst.value(inst.full) is not None)
    check("set-valued observations (minimal conflict sets)", ag == tot, f"{ag}/{tot}")
    ag = tot = 0
    for _ in range(600):                      # linear interval observations: pair conflicts suffice
        d = rng.choice([1, 2, 3])
        pts, exps = rand_linear(rng, rng.randint(2, 7), rng.randint(1, 6), d)
        inst = to_instance(pts, exps)
        tot += 1
        ag += (find_trap_boolean(inst, pairwise=True) is None) == (inst.value(inst.full) is not None)
    check("linear interval observations (pair conflicts)", ag == tot, f"{ag}/{tot}")
    ok = True
    for _ in range(300):
        inst = random_instance(rng, rng.randint(2, 6), rng.randint(1, 5), p_unsafe=0.5, max_unsafe=1)
        ok &= is_horn(clauses(inst))
    check("unsafe sets of size <= 1 give Horn clauses", ok)

    log("\nB. Planar hardness construction (unit circle), exact")
    cases = [(1, [(1,)]), (1, [(1,), (-1,)]), (2, []), (2, [()]), (2, [(1, 1, -2)]), (2, [(1, -1)]),
             (2, [(1, 2), (-1, 2), (1, -2), (-1, -2)]), (3, [(1, 2, 3), (-1, -2), (-3, 1)])]
    for _ in range(50):
        nv = rng.randint(1, 3)
        k = rng.randint(1, 2 * nv) if rng.random() < 0.6 else rng.randint(3 * nv, 4 * nv)
        cases.append((nv, [tuple(rng.choice([-1, 1]) * rng.randint(1, nv) for _ in range(rng.randint(1, 3)))
                           for _ in range(k)]))
    geo = ag = sat = 0
    maxn = 0
    for nv, cl in cases:
        pts, exps, meta = build(nv, cl)
        inst = to_instance(pts, exps)
        maxn = max(maxn, inst.n)
        geo += verify(pts, exps, meta) and all(p[0] ** 2 + p[1] ** 2 == 1 for p in pts)
        s = satisfiable(nv, cl)
        sat += s
        ag += s == (find_trap_boolean(inst, pairwise=True) is not None)
        assert inst.unsafe_size() <= 2
    check("every point on the unit circle; every unsafe set and separated-pair set as intended",
          geo == len(cases), f"{geo}/{len(cases)}")
    check("formula satisfiable <=> trap exists", ag == len(cases),
          f"{ag}/{len(cases)}, {sat} satisfiable, up to {maxn} parameters")
    # common noise radius: rescale every observation to delta = 1
    nv, cl = 2, [(1, 2), (-1, 2)]
    pts, exps, meta = build(nv, cl)
    exps1 = [(a, b, tuple(x / dl for x in c), Fr(1)) for a, b, c, dl in exps]
    check("common noise radius by rescaling observation vectors",
          to_instance(pts, exps1).actions == to_instance(pts, exps).actions)

    log("\nC. Dimension padding and block sums")
    ok = True
    for _ in range(200):
        d = rng.choice([1, 2])
        pts, exps = rand_linear(rng, rng.randint(2, 6), rng.randint(1, 5), d)
        D = d + rng.randint(1, 3)
        pad = lambda v: tuple(v) + (Fr(0),) * (D - d)  # noqa: E731
        ok &= to_instance([pad(p) for p in pts], [(pad(a), b, pad(c), dl) for a, b, c, dl in exps]).actions \
            == to_instance(pts, exps).actions
    check("zero padding R^d -> R^D leaves the instance unchanged", ok)
    ok = True
    for _ in range(200):
        n = rng.randint(2, 6)
        ds, do = rng.choice([1, 2]), rng.choice([1, 2])
        P, Q = [rvec(rng, ds) for _ in range(n)], [rvec(rng, do) for _ in range(n)]
        exps = []
        for _ in range(rng.randint(1, 5)):
            a, c = rvec(rng, ds, -3, 3), rvec(rng, do, -3, 3)
            exps.append((a, Fr(rng.randint(-4, 4)), c, Fr(rng.randint(0, 4), 2)))
        joint = [tuple(p) + tuple(q) for p, q in zip(P, Q)]
        jexps = [(tuple(a) + (Fr(0),) * do, b, (Fr(0),) * ds + tuple(c), dl) for a, b, c, dl in exps]
        inst = to_instance(joint, jexps)
        for u, (a, b, c, dl) in enumerate(exps):
            U = sum(1 << i for i in range(n) if dot(a, P[i]) > b)
            R = to_instance(Q, [((Fr(0),) * do, Fr(0), c, dl)]).actions[0][1]
            ok &= inst.actions[u] == (U, R)
    check("block sum (p_i, q_i): safety from p, observation from q, exactly", ok)

    log("\nD. XP algorithm in the number of observation lines")
    for k in (1, 2):
        ag = tot = 0
        for _ in range(300 if k == 1 else 120):
            d = rng.choice([1, 2, 3])
            dirs = [rvec(rng, d, -3, 3) for _ in range(k)]
            dirs = [v if any(v) else (Fr(1),) * d for v in dirs]
            pts, exps = rand_linear(rng, rng.randint(2, 7), rng.randint(1, 7), d, obs_dirs=dirs)
            eps = rng.choice([0, 0, 2])
            inst = to_instance(pts, exps, eps)
            tot += 1
            ag += (find_trap_obsdirs(pts, exps, eps) is None) == (inst.value(inst.full) is not None)
        check(f"k = {k} observation line(s): guessed-extremes box = exhaustive", ag == tot, f"{ag}/{tot}")

    log("\nE. Single-pair separation relations are exactly strictly antipodal pairs")
    ok = True
    hits = 0
    for _ in range(300):
        d = rng.choice([1, 2])
        pts = [rvec(rng, d) for _ in range(rng.randint(3, 7))]
        for _ in range(20):
            c = rvec(rng, d, -3, 3)
            v = [dot(c, p) for p in pts]
            for dl in {abs(x - y) / 2 for x in v for y in v}:
                far = [(i, j) for i in range(len(pts)) for j in range(i + 1, len(pts)) if abs(v[i] - v[j]) > 2 * dl]
                if len(far) == 1:
                    hits += 1
                    i, j = far[0]
                    lo, hi = sorted((i, j), key=lambda t: v[t])
                    ok &= all(v[lo] < v[t] < v[hi] for t in range(len(pts)) if t not in (i, j))
    check("a one-edge separation graph joins the unique min and unique max", ok, f"{hits} one-edge relations")

    text = "\n".join(lines) + "\n"
    OUT.write_text(text)
    log(f"\n{len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
