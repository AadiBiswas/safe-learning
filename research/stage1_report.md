# Stage 1 report — Structural foundations of safe identifiability

*2026-11-21. This is a self-contained handoff. Proofs are in the files cited, every result has an ID in `research/theorem_register.md`, and computations are recorded in `results/ledger.md` (E003, E004).*

## 1. The problem, briefly

An agent may run only experiments that are safe for *every* parameter still consistent with its data. Observations are bounded and worst-case, so the consistent set $\Theta_t$ determines the certified-safe experiments $\mathcal S(\Theta_t)$, and those experiments determine how $\Theta_t$ shrinks.

A **trap** is a set $K$ such that every experiment certified safe for $K$ has an observation compatible with all of $K$. Stage 0 found that traps characterize uniform identifiability in finite models, and that safety appeared to make the question coNP-complete.

Stage 1 asked four things:
- whether these claims survive scrutiny;
- whether they are already known;
- which restrictions make the problem tractable;
- whether the theory extends to compact parameter spaces and to geometric structure.

## 2. Answers to the six questions

1. **Does safety introduce a distinct computational obstruction?** Yes, though more precisely than Stage 0 said.
   - Without safety, identifiability of an explicit static instance is decided by a pairwise test, *for every observation model* (B1).
   - With safety it is coNP-complete (H1).
   - The hardness is an **interaction** between safety and overlapping, i.e. noisy, observations. Safety with deterministic observations is polynomial (P2, known), and so is overlap without safety (B1).
2. **Can it be characterized structurally?** Yes, at three levels.
   - Traps characterize identifiability (T1).
   - The **safety-witness number** $\sigma(K)$ characterizes when small traps exist. $\sigma(K)$ is the least number of members of $K$ that already block every experiment $K$ blocks.
   - The exact statement is G1′: identifiability is decided by $k$-subsets, for all sub-instances, iff every minimal trap has $\sigma\le k$. A minimal trap of size $k\ge3$ always has $\sigma=k$: every member individually blocks a distinct experiment (T5).
3. **Which restrictions make it tractable?**
   - no safety;
   - deterministic observations;
   - every experiment unsafe for at most one parameter (Horn closure, P3);
   - bounded $\sigma$, which covers nested safety, one-dimensional thresholds (the scalar model), safety through $k$ fixed functionals, and $k$ experiments;
   - homogeneous experiments in which safety and sensing share a functional (G4).

   **Hardness persists** with:
   - binary observations and unsafe sets of size 2, so the size-1/size-2 boundary is a dichotomy;
   - interval observations of a common width;
   - linear safety and linear sensing in unbounded dimension.
4. **Does the finite theory extend to compact or geometric spaces?**
   - **Compact spaces: yes, conditionally** (K1–K3). The extra condition is lower semicontinuity of the certified-safe correspondence, (L), which holds when strictly safe experiments are dense in the safe ones. Under (L):
     - no closed trap of diameter $\ge\varepsilon$ gives a uniform finite horizon;
     - the minimax asymptotic diameter is the largest closed-trap diameter;
     - eventual identification implies uniform identification.
   - **Without (L) it fails** (X1). The failing mechanism is the one the brief anticipated: an informative experiment that becomes admissible only in the limit of an infinite descent.
   - **Geometric spaces.** Geometry bounds obstructions only through safety (G3):
     - one dimension gives pairs;
     - in the plane, points in convex position give minimal traps of every size, even with linear safety and linear sensing.
5. **Are there local-to-global principles?** Yes, two of them, and they must not be conflated.
   - *Trap existence* is local exactly to the degree that $\sigma$ is bounded (G1, G1′). The bound is sharp.
   - *Non-trap-ness* is local to the observation Helly number $h$ (G2). This is the wrong direction for identification: deterministic observations ($h=2$) still allow minimal traps of every size.
   - G2b characterizes which trap families are realizable under a Helly bound. Every family is realizable without one (T6).
6. **What is potentially original?** See §5.

## 3. Stage 0 claims after scrutiny

| Stage 0 claim | Stage 1 verdict |
|---|---|
| F1 trap characterization | **Survives and generalizes** (T1): arbitrary set-valued observations, randomized policies. **Correction:** it needs *adaptive* noise. With oblivious noise a randomizing agent can escape a trap (example Ob). |
| F2, at most $n-1$ experiments | **Survives and strengthens** (T2): *any* myopic safe-informative policy succeeds. No lookahead is needed. |
| F3, unconstrained ⇒ pairwise "by Helly" | **Corrected.** Helly is irrelevant; downward closure suffices, for every observation model (B1). |
| F4, coNP-complete | **Survives.** Both directions re-proved and degenerate cases audited (CA §3): $n=1$ needs a padding variable, and my first Stage 1 encoding summed bitmasks of repeated literals instead of OR-ing them (the exhaustive check caught it). **Strengthened** to binary observations with unsafe sets of size $\le2$. |
| F5, non-locality | **Survives and is explained** (T5): the minimum number of experiments for a minimal trap of size $n$ is exactly $n$, and binary observations suffice. |
| Q-F1, price of not knowing $\theta^\*$ | **Resolved: it is zero** (T3). One myopic policy is instance-wise minimax for every $\theta^\*$ simultaneously. |
| Q-F3, continuum | **True under (L), false without it** (K1, X1). The scalar model satisfies (L), and K2 recovers S5. |
| C1, linear model decouples | **Explained** by G4. Shared-functional homogeneous models have hereditary traps. |
| S4a, $(\lambda_c-\lambda)^{-1/2}$ | **Survives, sharpened** (S4a′). Exact constant $(\operatorname{artanh}\rho+\operatorname{artanh}s)/\sqrt{ab}$ for every $p>1$. It is a statement about passage through the fold, with the start scaled to the basin. It is instance-wise only: the uniform problem has no slowing down (S5). |

## 4. What is already in the literature (`research/literature_review.md` §6)

- **Deterministic static identifiability under robust safety is known** (Hierons–Türker 2014; full text read).
  - A static instance is a partially specified FSM with self-loops. Their adaptive distinguishing sequences must use inputs "defined in all states" of the current set, which is exactly robust safety.
  - They prove existence polynomial. My P2 is that result's static case.
- **Active diagnosis (Haar et al.; JCSS text read) does not subsume this work.**
  - Their hidden object is an evolving fault event, admissibility does not depend on the hidden state, and the hardness is EXPTIME via imperfect-information safety games.
  - The static problem sits at coNP.
- **Nondeterministic distinguishing.** ACY 1995 (EXPTIME-complete) and Türker et al. 2023 (PSPACE-hard, partial nondeterministic FSMs) contain the static nondeterministic model as a special case. They supply *upper* bounds only, and their hardness uses dynamics.
  - **This is the main open originality question for H1:** whether any of this work proves hardness that survives the restriction to self-loops. I could not extract the 2023 paper's text.
- **Set-membership experiment design** (Shakouri et al. 2026; partly read) is offline and unconstrained. It does not treat uncertainty-dependent admissibility. Its "uniformly discrete prior" condition for exact identification under noise parallels the noise floor $D^\*$.
- Stage 0's framing items are unchanged:
  - SafeOpt's reachability closure;
  - self-confirming equilibrium and incomplete learning;
  - minimum-height decision trees, for experiment counts.

## 5. Potentially original contributions

In decreasing weight:
1. **The complexity classification** (CA §0).
   - H1: hardness with binary observations and unsafe sets of size 2.
   - P3: polynomial at size 1.
   - B1 and P2: each mechanism alone is polynomial.

   This is the strongest candidate. It is a structural dichotomy, not just a hardness proof, and it is not in the sources read. Pending §4's open question.
2. **The safety-witness number as the governing invariant** (T5, G1, G1′, P4). One quantity explains:
   - the arbitrarily large minimal traps;
   - the exact local-to-global principle;
   - the tractable classes;
   - why one-dimensional (scalar) models are easy and planar convex-position models are not.
3. **The continuum theorem with (L) and its counterexamples** (K1–K3, X1–X4). Standard tools, but a clean, correct statement whose condition has a transparent meaning: safety must not be attainable only tangentially. It connects the scalar example to the finite theory.
4. **G4** (shared-functional homogeneity ⇒ hereditary traps) and **G2b** (realizable trap families). Smaller.
5. **T3** (universal instance-optimal policy). Simple; probably folklore.

## 6. Strongest results, stated

- **H1.** Trap existence is NP-complete, and identifiability coNP-complete, already for binary observations ($\mathcal Y\in\{\{0\},\{1\},\{0,1\}\}$) with every experiment unsafe for at most two parameters. The same holds for interval observations of a common width, and for linear safety with linear sensing in unbounded dimension.
  - *Proof:* a 3-SAT reduction using three gadgets: "not both", "at least one, via bit experiments", and "implication". Each kills an exactly specified family of sets.
- **P3.** If every experiment is unsafe for at most one parameter, a least trap containing any pair is computed by closure, in $O(n^3m)$.
  - *Proof:* the trap constraints are Horn.
- **T5 / G1′.** A minimal trap $K$ of size $\ge3$ has $\sigma(K)=\lvert K\rvert$. "Identifiable iff all $k$-subsets are", for all sub-instances, holds iff every minimal trap has $\sigma\le k$.
  - *Proof:* any minimum witness set, plus a far pair, is a trap inside $K$.
- **K1–K3.** Assume compact $\Theta_0,\mathcal U$, continuous safety, closed-graph observations, and (L). Then, for each $\varepsilon>0$, uniform finite-time identification to $<\varepsilon$ holds iff no closed trap has diameter $\ge\varepsilon$, and eventual implies uniform.
  - *Proof:* the adversary-survival sets $W_t$ are closed and up-closed in the Hausdorff hyperspace. Their intersection has a minimal element by Zorn, and a minimal element is a trap.

## 7. Important counterexamples

- **X1:** compact and continuous, yet the agent is stuck at diameter $\ge\tfrac12$ while every trap has diameter $\le0.02$. (L) fails at the limit set.
- **X2:** the critical tolerance is never reached, and $T(\varepsilon)\to\infty$ as $\varepsilon\downarrow D^\*$.
- **X3:** a non-closed graph, where the adversary holds an open trap.
- **X4:** eventual ≠ uniform without joint continuity.
- **Ob:** oblivious noise lets randomization escape traps.
- **Closure failures** of the trap family under union, intersection, subsets and supersets, and projection failure for joint products: all with 3–4 parameters (FT §4).
- **The cycle trap and the convex-position trap:** $\Theta_0$ is the only trap of size $\ge2$, every proper subset is identified in one experiment, and $\sigma=n$.

## 8. Computation and verification

- **`scripts/traps.py`.** An exact solver over bitmask subsets, used as the reference, plus every algorithm and construction above.
- **`scripts/stage1_finite.py`** (E003, about 3 s) checks against the reference:
  - the characterization: 4000 random instances;
  - each polynomial algorithm: 3000 instances each;
  - the witness bound;
  - both reductions, including degenerate formulas;
  - the interval encoding;
  - the large-trap constructions up to $n=8$;
  - the closure counterexamples;
  - all $2^{11}$ trap families on 4 points.

  All checks pass. One encoding bug (repeated literals) was found and fixed.
- **`scripts/critical_scaling.py`** (E004) checks the fold asymptotics to within 0.1%.
- **`tests/`**: 30 tests (11 new), all passing.
- **No proof relies on computation.** The arithmetic is exact (integers, bitmasks, `Fraction`) wherever it decides a claim.

## 9. Recommended focus for Stage 2

**Recommendation.** The paper's core should be *safe identifiability as a structural and computational problem*. The parts:
- the trap characterization as the formulation (T1, K1–K3);
- $\sigma$ as the governing invariant (T5, G1′);
- the complexity dichotomy (H1, P3, P2, B1);
- the scalar model as the worked example that sits in the tractable threshold class.

Stage 2 in order:
1. **Close the literature question for H1** (LR §6.5 items 1–2). This is a one-session task. If a self-loop hardness result exists, H1 becomes a corollary, and the contribution shifts to the classification and to $\sigma$.
2. **G-O1, fixed-dimension halfspace safety.** This is the most natural "realistic restriction" left open. A polynomial algorithm, or hardness in $d=2$ or $d=3$, would complete the geometric picture. Bounded VC dimension of the unsafe traces is the starting point.
3. **A continuum $\sigma$ and local-to-global theorem** (G-O3, Q-K4). This connects the finite invariant to K1. The natural candidate is the support function of $\operatorname{conv}K$ on the experiment normals.
4. Secondary: Q-C2/G-O2 (different safety and sensing functionals with full scaling), and quantitative horizons (Q-K3).

**Not recommended:**
- the exact complexity of OPTCOUNT (tangential);
- Direction E, whose model is still unfixed;
- any RL or large-scale simulation.

## 10. Files

| File | Content |
|---|---|
| `research/finite_trap_theory.md` | T1–T6, Ob |
| `research/complexity_analysis.md` | M, B1, H1, P2–P5, OPTCOUNT, literature comparison |
| `research/continuum_analysis.md` | K1–K3, X1–X4, scalar check |
| `research/geometric_obstructions.md` | G1, G1′, G2, G2b, G3, G4 |
| `research/scalar_analysis.md` §6a | S4a′ |
| `research/literature_review.md` §6 | Stage 1 sources, comparison table, verdicts, open questions |
| `research/theorem_register.md` | All IDs, Stage 1 status changes |
| `scripts/traps.py`, `scripts/stage1_finite.py`, `scripts/critical_scaling.py` | Code and checks |
