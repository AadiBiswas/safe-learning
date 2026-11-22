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
        # Responses are windows [y - dl, y + dl] of the sorted projections. Only maximal ones
        # matter (smaller responses are dominated for the adversary), and every maximal
        # window can be slid until its left end sits on a projection.
        order = sorted(range(n), key=v.__getitem__)
        R, hi, mask = set(), 0, 0
        for lo in range(n):
            while hi < n and v[order[hi]] - v[order[lo]] <= 2 * dl:
                mask |= 1 << order[hi]
                hi += 1
            R.add(mask)
            mask &= ~(1 << order[lo])
        acts.append((U, tuple(sorted(r for r in R if r))))
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


# ---------------------------------------------------------------- few observation directions

def obs_lines(exps):
    """Distinct observation lines (c up to nonzero scaling; widths are sign-symmetric)."""
    lines = {}
    for a, b, c, dl in exps:
        if any(c):
            lines.setdefault(ray(c) if ray(c) > ray(tuple(-x for x in c)) else ray(tuple(-x for x in c)), c)
    return list(lines.values())


def find_trap_obsdirs(points, exps, eps=0):
    """XP in the number k of observation lines: guess the extreme parameters of a trap on
    every line (O(n^{2k}) guesses); the largest set with those extremes is a trap iff any is
    (Theorem D5). Exact for every dimension and every safety structure."""
    inst = to_instance(points, exps, eps)
    n = len(points)
    C = obs_lines(exps)
    vals = [[dot(c, p) for p in points] for c in C]
    for guess in itertools.product(*[itertools.product(range(n), repeat=2) for _ in C]):
        if any(vals[j][lo] > vals[j][hi] for j, (lo, hi) in enumerate(guess)):
            continue
        K = sum(1 << i for i in range(n)
                if all(vals[j][lo] <= vals[j][i] <= vals[j][hi] for j, (lo, hi) in enumerate(guess)))
        if inst.far(K) and inst.is_trap(K):
            return K
    if not C:                                   # no informative observation at all
        return inst.full if inst.far(inst.full) else None
    return None


# ---------------------------------------------------------------- aligned safety and sensing

def aligned(exps):
    """Every experiment has a_u = lambda_u c_u with lambda_u != 0 and c_u != 0."""
    def par(a, c):
        if not any(c) or not any(a):
            return False
        i = next(t for t, x in enumerate(c) if x)
        lam = a[i] / c[i]
        return lam != 0 and all(x == lam * y for x, y in zip(a, c))
    return all(par(a, c) for a, b, c, dl in exps)


def global_conflicts(points, exp):
    a, b, c, dl = exp
    v = [dot(c, p) for p in points]
    return {frozenset((i, j)) for i, j in itertools.combinations(range(len(points)), 2) if abs(v[i] - v[j]) > 2 * dl}


def aligned_2sat_trap(points, exps, eps=0):
    """Theorem AL2. Aligned experiments whose global conflict graph is empty, complete, or a
    single pair, with |unsafe set| <= 2 for the complete ones. Clauses: complete -> (OR B);
    single pair {i,j} -> tautology if B meets it, else (not i or not j) (Lemma AL1 rules out
    the remaining case). Then 2-SAT with x_i = x_j = 1 for each far pair, by Even-Itai-Shamir
    propagation. Returns a trap bitmask or None."""
    n = len(points)
    allpairs = n * (n - 1) // 2
    pos, negs = [], []
    for e in exps:
        a, b, c, dl = e
        B = [i for i, p in enumerate(points) if dot(a, p) > b]
        P = global_conflicts(points, e)
        if not P:
            continue
        if len(P) == allpairs:
            assert len(B) <= 2, "outside the AL2 family"
            pos.append(tuple(B))
        elif len(P) == 1:
            i, j = tuple(next(iter(P)))
            if i in B or j in B:
                continue
            assert not B, "Lemma AL1 violated: an aligned lone pair with a disjoint unsafe set"
            negs.append((i, j))
        else:
            raise ValueError("outside the AL2 family")
    inst = to_instance(points, exps, eps)
    for i, j in itertools.combinations(range(n), 2):
        P = 1 << i | 1 << j
        if not inst.far(P):
            continue
        sol = _two_sat(n, pos, negs, {i: 1, j: 1})
        if sol is not None:
            K = sum(1 << t for t in range(n) if sol[t])
            assert inst.is_trap(K)
            return K
    return None


def _two_sat(n, pos, negs, forced):
    """Clauses (x or y) / (not x or not y); a positive clause of length 1 or 0 allowed.
    Even-Itai-Shamir: propagate a tentative value; keep it if no contradiction arises."""
    val = dict(forced)

    def propagate(assign):
        assign = dict(assign)
        changed = True
        while changed:
            changed = False
            for cl in pos:
                if any(assign.get(x) == 1 for x in cl):
                    continue
                free = [x for x in cl if x not in assign]
                if not free:
                    return None
                if len(free) == 1:
                    assign[free[0]] = 1
                    changed = True
            for x, y in negs:
                if assign.get(x) == 0 or assign.get(y) == 0:
                    continue
                if assign.get(x) == 1 and assign.get(y) == 1:
                    return None
                if assign.get(x) == 1 and y not in assign:
                    assign[y] = 0
                    changed = True
                elif assign.get(y) == 1 and x not in assign:
                    assign[x] = 0
                    changed = True
        return assign

    val = propagate(val)
    if val is None:
        return None
    for t in range(n):
        if t in val:
            continue
        nxt = propagate({**val, t: 1}) or propagate({**val, t: 0})
        if nxt is None:
            return None
        val = nxt
    return [val[t] for t in range(n)]


def aligned_sat_u2(nvars, clauses):
    """Stage 1's sat_u2 realized with ALIGNED experiments (a_u = c_u) on the standard basis of
    Q^N. Each experiment's projection puts its unsafe set V on top (value M), then encodes the
    effective conflict pattern on the rest: a lone pair (not both), a star (implication x => V),
    or all pairs (V must be met). Effective conflicts are the only active ones (Theorem B1)."""
    from traps import lit
    nvars = max(nvars, 2)
    N = 2 * nvars + 2 * len(clauses)
    M = Fr(10 * N + 10)
    e = lambda i: tuple(Fr(1) if t == i else Fr(0) for t in range(N))  # noqa: E731
    pts = [e(i) for i in range(N)]

    def exp(V, g, dl):
        q = tuple(M * (t in V) + g[t] for t in range(N))
        return (q, (M + max(g)) / 2 if V else M, q, dl)    # unsafe iff projection > threshold

    exps = []

    def not_both(x, y):
        exps.append(exp(set(), [Fr(1) if t == x else Fr(-1) if t == y else Fr(0) for t in range(N)], Fr(3, 5)))

    def some(V):
        exps.append(exp(set(V), [Fr(3 * t) for t in range(N)], Fr(1)))

    def implies(x, V):
        exps.append(exp(set(V), [Fr(2) if t == x else Fr(0) for t in range(N)], Fr(3, 5)))

    for v in range(nvars):
        T, F = 2 * v, 2 * v + 1
        not_both(T, F)
        some([T, F])
    for j, c in enumerate(clauses):
        if not c:
            some([])
            continue
        l = [lit(x) for x in c] + [lit(c[-1])] * (3 - len(c))
        s, s2 = 2 * nvars + 2 * j, 2 * nvars + 2 * j + 1
        not_both(s, s2)
        some([s, s2])
        implies(s2, [l[0], l[1]])
        implies(s, [l[2]])
    return pts, exps
