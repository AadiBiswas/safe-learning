"""Stage 1 exhaustive checks for the finite theory (E003 in results/ledger.md).

    .venv/bin/python scripts/stage1_finite.py   ->  results/stage1_finite.txt

Every algorithm and construction in scripts/traps.py is compared with the
exhaustive solver Instance.value / Instance.traps on small instances. Agreement
here is a regression check, not the proof; the proofs are in research/*.md.
"""

import itertools
import random
import sys
from pathlib import Path

from traps import (Instance, action_from_sets, binary_to_intervals, convex_trap, cycle_trap,
                   find_trap_closure, find_trap_pairwise, find_trap_small, find_trap_split, members,
                   popcount, random_instance, realize, safety_witness_number, sat_u2, sat_u3,
                   satisfiable)

OUT = Path(__file__).resolve().parents[1] / "results" / "stage1_finite.txt"
SEED = 20261121
lines, failures = [], []


def log(s=""):
    lines.append(s)
    print(s)


def check(name, ok, detail=""):
    log(f"  [{'ok' if ok else 'FAIL'}] {name}{': ' + detail if detail else ''}")
    if not ok:
        failures.append(name)


def rand_inst(rng, **kw):
    n = rng.randint(2, 7)
    kw.setdefault("alphabet", rng.choice([2, 3, 4]))
    inst = random_instance(rng, n, rng.randint(1, 6), **kw)
    if rng.random() < 0.5:                    # metric version with a tolerance
        inst.points = sorted(rng.sample(range(12), n))
        inst.eps = rng.choice([0, 2, 4])
    return inst


def main():
    rng = random.Random(SEED)

    log("A. Characterization (F1') and experiment count (F2') with set-valued observations")
    agree = tot = worst_ratio = 0
    for _ in range(4000):
        inst = rand_inst(rng)
        v, T = inst.value(inst.full), inst.traps()
        tot += 1
        agree += (v is None) == bool(T)
        if v is not None and inst.n > 1:
            worst_ratio = max(worst_ratio, v / (inst.n - 1))
    check("identifiable <=> no far trap", agree == tot, f"{agree}/{tot}")
    check("optimal experiment count <= n - 1", worst_ratio <= 1, f"max ratio {worst_ratio:.3f}")
    # sharpness: equality tests on n points need n - 1 experiments
    for n in (3, 5, 8):
        inst = Instance(n, [(0, (1 << k, inst_full(n) & ~(1 << k))) for k in range(n)])
        check(f"equality tests, n = {n}: value n - 1", inst.value(inst.full) == n - 1)
    # myopic policies: if no trap, ANY safe informative action at every state succeeds
    ok = True
    for _ in range(1500):
        inst = rand_inst(rng)
        if inst.value(inst.full) is not None:
            ok &= all(inst.value(K) is not None for K in range(1, inst.full + 1))
    check("identifiable => every subset identifiable (so myopic play never gets stuck)", ok)

    log("\nB. Splitting recursion (exact always; laminar when observations are deterministic)")
    ag = tot = 0
    max_nodes = 0
    for _ in range(3000):
        inst = rand_inst(rng, deterministic=True)
        st = {}
        t = find_trap_split(inst, stats=st)
        tot += 1
        ag += (t is None) == (inst.value(inst.full) is not None) and (t is None or t in inst.traps())
        max_nodes = max(max_nodes, st.get("nodes", 0) / (2 * inst.n - 1))
    check("deterministic: split recursion = exhaustive", ag == tot, f"{ag}/{tot}")
    check("deterministic: nodes <= 2n - 1", max_nodes <= 1, f"max nodes/(2n-1) = {max_nodes:.3f}")
    ag = tot = 0
    for _ in range(3000):
        inst = rand_inst(rng)
        t = find_trap_split(inst)
        tot += 1
        ag += (t is None) == (inst.value(inst.full) is not None)
    check("general observations: split recursion = exhaustive", ag == tot, f"{ag}/{tot}")

    log("\nC. Closure algorithm when every unsafe set has size <= 1")
    ag = tot = 0
    for _ in range(3000):
        inst = rand_inst(rng, max_unsafe=1, p_unsafe=0.5)
        t = find_trap_closure(inst)
        tot += 1
        ag += (t is None) == (inst.value(inst.full) is not None) and (t is None or t in inst.traps())
    check("|U| <= 1: closure = exhaustive", ag == tot, f"{ag}/{tot}")

    log("\nD. No safety constraints: pairwise check, arbitrary set-valued observations")
    ag = tot = 0
    for _ in range(3000):
        inst = rand_inst(rng, p_unsafe=0.0)
        tot += 1
        ag += (find_trap_pairwise(inst) is None) == (inst.value(inst.full) is not None)
    check("no safety: pairwise = exhaustive", ag == tot, f"{ag}/{tot}")

    log("\nE. Safety-witness bound (G1): every far trap K contains a far trap of size <= sigma(K) + 2")
    ok, hist = True, {}
    for _ in range(1500):
        inst = rand_inst(rng, p_unsafe=0.4)
        T = set(inst.traps())
        for K in T:
            s = safety_witness_number(inst, K)
            ok &= any(K2 & K == K2 and popcount(K2) <= s + 2 for K2 in T)
        for K in inst.minimal_traps():
            key = (safety_witness_number(inst, K), popcount(K))
            hist[key] = hist.get(key, 0) + 1
    check("witness bound", ok)
    log(f"  (sigma, |minimal trap|) histogram: {dict(sorted(hist.items()))}")
    # nested (chain) safety: sigma <= 1, so ε = 0 traps are detected by pairs
    ag = tot = 0
    for _ in range(2000):
        n = rng.randint(2, 7)
        order = rng.sample(range(n), n)          # danger order: U(u) = first k of `order`
        acts = []
        for _ in range(rng.randint(1, 6)):
            k = rng.randint(0, n)
            Y = [set(rng.sample(range(3), rng.randint(1, 2))) for _ in range(n)]
            acts.append(action_from_sets(n, sum(1 << t for t in order[:k]), Y))
        inst = Instance(n, acts)
        tot += 1
        ag += (find_trap_pairwise(inst) is None) == (inst.value(inst.full) is not None)
    check("nested safety, eps = 0: pairwise = exhaustive", ag == tot, f"{ag}/{tot}")
    # one-dimensional threshold safety (every U is an up-set or a down-set of the line):
    # K is a far trap iff {min K, max K} is
    ag = tot = 0
    for _ in range(2000):
        n = rng.randint(2, 7)
        acts = []
        for _ in range(rng.randint(1, 6)):
            k = rng.randint(0, n)
            U = range(k, n) if rng.random() < 0.5 else range(0, k)
            Y = [set(rng.sample(range(3), rng.randint(1, 2))) for _ in range(n)]
            acts.append(action_from_sets(n, sum(1 << t for t in U), Y))
        inst = Instance(n, acts, points=sorted(rng.sample(range(15), n)), eps=rng.choice([0, 3]))
        ends = {1 << min(members(K)) | 1 << max(members(K)) for K in inst.traps()}
        tot += 1
        ag += all(inst.is_trap(E) for E in ends) and ((find_trap_pairwise(inst) is None) ==
                                                         (inst.value(inst.full) is not None))
    check("1-D threshold safety: endpoints of a trap form a trap", ag == tot, f"{ag}/{tot}")

    log("\nF. 3-SAT reductions (binary observations; |U| <= 3 and |U| <= 2)")
    cases = [(1, [(1,)]), (1, [(1,), (-1,)]), (2, []), (2, [()]), (2, [(1, 1, 1)]), (2, [(1, -1, 2)]),
             (3, [(1, 1, -2), (-1,), (2, 3)]), (3, [(1,), (-1, 2), (-2,)]), (4, [(1, 2, 3)])]
    for _ in range(300):
        nv = rng.randint(1, 4)
        k = rng.randint(0, 2 * nv) if rng.random() < 0.5 else rng.randint(3 * nv, 6 * nv)
        cases.append((nv, [tuple(rng.choice([-1, 1]) * rng.randint(1, nv) for _ in range(rng.randint(1, 3)))
                           for _ in range(k)]))
    for name, red, cap in (("U<=3", sat_u3, None), ("U<=2", sat_u2, 12)):
        ag = tot = nsat = 0
        for nv, cl in cases:
            inst = red(nv, cl)
            if cap and inst.n > cap:
                continue
            s = satisfiable(nv, cl)
            tot += 1
            nsat += s
            assert inst.unsafe_size() <= (3 if name == "U<=3" else 2)
            assert all(len(R) <= 2 for _, R in inst.actions)
            ag += s == (inst.value(inst.full) is None) == bool(find_trap_split(inst))
        check(f"reduction {name}: SAT <=> trap <=> not identifiable", ag == tot,
              f"{ag}/{tot}, {nsat} satisfiable (degenerate cases included)")

    log("\nG. Binary observations are interval observations")
    ag = tot = 0
    for _ in range(1500):
        inst = rand_inst(rng, alphabet=2)
        iv = binary_to_intervals(inst)
        tot += 1
        ag += set(iv.traps()) == set(inst.traps())
    check("same traps after the interval encoding", ag == tot, f"{ag}/{tot}")

    log("\nH. Large minimal traps")
    for n in range(3, 9):
        c = cycle_trap(n)
        g, pts, _ = convex_trap(n)
        check(f"n = {n}: cycle (binary, deterministic, n actions) and convex-position (linear) traps",
              c.minimal_traps() == [c.full] and g.minimal_traps() == [g.full]
              and all(g.value(K) is not None for K in range(1, g.full) if popcount(K) >= 2))
    ok = True
    for _ in range(2000):
        inst = rand_inst(rng, p_unsafe=0.4)
        inst.eps, inst.points = 0, list(range(inst.n))   # the bound is for exact identification
        for K in inst.minimal_traps():
            if popcount(K) >= 3:
                ok &= sum(1 for U, _ in inst.actions if U & K) >= popcount(K)
    check("eps = 0: a minimal trap of size k >= 3 meets >= k unsafe sets (random instances)", ok)

    log("\nI. Closure properties of the trap family (explicit counterexamples)")
    full3, full4 = 7, 15
    union = Instance(3, [action_from_sets(3, 0, [{0}, {0, 1}, {1}])])
    check("not closed under union: {0,1}, {1,2} traps, {0,1,2} not",
          union.is_trap(0b011) and union.is_trap(0b110) and not union.is_trap(full3))
    inter = Instance(4, [action_from_sets(4, 0b1100, [{0}, {1}, {0}, {0}])])
    check("not closed under intersection: {0,1,2}, {0,1,3} traps, {0,1} not",
          inter.is_trap(0b0111) and inter.is_trap(0b1011) and not inter.is_trap(0b0011))
    c3 = cycle_trap(3)
    check("not closed under subsets: cycle trap of size 3, no 2-subset is a trap",
          c3.is_trap(full3) and not any(c3.is_trap(P) for P in (3, 5, 6)))
    check("not closed under supersets: union example", union.is_trap(3) and not union.is_trap(full3))
    # restriction to a subset of parameters: traps of the restriction are the traps inside it
    ok = True
    for _ in range(500):
        inst = rand_inst(rng)
        sub = rng.randrange(1, inst.full + 1)
        idx = list(members(sub))
        rest = Instance(len(idx), [(sum(1 << j for j, t in enumerate(idx) if U >> t & 1),
                                    tuple(r for r in (sum(1 << j for j, t in enumerate(idx) if R >> t & 1)
                                                      for R in Rs) if r))
                                   for U, Rs in inst.actions],
                        [inst.points[t] for t in idx], inst.eps)
        lift = lambda K: sum(1 << idx[j] for j in members(K))  # noqa: E731
        ok &= {lift(K) for K in rest.traps()} == set(inst.traps(within=sub))
    check("hereditary: traps of a restriction = traps contained in it", ok)
    # products with independent experiments: K trap iff both projections are traps
    ok = True
    for _ in range(300):
        A, B = (random_instance(rng, rng.randint(2, 3), rng.randint(1, 3), p_unsafe=0.3) for _ in range(2))
        P = product_disjoint(A, B)
        for K in range(1, P.full + 1):
            pa, pb = project(K, A.n, B.n)
            ok &= P.is_trap(K) == (A.is_trap(pa) and B.is_trap(pb))
        ok &= (P.value(P.full) is None) == (A.value(A.full) is None or B.value(B.full) is None)
        if P.value(P.full) is not None:
            ok &= P.value(P.full) == A.value(A.full) + B.value(B.full)
    check("disjoint-action product: traps = sets with trap projections; counts add", ok)
    # joint actions (u_A, u_B) both applied: a parameter with no safe action couples the factors
    A = Instance(2, [(0, (1, 2))])                     # identifiable in one experiment
    B = Instance(1, [(1, (1,))])                       # single parameter, its action unsafe
    J = product_joint(A, B)
    check("joint-action product: A identifiable, B trivial, A x B is a trap", A.value(A.full) == 1
          and J.is_trap(J.full) and J.value(J.full) is None)

    log("\nJ. Realizability of trap families (n = 4, all 2^11 families)")
    n = 4
    sets2 = [K for K in range(1, 1 << n) if popcount(K) >= 2]
    ok_all, n_int = True, 0
    for mask in range(1 << len(sets2)):
        N = [sets2[i] for i in range(len(sets2)) if mask >> i & 1]
        Ns = set(N)
        ok_all &= set(K for K in sets2 if not realize(n, N).is_trap(K)) == Ns
        # interval condition: each N contains a pair P with every K in [P, N] a non-trap
        pairs = {}
        for X in N:
            for p, q in itertools.combinations(members(X), 2):
                P = 1 << p | 1 << q
                if all(K in Ns for K in sets2 if K & P == P and K & X == K):
                    pairs[X] = P
                    break
        if len(pairs) == len(N):
            n_int += 1
            inst = realize(n, N, pairs)
            iv = binary_to_intervals(inst)
            ok_all &= set(K for K in sets2 if not iv.is_trap(K)) == Ns
    check("every family is a trap family; interval-condition families realized by intervals", ok_all,
          f"{n_int}/{1 << len(sets2)} families satisfy the interval (Helly-2) condition")

    text = "\n".join(lines) + "\n"
    OUT.write_text(text)
    log(f"\n{len(failures)} failures")
    return 1 if failures else 0


def inst_full(n):
    return (1 << n) - 1


def project(K, na, nb):
    pa = pb = 0
    for t in members(K):
        pa |= 1 << (t % na)
        pb |= 1 << (t // na)
    return pa, pb


def product_disjoint(A, B):
    """Parameter (a, b) is index a + na * b. Actions of A act on the A coordinate only."""
    na, nb = A.n, B.n
    n = na * nb
    lift = lambda f, M: sum(1 << (a + na * b) for a in range(na) for b in range(nb) if f(a, b, M))  # noqa
    acts = [(lift(lambda a, b, M: M >> a & 1, U), tuple(lift(lambda a, b, M: M >> a & 1, r) for r in R))
            for U, R in A.actions]
    acts += [(lift(lambda a, b, M: M >> b & 1, U), tuple(lift(lambda a, b, M: M >> b & 1, r) for r in R))
             for U, R in B.actions]
    return Instance(n, acts)


def product_joint(A, B):
    na, nb = A.n, B.n
    n = na * nb
    idx = lambda a, b: a + na * b  # noqa: E731
    acts = []
    for (UA, RA), (UB, RB) in itertools.product(A.actions, B.actions):
        U = sum(1 << idx(a, b) for a in range(na) for b in range(nb) if UA >> a & 1 or UB >> b & 1)
        R = tuple(sum(1 << idx(a, b) for a in range(na) for b in range(nb) if ra >> a & 1 and rb >> b & 1)
                  for ra in RA for rb in RB)
        acts.append((U, tuple(r for r in R if r)))
    return Instance(n, acts)


if __name__ == "__main__":
    sys.exit(main())
