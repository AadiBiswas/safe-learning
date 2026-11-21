"""Stage 2 exhaustive checks (ledger E005).

    .venv/bin/python scripts/stage2_checks.py   ->  results/stage2_checks.txt

Geometric statements of research/linear_identifiability.md, research/witness_geometry.md
and research/approximate_witnesses.md, compared with the exhaustive solver of
scripts/traps.py. Exact rational arithmetic except in §J (marked). Not proofs.
"""

import itertools
import math
import random
import sys
from fractions import Fraction as Fr
from pathlib import Path

from linear import (blocked_rays, dot, extreme_points, find_trap_1d, geometric_trap,
                    has_multicolored_clique, in_convex_position, multicolored_clique,
                    sigma_convex_planar, sigma_ray_bound, support, to_instance, width)
from traps import (find_trap_split, is_laminar, members, popcount, safety_witness_number,
                   sat_laminar, satisfiable)

OUT = Path(__file__).resolve().parents[1] / "results" / "stage2_checks.txt"
SEED = 20261122
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


def random_points(rng, n, d, kind):
    if kind == "collinear":                      # all on one line through a random point
        o, v = rvec(rng, d), rvec(rng, d, -2, 2)
        return [tuple(oi + t * vi for oi, vi in zip(o, v)) for t in rng.sample(range(-5, 6), n)]
    if kind == "repeated":
        base = [rvec(rng, d) for _ in range(max(1, n - 2))]
        return [rng.choice(base) for _ in range(n)]
    if kind == "circle":                         # rational points on the unit circle (exact)
        ts = rng.sample(range(-9, 10), n)
        return [(Fr(1 - t * t, 1 + t * t), Fr(2 * t, 1 + t * t)) for t in ts] if d == 2 else None
    return [rvec(rng, d) for _ in range(n)]


def random_exps(rng, pts, m, d, rays=None, aligned=False):
    exps = []
    for _ in range(m):
        r = rng.random()
        if r < 0.1:
            a = tuple(Fr(0) for _ in range(d))   # constant safety: always or never safe
            b = Fr(rng.choice([-1, 0, 1]))
        else:
            a = rng.choice(rays) if rays else rvec(rng, d, -3, 3)
            if rays:
                a = tuple(rng.randint(1, 3) * x for x in a)   # positive rescaling of a ray
            vals = sorted(dot(a, p) for p in pts)
            b = rng.choice(vals) if rng.random() < 0.6 else vals[0] - 1 + rng.random() * 0  # equality cases
            b = Fr(b)
        c = a if aligned else (rvec(rng, d, -3, 3) if rng.random() > 0.05 else tuple(Fr(0) for _ in range(d)))
        cv = sorted(dot(c, p) for p in pts)
        gaps = [y - x for x, y in zip(cv, cv[1:]) if y > x]
        if rng.random() < 0.4 and gaps:
            dl = rng.choice(gaps) / 2                  # some intervals touch exactly
        else:
            dl = Fr(rng.choice([0, 1, 2, 3]), rng.choice([1, 2]))
        exps.append((a, b, c, dl))
    return exps


def main():
    rng = random.Random(SEED)

    log("A. Support-function characterization of traps (all subsets, exact)")
    tot = ok = 0
    for kind in ("generic", "collinear", "repeated", "circle"):
        for d in (1, 2, 3):
            if kind == "circle" and d != 2:
                continue
            for _ in range(120):
                n = rng.randint(2, 7)
                pts = random_points(rng, n, d, kind)
                exps = random_exps(rng, pts, rng.randint(1, 6), d, aligned=rng.random() < 0.2)
                inst = to_instance(pts, exps)
                for K in range(1, inst.full + 1):
                    tot += 1
                    ok += geometric_trap(pts, exps, K) == inst.is_trap(K)
    check("trap <=> every experiment blocked (h_K(a) > b) or blind (w_K(c) <= 2 delta)", ok == tot,
          f"{ok}/{tot} subsets; generic/collinear/repeated/circle, d = 1, 2, 3")

    log("\nB. Convex-hull invariance (planar)")
    ok_inv = ok_min = True
    nmin = 0
    for kind in ("generic", "collinear", "repeated", "circle"):
        for _ in range(300):
            n = rng.randint(2, 8)
            pts = random_points(rng, n, 2, kind)
            exps = random_exps(rng, pts, rng.randint(1, 7), 2)
            inst = to_instance(pts, exps)
            for K in range(1, inst.full + 1):
                ok_inv &= inst.is_trap(K) == inst.is_trap(extreme_points(pts, K))
            for K in inst.minimal_traps():
                if popcount(K) >= 3:
                    nmin += 1
                    ok_min &= in_convex_position(pts, K)
    check("K is a trap iff its set of hull vertices is", ok_inv)
    check("minimal traps of size >= 3 are in convex position", ok_min, f"{nmin} such minimal traps seen")

    log("\nC. Directional bound sigma(K) <= r(K) (number of blocked positive rays)")
    ok, tight = True, 0
    for _ in range(600):
        d = rng.choice([2, 3])
        n = rng.randint(2, 7)
        pts = random_points(rng, n, d, "generic")
        rays = [rvec(rng, d, -2, 2) for _ in range(rng.randint(1, 3))]
        rays = [r for r in rays if any(r)] or [tuple(Fr(1) for _ in range(d))]
        exps = random_exps(rng, pts, rng.randint(1, 8), d, rays=rays)
        inst = to_instance(pts, exps)
        for K in range(1, inst.full + 1):
            s, r = safety_witness_number(inst, K), sigma_ray_bound(pts, exps, K)
            ok &= s <= r
            tight += s == r and r >= 2
    check("sigma <= r on every subset", ok, f"{tight} subsets with sigma = r >= 2")
    # sharpness and opposite rays: a and -a are different rays
    pts = [(Fr(0),), (Fr(1),)]
    exps = [((Fr(1),), Fr(1, 2), (Fr(1),), Fr(0)), ((Fr(-1),), Fr(-1, 2), (Fr(1),), Fr(0))]
    inst = to_instance(pts, exps)
    check("opposite normals count separately (two points, sigma = 2 = r)",
          safety_witness_number(inst, 3) == 2 == sigma_ray_bound(pts, exps, 3))

    log("\nD. A minimum witness may need a non-extreme point")
    pts = [(Fr(0), Fr(0)), (Fr(6), Fr(0)), (Fr(0), Fr(6)), (Fr(2), Fr(2))]   # triangle + centroid
    exps = [((Fr(-1), Fr(-1)), Fr(-5), (Fr(1), Fr(0)), Fr(100)),   # x + y < 5: {v0, centroid}
            ((Fr(1), Fr(0)), Fr(3, 2), (Fr(1), Fr(0)), Fr(100)),   # x > 3/2: {v1, centroid}
            ((Fr(0), Fr(1)), Fr(3, 2), (Fr(1), Fr(0)), Fr(100))]   # y > 3/2: {v2, centroid}
    inst = to_instance(pts, exps)
    traces = [U for U, _ in inst.actions]
    ext = extreme_points(pts, inst.full)
    ext_only = min(len(c) for k in range(1, 4) for c in itertools.combinations(members(ext), k)
                   if all(U & sum(1 << i for i in c) for U in traces))
    check("traces {v0,c}, {v1,c}, {v2,c}: sigma = 1 via the centroid, 3 using hull vertices only",
          [popcount(U) for U in traces] == [2, 2, 2] and safety_witness_number(inst, inst.full) == 1
          and ext_only == 3)

    log("\nE. d = 1: endpoint pairs decide trap existence")
    ag = tot = 0
    for _ in range(1500):
        n = rng.randint(2, 7)
        pts = [(Fr(x),) for x in rng.sample(range(-8, 9), n)]
        exps = random_exps(rng, pts, rng.randint(1, 6), 1)
        eps = rng.choice([0, 0, 3])
        inst = to_instance(pts, exps, eps)
        inst.points = [p[0] for p in pts]
        tot += 1
        ag += (find_trap_1d(pts, exps, eps) is None) == (inst.value(inst.full) is not None)
    check("pairs = exhaustive", ag == tot, f"{ag}/{tot}")

    log("\nF. sigma in planar convex position = circular-arc hitting set")
    ag = tot = 0
    for _ in range(400):
        n = rng.randint(3, 10)
        pts = random_points(rng, n, 2, "circle")
        exps = random_exps(rng, pts, rng.randint(1, 8), 2)
        inst = to_instance(pts, exps)
        for K in rng.sample(range(1, inst.full + 1), min(40, inst.full)):
            tot += 1
            ag += sigma_convex_planar(pts, exps, K) == safety_witness_number(inst, K)
    check("circular-arc greedy = brute-force minimum hitting set", ag == tot, f"{ag}/{tot} (instance, K) pairs")

    log("\nG. Multicolored clique -> trap existence with k safety rays")
    ag = tot = yes = 0
    for _ in range(150):
        k = rng.randint(2, 3)
        classes, nxt = [], 0
        for _ in range(k):
            s = rng.randint(1, 3)
            classes.append(list(range(nxt, nxt + s)))
            nxt += s
        allp = [(v, w) for v, w in itertools.combinations(range(nxt), 2)]
        edges = [e for e in allp if rng.random() < 0.6]
        pts, exps, verts = multicolored_clique(classes, edges)
        inst = to_instance(pts, exps)
        rays, _ = blocked_rays(pts, exps, inst.full)
        truth = has_multicolored_clique(classes, edges)
        tot += 1
        yes += truth
        ag += truth == (find_trap_split(inst) is not None) and len(rays) <= k
    check("clique <=> trap; at most k safety rays", ag == tot, f"{ag}/{tot}, {yes} with a clique")

    log("\nH. Laminar unsafe families of size <= 2 (binary observations)")
    cases = [(1, [(1,)]), (2, []), (2, [()]), (2, [(1, 1)]), (2, [(1, -1)]), (2, [(1,), (-1,)]),
             (2, [(1, -2), (-1, 2), (1, 2)])]
    for _ in range(80):
        nv = rng.randint(2, 3)
        cases.append((nv, [tuple(rng.choice([-1, 1]) * rng.randint(1, nv) for _ in range(rng.randint(1, 3)))
                           for _ in range(rng.randint(1, 2))]))
    ag = tot = sat = 0
    for nv, cl in cases:
        inst = sat_laminar(nv, cl)
        if inst.n > 14:
            continue
        s = satisfiable(nv, cl)
        tot += 1
        sat += s
        ag += is_laminar(inst) and inst.unsafe_size() <= 2 and s == (find_trap_split(inst) is not None)
    check("laminar reduction: SAT <=> trap", ag == tot, f"{ag}/{tot}, {sat} satisfiable")

    log("\nI. Aligned safety and observation (c_u = a_u): minimal trap sizes")
    hist, hered_fail = {}, 0
    for _ in range(1500):
        n = rng.randint(3, 8)
        pts = random_points(rng, n, 2, rng.choice(["generic", "circle"]))
        exps = random_exps(rng, pts, rng.randint(2, 8), 2, aligned=True)
        inst = to_instance(pts, exps)
        T = set(inst.traps())
        hered_fail += any(not inst.is_trap(K & ~(1 << i)) for K in T for i in members(K) if popcount(K) >= 3)
        for K in inst.minimal_traps():
            hist[popcount(K)] = hist.get(popcount(K), 0) + 1
    log(f"  minimal trap sizes {dict(sorted(hist.items()))}; instances where traps are not hereditary: {hered_fail}")
    for n in range(3, 9):
        pts = [(Fr(i), Fr(i * i)) for i in range(n)]
        exps = [((Fr(2 * k), Fr(-1)), Fr(k * k) - Fr(1, 2), (Fr(2 * k), Fr(-1)), Fr(1, 4)) for k in range(n)]
        inst = to_instance(pts, exps)
        log(f"  aligned parabola n = {n}: minimal traps {[popcount(K) for K in inst.minimal_traps()]}")

    log("\nJ. Support-function sampling bound and the sqrt(R/gamma) witness count (floats)")
    worst = 0.0
    NETS = {}
    for _ in range(300):
        d = rng.choice([2, 3])
        P = [[rng.uniform(-1, 1) for _ in range(d)] for _ in range(60)]
        P = [p for p in P if sum(x * x for x in p) <= 1]
        rho = rng.choice([0.05, 0.1, 0.3] if d == 2 else [0.2, 0.3])
        net = NETS.setdefault((d, rho), _sphere_net(d, rho))
        F = [max(P, key=lambda p: sum(v[i] * p[i] for i in range(d))) for v in net]
        for _ in range(50):
            a = _unit([rng.gauss(0, 1) for _ in range(d)])
            hK = max(sum(a[i] * p[i] for i in range(d)) for p in P)
            hF = max(sum(a[i] * p[i] for i in range(d)) for p in F)
            worst = max(worst, (hK - hF) / (2 * rho))
    check("0 <= h_K(a) - h_F(a) <= 2 R rho (R = 1)", worst <= 1 + 1e-12, f"max ratio to 2 R rho = {worst:.3f}")
    for g in (Fr(1, 50), Fr(1, 200), Fr(1, 800)):
        cnt = _circle_gamma_witness(g)
        log(f"  unit circle, margin gamma = {g}: minimum approximate witness size {cnt}, "
            f"times sqrt(gamma) = {cnt * math.sqrt(g):.3f} (prediction pi/sqrt(2) = {math.pi / math.sqrt(2):.3f})")

    log("\nK. Net perturbation statements (exact, L-infinity nets, L1 Lipschitz constants)")
    okA = okB = True
    n_cases = 0
    for _ in range(300):
        n = rng.randint(3, 5)
        pts = random_points(rng, n, 2, "generic")
        exps = random_exps(rng, pts, rng.randint(1, 6), 2)
        inst = to_instance(pts, exps)
        for K in range(1, inst.full + 1):
            for F in range(1, K + 1):
                if F & K != F:
                    continue
                n_cases += 1
                h = max(min(max(abs(x - y) for x, y in zip(pts[i], pts[j])) for j in members(F)) for i in members(K))
                tight = [(a, b - sum(abs(x) for x in a) * h, c, dl) for a, b, c, dl in exps]
                loose = [(a, b, c, dl + sum(abs(x) for x in c) * h) for a, b, c, dl in exps]
                if geometric_trap(pts, exps, K):
                    okA &= geometric_trap(pts, tight, F)
                if geometric_trap(pts, exps, F):
                    okB &= geometric_trap(pts, loose, K)
    check("A: K trap => net F trap under safety tightened by L_g h", okA, f"{n_cases} (K, F) pairs")
    check("B: net F trap => K trap with noise enlarged by L_h h", okB)

    text = "\n".join(lines) + "\n"
    OUT.write_text(text)
    log(f"\n{len(failures)} failures")
    return 1 if failures else 0


def _unit(v):
    s = math.sqrt(sum(x * x for x in v))
    return [x / s for x in v]


def _sphere_net(d, rho):
    """A rho-net of the unit sphere: normalized grid points (covering checked by sampling below)."""
    k = int(math.ceil(2 * math.sqrt(d) / rho)) + 1
    grid = [i * 2 / (k - 1) - 1 for i in range(k)]
    pts = {tuple(round(x, 12) for x in _unit(list(g))) for g in itertools.product(grid, repeat=d) if any(g)}
    net = [list(p) for p in pts]
    rng = random.Random(0)
    for _ in range(300):
        a = _unit([rng.gauss(0, 1) for _ in range(d)])
        assert min(math.dist(a, v) for v in net) <= rho + 1e-12, "grid is not a rho-net"
    return net


def _circle_gamma_witness(gamma, N=720):
    """K = N rational points on the unit circle; for every direction a of the same set, the
    experiment with b = 1 - gamma - tiny is gamma-robustly blocked. Minimum number of points
    of K hitting every such cap, by the circular-arc algorithm."""
    # point angle = 2 arctan t, so t = tan(pi j / (2N)), |j| < N, covers the whole circle
    ts = [Fr(math.tan(math.pi * j / N / 2)).limit_denominator(10**6) for j in range(-N + 1, N)]
    pts = sorted({(Fr(1 - t * t, 1 + t * t), Fr(2 * t, 1 + t * t)) for t in ts},
                 key=lambda p: math.atan2(p[1], p[0]))
    exps = [((a[0], a[1]), 1 - gamma - Fr(1, 10**9), (Fr(0), Fr(0)), Fr(0)) for a in pts]
    return sigma_convex_planar(pts, exps, (1 << len(pts)) - 1)


if __name__ == "__main__":
    sys.exit(main())
