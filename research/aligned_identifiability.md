# Stage 4 — Aligned safety and sensing

*2026-11-24. Code: `scripts/linear.py` (`aligned`, `aligned_2sat_trap`, `aligned_sat_u2`). Checks: `scripts/stage4_checks.py`, output `results/stage4_checks.txt` (ledger E008).*

## 0. Summary

| ID | Statement | Status |
|---|---|---|
| AL0 | Normal form: with orientation chosen, every aligned experiment reads "$\max_Kq>\beta$ or $\max_Kq-\min_Kq\le t$" for a single projection $q$. | proved |
| AL1 | **Lone-pair alignment lemma.** If an aligned experiment's *global* conflict graph is a single pair $\{i,j\}$, then its unsafe set is empty or contains $i$ or $j$. The clause is then $\neg x_i\vee\neg x_j$ or a tautology. | proved |
| AL2 | **Aligned tractability in the D2 family.** Take aligned experiments with global conflict graphs that are empty, complete, or a single pair, where complete ones have $\lvert B_u\rvert\le2$. Then $\mathrm{TRAP}_\varepsilon$ reduces to 2-SAT with two forced ones, and is polynomial in every dimension. | proved |
| AL3 | **Alignment alone does not remove hardness.** Aligned $\mathrm{TRAP}_0$ is NP-complete when $d$ is part of the input, even with: $\lvert B_u\rvert\le2$; parameters in convex position (the standard basis); a common noise radius; and effective conflict graphs that are complete, a single pair, or a star. | proved |
| AL4 | **Locality.** On a convex configuration in the plane, an aligned experiment whose *effective* conflict graph is one pair $\{x,w\}$, with nonempty unsafe arc $V$, forces $x$ to be cyclically adjacent to $V$ and $w$ to be the unique minimum. So aligned implications are local. | proved |
| AL-O1 | Aligned $\mathrm{TRAP}$ in fixed dimension $d\ge2$, including the unit circle. | **open**. AL4 and a bounded-width sketch suggest tractability for the D2-type family in the plane, but this is unproved. |
| OR-O1 | Orthogonal functionals in the plane. | **open**. The quarter-turn constraint is recorded. |

**Answers to the brief's questions 1 and 2.**
- **Q1: yes.** Within the exact experiment family of D2 (global conflicts complete or a lone pair, unsafe sets of size $\le2$), aligning safety and sensing makes safe identifiability polynomial (AL2). Since D2 shows the same family is coNP-complete with independent directions, **in that family, hardness requires safety and sensing to act through different functionals.**
- **Q2: partly.**
  - In unbounded dimension, alignment does not help (AL3). The reason is precise: the conflicts that matter are those *outside* the unsafe set (B1). Alignment constrains global lone pairs (AL1), but not effective ones.
  - In fixed dimension the aligned classification is open. In the plane, AL4 shows that the effective lone pairs that alignment permits are geometrically local. That is the reason to expect tractability there, but no algorithm is proved.

## 1. The aligned model

**Definition.** Experiment $u$ is **aligned** if $c_u\ne0$ and $a_u=\lambda_uc_u$ with $\lambda_u\ne0$.
- $\lambda_u>0$: **positive alignment**. The unsafe set is an upper cap of $q=c_u^\top\theta$.
- $\lambda_u<0$: **negative alignment**. The unsafe set is a lower cap.
- $\lambda_u=1$: identical functionals.
- *Parallel* means either sign.

**Exclusions.**
- Experiments with $a_u=0$ (constant safety) or $c_u=0$ (blind) are **not aligned**. Constant safety with $c_u\ne0$ is the unrestricted "always safe" gadget, and it is exactly what D2 uses.
- "Always safe" is still available to aligned experiments, through a threshold above $\max\lambda_uq$.
- Stage 0's shared-functional model, with freely scaled actions, is a different and stronger restriction. It is not used here: Stage 1's G4 needs that scaling.

> **AL0.** For an aligned $u$, put $v_u=\operatorname{sign}(\lambda_u)\,c_u$, $q_i=v_u^\top\theta_i$, $\beta_u=b_u/\lvert\lambda_u\rvert$ and $t_u=2\delta_u$. Then $u$ is blocked by $K$ iff $\max_Kq>\beta_u$, and blind iff $\max_Kq-\min_Kq\le t_u$.

*Proof.*
- $a_u^\top\theta=\lvert\lambda_u\rvert\,v_u^\top\theta$.
- The width is invariant under $c\mapsto-c$. ∎

## 2. The lone-pair alignment lemma

> **Lemma AL1.** Let $u$ be aligned, and suppose its global conflict graph $P_u=\{ij : \lvert q_i-q_j\rvert>2\delta_u\}$ is exactly $\{\{i,j\}\}$. Then either the unsafe set $B_u$ is empty, or $B_u\cap\{i,j\}\ne\varnothing$.

*Proof.*
- By R1, $\{i,j\}=\{\arg\min q,\arg\max q\}$, and both extremes are unique.
- By AL0, a nonempty $B_u$ is an upper cap of $q$ (positive alignment) or a lower cap (negative alignment), so it contains the maximizer or the minimizer.
- Ties do not arise, because the extremes are unique. ∎

*Check:* 19,049 (experiment, threshold) cases with a single global conflict, in $d=1,2,3$, under both orientations (E008 §A).

**What this rules out in D2.** D2's conditional gadgets imply$(x\to V)$ have $V$ nonempty and disjoint from the lone pair $\{x,w_x\}$. By AL1 they cannot be aligned.
- The gadgets **force** (complete conflicts, cap $\{w\}$) and **some** (complete conflicts, cap $\{s,s'\}$) can be aligned with a suitable direction. **notboth** (lone pair, $B=\varnothing$) can too.
- So exactly the implication gadgets rely on independent safety and observation directions.

## 3. Tractability in the D2 family

> **Theorem AL2.** Let every experiment be aligned, with global conflict graph empty, complete, or a single pair, and let every complete one have $\lvert B_u\rvert\le2$. Then $\mathrm{TRAP}_\varepsilon$ is decidable in $O(n^2(n+m))$ time after $O(mn\log n)$ preprocessing, in every dimension.

*Proof.* By B1, the clauses are as follows:
- empty conflicts: none;
- complete conflicts: $\bigvee_{k\in B_u}x_k$, under $\lvert K\rvert\ge2$, a positive clause of length $\le2$ (length 0 means no trap);
- one pair: by AL1, a tautology or $\neg x_i\vee\neg x_j$.

**Algorithm.**
- *Classification.* Each experiment's conflict graph is classified from its sorted projections. It is complete iff the minimum gap exceeds $2\delta$, and a single pair iff the unique minimum and maximum are the only pair beyond $2\delta$.
- *Solve.* Trap existence is 2-SAT with $x_i=x_j=1$, for some far pair $\{i,j\}$. Each 2-SAT instance with fixed literals takes linear time (implication graph, or Even–Itai–Shamir propagation). There are $O(n^2)$ far pairs.
- *Dimension.* The argument uses only projections, so it is dimension-free.
- *Approximate identification.* The cardinality condition becomes "some forced pair is far", exactly as in B1, and the same algorithm applies.
- *Regression:* 600/600 random instances in $d=1,2,3$, with both orientations and blind experiments, against exhaustive search (E008 §B). ∎

**Extension.** The proof uses only *effective* conflicts. So AL2 extends to every experiment whose effective conflict graph on $\Theta_0\setminus B_u$ is:
- empty;
- complete with $\lvert B_u\rvert\le2$; or
- a single pair with $B_u=\varnothing$.

Alignment is used only to exclude an effective lone pair with nonempty $B_u$, through AL1, when the effective pair is also global. **The extension fails exactly when an effective lone pair coexists with a nonempty unsafe set.** That is AL3's gadget.

## 4. Alignment is not enough in unbounded dimension

> **Theorem AL3.** $\mathrm{TRAP}_0$ restricted to aligned experiments ($a_u=c_u$) is NP-complete when $d$ is part of the input. This holds even with: parameters the standard basis of $\mathbb Q^N$, hence in convex position; $\lvert B_u\rvert\le2$; and a common noise radius after rescaling.

*Proof.*
- **Construction.** Realize the Stage 1 reduction `sat_u2` gadget by gadget (`aligned_sat_u2`).
  - Each experiment gets a projection $q=M\mathbf 1_V+g$, with unsafe set $V$ placed on top at value $\ge M$, and threshold between $\max g$ and $M$.
  - The pattern $g$ on the other points realizes the required effective conflicts:
    - **not both** $(a,b)$: $V=\varnothing$, $g=e_a-e_b$, $\delta=\tfrac35$. Lone pair, aligned with a threshold above everything.
    - **some** $(V)$: $g_t=3t$, $\delta=1$. Every pair outside $V$ conflicts.
    - **implies** $(x\to V)$: $g=2e_x$, $\delta=\tfrac35$. The effective conflicts form the star at $x$, and the conflicts between $V$ and others are inactive.
- **Correctness.** Each experiment imposes exactly the constraint of the corresponding `sat_u2` gadget, by B1. The reduction is then Stage 1's H1(a).
- **Common noise radius.** Rescale $(a,b,c)$ together.
- *Regression:* 47/47 formulas, including degenerate ones, with every experiment verified aligned (E008 §C). ∎

**Reading.** AL1 and AL3 together show that what matters is not whether the two functionals coincide, but whether an *effective* lone forbidden pair can coexist with a nonempty unsafe set.
- With aligned functionals, the unsafe cap sits at the top of the same order. So the conditional pair must be (second-from-top, bottom), not (top, bottom).
- In high dimension that is free.

## 5. The plane under alignment

> **Lemma AL4 (locality).** Let $\Theta_0$ be in strictly convex position in $\mathbb R^2$, and let $u$ be aligned with nonempty unsafe set $V$ and effective conflict graph exactly $\{\{x,w\}\}$. Then:
> - $V$ is an arc of the cyclic order;
> - $x$ is one of the two cyclic neighbours of $V$;
> - $w$ is the unique minimizer of $q$ over $\Theta_0$.

*Proof.*
- $V$ is an upper cap of $q$ (AL0), and caps of convex-position point sets are arcs.
- Effective conflicts live on $\Theta_0\setminus V$. By R1 applied there, $x$ and $w$ are the unique maximizer and minimizer of $q$ on $\Theta_0\setminus V$. The maximizer cannot be $w$, which is the global minimizer.
- Along the cyclic order of a strictly convex configuration, a linear functional is **unimodal**: it is non-decreasing up to its maximum region and non-increasing after it, because a line meets the boundary in at most two points. The upper cap $V$ is therefore an arc containing the maximum, and the largest value outside it is attained at one of its two neighbours. ∎

**Consequence.** In the plane, aligned implications join cyclic neighbours. Information can travel along the cycle only by chains of adjacent implications ("wires"), and wires cannot cross on a cycle. What else can create long-range constraints:
- lone-pair "not both" constraints, which join strictly antipodal pairs, a monotone family in rotating-calipers order;
- implications to a forced helper $w$ near the antipode;
- conflict graphs with many pairs, which AL4 does not cover.

**Sketch towards AL-O1 (not a proof).** Restrict to effective conflict graphs that are complete or a single pair, with $\lvert B\rvert\le2$, in planar convex position. Then every clause involves only:
- cyclic neighbours;
- strictly antipodal pairs, or the global minimum of a direction, which is again an antipodal-type pair.

The constraint graph would then be the cycle plus a calipers-monotone family of chords. Such graphs plausibly have bounded pathwidth (cf. Möbius ladders), which would give a polynomial DP. **Two points are unverified:** the pathwidth bound when a single vertex has a wide antipodal range, and the handling of the cardinality condition. **Precise open problem:** aligned TRAP in the plane, (a) for that restricted family, and (b) in general, where effective conflict graphs with many pairs are non-local.

## 6. Orthogonal functionals (secondary; OR-O1)

In the plane with $a_u\perp c_u$, on a strictly convex configuration:
- a global lone pair in direction $c$ is the unique extreme pair in $c$, near angles $\varphi_a\pm\tfrac\pi2$;
- the unsafe cap is around $\varphi_a$.

So an implication $x\Rightarrow V$, with lone pair $\{x,w\}$, needs $V$ a quarter-turn away from both $x$ and $w$.

**Effect on D2.** The copy-to-literal implications $\kappa\Rightarrow\ell$ then need every copy of $\ell$ at a quarter-turn from $\ell$, each the unique maximum of its own direction. Several copies are possible only when $\ell$'s normal cone is wide. I did not determine whether D2 can be rearranged to satisfy all quarter-turn constraints at once, so this remains open (OR-O1).
