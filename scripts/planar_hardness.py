"""3-SAT -> linear safe identifiability in the PLANE, parameters on the unit circle
(research/fixed_dimension_complexity.md, Theorem D2).

Every parameter is a rational point of the unit circle. Each experiment is one of:
  force(w)          unsafe {w}, observation separates every pair: every trap contains w
  imply(x, w, V)    unsafe V, observation separates exactly the antipodal pair {x, w}:
                    with w forced, x in K  =>  K meets V
  notboth(a, b)     always safe, observation separates exactly the antipodal pair {a, b}
  some(V)           unsafe V, observation separates every pair: K meets V
Unsafe sets are singletons or cyclically adjacent pairs (halfplane traces on the circle);
separated pairs are antipodal points (unique max / min of the observation functional).
"""

from fractions import Fraction as Fr

from linear import dot, to_instance


def circle_point(s):
    """Rational point of the unit circle at angle 2 arctan(s)."""
    return (Fr(1 - s * s, 1 + s * s), Fr(2 * s, 1 + s * s))


def neg(p):
    return (-p[0], -p[1])


def build(nvars, clauses):
    """Returns (points, exps, meta). meta maps names to indices and records the intended
    unsafe set and separated pairs of every experiment, for exact verification."""
    uppers, pairs_of = [], {}           # upper points in angular order; partner of each upper

    def add_pair(up, down):
        uppers.append(up)
        pairs_of[up] = down

    # Upper half-circle, in this order: T_v, F_v (each with a helper below), T'_v (partner F'_v below);
    # then per clause s, s', k1, k2, k3 consecutively (each with a helper below).
    for v in range(nvars):
        add_pair(("T", v), ("wT", v))
        add_pair(("F", v), ("wF", v))
        add_pair(("Tp", v), ("Fp", v))
    for j, c in enumerate(clauses):
        if not c:
            continue
        for nm in ("s", "sp", "k1", "k2", "k3"):
            add_pair((nm, j), ("w" + nm, j))
    names, pts = [], []
    for k, up in enumerate(uppers):
        p = circle_point(Fr(k + 1, 1))   # angles 2 arctan(k+1): increasing in (0, pi)
        names.append(up)
        pts.append(p)
    for up in uppers:
        names.append(pairs_of[up])
        pts.append(neg(pts[names.index(up)]))
    idx = {nm: i for i, nm in enumerate(names)}
    n = len(pts)
    order = sorted(range(n), key=lambda i: _angle_key(pts[i]))   # cyclic order
    pos = {i: t for t, i in enumerate(order)}

    def unsafe_halfplane(V):
        """(a, b) with trace exactly V: V empty, a singleton, or a cyclically adjacent pair."""
        if not V:
            return (Fr(0), Fr(0)), Fr(1)        # 0 <= 1 with margin 1: safe for everything
        a = tuple(sum(pts[i][t] for i in V) for t in range(2))
        vals = sorted((dot(a, pts[i]) for i in range(n)), reverse=True)
        k = len(V)
        assert sorted(dot(a, pts[i]) for i in V)[0] == vals[k - 1] > vals[k], "V is not a cap"
        return a, (vals[k - 1] + vals[k]) / 2

    def antipodal_obs(x, y):
        """Direction c = pts[x]: x the unique max, y = -x the unique min; delta separates only {x, y}."""
        c = pts[x]
        others = [dot(c, pts[i]) for i in range(n) if i not in (x, y)]
        M = max(1 - min(others), max(others) + 1)
        return c, (M + 2) / 4

    # one direction with distinct projections on the circle; scaled so gaps exceed 2 delta
    cstar = (Fr(1), Fr(1, 7))
    proj = sorted(dot(cstar, p) for p in pts)
    gap = min(b - a for a, b in zip(proj, proj[1:]))
    assert gap > 0
    full_sep = (cstar, gap / 3)

    exps, intent = [], []

    def experiment(V, obs, sep):
        a, b = unsafe_halfplane(V)
        c, dl = obs
        exps.append((a, b, c, dl))
        intent.append((frozenset(V), sep))

    def force(w):
        experiment([w], full_sep, "all")

    def imply(x, V):
        w = idx[pairs_of[names[x]]]
        experiment(V, antipodal_obs(x, w), frozenset((x, w)))

    for up in uppers:
        if up[0] != "Tp":
            force(idx[pairs_of[up]])                       # every helper is forced
    lit = lambda l: idx[("T" if l > 0 else "F", abs(l) - 1)]  # noqa: E731
    for v in range(nvars):
        imply(idx[("T", v)], [idx[("Tp", v)]])            # T => T'
        imply(idx[("F", v)], [idx[("Fp", v)]])            # F => F'
        a, b = idx[("Tp", v)], idx[("Fp", v)]
        experiment([], antipodal_obs(a, b), frozenset((a, b)))   # not both T', F'
    for j, c in enumerate(clauses):
        if not c:
            experiment([], full_sep, "all")                # empty clause: nothing survives
            continue
        l = list(c) + [c[-1]] * (3 - len(c))
        k1, k2, k3 = (idx[(nm, j)] for nm in ("k1", "k2", "k3"))
        s, sp = idx[("s", j)], idx[("sp", j)]
        experiment([s, sp], full_sep, "all")               # s or s'
        imply(sp, [k1, k2])                                # s' => k1 or k2
        imply(s, [k3])                                     # s  => k3
        for k, li in zip((k1, k2, k3), l):
            imply(k, [lit(li)])                            # copy => its literal
    return pts, exps, dict(names=names, idx=idx, intent=intent, order=order, pos=pos)


def _angle_key(p):
    # exact angular order for points of the unit circle: upper half by decreasing x, then lower half
    x, y = p
    return (0, -x) if y > 0 or (y == 0 and x > 0) else (1, x)


def verify(pts, exps, meta):
    """Exact check that every experiment has its intended unsafe set and separated-pair set."""
    n = len(pts)
    for (a, b, c, dl), (V, sep) in zip(exps, meta["intent"]):
        U = {i for i in range(n) if dot(a, pts[i]) > b}
        if U != set(V):
            return False
        far = {frozenset((i, j)) for i in range(n) for j in range(i + 1, n)
               if abs(dot(c, pts[i]) - dot(c, pts[j])) > 2 * dl}
        want = {frozenset((i, j)) for i in range(n) for j in range(i + 1, n)} if sep == "all" else {sep}
        if far != want:
            return False
    return True


def instance(nvars, clauses):
    pts, exps, meta = build(nvars, clauses)
    return pts, exps, meta, to_instance(pts, exps)
