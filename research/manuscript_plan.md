# Manuscript plan (not manuscript text)

*2026-11-24. Repository IDs are kept, and no final numbering is assigned. This file proposes structure only.*

## 1. Theorem hierarchy

**Principal theorems** (the central contribution):

| ID | One line |
|---|---|
| T1 | Finite safe identifiability ⇔ no far informational trap. Adaptive noise; randomization does not help. |
| H1 + P3 + P2 + B1 | The finite complexity map: no safety → P; deterministic observations → P (known); ambiguous observations with safety → coNP-complete; unsafe sets of size 1 → P, size 2 → coNP-complete. |
| D2 + D3 | **Dimensional dichotomy:** linear safe identifiability is P for $d=1$ and coNP-complete for every fixed $d\ge2$, already on the unit circle. |
| T5 + G1′ | Minimal traps: $\sigma(K)=\lvert K\rvert$, and an exact local-to-global principle. |
| K1–K3 | Compact parameter spaces: the trap characterization under (L); eventual implies uniform. |

**Supporting theorems and propositions:**
- T2, T3 (myopic policy, instance optimality); Lemma W; T4; T6, G2b;
- L1–L3 (support-function traps, hull invariance, convex position); L5;
- L6, L7 (unbounded-dimension hardness; W[1] in safety rays); D5 (XP in observation lines);
- AL1–AL3 (alignment);
- R1 (lone pair ⇔ strict antipodality); D1 (padding);
- W1, W4 (σ ≤ rays; planar σ polynomial);
- Q1′, Q2 (horizons);
- A3, A4 (certificates).

**Illustrative results:**
- the scalar model S1–S8 and S4a′;
- the cycle trap and convex-position trap (T5(b), G3(c)); the aligned parabola L9;
- the counterexamples X1–X5 and Ob; the interior-witness example L4;
- the realizability examples R5.

**Technical results** (appendix candidates):
- the D2 gadget table and the full rational realization (`planar_hardness_audit.md` §§2, 4–5);
- the H1, L6 and AL3 constructions;
- the B1 conflict clauses and Schaefer classification (B2, B3);
- R2–R4, R6, R7; W5, W5′;
- A1, A2, A2′; CandA, CandB;
- AL4; OPTCOUNT; the circular-arc algorithm W4(b).

## 2. Dependency map for the principal theorems

| Theorem | Definitions | Lemmas used | External literature | Original arguments | Verification artifact | Unverified dependency? |
|---|---|---|---|---|---|---|
| T1 | safe set, response, trap, far, adaptive noise | lazy adversary | minimal-losing-set technique (standard) | the formulation | E002, E003 §A | no |
| H1 | T1, conflicts | M; gadgets N, Bits, O | 3-SAT (Karp) | the reduction | E003 §F, E006 | no |
| P3 | B1 | Horn least model | Horn-SAT (standard) | application | E003 §C | no |
| P2 | split recursion | — | Hierons–Türker 2014 (**known**) | simpler static proof | E003 §B | no |
| D2 | linear model, L1, T1 | R1, R4(a–b), the distinctness lemma (PA §4) | 3-SAT | the whole construction | E006 §B, E007 | no |
| D3 | D1, D2, L5 | — | — | — | E006 §C | no |
| D4 | D2 | the size bound (PA §6) | ETH, sparsification lemma | — | — | standard assumptions only |
| T5, G1′ | σ, Lemma W | — | — | yes | E003 §§E, H | no |
| K1–K3 | hyperspace, (L) | Lemmas 0–3 | Hausdorff compactness, Zorn | yes | — (analytic) | no |
| Q1′ | Δ, μ(ε), packing | K1, lower semicontinuity of Δ | volume bounds (standard) | yes | — | no |

**No principal theorem depends on an unverified citation or an unresolved proposition.** The cited-only items are:
- W4(c), the general planar σ;
- W5, σ in $\mathbb Q^3$;
- the sharp coreset exponent;
- OPTCOUNT hardness;
- R5(c).

All are supporting or illustrative.

## 3. Proposed narrative

The proposed order largely keeps the anticipated progression, with two changes. The Boolean formulation moves into the complexity chapter, and aligned functionals become part of the geometric chapter.

1. **Learning without making mistakes.**
   - The certified-safety loop: knowledge restricts experiments, and experiments produce knowledge.
   - Relation to SafeOpt reachability, self-confirming equilibrium, set-membership estimation, and partial-FSM testing.
2. **Model.** Finite and compact parameter sets; robust safety; bounded adaptive noise; uniform versus instance-wise guarantees.
3. **A scalar example** (S2, S3–S6, S4a′).
   - Its instance-wise threshold $\lambda_c$ is *not* a uniform transition. The uniform value is one-shot.
   - Motivates traps through the one-sided deadlock.
4. **Informational traps** (T1–T3, Ob). The characterization, myopic sufficiency, instance optimality, and why adaptivity of the noise matters.
5. **The structure of obstruction** (T4, T5, G1′, T6/G2b).
   - Minimal traps and σ; local-to-global; what Helly does and does not give.
6. **The computational complexity of safe learning** (B1, B2, H1, P2, P3, B3/B4).
   - The finite map. Safety and ambiguity are each harmless alone.
   - The negation primitive: a lone forbidden pair.
7. **The dimensional dichotomy** (L1–L3, L5, D1–D4).
   - Linear models; hull invariance; P in $d=1$; the unit-circle construction; ETH.
8. **Geometry that restores tractability** (L7, D5, L8, AL1–AL3, W1/W4 versus D2).
   - Directional parameters (XP, W[1]).
   - Alignment, which is tractable in the D2 family and hard in high dimension.
   - The σ-versus-identifiability separation in the plane.
9. **Compact parameter spaces** (K1–K3, X1–X4, the scalar consistency check).
10. **Quantitative guarantees** (Q1′, Q2, Q3, Q4, A2′–A4, X5). Horizons, certificates, and the impossibility of margin-free bounds.

**Main text versus appendices.**
- *Main text:* chapters 1–10 with the principal theorems and short proofs (T1, T5, G1′, P3, D3, AL1, AL2, K1).
- *Appendix:* full reductions (H1, L6, D2 with its rational realization, AL3, L7(b)); Boolean and Schaefer details; realization lemmas; the continuum lemmas; the approximation proofs; the computational verification.

## 4. Candidate figures

| Figure | Content | Data source |
|---|---|---|
| F1 | The safety–knowledge loop schematic | conceptual |
| F2 | Scalar map: fixed points, basins and the fold | `scripts/scalar.py`, `results/scalar_check.txt` §§B, F |
| F3 | Cycle trap / convex-position trap with $n=6$ (each point blocking "its" experiment) | `scripts/traps.py` `cycle_trap`; `convex_trap` |
| F4 | **D2 on the unit circle** for a small formula: upper and lower half, adjacent-pair caps, antipodal lone pairs | `scripts/planar_hardness.py` `build(2, [(1, -2), (-1, 2)])` |
| F5 | Complexity map as a diagram (`complexity_map.md` §2) | — |
| F6 | Aligned versus independent directions: AL1 picture (cap on top, lone pair as extremes) versus the AL3 effective pair | conceptual; AI §§2, 4 |
| F7 | X1: admissibility only in the limit (sets $[0,m_t]$ and the sharp experiment's safe region) | analytic, CO §3 |
| F8 | Approximate witnesses on the circle: $\sigma_\gamma\sim\pi/\sqrt{2\gamma}$ | `results/stage2_checks.txt` §J |
