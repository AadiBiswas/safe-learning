# Theorem register

*Stage 0, 2026-11-20. IDs are stable: a result keeps its ID if it is later strengthened, refuted or found in the literature, and the status column records the change.*

**Status codes:**
- **P**: proved in this repository;
- **P-std**: proved here, but by a standard argument (no contribution claimed);
- **N**: numerical evidence only;
- **C**: conjecture;
- **O**: open question;
- **R**: refuted;
- **K**: known in the literature.

**Abbreviations.** SA = `research/scalar_analysis.md`, FA = `research/finite_analysis.md`, RD = `research/research_directions.md`, LR = `research/literature_review.md`.

## Scalar model ($\theta^\* x \le 1$; $Y = \theta^\* x^p + \eta$, $|\eta| \le \delta$)

| ID | Statement | Status | Proof | Checks |
|---|---|---|---|---|
| S1 | One experiment at $x > 0$: the adversary can produce exactly the sets $\Theta_t \cap I$, with $I$ any closed interval of length $2\delta x^{-p}$ containing $\theta^\*$. | P | SA §2 | — |
| S2 | Maximum safe intensity $x_t = 1/U_t$ is worst-case optimal for every inclusion-monotone objective, at every horizon, instance-wise and uniformly. Consequently no policy separation exists in the scalar model. | P (elementary coupling) | SA §3 | `scalar_check` §C: 80,000 coupled steps, 0 violations |
| S3 | Instance-wise: $\eta \equiv \delta$ maximises $U_T$, so $U_{t+1} = \min(U_t, \theta^\* + 2\delta U_t^p)$; and $L_t = \theta^\*$ for all $t \ge 1$. Any $\vert\eta_t\vert \le \delta$ is consistent. | P | SA §4 | §D |
| S4 | Full fixed-point and basin structure for every $p > 0$. The threshold is $\lambda_c = (p-1)^{p-1}/p^p$ for $p > 1$; $8\delta\theta^\* = 1$ and $U_\pm = (1 \pm \sqrt{1 - 8\delta\theta^\*})/(4\delta)$ at $p = 2$; $\delta = 1/2$ at $p = 1$; no threshold for $p < 1$. | P | SA §5 | §A, §B, §F, §G |
| S4a | At $\lambda = \lambda_c$ nothing moves. The passage time from $v_c$ is $\Theta\bigl((\lambda_c - \lambda)^{-1/2}\bigr)$, equal to $\operatorname{artanh}(s)/\sqrt{\lambda_c - \lambda}$ at $p = 2$ (normal-form calculation). | P (normal form) + N | SA §6 | §F: fitted exponent −0.506; constant 2.646 against 2.647 |
| S4b | The asymptotic upper bound is discontinuous in $\delta$ and in $U_0$ at the unstable fixed point $v_+$. | P | SA §7 | — |
| S5 | **Uniform one-shot trap.** $\inf_\pi\sup_{\theta^\*,\eta}\operatorname{diam}\Theta_T = \min(U_0 - L_0, 2\delta U_0^p)$ for every $T \ge 1$, attained at $T = 1$. | P | SA §8 | §E |
| S6 | Total deadlock iff $2\delta U_0^p \ge U_0 - L_0$. For $p > 1$ and $L_0 \ge 0$ it is implied by $U_0 \ge (2\delta)^{-1/(p-1)}$. | P | SA §8 | — |
| S7 | Favourable data ($+\delta$ then $-\delta$) identify $\theta^\*$ exactly in two experiments. | P | SA §9 | §H |
| S8 | The instance-wise asymptotic set $[\theta^\*, \theta^\* v_-]$ satisfies the trap condition with equality. | P | SA §8 | — |

## Finite spaces (Direction B)

| ID | Statement | Status | Proof | Checks |
|---|---|---|---|---|
| F1 | Uniform $\varepsilon$-identifiability holds iff there is no trap of diameter $> \varepsilon$. | P-std (attractor / minimal losing set) | FA §2 | `finite_game`: 3,000/3,000 random instances agree |
| F2 | An optimal policy uses at most $\vert\Theta_0\vert - 1$ experiments, and every one of its experiments strictly shrinks the set. Tight. | P | FA §2 | ratio 1.000 attained |
| F3 | Without safety constraints, with interval observations: identifiable iff every far pair is separated by some action. Polynomial. | P | FA §3 | — |
| F4 | With robust safety and interval observations: trap existence ($\varepsilon = 0$) is NP-complete; identifiability is coNP-complete. | P (3-SAT reduction) | FA §3 | 400/400 random 3-SAT instances (232 satisfiable) |
| F5 | **Non-locality.** For every $n$ there is a trap of size $n$ with every proper subset identifiable in one experiment. In particular, pairwise safe distinguishability does not imply safe identifiability. | P | FA §3 | $n \le 7$ checked; 30/3,000 random instances are pairwise-OK but not identifiable |

## Multidimensional (Direction C)

| ID | Statement | Status | Proof | Checks |
|---|---|---|---|---|
| C1 | Linear observation $\theta^\top u$, linear safety $\theta^\top u \le 1$, $u \ge 0$, $\Theta_0 \subset \mathbb R^d_{>0}$: $K$ is a trap iff every coordinate projection is a scalar trap, $\min K_i \ge (1 - 2\delta)\max K_i$. Coupling creates no new traps. | P | RD, Direction C | `tests/test_linear_traps.py` (random point sets) |
| C1a | If negative action components are allowed while $\Theta_0 \subset \mathbb R^d_{>0}$, then identification is immediate (unbounded safe scaling). | P (one line) | RD, Direction C | — |

## Conjectures and open questions

| ID | Statement | Status |
|---|---|---|
| Q-F1 | One policy identifies exactly those $\theta^\*$ contained in no trap of diameter $> \varepsilon$ (the instance-wise version of F1). | O |
| Q-F2 | Trap detection is polynomial for threshold-monotone safety, for linear structures, and for other natural classes. A dichotomy? | O |
| Q-F3 | Continuum: the worst-case asymptotic diameter equals $\sup\operatorname{diam}$ over closed traps (compact $\Theta_0$, continuous $g$, $h$). | C (holds in the scalar model: S5, S8) |
| Q-F4 | The minimum number of experiments is NP-hard to approximate within $o(\log n)$ (via test cover). | C |
| Q-C2 | Genuinely $d$-dimensional traps exist when safety and observation use different linear functionals of $\theta$. | C |
| Q-C3 | There is a safe-identification model with a large *uniform* adaptivity gap. In the scalar model there is none. | O |
| Q-E1 | The risk-allowance frontier is continuous at $\epsilon = 0$ under bounded noise. | O (model not yet fixed) |

## Refuted or corrected (from the brief)

| Item | Correction |
|---|---|
| "Ability to reduce the upper bound depends on $8\delta\theta^\* < 1$" (read as a learnability criterion) | True **instance-wise** only. The criterion involves the unknown $\theta^\*$. The uniform worst case has no threshold (S5). |
| Tracking only the upper endpoint | Under the same worst case the lower endpoint is identified exactly at $t = 1$ (S3). |
| "A deliberately less informative experiment may be better" (as a scalar possibility) | Refuted in the scalar model (S2). Still open in richer models. |
| "Each coordinate identifiable but not the vector" (as a linear-model possibility) | Refuted for the natural linear model at the level of traps (C1). Still open for richer models (Q-C2). |

## Literature status

See LR §2. Nothing here is labelled novel. F1 is standard in technique. F4 and F5 are "potentially distinct", pending the active-diagnosis complexity literature (Haar–Haddad–Melliti–Schwoon) and safe diagnosability (Paoli–Lafortune).

---

# Stage 1 additions (2026-11-21)

**Abbreviations.**
- FT = `research/finite_trap_theory.md`
- CA = `research/complexity_analysis.md`
- CO = `research/continuum_analysis.md`
- GO = `research/geometric_obstructions.md`

**Checks.**
- E003 = `scripts/stage1_finite.py` → `results/stage1_finite.txt`
- E004 = `scripts/critical_scaling.py` → `results/critical_scaling.txt`

**Additional status codes.**
- **P-known**: proved here, and also a special case of a published result.
- **K?**: possibly known; literature question open.

## Status changes to Stage 0 items

| ID | Change |
|---|---|
| F1 | Generalized to arbitrary set-valued observations, an adaptive adversary and randomized policies (T1). Uniform ⇔ eventual ⇔ within $n-1$ steps. Still **P-std**. Its deterministic special case is **P-known** (Hierons–Türker 2014). |
| F2 | Generalized: *every* myopic policy succeeds within $n-1$ steps (T2). |
| F3 | **Corrected (strengthened).** The pairwise test needs no Helly property. Downward closure gives it for every observation model (B1). |
| F4 | **Strengthened** to H1. Both directions re-proved and degenerate inputs handled. The $n=1$ padding is necessary. Not subsumed by the literature read (LR §6.4). |
| F5 | **Strengthened** to T5: the exact minimum is $n$ experiments, and binary deterministic observations suffice. |
| S4a | **Sharpened** to S4a′: exact constant for all $p>1$, with explicit hypotheses on start and target. |
| Q-F1 | **Resolved: yes** (T3). |
| Q-F2 | **Largely resolved** (CA §0 classification). The fixed-dimension geometric case remains open (G-O1). |
| Q-F3 | **Resolved, conditionally** (K1–K3). True under (L); false without it (X1). |
| Q-F4 | Partly addressed. OPTCOUNT is NP-hard without safety (via literature, **A**), coNP-hard with safety, and in PSPACE. |

## New results

| ID | Statement | Status | Proof | Checks |
|---|---|---|---|---|
| T1 | Characterization for set-valued observations; randomization does not help against adaptive noise. | P-std; deterministic case P-known | FT §2 | E003 §A: 4000/4000 |
| Ob | Oblivious noise with randomization can identify inside a trap. Adaptivity of the noise is essential to T1. | P (example) | FT §2 | — |
| T2 | No far trap ⇒ every myopic safe-informative policy succeeds within $n-1$ experiments. Tight. | P | FT §3 | E003 §A |
| T3 | One myopic policy achieves the instance-wise minimax terminal diameter $D(\theta^\*)$ for every $\theta^\*$ simultaneously. | P; K? (folklore-level) | FT §3 | — |
| T4 | Restriction is hereditary. Independent products: trap ⇔ both projections are traps, and counts add. No closure under union, intersection, subsets, supersets, or projection of joint products. | P | FT §4 | E003 §I (explicit counterexamples; random products) |
| W / G1 | Every far trap contains a far trap of size $\le\sigma(K)+2$ ($\max(2,\sigma)$ at $\varepsilon=0$). | P | FT §5, GO §1 | E003 §E |
| T5 | A minimal trap of size $k\ge3$ has $\sigma=k$, hence $\ge k$ experiments unsafe on it. The cycle trap realizes it with $n$ experiments and binary deterministic observations. | P | FT §5 | E003 §H ($n\le8$) |
| T6 | Every family of subsets is a trap family. | P | FT §6 | E003 §J (all $2^{11}$ families, $n=4$) |
| M | $\mathrm{TRAP}\in\mathrm{NP}$, $\mathrm{SAFEID}\in\mathrm{coNP}$ under the explicit and interval encodings. | P | CA §1 | — |
| B1 | No safety ⇒ pairwise test, for any metric and any observation model. | P | CA §2 | E003 §D |
| H1 | NP-complete trap existence with (a) binary observations and $\lvert U\rvert\le2$; (b) $\lvert U\rvert\le3$ and $n+m\lceil\log 2n\rceil$ experiments; (c) intervals of common width; (d) linear safety and linear sensing in unbounded dimension. | P; originality open (LR §6.5) | CA §3 | E003 §F (309/309 and 146/146, including degenerate formulas), §G |
| P2 | Deterministic observations ⇒ split recursion, $O(n^2m)$. | P-known | CA §4 | E003 §B |
| P3 | $\lvert U\rvert\le1$ ⇒ Horn closure, $O(n^3m)$. With H1(a), a dichotomy in the unsafe-set size. | P | CA §4 | E003 §C |
| P4 | $\sigma\le k$ ⇒ $O(n^{k+2}m)$. Covers nested safety, 1-D thresholds (pairs), $k$ functionals, $k$ experiments (XP). | P | CA §4 | E003 §E |
| P5 | Promise of small minimal traps ⇒ enumeration. | P | CA §4 | — |
| G1′ | **Exact local-to-global** ($\varepsilon=0$): "identifiable iff all $k$-subsets are" holds for all sub-instances ⇔ minimal traps have size $\le k$ ⇔ $\sigma\le k$ on minimal traps. | P | GO §1 | via T5, E003 §H |
| G2 | Observation Helly number $h$ ⇒ a set is a trap if all its $\le h$-subsets are. This gives nothing for trap existence. | P | GO §2 | — |
| G2b | Characterization of the trap families realizable with Helly-$h$ observations. With $h=2$, intervals realize them: 1218 of 2048 families on 4 points. | P | GO §2 | E003 §J |
| G3 | Halfspace safety: $\sigma\le\lvert\operatorname{ext}\operatorname{conv}K\rvert$. $d=1$ ⇒ pairs. $d=2$ ⇒ minimal traps of every size (convex position, linear sensing). Unbounded $d$ ⇒ NP-complete. | P | GO §3 | E003 §H |
| G4 | Homogeneous experiments where safety and sensing share one functional ⇒ traps are hereditary ⇒ pairwise. Explains C1. | P | GO §4 | (C1 tests) |
| K1 | Continuum: under compactness, continuity of $g$, closed-graph $\mathcal Y$ and (L), no closed trap of diameter $\ge\varepsilon$ ⇒ uniform finite horizon. | P | CO §2 | — |
| K2 | Closed traps form a closed family. The minimax asymptotic diameter is $D^\*=\max$ closed-trap diameter, reached in finite time above $D^\*$. | P | CO §2 | scalar case = S5 |
| K3 | Under (L): eventual ⇒ uniform. | P | CO §2 | — |
| X1–X4 | Counterexamples: no (L) (admissibility in the limit); the critical tolerance; non-closed graph; joint discontinuity. | P | CO §3 | — |
| S4a′ | Fold passage time $\sqrt\epsilon N\to(\operatorname{artanh}\rho+\operatorname{artanh}s)/\sqrt{ab}$, with $ab=\tfrac12p^{p-1}(p-1)^{2-p}$. Same exponent for relaxation at $v_-$. | P (Euler/normal-form argument) + N | SA §6a | E004: within 0.1% for $p=1.5,2,3$ |

## Open after Stage 1

| ID | Question |
|---|---|
| G-O1 | Complexity of trap existence for halfspace safety in fixed dimension $d\ge2$. |
| G-O2 / Q-C2 | Large minimal traps with full scaling but different safety and sensing functionals? |
| G-O3 | A continuum analogue of $\sigma$ and a continuum local-to-global theorem. |
| Q-K1 | Eventual ⇒ uniform under continuity alone, without (L)? |
| Q-K2 | A universal instance-optimal policy in the continuum. |
| Q-K3 | Quantitative horizons $T(\varepsilon)$. |
| Q-K4 | A relaxed-trap characterization without (L). |
| Q-P1 | Exact complexity of OPTCOUNT with safety; FPT status of TRAP in the number of experiments. |
| Q-C3 | Uniform adaptivity gap (unchanged). |
| Q-E1 | Risk-allowance frontier (unchanged; model not fixed). |

---

# Stage 2 additions (2026-11-22)

**Abbreviations.**
- LI = `research/linear_identifiability.md`
- WG = `research/witness_geometry.md`
- AW = `research/approximate_witnesses.md`
- CO §7 = the Stage 2 section of `research/continuum_analysis.md`

**Checks.** E005 = `scripts/stage2_checks.py`.

## Status changes

| ID | Change |
|---|---|
| H1 | **Literature status settled** (LR §7.1). Türker et al. 2023 contains the static model, as self-loop observable partial NFSMs, but proves hardness only for forest size, with dynamics. So it gives an upper bound, not H1's lower bound. H1 is a sharper classification of a special case. |
| P2 | Unchanged: P-known (Hierons–Türker 2014). |
| G3 | **Sharpened** by L3: minimal traps have size $\le c(\Theta_0)$, not $c+2$. |
| Q-K3 | **Answered** (Q1′, Q2): yes, via the margin $\mu(\varepsilon)$, and no margin-free bound exists. |
| G-O1 | **Still open** (LI §5). The obstruction is identified (L10). |

## New results

| ID | Statement | Status | Proof | Checks |
|---|---|---|---|---|
| L1 | Linear model: trap ⇔ every experiment is blocked ($h_K(a)>b$) or blind ($w_K(c)\le2\delta$). | P | LI §2 | E005 §A: 48,520/48,520 |
| L2 | Hull invariance of the trap, far, safe-set and diameter properties. | P | LI §2 | E005 §B |
| L3 | Minimal far traps are in convex position; size $\le c(\Theta_0)$. | P | LI §2 | E005 §B (weak: 2 instances) |
| L4 | A minimum witness may need a non-vertex: $\sigma(K)<\sigma(V(K))$ is possible. | P (example) | LI §2 | E005 §D |
| L5 | $d=1$: pairs, $O(n^2m)$. | P | LI §3.1 | E005 §E |
| L6 | NP-complete with $d$ in the input, even with convex position, common $\delta$, and laminar unsafe traces of size $\le2$. | P | LI §3.2 | E005 §H |
| L7 | XP $O(n^{r+2}m)$ in the number of safety rays $r$; W[1]-hard in $r$ ($d$ unbounded), via multicolored clique. | P | LI §3.3 | E005 §G |
| L8 | Opposite-ray safety ⇒ pairs at $\varepsilon=0$. | P | LI §3.4 | — |
| L9 | Aligned parabola: minimal traps of size $n$ in the plane for $n\ge4$. | P | LI §3.4 | E005 §I ($n\le8$) |
| L10 | An always-safe "not both" constraint forces opposite caps. | P | LI §5 | — |
| W1 | $\sigma\le r$ (one maximizer per ray); sharp; opposite rays count twice. | P | WG §1 | E005 §C |
| W2 | $\sigma\le\min(r,\lvert V(K)\rvert,\lvert B(K)\rvert)$; no dimension bound; $\sigma(K)\le\sigma(V(K))$, possibly strictly. | P | WG §2 | E005 §D |
| W3 | Computing $\sigma$: NP-complete and $(1-o(1))\ln$-inapproximable for linear safety with $d$ unbounded. | P (inapproximability cited, A) | WG §3 | — |
| W4 | $\sigma$: $d=1$ trivial; planar convex position exact via circular arcs, $O(km\log m)$; planar general polynomial. | P / P / cited (A) | WG §3 | E005 §F: 12,647/12,647 |
| W5 | $\sigma$ NP-hard in $d=3$, even in convex position (paraboloid lifting of DUDC). | P from cited NP-hardness (A) | WG §3 | — |
| A1 | Support-function sampling: error $\le2R\rho$. | P (classical) | AW §1 | E005 §J |
| A2 | $\sigma_\gamma\le N(S^{d-1},\gamma/2R)$, with intrinsic dimension replacing $d$. Lower bound $\Omega((R/\gamma)^{(d-1)/2})$ for the sphere, exactly $\lceil\pi/\arccos(1-\gamma/R)\rceil$ in $d=2$. | P (sharp upper exponent cited) | AW §1 | E005 §J: $\sqrt\gamma\,\sigma_\gamma\to2.227$ (prediction 2.221) |
| A2′ | Robust Lemma W: a far trap of the $\gamma$-tightened model with $\le\sigma_\gamma+2$ points. | P | AW §1 | — |
| CandA, CandB | Net perturbations, for nets inside the set: safety tightened by $L_gh$ (A); noise enlarged by $L_hh$ (B). | P | AW §2 | E005 §K: 33,056 pairs |
| A3 | Two-sided net certificates are sound. | P | AW §3 | — |
| A4 | Completeness of the upper certificate under density and $D^\*<\varepsilon$, and of the lower certificate for margin-robust traps. | P | AW §3 | — |
| X5 | Certificates can fail forever: tangential safety (upper); zero-margin traps (lower). | P (example) | AW §3 | — |
| Q1 | Packing horizon $T\le M(\Theta_0,\mu/2L_h)$ under a uniform informativeness margin $\mu$. | P | CO §7 | — |
| Q1′ | Under the K1 hypotheses: $\mu(\varepsilon)>0$ and $T(\varepsilon)\le M(\Theta_0,\mu(\varepsilon)/4L_h)$. | P | CO §7 | — |
| Q2 | Exponent $d$ and scale $L_h/\mu$ are necessary (bump family). Without a margin, horizons are unbounded at fixed $d$, $D$, $L_g$, $L_h$. | P | CO §7 | — |
| Q3 | No universal approach rate to an asymptotic obstruction. | P | CO §7 | — |
| Q4 | The attainable accuracy can jump under arbitrarily small safety relaxation (X1). Under density, $\limsup_{\gamma\downarrow0}D^\*(\gamma)\le D^\*(0)$. | P | CO §7 | — |

## Open after Stage 2

| ID | Question |
|---|---|
| G-O1 | **Main open problem.** TRAP for the linear model in fixed $d=2$ or $d=3$: P or NP-hard? Partial results and the obstruction are in LI §§4–5. |
| W-O1 | Is TRAP FPT in the number of safety rays $r$ for fixed $d$? |
| W-O2 | Planar convex position: an algorithm polynomial in both $n$ and $r$? **Resolved negatively in Stage 3 (D2).** |
| Q-K4′ | Under density, is $D^\*(\gamma)\to D^\*(0)$ as the safety relaxation $\gamma\to0$? |
| Q-K5 | Bound the margin $\mu(\varepsilon)$ from quantitative regularity of $g$, $h$ and $\mathcal S$. |
| L-O1 | Orthogonal safety and observation directions: any structural effect? |
| Lit | Confirm Johnson 1982 (DUDC) for rational discrete inputs; confirm the Dudley / AHPV coreset size bound from text. |

---

# Stage 3 additions (2026-11-23)

**Abbreviations.**
- BF = `research/boolean_trap_formulation.md`
- FD = `research/fixed_dimension_complexity.md`
- GR = `research/geometric_realizations.md`

**Checks.** E006 = `scripts/stage3_checks.py`.

## Status changes

| ID | Change |
|---|---|
| G-O1 | **Resolved: coNP-complete for every fixed $d\ge2$** (D2, D3). The critical dimension is exactly 2. |
| W-O2 | **Resolved negatively** (D2): no polynomial algorithm in planar convex position unless P $=$ NP. |
| L10 | Retained and strengthened to an iff (R1). Its Stage 2 reading, "obstruction to fixed-$d$ hardness", is **corrected**: it obstructs only direct clause encodings. |
| L7 (wording) | **Corrected.** W[1]-hardness excludes FPT. It does not establish optimality of the XP exponent. |
| W5 | Still rests on a cited NP-hardness (Johnson 1982, unread). |

## New results

| ID | Statement | Status | Proof | Checks |
|---|---|---|---|---|
| B1 | Exact CNF form of trap existence, with minimal-conflict clauses (pairs under Helly 2). | P | BF §1 | E006 §A: 600/600 set-valued, 600/600 linear |
| B2 | $\lvert B\rvert\le1$ ⇒ Horn ⇒ P3. | P (standard) | BF §2 | E006 §A |
| B3 | The hardness language is Schaefer-hard; each clause type is needed. | P (classification standard) | BF §2 | — |
| B4 | Deterministic observations give complete-multipartite conflicts with no lone pair; hardness needs lone forbidden pairs. | P | BF §3 | — |
| D0 | NP / coNP membership in every dimension. | P | FD §1 | — |
| D1 | Zero-padding preserves instances exactly (dimension monotonicity). | P | FD §1 | E006 §C |
| **D2** | **$\mathrm{TRAP}_0$ is NP-complete in $\mathbb Q^2$** with: all parameters on the unit circle; laminar unsafe traces that are singletons or adjacent pairs; one-pair-or-all-pairs separation; common $\delta$; linear size. | **P** | FD §2 | E006 §B: 58/58 formulas, exact geometry, up to 138 parameters |
| **D3** | **Critical dimension $=2$:** P for $d=1$, coNP-complete for every fixed $d\ge2$. This also holds for $\varepsilon$-identification with every $\varepsilon<1$. | **P** | FD §2 | — |
| D4 | ETH ⇒ no $2^{o(n)}$ algorithm in the plane. | P (conditional on ETH) | FD §2 | — |
| D5 | XP $O(n^{2k+1}m)$ in the number $k$ of observation lines, in every dimension and for every safety structure. | P | FD §3 | E006 §D |
| R1 | A one-edge conflict graph is realizable iff the pair is strictly antipodal. | P | GR §1 | E006 §E |
| R2 | $O(n^{2d})$ realizable conflict graphs per configuration in $\mathbb R^d$. | P | GR §1 | — |
| R3 | Block sums preserve exact-identification instances; distances change. | P | GR §3 | E006 §C |
| R4 | Safety realizations: singletons; adjacent pairs on circles; arbitrary pairs in $\mathbb Q^4$; $k$-sets in $\mathbb Q^{2k}$. | P | GR §2 | — |
| R5 | One-edge gadgets: matchings in $\mathbb Q^2$, bipartite graphs in $\mathbb Q^3$; at most $n$ in the plane. | P / P / cited (A) | GR §1 | — |
| R6 | A joint circle realization exists for matched-pair instances with placeable adjacent pairs. | P | GR §3 | (D2 instances) |
| R7 | The binary-pattern interval encoding with $\delta=\tfrac12$. Linear realization of general binary patterns needs cap structure (remark). | P / remark | GR §4 | — |

## Open after Stage 3

| ID | Question |
|---|---|
| A-O1 | Aligned observations ($c_u\parallel a_u$) in the plane: P or coNP-complete? |
| A-O2 | Orthogonal observations ($c_u\perp a_u$) in the plane. |
| D-O1 | Is TRAP FPT, or W[1]-hard, in the number $k$ of observation lines? In $k+r$? |
| D-O2 | Planar instances whose observations are binary patterns with classes of size $\ge2$ (R7), with no lone pairs: P or coNP-complete? With only complete or empty conflict graphs the problem is trivial, since traps are then closed under supersets. |
| W-O1 | FPT in $r$ for fixed $d$ (unchanged). |
| Lit | Johnson 1982; the coreset size bound (unchanged). |

---

# Stage 4 additions and consolidation (2026-11-24)

**Abbreviations.**
- AI = `research/aligned_identifiability.md`
- PA = `research/planar_hardness_audit.md`
- CM = `research/complexity_map.md`
- MA = `research/mathematical_audit.md`

**Checks.**
- E007 = `scripts/verify_d2.py`
- E008 = `scripts/stage4_checks.py`

## New results

| ID | Statement | Status | Proof | Checks |
|---|---|---|---|---|
| AL0 | Aligned normal form ($\max q>\beta$ or range $\le t$). | P | AI §1 | — |
| AL1 | An aligned global lone pair meets every nonempty unsafe set. | P | AI §2 | E008 §A: 19,049 cases |
| AL2 | Aligned D2 family (global conflicts empty, complete or lone; $\lvert B\rvert\le2$ for complete) ⇒ 2-SAT, $O(n^2(n+m))$, any $d$, any $\varepsilon$. | P | AI §3 | E008 §B: 600/600 |
| AL3 | Aligned $\mathrm{TRAP}_0$ is NP-complete with $d$ unbounded ($\lvert B\rvert\le2$, convex position, common $\delta$). | P | AI §4 | E008 §C: 47/47 |
| AL4 | Planar convex position: aligned effective lone-pair implications are cyclically local. | P | AI §5 | — |
| W5′ | Computing $\sigma$ is NP-complete in $\mathbb Q^4$, in convex position, by a self-contained proof. | P | WG §3 | E008 §D: 200/200 |
| PA | D2 audit: both implications from the trap property alone; rational realization with an analytic distinctness proof; strict margins; $O(\log(n+m))$ bits per number; ETH in parameters, experiments and bit length; $\varepsilon<1$ via $\sqrt{306}/17$. | P (audit) | PA | E007: 48/48 formulas |

## Corrections (see MA §0)

- **C1.** D2's constant safety uses $b=1$, giving a strict margin.
- **C2.** D2 has $\le5n+11m$ experiments.
- **C3.** The B4 "lone pair" claim is reformulated as a property of all known constructions; D-O2 is open.
- **C4.** W5′ added.
- **C5, C6.** Recorded earlier (E005 generator; L7 wording).

## Status of principal results

| ID | Status | Depends on external citation? |
|---|---|---|
| T1 | P-std | no |
| T5, G1′ | P | no |
| H1 | P | no |
| P3 | P | no |
| D2, D3 | P (audited) | no |
| D4 | P, conditional on ETH and the sparsification lemma | standard complexity assumptions only |
| AL2, AL3 | P | no |
| K1–K3 | P | no |
| Q1′, Q2 | P | no |
| A3–A4 | P | no |
| W4(c) (planar $\sigma$ general) | cited (A) | yes; the convex case W4(b) is proved |
| W5 ($\sigma$, $d=3$) | cited (M) | yes; W5′ ($d=4$) is self-contained |
| A2 sharp exponent | cited (A) | yes; used only as a remark |

## Open after Stage 4

AL-O1 (aligned, fixed $d\ge2$), OR-O1 (orthogonal, plane), D-O1 (FPT in observation lines), D-O2 (no lone pairs), W-O1, Q-K1, Q-K4′, Q-K5.
