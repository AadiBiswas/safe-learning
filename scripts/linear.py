"""Linear safety and linear interval observations (research/linear_identifiability.md,
research/witness_geometry.md).

Parameters are points in Q^d (tuples of Fractions). Experiment u = (a, b, c, delta):
unsafe for theta iff a.theta > b (safe at equality), observation c.theta + [-delta, delta].
Everything is exact. `to_instance` builds the combinatorial instance of scripts/traps.py,
whose exhaustive solver is the reference for every geometric statement checked here.
"""

import itertools
from fractions import Fraction as Fr

from traps import Instance, members, popcount


def dot(a, x):
    return sum(ai * xi for ai, xi in zip(a, x))


def to_instance(points, exps, eps=0):
    n = len(points)
    acts = []
    for a, b, c, dl in exps:
        U = sum(1 << i for i, p in enumerate(points) if dot(a, p) > b)
        v = [dot(c, p) for p in points]
        cand = sorted({x + s * dl for x in v for s in (-1, 1)})
        cand += [(x + y) / 2 for x, y in zip(cand, cand[1:])]
        R = {sum(1 << i for i in range(n) if abs(y - v[i]) <= dl) for y in cand}
        acts.append((U, tuple(r for r in R if r)))
    return Instance(n, acts, eps=eps)


def support(points, K, v):
    return max(dot(v, points[i]) for i in members(K))


def width(points, K, v):
    return support(points, K, v) + support(points, K, tuple(-x for x in v))


def geometric_trap(points, exps, K):
    """Support-function form: every experiment is blocked (h_K(a) > b) or blind (w_K(c) <= 2 delta)."""
    return all(support(points, K, a) > b or width(points, K, c) <= 2 * dl for a, b, c, dl in exps)


# ---------------------------------------------------------------- convex position (planar)

def cross(o, p, q):
    return (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])


def extreme_points(points, K):
    """Bitmask of the vertices of conv K in the plane (exact; collinear boundary points excluded).
    Duplicated coordinates: one representative (the lowest index) counts as the vertex."""
    idx = list(members(K))
    first = {}
    for i in idx:
        first.setdefault(points[i], i)
    pts = sorted(first)
    if len(pts) <= 2:
        return sum(1 << first[p] for p in pts)

    def half(seq):
        h = []
        for p in seq:
            while len(h) >= 2 and cross(h[-2], h[-1], p) <= 0:
                h.pop()
            h.append(p)
        return h
    hull = half(pts)[:-1] + half(pts[::-1])[:-1]
    return sum(1 << first[p] for p in hull)


def in_convex_position(points, K):
    return extreme_points(points, K) == K


# ---------------------------------------------------------------- safety directions

def ray(a):
    """Canonical positive ray of a nonzero rational vector: a / max|a_i|."""
    s = max(abs(x) for x in a)
    return tuple(x / s for x in a)


def blocked_rays(points, exps, K):
    rays, const = set(), False
    for a, b, c, dl in exps:
        if support(points, K, a) > b:
            if any(a):
                rays.add(ray(a))
            else:
                const = True                      # a = 0, b < 0: unsafe for everything
    return rays, const


def sigma_ray_bound(points, exps, K):
    """One maximizer per blocked ray reproduces every blocked experiment (Prop. W1)."""
    rays, const = blocked_rays(points, exps, K)
    return len(rays) + (1 if const and not rays else 0)


# ---------------------------------------------------------------- one dimension

def find_trap_1d(points, exps, eps=0):
    """d = 1: K is a trap iff {min K, max K} is (same support values, same diameter)."""
    inst = to_instance(points, exps, eps)
    inst.points = [p[0] for p in points]
    order = sorted(range(len(points)), key=lambda i: points[i])
    for i, j in itertools.combinations(order, 2):
        P = 1 << i | 1 << j
        if inst.far(P) and inst.is_trap(P):
            return P
    return None


# ---------------------------------------------------------------- sigma in planar convex position

def sigma_convex_planar(points, exps, K):
    """Exact sigma(K) when K is in convex position in the plane. Each blocked trace is a
    contiguous arc of the cyclic hull order, so this is circular-arc hitting set: cut the
    cycle at each point of the first arc and run the interval greedy (right endpoints)."""
    idx = list(members(K))
    hull = [i for i in _hull_order(points, K)]
    pos = {v: t for t, v in enumerate(hull)}
    k = len(hull)
    arcs = []
    for a, b, c, dl in exps:
        tr = [pos[i] for i in idx if dot(a, points[i]) > b]
        if not tr:
            continue
        if len(tr) == k:
            arcs.append(None)                    # whole cycle: any point hits it
            continue
        s = set(tr)
        start = next(t for t in tr if (t - 1) % k not in s)
        L = len(tr)
        assert all((start + j) % k in s for j in range(L)), "trace is not an arc"
        arcs.append((start, L))
    if not arcs:
        return 0
    real = [x for x in arcs if x is not None]
    if not real:
        return 1
    best = None
    s0, L0 = real[0]
    for cut in range(L0):                        # some point of the first arc is chosen
        p0 = (s0 + cut) % k
        chosen = [p0]
        # unroll the cycle starting just after p0; arcs containing p0 are already hit
        rest = []
        for s, L in real:
            if (p0 - s) % k < L:
                continue
            a0 = (s - p0) % k                    # in 1..k-1
            rest.append((a0, a0 + L - 1))
        rest.sort(key=lambda x: x[1])
        last = None
        for lo, hi in rest:
            if last is None or lo > last:
                last = hi
                chosen.append(last)
        best = len(chosen) if best is None else min(best, len(chosen))
    return best


def _hull_order(points, K):
    pts = sorted(((points[i], i) for i in members(K)))
    if len(pts) <= 2:
        return [i for _, i in pts]
    p = [x for x, _ in pts]
    ids = [i for _, i in pts]

    def half(order):
        h = []
        for t in order:
            while len(h) >= 2 and cross(p[h[-2]], p[h[-1]], p[t]) <= 0:
                h.pop()
            h.append(t)
        return h
    o = list(range(len(p)))
    hull = half(o)[:-1] + half(o[::-1])[:-1]
    return [ids[t] for t in hull]


# ---------------------------------------------------------------- reductions and constructions

def multicolored_clique(classes, edges):
    """Multicolored clique -> trap existence with k = len(classes) safety rays.
    Coordinates: one class indicator per color, one coordinate per conflicting pair,
    one 'index' coordinate. A trap of size >= 2 is exactly a multicolored clique."""
    verts = [v for cl in classes for v in cl]
    col = {v: i for i, cl in enumerate(classes) for v in cl}
    k = len(classes)
    E = {frozenset(e) for e in edges}
    conflicts = [(v, w) for v, w in itertools.combinations(verts, 2)
                 if col[v] == col[w] or frozenset((v, w)) not in E]
    D = k + len(conflicts) + 1
    pts = []
    for t, v in enumerate(verts):
        x = [Fr(0)] * D
        x[col[v]] = Fr(1)
        for j, (p, q) in enumerate(conflicts):
            x[k + j] = Fr(1) if v == p else Fr(-1) if v == q else Fr(0)
        x[-1] = Fr(10 * t)
        pts.append(tuple(x))
    zero = tuple(Fr(0) for _ in range(D))
    e = lambda i: tuple(Fr(1) if j == i else Fr(0) for j in range(D))  # noqa: E731
    exps = []
    for i in range(k):                     # unsafe exactly on class i; separating observation
        exps.append((e(i), Fr(1, 2), e(D - 1), Fr(1)))
    for j in range(len(conflicts)):        # always safe; kills exactly the sets holding both ends
        exps.append((zero, Fr(0), e(k + j), Fr(3, 5)))
    return pts, exps, verts


def has_multicolored_clique(classes, edges):
    E = {frozenset(e) for e in edges}
    return any(all(frozenset((p, q)) in E for p, q in itertools.combinations(pick, 2))
               for pick in itertools.product(*classes))
