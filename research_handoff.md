# Research handoff — Can You Learn Without Making Mistakes?

## Fundamental limits of information acquisition under safety constraints

*Sourcebook for manuscript development. 2026-11-21. Repository `~/code/safe-learning`, branch `main`. The final commit and test count are in §14.*

**How to use this document.**
- §§1–12 state the mathematics with complete hypotheses, and point to the authoritative proof location for each result.
- §13 holds research-status notes: what is cited, what is open, what is weak. **Keep §13 out of manuscript prose.**
- IDs are the repository's stable identifiers (`research/theorem_register.md`).

---

## 1. Formal model and notation

**Finite model.**
- $\Theta_0$: a finite parameter set, with metric $d$.
- $\mathcal U$: a finite experiment set.
- For each experiment $u$:
  - an **unsafe set** $B_u=\{\theta : u\text{ unsafe for }\theta\}$;
  - an **observation correspondence** $\theta\mapsto\mathcal Y(\theta,u)$, nonempty subsets of an observation space.
- The **certified-safe set** of $K\subseteq\Theta_0$ is $\mathcal S(K)=\{u : B_u\cap K=\varnothing\}$.
- **Protocol.**
  - $\Theta_t$ starts at $\Theta_0$. The agent chooses $u_t\in\mathcal S(\Theta_t)$.
  - Nature reports $y_t\in\mathcal Y(\theta^\*,u_t)$. **The report is adaptive:** it may depend on the history and on $u_t$.
  - The consistent set updates to $\Theta_{t+1}=\{\theta\in\Theta_t : y_t\in\mathcal Y(\theta,u_t)\}$.
- **Goal.** Uniform identification to tolerance $\varepsilon\ge0$: a policy such that for all $\theta^\*$ and all admissible reports, $\operatorname{diam}\Theta_t\le\varepsilon$ eventually. Exact identification is $\varepsilon=0$, i.e. $\Theta_t=\{\theta^\*\}$.

**Linear model.**
- $\Theta_0\subset\mathbb Q^d$, and experiments $(a_u,b_u,c_u,\delta_u)$.
- $u$ is unsafe for $\theta$ iff $a_u^\top\theta>b_u$, so it is safe at equality.
- The observation is $\mathcal Y(\theta,u)=[c_u^\top\theta-\delta_u,\ c_u^\top\theta+\delta_u]$, a closed interval.
- Support function $h_K(v)=\max_Kv^\top\theta$; width $w_K(v)=h_K(v)+h_K(-v)$.

**Compact model.**
- $\Theta_0$, $\mathcal U$ and the observation space are compact metric spaces.
- Safety is $g(\theta,u)\le0$ with $g$ continuous.
- $\mathcal Y$ has a closed graph.
- Consistent sets are closed, and live in the hyperspace $\mathcal K$ of nonempty closed sets with the Hausdorff metric.

**Scalar model.**
- $\theta^\*\in[L_0,U_0]$ with $L_0>0$.
- Intensity $x\ge0$, safe iff $\theta x\le1$.
- Observation $Y=\theta x^p+\eta$, $\lvert\eta\rvert\le\delta$.

## 2. Definitions

- **Trap.** $K\ne\varnothing$ with $\bigcap_{\theta\in K}\mathcal Y(\theta,u)\ne\varnothing$ for every $u\in\mathcal S(K)$.
  - Singletons are traps.
  - A $K$ with $\mathcal S(K)=\varnothing$ is a trap vacuously.
  - **Far** means $\operatorname{diam}K>\varepsilon$; for $\varepsilon=0$, $\lvert K\rvert\ge2$.
- **Informative.** $u$ is informative on $K$ if no observation is compatible with all of $K$.
- **Conflict.** An inclusion-minimal $F$ with $\bigcap_F\mathcal Y(\cdot,u)=\varnothing$. For intervals, conflicts are pairs: $\lvert c^\top(\theta_i-\theta_j)\rvert>2\delta$.
- **Lone forbidden pair.** A conflict $\{i,j\}$ of $u$ such that no other conflict of $u$ lies outside $B_u$. It is *global* if it is $u$'s only conflict on all of $\Theta_0$.
- **Safety-witness number.**
  - $\sigma(K)=\min\{\lvert W\rvert : W\subseteq K,\ \mathcal S(W)=\mathcal S(K)\}$, the minimum hitting set of the nonempty traces $B_u\cap K$.
  - Its approximate version for unit normals is $\sigma_\gamma(K)$: the minimum $\lvert F\rvert$ with $h_K(a_u)>b_u+\gamma\Rightarrow h_F(a_u)>b_u$.
- **Lower semicontinuity (L)** of $K\mapsto\mathcal S(K)$ on $\mathcal K$. It is implied by density of strictly safe experiments (Lemma 0).
- **Alignment.** $a_u=\lambda_uc_u$ with $\lambda_u\ne0$ and $c_u\ne0$.

## 3. Principal theorems

> **T1 (finite characterization).** For finite $\Theta_0$ and $\mathcal U$, and arbitrary set-valued observations, the following are equivalent:
> - (i) no far trap exists;
> - (ii) some deterministic policy reaches $\operatorname{diam}\le\varepsilon$ within $\lvert\Theta_0\rvert-1$ experiments, uniformly;
> - (iii) some policy, possibly randomized, eventually identifies surely.
>
> This is a theorem about adaptive noise. Under oblivious noise, a randomizing agent can escape a trap (example Ob).
>
> *Proof.* `research/finite_trap_theory.md` §§2–3: a held trap blocks every policy; a strictly shrinking safe informative experiment always exists when no trap is present.

> **T5 / G1′ (minimal traps; local to global; $\varepsilon=0$).**
> - A minimal trap $K$ with $\lvert K\rvert\ge3$ has $\sigma(K)=\lvert K\rvert$. Hence at least $\lvert K\rvert$ experiments are unsafe on it, each isolating a different member. This is tight: the cycle trap has $n$ experiments and binary deterministic observations.
> - For $k\ge2$: "every $\Theta'\subseteq\Theta_0$ is identifiable whenever all its $k$-subsets are" ⇔ every minimal trap has size $\le k$ ⇔ $\sigma\le k$ on minimal traps of size $\ge3$.
>
> *Proof.* `research/finite_trap_theory.md` §5 (Lemma W) and `research/geometric_obstructions.md` §1.

> **Finite complexity map** (explicit encodings; TRAP = "does a far trap exist", SAFEID its complement).
> - **B1:** no safety ⇒ P, by pair tests, for every observation model.
> - **P2:** deterministic observations ⇒ P (**known**, Hierons–Türker 2014).
> - **P3:** unsafe sets of size $\le1$ ⇒ P (Horn), $O(n^3m)$.
> - **H1:** with safety and interval or binary observations, TRAP is NP-complete and SAFEID coNP-complete, already when unsafe sets have size $\le2$. The laminar version is L6.
>
> *Proofs.* `research/complexity_analysis.md` §§2–4; `research/boolean_trap_formulation.md`.

> **D2 / D3 (dimensional dichotomy).**
> - **D2:** for the linear model, $\mathrm{TRAP}^{(2)}_0$ is NP-complete, already when:
>   - every parameter is a rational point of the unit circle;
>   - unsafe sets are singletons or cyclically adjacent pairs, and form a laminar family;
>   - each experiment separates all pairs, or exactly one antipodal pair;
>   - there is a common noise radius;
>   - the size is $O(n+m)$ with $O(\log(n+m))$ bits per number.
> - **D3:** linear SAFEID is in P for $d=1$, and coNP-complete for every fixed $d\ge2$ and every tolerance $0\le\varepsilon<1$.
> - **D4:** under ETH, there is no $2^{o(N)}$ algorithm in the plane, for $N$ parameters, and no $2^{o(L/\log L)}$ algorithm for bit length $L$.
>
> *Proofs.* `research/fixed_dimension_complexity.md` §2, with the independent audit in `research/planar_hardness_audit.md`.

> **K1–K3 (compact spaces).** Assume compactness, continuous $g$, a closed observation graph and (L), and let $\varepsilon>0$.
> - **K1:** if no closed trap has diameter $\ge\varepsilon$, a uniform horizon $T$ exists with $\operatorname{diam}\Theta_T<\varepsilon$.
> - **K2:** the closed traps form a closed family. The minimax limiting diameter is $D^\*=\max$ closed-trap diameter.
> - **K3:** eventual identification implies uniform identification.
>
> *Proofs.* `research/continuum_analysis.md` §2.

## 4. Supporting results

| ID | Statement | Location |
|---|---|---|
| T2, T3 | Myopic play suffices within $n-1$ steps. One policy attains the instance-wise optimum $D(\theta^\*)$ for every $\theta^\*$. | FT §3 |
| T4 | Traps are closed under restriction and independent products. They are not closed under union, intersection, subsets, supersets, or joint-product projection. | FT §4 |
| T6, G2b | Every family is a trap family. Helly-$h$ realizability is characterized. | FT §6, GO §2 |
| L1–L3 | Trap ⇔ every experiment blocked or blind; hull invariance; minimal traps in convex position, of size $\le c(\Theta_0)$. | `linear_identifiability.md` §2 |
| L5, L8 | $d=1$: pairs suffice. Safety on one line: pairs suffice. | same, §3 |
| L6 | NP-complete in unbounded $d$, with convex position, common $\delta$, laminar size-$\le2$. | same, §3.2 |
| L7 | XP $O(n^{r+2}m)$ in safety rays; W[1]-hard in $r$ (unbounded $d$). | same, §3.3 |
| D5 | XP $O(n^{2k+1}m)$ in observation lines, in any $d$. | FD §3 |
| R1 | A one-edge conflict graph is realizable iff the pair is strictly antipodal. | GR §1 |
| AL1–AL3 | An aligned global lone pair meets every nonempty unsafe set. The aligned D2 family reduces to 2-SAT (P). Aligned TRAP is NP-complete in unbounded $d$. | `aligned_identifiability.md` |
| W1, W4, W5′ | σ ≤ number of blocked rays; planar σ polynomial (convex case proved); σ NP-hard in $\mathbb Q^4$ (self-contained). | `witness_geometry.md` |
| Q1′, Q2 | $T(\varepsilon)\le\operatorname{Pack}(\Theta_0,\mu(\varepsilon)/4L_h)$. Exponent $d$ and margin dependence are necessary; no margin-free bound exists. | CO §7 |
| A2′–A4 | Robust Lemma W. Two-sided net certificates, sound always and complete away from tangential safety and zero-margin traps. | `approximate_witnesses.md` |

## 5. Exact reduction: D2

Source: 3-CNF $\phi$, with nonempty clauses padded to three literals.

**Parameters** ($6n+10m'$, where $m'$ is the number of nonempty clauses):
- $T_v,F_v,T'_v,F'_v$ for each variable;
- $s_j,s'_j,\kappa_{j1},\kappa_{j2},\kappa_{j3}$ for each nonempty clause;
- a helper $w_x$ for each antecedent $x\in\{T_v,F_v,s_j,s'_j,\kappa_{ji}\}$.

**Geometry.**
- **Upper points** sit at $v(k)=\bigl(\tfrac{1-k^2}{1+k^2},\tfrac{2k}{1+k^2}\bigr)$, $k=1..M$, in the order $T_v,F_v,T'_v$ (each $v$), then $s_j,s'_j,\kappa_{j1},\kappa_{j2},\kappa_{j3}$ (each $j$).
- **Partners** sit at $-v(k)$: helpers for antecedents, and $F'_v$ for $T'_v$.

**Experiments** ($B$ = unsafe set, $P$ = separated pairs, $\mathbf 1$ = all pairs):

| Experiment | $B$ | $P$ | Constraint |
|---|---|---|---|
| force$(w)$ | $\{w\}$ | $\mathbf 1$ | $w\in K$ |
| imply$(T_v\to T'_v)$, imply$(F_v\to F'_v)$ | $\{T'_v\}$, $\{F'_v\}$ | $\{T_v,w\}$, $\{F_v,w\}$ | implications |
| notboth$(T'_v,F'_v)$ | $\varnothing$ | $\{T'_v,F'_v\}$ | not both |
| some$(s_j,s'_j)$ | $\{s_j,s'_j\}$ | $\mathbf 1$ | $s_j\vee s'_j$ |
| imply$(s'_j\to\kappa_{j1}\vee\kappa_{j2})$ | $\{\kappa_{j1},\kappa_{j2}\}$ | $\{s'_j,w\}$ | |
| imply$(s_j\to\kappa_{j3})$ | $\{\kappa_{j3}\}$ | $\{s_j,w\}$ | |
| imply$(\kappa_{ji}\to\ell_{ji})$ | $\{$literal point$\}$ | $\{\kappa_{ji},w\}$ | |
| empty clause | $\varnothing$ | $\mathbf 1$ | false |

**Realizations.**
- **Singleton cap $\{y\}$:** $a=v_y$, with $b$ the midpoint of 1 and the second-largest value.
- **Adjacent pair $\{x,y\}$:** $a=v_x+v_y$, with $b$ the midpoint of the 2nd and 3rd largest values.
- **$B=\varnothing$:** $a=0$, $b=1$.
- **Lone pair $\{v,-v\}$:** $c=v$, $\delta=(M_k+2)/4$, with $M_k=\max(1-\min_{\rm o},1+\max_{\rm o})$.
- **All pairs:** $c^\*=(1,\tfrac17)$, with $\delta^\*$ one third of the minimum projection gap. Distinctness of the projections is proved analytically: it reduces to $7kl-k-l=7$, which has no positive-integer solutions.

**Proof.**
- *(⇐) Trap ⇒ satisfying assignment.* The helpers are forced. Then follow the implications, consistency via notboth, and the clauses via selectors and copies.
- *(⇒) Satisfying assignment ⇒ trap.* Take the helpers, the true literals and their primes, the copies of true literals, and one selector per clause.

Full proof: `research/planar_hardness_audit.md` §3.

**Approximate identification.** For $0\le\varepsilon<1$: when $n\ge2$, the helpers $-v(1)$ and $-v(4)$ are at distance $\sqrt{306}/17>1$, so every trap of size $\ge2$ is far.

**Other reductions** (locations):
- H1(a/b): `complexity_analysis.md` §3, code `scripts/traps.py` `sat_u2`, `sat_u3`;
- L6: `sat_laminar`;
- L7(b): `scripts/linear.py` `multicolored_clique`;
- AL3: `aligned_sat_u2`;
- W5′: vertex cover on moment-curve pairs.

## 6. Counterexamples and examples

| ID | Statement | Location |
|---|---|---|
| Ob | Oblivious noise plus randomization identifies inside a trap. | FT §2 |
| Cycle trap; G3(c); L9 | Minimal traps of every size (binary deterministic; planar linear; planar aligned). | FT §5, GO §3, LI §3.4 |
| T4 closure failures | Explicit instances on 3–4 parameters. | FT §4 |
| L4 | A minimum σ-witness needing a non-vertex. | LI §2 |
| X1 | Without (L), K1 fails: an informative experiment becomes safe only in the limit. | CO §3 |
| X2 | The critical tolerance $D^\*$ is approached but not attained; $T(\varepsilon)\to\infty$ as $\varepsilon\downarrow D^\*$. | CO §3 |
| X3 | Without a closed graph, the supremum of closed-trap diameters is not attained. | CO §3 |
| X4 | Eventual ≠ uniform without joint continuity. | CO §3 |
| X5 | Net certificates can fail forever: tangential safety, or zero-margin traps. | AW §3 |
| Q2 | Bump experiments need $\sim(L_h/\mu)^d$ steps; without a margin, horizons are unbounded at fixed constants. | CO §7 |
| Q3, Q4 | No universal approach rate; accuracy can jump under arbitrarily small safety relaxation. | CO §7.1 |

## 7. Scalar results

All in `research/scalar_analysis.md`.

| ID | Statement |
|---|---|
| S1 | One experiment at $x>0$ yields intervals of length $2\delta x^{-p}$. |
| S2 | Maximum safe intensity $x=1/U_t$ is optimal for every inclusion-monotone objective, at every horizon (coupling). |
| S3 | Worst case $\eta\equiv\delta$: $U_{t+1}=\min(U_t,\theta^\*+2\delta U_t^p)$, and the lower endpoint is exact from $t=1$. |
| S4 | Fixed points and basins for every $p>0$. Fold at $\lambda=2\delta\theta^{\*\,p-1}=\lambda_c=(p-1)^{p-1}/p^p$; at $p=2$ the condition is $8\delta\theta^\*=1$. |
| S4a′ | $\sqrt\epsilon N_\epsilon\to(\operatorname{artanh}\rho+\operatorname{artanh}s)/\sqrt{ab}$, with $ab=\tfrac12p^{p-1}(p-1)^{2-p}$, for starts scaled to the basin. |
| S5 | **Uniform value** $\min(U_0-L_0,2\delta U_0^p)$, attained after one experiment and never improved. |
| S6 | Total deadlock iff $2\delta U_0^p\ge U_0-L_0$. |

**Manuscript caution.** $\lambda_c$ is an *instance-wise* threshold. It is not a transition in uniform minimax learnability.

## 8. Geometric complexity classification

The definitive table, with hypotheses and references, is in `research/complexity_map.md`. In brief:

| Polynomial | Hard | Open |
|---|---|---|
| no safety; deterministic observations; $\lvert B\rvert\le1$; nested $B$; $d=1$; safety normals on one line | general $\lvert B\rvert\le2$; laminar; unbounded $d$, even convex position; **every fixed $d\ge2$, on the unit circle**; aligned in unbounded $d$ | aligned and orthogonal in fixed $d$; FPT in observation lines |

**XP:** in safety rays (W[1]-hard), in observation lines, and in σ.

**Polynomial within the D2 family:** aligned functionals.

**Separation.** In the plane, computing σ is polynomial while SAFEID is coNP-complete.

## 9. Compact and quantitative results

- K1–K3 as in §3, with the counterexamples X1–X4.
- **Q1′.** $T(\varepsilon)\le\operatorname{Pack}(\Theta_0,\mu(\varepsilon)/4L_h)\le(1+8L_hD/\mu(\varepsilon))^d$.
  - $\operatorname{Pack}$ is the maximal number of points with pairwise distance $\ge r$.
  - $\mu(\varepsilon)=\min$ over closed $K$ with $\operatorname{diam}\ge\varepsilon$ of $\sup_{u\in\mathcal S(K)}(w_K(u)-2\delta_u)$. It is positive under the K1 hypotheses when $D^\*<\varepsilon$.
- **A3–A4.**
  - The upper instance (safety tightened by $L_gh$, noise enlarged by $L_hh$) having no trap of diameter $\ge\varepsilon-2h$ ⇒ no closed trap of diameter $\ge\varepsilon$.
  - The lower instance (safety relaxed, noise shrunk) having a far trap ⇒ a closed trap of $\Theta_0$.
  - Completeness under density, resp. margin-robust traps.
- **A2.** $\sigma_\gamma\le N(S^{d-1},\gamma/2R)$ and $\ge c_d(R/\gamma)^{(d-1)/2}$ on the sphere; exactly $\lceil\pi/\arccos(1-\gamma/R)\rceil$ in $d=2$.

## 10. Literature and bibliographic details

Access levels: **F** full text, **P** partial, **A** abstract or secondary, **M** metadata.

- **R. M. Hierons, U. C. Türker.** *Distinguishing Sequences for Partially Specified FSMs.* NFM 2014, LNCS 8430:62–76, DOI 10.1007/978-3-319-06200-6_5. **F.** Deterministic static case, polynomial (overlaps P2).
- **U. C. Türker, R. M. Hierons, G. Barlas, K. El-Fakih.** *Incomplete adaptive distinguishing sequences for non-deterministic FSMs.* IEEE TSE 49(9):4371–4389, 2023, DOI 10.1109/TSE.2023.3291137. **F.** Contains the static model as the self-loop case. Its PSPACE-hardness is for forest size, by FA-INT with dynamics. Upper bounds only for the static case.
- **S. Haar, S. Haddad, T. Melliti, S. Schwoon.** *Optimal constructions for active diagnosis.* FSTTCS 2013, LIPIcs 24:527–539; JCSS (2016), DOI 10.1016/j.jcss.2016.04.007. **P.** Evolving fault events; EXPTIME-complete; not subsuming.
- **R. Alur, C. Courcoubetis, M. Yannakakis.** *Distinguishing tests for nondeterministic and probabilistic machines.* STOC 1995, DOI 10.1145/225058.225161. **A.**
- **Y. Sui, A. Gotovos, J. Burdick, A. Krause.** *Safe exploration for optimization with Gaussian processes.* ICML 2015. **P.** Reachability closure.
- **D. Fudenberg, D. K. Levine.** *Self-confirming equilibrium.* Econometrica 61(3), 1993. **A.**
- **D. Easley, N. M. Kiefer.** *Controlling a stochastic process with unknown parameters.* Econometrica 56(5), 1988. **A.**
- **M. Milanese, A. Vicino.** Automatica 27(6), 1991 (set-membership estimation). **A.**
- **A. Shakouri, H. J. van Waarde, M. K. Camlibel.** arXiv:2607.00844 (2026). **P.** Offline, unconstrained.
- **S. Amani et al.** NeurIPS 2019; **A. Gangrade et al.** COLT 2024; **T. M. Moldovan, P. Abbeel.** ICML 2012. **P.**
- **J. H. Reif.** JCSS 29(2), 1984. **A.**
- **S. Har-Peled, M. Lee.** JoCG 3(1), 2012; arXiv:2506.16979. **A.** Halfplane cover / hitting set.
- **D. S. Johnson.** J. Algorithms 3(2):182–195, 1982 (DUDC NP-hard, as cited). **M.**
- **P. K. Agarwal, S. Har-Peled, K. Varadarajan.** JACM 51(4), 2004 ($\varepsilon$-kernels). **A.**
- **Dudley 1974; Bronshteyn–Ivanov 1975.** **A**, via Mount et al. SoCG 2012 / 2016 and arXiv:2512.02379.
- **Matoušek–Seidel–Welzl 1990; Brönnimann–Goodrich 1995.** **M.**
- **Hyafil–Rivest 1976; Laber–Nogueira 2004**, DOI 10.1016/j.dam.2004.06.002. **A.**
- **Nguyên–Soltan**, via arXiv:1406.2052. **A.**
- **Schaefer 1978; Dowling–Gallier 1984; Even–Itai–Shamir 1976; sparsification lemma (Impagliazzo–Paturi–Zane 2001).** Standard.

Full review: `research/literature_review.md`. The originality audit is §9 there.

## 11. Computational methodology

- **Reference solver.** `scripts/traps.py` `Instance.value` (exact attractor rank over bitmask subsets) and `Instance.traps` (full enumeration).
- **Linear models.** `scripts/linear.py`, exact Fractions, compiled to Instances. Interval responses come from a sweep over sorted projections; only maximal responses are kept, since dominated ones never matter.
- **Boolean reference.** `scripts/boolean.py`, a DPLL with the cardinality bound built in.
- **D2.** Builder `scripts/planar_hardness.py`. The independent verifier `scripts/verify_d2.py` shares only output and labels with the builder.
- **Method.** Every efficient algorithm and every reduction is compared against exhaustive enumeration or the DPLL on small instances. Arithmetic is exact (integers, bitmasks, `Fraction`), except in E005 §J and the scalar numerics. **No theorem relies on computation.**

## 12. Inventory, reproduction, figures, dependencies

- **Inventory.** `results/ledger.md`, "Computational inventory": E001–E008, with incomparable counts kept separate.
- **Reproduction** (in `~/code/safe-learning`):

```bash
python3.12 -m venv .venv && .venv/bin/pip install numpy pytest
```

```bash
.venv/bin/python -m pytest
```

```bash
.venv/bin/python scripts/scalar_check.py
```

```bash
.venv/bin/python scripts/finite_game.py
```

```bash
.venv/bin/python scripts/stage1_finite.py
```

```bash
.venv/bin/python scripts/critical_scaling.py
```

```bash
.venv/bin/python scripts/stage2_checks.py
```

```bash
.venv/bin/python scripts/stage3_checks.py
```

```bash
.venv/bin/python scripts/verify_d2.py
```

```bash
.venv/bin/python scripts/stage4_checks.py
```

- **Figures.** `research/manuscript_plan.md` §4 lists the candidate figures F1–F8, with their data sources.
- **Dependencies.** `research/manuscript_plan.md` §2. No principal theorem depends on an unverified citation.

## 13. Research-status notes (not for manuscript prose)

- **Cited, not read:**
  - W4(c), general planar σ (Har-Peled–Lee / arXiv:2506.16979);
  - W5, σ NP-hard in $\mathbb Q^3$ (Johnson 1982);
  - the sharp $(d-1)/2$ coreset exponent;
  - OPTCOUNT NP-hardness;
  - R5(c), the antipodal-pair count;
  - ACY 1995 theorem statements.
- **Open:**
  - AL-O1: aligned, fixed $d\ge2$. There is a bounded-width sketch for the plane, unproved.
  - OR-O1: orthogonal.
  - D-O1: FPT in observation lines.
  - D-O2: hardness without lone pairs.
  - W-O1: FPT in $r$ for fixed $d$.
  - Q-K1: K3 without (L).
  - Q-K4′: continuity under safety relaxation.
  - Q-K5: bounding $\mu(\varepsilon)$.
- **Weak computational evidence**, the proof carrying the result:
  - L3 (only 2 minimal traps of size $\ge3$ in E005 §B);
  - A1 (floats).
- **Corrections made over Stages 1–4:** `research/mathematical_audit.md` §0, and the register's "Refuted or corrected" and status-change tables.
- **Novelty.** "Not found" is not priority. Run a final search in the geometric-CSP and adaptive-testing literatures before submission.

## 14. Repository status

- Branch `main`, pushed to the private remote.
- Test suite: 51 tests, all passing at the Stage 4 commit.
- Stage commits: Stage 0 `5e9a078`/`04a5193`; Stage 1 to `7944cc7`; Stage 2 to `4e4b5b5`; Stage 3 to `1cf7d6e`; Stage 4 `6469030` to `48190ba`, followed by a date and hash correction.
