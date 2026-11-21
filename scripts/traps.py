"""Finite safe identification with explicit set-valued observations.

Theory: research/finite_trap_theory.md, research/complexity_analysis.md,
research/geometric_obstructions.md.

Parameters are 0..n-1 and every subset is a bitmask. An action is a pair
(unsafe, resp): `unsafe` is the bitmask of parameters for which the action is
unsafe, and resp[y] = {theta : y in Y(theta, u)} for each observation symbol y.
Every parameter must lie in at least one resp[y] (Y is nonempty). An observation
leaves the consistent set K & resp[y], so the responses of u at K are the nonempty
sets K & resp[y]: finitely many, whatever the observation space was originally.

`Instance.value` is the exhaustive reference solver. Everything else in this file
is checked against it in scripts/stage1_finite.py.
"""

import itertools
from functools import lru_cache


def popcount(K):
    return bin(K).count("1")


def members(K):
    i = 0
    while K:
        if K & 1:
            yield i
        K >>= 1
        i += 1


def action_from_sets(n, unsafe, Y):
    """Build (unsafe, resp) from Y[theta] = set of observation symbols."""
    symbols = sorted(set().union(*Y))
    resp = tuple(sum(1 << t for t in range(n) if y in Y[t]) for y in symbols)
    return unsafe, resp


def bits(i, k):
    return i >> k & 1


class Instance:
    def __init__(self, n, actions, points=None, eps=0):
        self.n = n
        self.actions = [(U, tuple(R)) for U, R in actions]
        self.points = list(range(n)) if points is None else list(points)
        self.eps = eps
        self.full = (1 << n) - 1
        for U, R in self.actions:
            assert sum(R) and (self.full & ~_or(R)) == 0, "every Y(theta, u) must be nonempty"
        self.value = lru_cache(maxsize=None)(self._value)

    def diam(self, K):
        v = [self.points[i] for i in members(K)]
        return max(v) - min(v) if v else 0

    def far(self, K):
        return popcount(K) >= 2 and self.diam(K) > self.eps

    def safe(self, K):
        return [u for u, (U, _) in enumerate(self.actions) if not U & K]

    def responses(self, K, u):
        return {K & R for R in self.actions[u][1] if K & R}

    def informative(self, K, u):
        """No single observation is compatible with every member of K."""
        return all(K & R != K for R in self.actions[u][1])

    def is_trap(self, K):
        return K != 0 and not any(self.informative(K, u) for u in self.safe(K))

    def _value(self, K):
        """Least worst-case number of experiments to reach diam <= eps from K, or None."""
        if not self.far(K):
            return 0
        best = None
        for u in self.safe(K):
            if not self.informative(K, u):
                continue                      # some response is K itself: no progress
            worst = 0
            for K2 in self.responses(K, u):
                r = self.value(K2)
                if r is None:
                    worst = None
                    break
                worst = max(worst, r)
            if worst is not None and (best is None or worst + 1 < best):
                best = worst + 1
        return best

    def traps(self, within=None):
        within = self.full if within is None else within
        return [K for K in range(1, within + 1) if K & within == K and self.far(K) and self.is_trap(K)]

    def minimal_traps(self):
        T = self.traps()
        return [K for K in T if not any(K2 != K and K2 & K == K2 for K2 in T)]

    def unsafe_size(self):
        return max((popcount(U) for U, _ in self.actions), default=0)

    def deterministic(self):
        """Responses of every action are pairwise disjoint (partition observations)."""
        return all(not (a & b) for _, R in self.actions for a, b in itertools.combinations(R, 2))


def _or(R):
    out = 0
    for r in R:
        out |= r
    return out


# ---------------------------------------------------------------- algorithms

def find_trap_split(inst, K=None, stats=None):
    """Exact for every instance. If u is safe for K, every trap inside K is safe for u
    too, so it lies inside a single response K & resp[y]. Recurse into the responses.
    With disjoint responses the recursion tree is laminar: at most 2n - 1 nodes."""
    seen = set()

    def go(K):
        if K in seen or not inst.far(K):
            return None
        seen.add(K)
        if stats is not None:
            stats["nodes"] = stats.get("nodes", 0) + 1
        for u in inst.safe(K):
            if inst.informative(K, u):
                for K2 in inst.responses(K, u):
                    t = go(K2)
                    if t is not None:
                        return t
                return None
        return K                              # no safe informative action: K is a trap

    return go(inst.full if K is None else K)


def far_pairs(inst):
    for a, b in itertools.combinations(range(inst.n), 2):
        P = 1 << a | 1 << b
        if inst.far(P):
            yield P


def find_trap_pairwise(inst):
    """Exact when traps are closed under subsets, e.g. with no safety constraints."""
    return next((P for P in far_pairs(inst) if inst.is_trap(P)), None)


def find_trap_closure(inst):
    """Exact when every action is unsafe for at most one parameter. Grow the least
    trap containing a far pair: a safe informative action u with unsafe set {w}
    forces w into every trap that contains the current set."""
    assert inst.unsafe_size() <= 1
    for K in far_pairs(inst):
        while True:
            u = next((u for u in inst.safe(K) if inst.informative(K, u)), None)
            if u is None:
                return K
            U = inst.actions[u][0]
            if not U:
                break                         # an always-safe action kills every superset
            K |= U
    return None


def find_trap_small(inst, k):
    """Search far traps of cardinality <= k. Exact whenever some far trap has a far
    trap of size <= k inside it, e.g. k = sigma + 2 (Theorem G1)."""
    for size in range(2, k + 1):
        for c in itertools.combinations(range(inst.n), size):
            K = sum(1 << i for i in c)
            if inst.far(K) and inst.is_trap(K):
                return K
    return None


def safety_witness_number(inst, K):
    """sigma(K) = min |W|, W subset of K, with S(W) = S(K): a minimum hitting set of
    the nonempty traces U(u) & K. Brute force."""
    hit = [U & K for U, _ in inst.actions if U & K]
    if not hit:
        return 0
    idx = list(members(K))
    for size in range(1, len(idx) + 1):
        for c in itertools.combinations(idx, size):
            W = sum(1 << i for i in c)
            if all(h & W for h in hit):
                return size
    raise AssertionError("unreachable")


# ---------------------------------------------------------------- constructions

def not_both(n, a, b):
    """Always safe, binary, Y(a) = {0}, Y(b) = {1}, everyone else {0, 1}:
    kills exactly the sets containing both a and b."""
    return 0, (((1 << n) - 1) & ~(1 << b), ((1 << n) - 1) & ~(1 << a))


def bit_actions(n, unsafe):
    """ceil(log2 n) deterministic binary actions with the given unsafe set. Together
    they separate every pair, so they kill every K with |K| >= 2 that avoids `unsafe`."""
    full = (1 << n) - 1
    out = []
    for k in range(max(1, (n - 1).bit_length())):
        one = sum(1 << i for i in range(n) if bits(i, k))
        out.append((unsafe, tuple(r for r in (full & ~one, one) if r)))
    return out


def singles_out(n, unsafe, x):
    """Deterministic binary action separating x from the rest."""
    full = (1 << n) - 1
    return unsafe, (1 << x, full & ~(1 << x))


def lit(v):
    return 2 * (abs(v) - 1) + (0 if v > 0 else 1)


def sat_u3(nvars, clauses):
    """3-SAT -> trap existence. Binary observations, every unsafe set = one clause
    (<= 3 parameters). Traps are the consistent literal sets meeting every clause."""
    nvars = max(nvars, 2)                     # a trap needs two parameters
    n = 2 * nvars
    acts = [not_both(n, 2 * v, 2 * v + 1) for v in range(nvars)]
    for c in clauses:
        # OR, not sum: a repeated literal must not carry into the next bit
        acts += bit_actions(n, _or(1 << lit(x) for x in c))
    return Instance(n, acts)


def sat_u2(nvars, clauses):
    """3-SAT -> trap existence with every unsafe set of size <= 2. Per clause
    (l1 v l2 v l3) two auxiliary parameters s, s' with exactly one in the trap,
    s' => (l1 or l2), s => l3."""
    nvars = max(nvars, 2)
    n = 2 * nvars + 2 * len(clauses)
    acts = []
    for v in range(nvars):
        T, F = 2 * v, 2 * v + 1
        acts.append(not_both(n, T, F))
        acts += bit_actions(n, 1 << T | 1 << F)
    for j, c in enumerate(clauses):
        if not c:
            acts += bit_actions(n, 0)         # empty clause: nothing survives
            continue
        l = [lit(x) for x in c] + [lit(c[-1])] * (3 - len(c))
        s, s2 = 2 * nvars + 2 * j, 2 * nvars + 2 * j + 1
        acts.append(not_both(n, s, s2))
        acts += bit_actions(n, 1 << s | 1 << s2)
        acts.append(singles_out(n, 1 << l[0] | 1 << l[1], s2))
        acts.append(singles_out(n, 1 << l[2], s))
    return Instance(n, acts)


def satisfiable(nvars, clauses):
    return any(all(any((x > 0) == bs[abs(x) - 1] for x in c) for c in clauses)
               for bs in itertools.product([False, True], repeat=nvars))


def cycle_trap(n):
    """Minimal trap of size n with n actions and deterministic binary observations:
    a_j is unsafe only for j and reports whether theta = j + 1 (mod n)."""
    return Instance(n, [singles_out(n, 1 << j, (j + 1) % n) for j in range(n)])


def interval_instance(h, unsafe, delta, points=None, eps=0):
    """Observations Y(theta, u) = [h - delta, h + delta]. h[theta][u] rational or int."""
    n, m = len(h), len(h[0])
    acts = []
    for u in range(m):
        vals = sorted({h[t][u] for t in range(n)})
        # the response changes only at h +- delta, so these candidates see every response
        cand = sorted({v + s * delta for v in vals for s in (-1, 1)})
        cand += [(a + b) / 2 for a, b in zip(cand, cand[1:])]
        R = {sum(1 << t for t in range(n) if abs(y - h[t][u]) <= delta) for y in cand}
        acts.append((unsafe[u], tuple(r for r in R if r)))
    return Instance(n, acts, points, eps)


def binary_to_intervals(inst):
    """Binary observations as intervals: {0} -> h = -1, {1} -> h = 1, {0,1} -> h = 0,
    delta = 3/5. Only the overlap pattern matters, so traps are unchanged."""
    from fractions import Fraction
    h = [[0] * len(inst.actions) for _ in range(inst.n)]
    for u, (_, R) in enumerate(inst.actions):
        assert len(R) <= 2
        for t in range(inst.n):
            ys = [y for y, r in enumerate(R) if r >> t & 1]
            h[t][u] = 0 if len(ys) == 2 else (-1 if ys == [0] else 1)
    return interval_instance(h, [U for U, _ in inst.actions], Fraction(3, 5), inst.points, inst.eps)


def convex_trap(n):
    """Points (i, i^2) in the plane, linear safety, linear interval observations.
    Action a_k is unsafe iff 2k x - y - k^2 + 1/2 > 0, i.e. only at the k-th point
    ((i - k)^2 < 1/2), and observes x with delta = 1/4."""
    from fractions import Fraction
    pts = [(i, i * i) for i in range(n)]
    unsafe = [sum(1 << i for i, (x, y) in enumerate(pts) if 4 * k * x - 2 * y - 2 * k * k + 1 > 0)
              for k in range(n)]
    h = [[x for _ in range(n)] for x, _ in pts]
    return interval_instance(h, unsafe, Fraction(1, 4)), pts, unsafe


def realize(n, nontraps, pairs=None):
    """An instance whose non-traps of size >= 2 are exactly `nontraps`.
    Without `pairs`: one action per N, unsafe outside N, Y(theta) = N minus theta,
    which kills exactly N inside N's safe region. With pairs[N] = {p, q}: a binary
    (interval-realizable) action that kills exactly [P, N] = {K : P <= K <= N}."""
    full = (1 << n) - 1
    acts = []
    for N in nontraps:
        if pairs is None:
            acts.append((full & ~N, tuple(full & ~(1 << y) for y in members(N))))
        else:
            p, q = members(pairs[N])
            acts.append((full & ~N, (full & ~(1 << q), full & ~(1 << p))))
    return Instance(n, acts)


def random_instance(rng, n, m, alphabet=2, p_unsafe=0.25, max_unsafe=None, deterministic=False,
                    p_multi=0.4):
    acts = []
    for _ in range(m):
        U = [t for t in range(n) if rng.random() < p_unsafe]
        if max_unsafe is not None:
            U = rng.sample(U, min(len(U), max_unsafe))
        Y = []
        for _ in range(n):
            if deterministic or rng.random() > p_multi:
                Y.append({rng.randrange(alphabet)})
            else:
                Y.append(set(rng.sample(range(alphabet), rng.randint(1, alphabet))))
        acts.append(action_from_sets(n, sum(1 << t for t in U), Y))
    return Instance(n, acts)
