# Definitive complexity map of safe identification (Stages 0–4)

*2026-11-21. This file is authoritative for complexity statements; individual documents hold the proofs.*

## 1. Conventions

**Problems.**
- $\mathrm{TRAP}_\varepsilon$: does a far trap exist? For $\varepsilon=0$, "far" means size $\ge2$; for $\varepsilon>0$, Euclidean diameter $>\varepsilon$.
- $\mathrm{SAFEID}_\varepsilon$: is $\Theta_0$ uniformly $\varepsilon$-identifiable by an adaptive robust-safe policy against adaptive bounded noise? It is the complement of $\mathrm{TRAP}_\varepsilon$ by Theorem T1.
- **Every hardness statement below is for TRAP. SAFEID has the complementary class:** NP-complete becomes coNP-complete, and W[1]-hard becomes co-W[1]-hard for the complement.

**Inputs.**
- Finite models: parameters and experiments explicitly listed; a safety matrix; observations either as explicit finite symbol lists or as rational intervals.
- Linear models: rational points and coefficients, in binary.
- $n$ parameters, $m$ experiments, $d$ the dimension.

**Observation models.**
- *Set-valued*: arbitrary finite sets.
- *Interval*: closed rational intervals, Helly number 2.
- *Deterministic*: singletons.
- *Linear*: $[c^\top\theta-\delta,c^\top\theta+\delta]$.

**Lone pair.** A **lone pair** of an experiment is a conflict $\{i,j\}$ such that neither member conflicts with anything else outside the unsafe set. It is *global* if it is the only conflict over all of $\Theta_0$.

## 2. The table

| # | Model and restriction | $\mathrm{TRAP}_\varepsilon$ | Hypotheses that matter | Reference | Literature |
|---|---|---|---|---|---|
| 1 | General finite, set-valued or interval | NP-complete | explicit encoding | Stage 1 M, H1 | static case of partial observable ND-FSMs. Known upper bounds (PSPACE / EXPTIME) via Türker et al. 2023 and ACY 1995. The lower bound was not found. |
| 2 | No safety constraints, any observation model | P, $O(n^2m)$ pair tests | pair-intersection test polynomial; diameter-type goal | B1 (Stage 1 §2) | elementary |
| 3 | Deterministic observations, any safety | P, $O(n^2m)$ | responses form a partition | P2 | **known:** Hierons–Türker 2014 (PSFSM ADS existence) |
| 4 | Unsafe sets of size $\le1$, any observations | P, $O(n^3m)$ | Horn clauses | P3, B2 | Horn-SAT technique standard; statement not found |
| 5 | Unsafe sets of size $\le2$, binary or interval observations | NP-complete | lone pairs and stars available | H1(a), (c) | not found |
| 6 | $\le2$, laminar | NP-complete | — | L6 (via `sat_laminar`) | not found |
| 7 | Nested unsafe sets (a chain) | P, $O(n^2m)$ at $\varepsilon=0$; $O(n^3m)$ in general | $\sigma\le1$ | P4 | — |
| 8 | Safety-witness number $\le k$ on far traps | P for fixed $k$ (XP), $O(n^{k+2}m)$ | Lemma W | P4 | — |
| 9 | Promise: minimal far traps of size $\le k$ | P for fixed $k$, $O(n^km)$ | promise | P5 | — |
| 10 | Linear, $d=1$ | P, $O(n^2m)$ | hull invariance | L5 | — |
| 11 | Linear, $d$ part of the input | NP-complete, even in convex position, common $\delta$, laminar size-$\le2$ | basis-vector embedding | L6 | — |
| 12 | **Linear, every fixed $d\ge2$** | **NP-complete**, even on the unit circle, common $\delta$, laminar size-$\le2$ arcs, conflicts all-or-one antipodal pair, and every $0\le\varepsilon<1$ | rational circle points; strict margins | **D2, D3** (audit: `planar_hardness_audit.md`) | not found (LR §8) |
| 13 | Linear, $\le r$ safety rays | XP, $O(n^{r+2}m)$ | $\sigma\le r$ | L7(a), W1 | — |
| 14 | — parameterized by $r$ | W[1]-hard, with $d$ unbounded | multicolored clique | L7(b) | — |
| 15 | Linear, $\le k$ observation lines | XP, $O(n^{2k+1}m)$, any $d$, any safety | guessed-extremes box | D5 | — |
| 16 | — parameterized by $k$ | **open** (FPT or W[1]-hard?) | — | D-O1 | — |
| 17 | Linear, safety normals on one line ($\pm a$) | P at $\varepsilon=0$, $O(n^2m)$ | — | L8 | — |
| 18 | Linear, aligned ($a_u=\lambda_uc_u$), global conflicts empty, complete or lone, complete ones with $\lvert B\rvert\le2$ | **P**, $O(n^2(n+m))$, any $d$ | AL1 ⇒ 2-SAT | **AL2** | not found |
| 19 | Linear, aligned, $d$ part of the input | NP-complete, even with $\lvert B\rvert\le2$, convex position, common $\delta$ | effective lone pairs and stars | **AL3** | not found |
| 20 | Linear, aligned, fixed $d\ge2$ (incl. the unit circle) | **open** | AL4 locality | AL-O1 | — |
| 21 | Linear, orthogonal ($a_u\perp c_u$), plane | **open** | quarter-turn constraint | OR-O1 | — |
| 22 | Homogeneous shared functional, freely scaled actions | P (pair tests) | full scaling | G4 | — |
| 23 | Least worst-case number of experiments (OPTCOUNT) | NP-hard even without safety (cited); coNP-hard with safety; in PSPACE | — | Stage 1 §6 | Hyafil–Rivest; Laber–Nogueira (A) |

**Restrictions that do not restore tractability, as distinct from merely permitting large minimal traps:**
- **Proved hard:** convex position (rows 11, 12), unit circle (12), common noise (12), laminarity (6, 12), aligned functionals in unbounded dimension (19).
- **Large minimal traps only, complexity open:** aligned in the plane (L9 gives minimal traps of every size, but row 20 is open).
- **Large minimal traps, yet polynomial:** deterministic observations (row 3; the cycle trap is deterministic) and $d=1$ (row 10, where minimal traps are pairs).

## 3. The safety-witness number versus identifiability

> **Separation (planar).** For finite $K\subset\mathbb Q^2$ and linear safety:
> - **computing** $\sigma(K)$ is polynomial (W4(c)). The convex-position case W4(b) is proved here; the general planar case is cited (Har-Peled–Lee 2012; arXiv:2506.16979; access A).
> - **deciding** $\mathrm{SAFEID}$ is coNP-complete (D2).

*Hypotheses.*
- The $\sigma$ result needs only the safety halfplanes and $K$.
- The hardness instance lies on the unit circle, where W4(b) applies with a self-contained proof.

So the separation is fully proved on the unit circle: polynomial $\sigma$ (W4(b)) together with coNP-complete identifiability (D2). It is clean: **the geometry of safety alone cannot determine the complexity of safe learning; the interaction with sensing does.**

**In three dimensions**, $\sigma$ is NP-hard:
- in $\mathbb Q^3$ via DUDC (W5; Johnson 1982 cited, unread);
- independently in $\mathbb Q^4$ via vertex cover on pairs of the moment curve (W5′: R4(c) makes any graph's edges halfspace traces, and $\sigma$ becomes minimum vertex cover).

## 4. The status of "hardness needs a lone forbidden pair"

This is **not** a theorem about all observation models. What is proved:
- (i) **Deterministic observations** have no lone pairs when $n\ge3$ (B4), and are polynomial (P2).
- (ii) **Every hardness reduction in this project** (H1, L6, D2, AL3) uses lone pairs or stars as its negation primitive.
- (iii) **In the aligned D2 family, global lone pairs cannot be conditional** (AL1), and the family becomes polynomial (AL2).

What is open: whether observation families with no effective lone pairs, but with richer conflict graphs (for example complete bipartite between classes of size $\ge2$), can be NP-hard (D-O2). The correct reading is: *lone pairs are the negation primitive of all known hardness constructions, and removing them removes hardness in the families studied.*

## 5. Parameterized and exponent statements

| Statement | Exact form |
|---|---|
| L7(a) | XP in the number of safety rays $r$: $O(n^{r+2}m)$. |
| L7(b) | TRAP parameterized by $r$ is W[1]-hard ($d$ unbounded). So TRAP has no $f(r)\,\mathrm{poly}$ algorithm unless FPT $=$ W[1], and the same holds for SAFEID. **No claim that $r+2$ is the optimal exponent.** |
| D5 | XP in the number of observation lines $k$: $O(n^{2k+1}m)$. FPT status open. |
| D4 | Under ETH: no $2^{o(n)}$ and no $2^{o(m)}$ algorithm for $\mathrm{TRAP}^{(2)}_0$, and no $2^{o(L/\log L)}$ in bit length $L$. It follows from sparsified 3-SAT through D2's linear-size reduction. No exponent bound for L7 or D5 follows. |
