# Stage 3 — The critical dimension of safe identifiability

*2026-11-23. This is the principal Stage 3 document. Notation follows `research/linear_identifiability.md`.*
- *Construction:* `scripts/planar_hardness.py`.
- *Exact checks:* `scripts/stage3_checks.py`, output `results/stage3_checks.txt` (ledger E006).
- *Status of computation:* no theorem below relies on computation. The checks are regressions against the exhaustive and Boolean reference solvers.

## 0. Summary

| ID | Statement | Status |
|---|---|---|
| D0 | Problems, encodings, and NP / coNP membership in every dimension. | proved |
| D1 | **Dimension monotonicity.** Zero-padding $\mathbb Q^d\to\mathbb Q^D$ preserves the instance exactly. | proved |
| D2 | **Planar hardness.** $\mathrm{TRAP}_0$ is NP-complete, and exact safe identifiability coNP-complete, in $\mathbb Q^2$, already when *all* of the following hold: (i) every parameter lies on the unit circle (strict convex position); (ii) every unsafe trace is a singleton or a cyclically adjacent pair, and the traces form a laminar family; (iii) every experiment's observation separates either all pairs or exactly one antipodal pair; (iv) one common noise radius; (v) the instance has $O(n+m)$ parameters and experiments. | **proved** |
| D3 | **The critical dimension is 2.** Linear safe identifiability is polynomial in $d=1$ (L5), and coNP-complete in every fixed $d\ge2$ (D1 + D2). The same holds for $\varepsilon$-identifiability for every $\varepsilon$ below a constant fraction of the parameter diameter. | **proved** |
| D4 | *ETH lower bound.* Under ETH, there is no $2^{o(n)}$-time algorithm in the plane, where $n$ is the number of parameters. | proved (conditional) |
| D5 | **XP in the observation directions.** With $k$ distinct observation lines, $\mathrm{TRAP}_\varepsilon$ is decidable in $O(n^{2k+1}m)$, in every dimension and for every safety structure. One observation direction gives polynomial time. | proved |
| D6 | The Stage 2 obstruction (opposite caps) is real, but it constrains only *direct* clause encodings. Forced helpers and private copies route around it. | explanation |

**Answers to the brief's questions 2–4.**
- **Q2: yes, coNP-complete in fixed dimension.** Already in the plane, with all parameters on a circle. This resolves the Stage 2 open problem G-O1 negatively for tractability.
- **Q3: the smallest dimension with hardness is 2, and it is tight**, since $d=1$ is polynomial. So the full dimensional dichotomy is: polynomial for $d=1$, coNP-complete for $d\ge2$.
- **Q4: the planar model is not polynomial unless P = NP**, even in strict convex position. It becomes polynomial when:
  - the number of observation directions is bounded (XP, D5), or
  - the number of safety directions is bounded (XP, L7), or
  - every unsafe set has size $\le1$ (P3).

## 1. Problems and encodings

**The instance.**
- Parameters $\theta_1,\dots,\theta_n\in\mathbb Q^d$, with experiments $(a_u,b_u,c_u,\delta_u)\in\mathbb Q^d\times\mathbb Q\times\mathbb Q^d\times\mathbb Q_{\ge0}$.
- All numbers are in binary, and $d$ is fixed unless stated otherwise.

**The problems.**
- $\mathrm{TRAP}^{(d)}_0$: is there a trap $K$ with $\lvert K\rvert\ge2$?
- $\mathrm{SAFEID}^{(d)}_0$: is $\Theta_0$ exactly identifiable by an adaptive robust-safe policy? By Theorem T1 this is the complement of $\mathrm{TRAP}^{(d)}_0$.
- For $\varepsilon>0$, "far" means Euclidean diameter $>\varepsilon$. Squared distances are compared, so everything stays rational.

> **D0 (membership).** For every $d$, $\mathrm{TRAP}^{(d)}_\varepsilon\in\mathrm{NP}$ and $\mathrm{SAFEID}^{(d)}_\varepsilon\in\mathrm{coNP}$.

*Proof.* Proposition M of Stage 1. Every test is a comparison of rational linear forms, or of squared distances. ∎

**Complexity is in the Turing model.** All constructions below use rationals of polynomial bit length, with explicit separating margins, so no real-arithmetic feasibility question arises.

> **D1 (dimension monotonicity).** Let $\iota:\mathbb Q^d\to\mathbb Q^D$ append $D-d$ zero coordinates. Map an instance by $\theta_i\mapsto\iota\theta_i$ and $(a,b,c,\delta)\mapsto(\iota a,b,\iota c,\delta)$. Then every unsafe set, every observation projection and every pairwise distance is unchanged. So the two instances have identical traps and identical game values, and hardness in $\mathbb Q^d$ implies hardness in $\mathbb Q^D$.

*Proof.* $\langle\iota x,\iota y\rangle=\langle x,y\rangle$. Verified on 200 random instances (E006 §C). ∎

## 2. The planar hardness theorem

**Source problem.** 3-SAT, in its general form: clauses of length 1–3, repeated literals and tautologies allowed, and possibly the empty clause.

### 2.1 Construction

Given variables $x_1,\dots,x_n$ and clauses $C_1,\dots,C_m$, pad each nonempty clause to length 3 by repeating its last literal.

**Parameters.**
- *Literal points:* $T_v,F_v$ for each variable.
- *Primed copies:* $T'_v,F'_v$, used only to express "not both".
- *Per clause $j$:* two selectors $s_j,s'_j$, and private copies $\kappa_{j1},\kappa_{j2},\kappa_{j3}$ of its literals.
- *Helpers:* one helper $w_x$ for every *antecedent* $x\in\{T_v,F_v,s_j,s'_j,\kappa_{ji}\}$.

That makes $6n+10m$ parameters.

**Geometry.** All parameters lie on the unit circle.
- *Upper points.* Each antecedent, and each $T'_v$, is an "upper" point $v(k)=\bigl(\tfrac{1-k^2}{1+k^2},\tfrac{2k}{1+k^2}\bigr)$ at angle $2\arctan k$, for $k=1,2,\dots$ in this order:
  - $T_v,F_v,T'_v$ for each $v$;
  - then $s_j,s'_j,\kappa_{j1},\kappa_{j2},\kappa_{j3}$ for each nonempty clause.
- *Partners.* The partner of each upper point is its antipode $-v(k)$: $w_x$ for an antecedent $x$, and $F'_v$ for $T'_v$.
- Upper points lie in the open upper half-circle and partners in the lower. So $s_j,s'_j$ are cyclically adjacent, and so are $\kappa_{j1},\kappa_{j2}$.

**Experiments.** Let $\mathbf 1$ denote "separates every pair". It is realized by $c^\*=(1,\tfrac17)$, which gives distinct projections on these points (checked exactly), with $\delta^\*$ one third of the smallest projection gap.

| Experiment | Unsafe set $B_u$ | Separated pairs $P_u$ | Boolean constraint (on traps, $\lvert K\rvert\ge2$) |
|---|---|---|---|
| force$(w)$, every helper | $\{w\}$ | $\mathbf 1$ | $w\in K$ |
| imply$(T_v\to T'_v)$; imply$(F_v\to F'_v)$ | $\{T'_v\}$; $\{F'_v\}$ | $\{T_v,w_{T_v}\}$; $\{F_v,w_{F_v}\}$ | $T_v\Rightarrow T'_v$; $F_v\Rightarrow F'_v$ |
| notboth$(T'_v,F'_v)$ | $\varnothing$ | $\{T'_v,F'_v\}$ | $\neg(T'_v\wedge F'_v)$ |
| some$(s_j,s'_j)$ | $\{s_j,s'_j\}$ | $\mathbf 1$ | $s_j\vee s'_j$ |
| imply$(s'_j\to\kappa_{j1}\vee\kappa_{j2})$ | $\{\kappa_{j1},\kappa_{j2}\}$ | $\{s'_j,w_{s'_j}\}$ | $s'_j\Rightarrow\kappa_{j1}\vee\kappa_{j2}$ |
| imply$(s_j\to\kappa_{j3})$ | $\{\kappa_{j3}\}$ | $\{s_j,w_{s_j}\}$ | $s_j\Rightarrow\kappa_{j3}$ |
| imply$(\kappa_{ji}\to\ell_{ji})$ | $\{\ell_{ji}\}$, the literal point | $\{\kappa_{ji},w_{\kappa_{ji}}\}$ | $\kappa_{ji}\Rightarrow\ell_{ji}$ |
| empty clause | $\varnothing$ | $\mathbf 1$ | false |

**Realizing the safety side.** Each unsafe set is a halfplane trace.
- For $V=\{x\}$: take $a=v_x$, with $b$ strictly between $1=a^\top v_x$ and the next largest value $a^\top z$.
- For an adjacent pair $V=\{x,y\}$: take $a=v_x+v_y$. On the circle, $a^\top z$ decreases with the angular distance from the bisector of $x,y$. No point lies on the arc between them, so $x,y$ are the two largest values, and $b$ goes between the second and third largest.
- For $V=\varnothing$: $a=0$, $b=0$.

**Realizing the observation side.** Each separated pair is realized by a direction.
- For an antipodal pair $\{x,-x\}$: take $c=v_x$. Then $c^\top x=1$ is the unique maximum and $c^\top(-x)=-1$ the unique minimum, because distinct unit vectors $z$ satisfy $\lvert c^\top z\rvert<1$.
- With $M=\max(1-\min_{\rm others},\ 1+\max_{\rm others})<2$, take $2\delta=(M+2)/2$. Then exactly the pair $\{x,-x\}$ is separated (Lemma R1 below).
- *Common noise radius.* Rescaling $c$ by $1/\delta$ gives every experiment $\delta=1$ without changing any relation (E006 §B).

### 2.2 Correctness

> **Theorem D2.** The formula is satisfiable iff the instance has a trap of size $\ge2$.

*Proof.*

**Each experiment's constraint.** An experiment kills $K$ iff it is safe for $K$ ($K\cap B_u=\varnothing$) and $K$ contains a separated pair (L1 with 1-D Helly). Reading off the table:
- *"Separates everything" with unsafe set $V$* kills exactly the sets of size $\ge2$ avoiding $V$, so it imposes "$K$ meets $V$".
- *One separated pair $\{x,w_x\}$ with unsafe set $V$* imposes $x\in K\wedge w_x\in K\Rightarrow K\cap V\ne\varnothing$. Together with the forcing of $w_x$, this is exactly the stated implication.
- *notboth* imposes $\neg(T'_v\wedge F'_v)$.

**(⇒) A trap gives a satisfying assignment.** Let $K$ be a trap with $\lvert K\rvert\ge2$, and set $x_v=\mathrm{true}$ iff $T_v\in K$.
- *Consistency.* If $T_v,F_v\in K$, then $T'_v,F'_v\in K$ by the implications, and notboth kills $K$. So at most one of $T_v,F_v$ is in $K$.
- *Literals in $K$ are true.* If $T_v\in K$ then $x_v$ is true. If $F_v\in K$ then $T_v\notin K$, so $\neg x_v$ is true.
- *Clauses.* For clause $j$, $s_j$ or $s'_j$ is in $K$.
  - If $s'_j\in K$: some $\kappa_{j1},\kappa_{j2}\in K$, hence its literal point is in $K$, hence that literal is true.
  - If $s_j\in K$: $\kappa_{j3}\in K$, and likewise.
- *Empty clause.* If one exists, every $K$ of size $\ge2$ is killed, so no trap exists, consistent with unsatisfiability.

**(⇐) A satisfying assignment gives a trap.** Given $\alpha$, let $K$ consist of:
- all helpers;
- the true literal points, and the primes of those literal points;
- every $\kappa_{ji}$ whose literal is true;
- $s'_j$ if $\ell_{j1}$ or $\ell_{j2}$ is true, and $s_j$ otherwise (then $\ell_{j3}$ is true).

Check every row of the table:
- force: $\checkmark$;
- imply$(T\to T')$: $\checkmark$;
- notboth: $T_v,F_v$ are not both true, so the primes are not both present;
- some: $\checkmark$;
- clause implications: $\checkmark$ by the choice of $s/s'$;
- copy implications: a copy is present only if its literal is true.

Finally $\lvert K\rvert\ge2$, since $n\ge1$ gives at least two helpers.

**Unintended traps.** There are none. The argument characterizes *every* trap of size $\ge2$, because each experiment's kill family was determined exactly.

**Size and encoding.**
- $6n+10m$ parameters and $\le7n+13m$ experiments.
- Circle points $v(k)$ have numerators and denominators $\le1+k^2=O((n+m)^2)$.
- Thresholds are midpoints of such values, and the noise radii are explicit rational functions of them.
- All bit lengths are $O(\log(n+m))$ per coordinate. ∎

**Corollaries.**
- **Restrictions (i)–(v).** All hold by construction.
  - *Laminarity:* the pairs $\{s_j,s'_j\}$ and $\{\kappa_{j1},\kappa_{j2}\}$ are pairwise disjoint, and every singleton is either inside one of them or disjoint from all.
  - *Exact checks:* on 58 formulas, including the degenerate ones, every point lies on the unit circle, and every unsafe set and every separated-pair set is the intended one. Satisfiability agreed with Boolean trap existence in every case (E006 §B).
- **D3.** Combine D2 with L5 ($d=1$ polynomial) and D1.
- **D3 for $\varepsilon>0$.** Every trap of size $\ge2$ contains all helpers, which are spread over the lower half-circle. For any $\varepsilon$ smaller than the diameter of the helper set (which exceeds $\sqrt2$ once there are $\ge3$ helpers), trap existence is unchanged.
- **D4.** The reduction is linear in the size of the formula. The sparsification lemma gives 3-SAT instances with $m=O(n)$, so under ETH 3-SAT has no $2^{o(n)}$ algorithm. Hence $\mathrm{TRAP}^{(2)}_0$ has no $2^{o(N)}$ algorithm, for $N$ parameters.

### 2.3 Why the Stage 2 reductions failed, and why this one does not

Stage 2's Lemma L10 holds: an always-safe experiment that separates exactly one pair forces that pair to be the unique minimum and maximum of its observation functional. In D2 this is used, not avoided. Every one-pair gadget is an antipodal pair on the circle.

What Stage 2 assumed, and D2 drops, is that the clause unsafe sets must contain the *literal points themselves*, and that negations must be realized between literal clusters. D2 changes three things:
1. **Clauses never touch literal points.** They act on private copies placed contiguously, so clause traces are adjacent pairs.
2. **Every negative literal pairs with a forced helper.** That turns the arbitrary negative-literal graph into a **perfect matching**, which antipodal points realize in the plane.
3. **The cyclic-bandwidth obstruction disappears.** The non-local structure of the formula is carried by the implications $\kappa\Rightarrow\ell$. Their unsafe sets are singletons, which are halfplane traces anywhere on the circle.

The Stage 2 remark that "the realizable formulas have bounded cyclic bandwidth" is correct only for direct encodings. It is not an obstruction to hardness. The corresponding passages are corrected in `research/linear_identifiability.md`.

## 3. Tractability in fixed dimension

> **Theorem D5 (few observation directions).** Let the observation vectors span $k$ distinct lines, with $c$ and $-c$ identified and $c=0$ ignored. Then $\mathrm{TRAP}_\varepsilon$ is decidable in $O(n^{2k}\cdot nm)$ time, in every dimension and for every safety structure.

*Proof.*
- **Setup.** Let $K_0$ be a far trap, and for each line $j$ let $\ell_j,h_j\in K_0$ attain $\min_{K_0}c_j^\top\theta$ and $\max_{K_0}c_j^\top\theta$. Put
  $$K=\{\theta\in\Theta_0 : c_j^\top\ell_j\le c_j^\top\theta\le c_j^\top h_j\ \forall j\}\supseteq K_0 .$$
- **Same widths.** $K$ has the same width as $K_0$ on every line: it contains $K_0$, and lies within $K_0$'s extremes.
- **No new safe experiments.** $K\supseteq K_0$ gives $\mathcal S(K)\subseteq\mathcal S(K_0)$.
- **Trap.** For $u\in\mathcal S(K)$, $w_K(c_u)=w_{K_0}(c_u)\le2\delta_u$. So $K$ is a trap, and it is far.
- **Algorithm.** Guess the $2k$ extreme parameters, build $K$, and test it. ∎

**Remarks.**
- $k=1$ gives $O(n^3m)$.
- *Regression:* 300/300 instances for $k=1$ and 120/120 for $k=2$, in $d=1,2,3$, with rescaled and sign-flipped directions (E006 §D).
- D5 is the observation-side twin of L7. **Hardness needs both unboundedly many safety directions and unboundedly many observation directions.** D2 uses $\Theta(n)$ of each.
- Whether TRAP is FPT, or W[1]-hard, in $k$ is open. L7's clique reduction uses many observation directions.

**Classification of the planar restrictions listed in the brief.**

| Restriction | Status |
|---|---|
| $d=1$; parameters on a line | P (L5) |
| bounded number of safety rays $r$ | XP $O(n^{r+2}m)$ (L7); W[1]-hard in $r$ when $d$ is unbounded |
| bounded number of observation lines $k$ | XP $O(n^{2k+1}m)$ (D5) |
| unsafe sets of size $\le1$ | P (P3, Horn closure) |
| strict convex position, common $\delta$, laminar unsafe sets of size $\le2$, one-pair or all-pair separation | **coNP-complete** (D2) |
| parameters on a convex curve | coNP-complete (D2, on the circle) |
| boundedly many interior points or convex layers | coNP-complete (D2 has none) |
| aligned $c_u\parallel a_u$ | **open** in the plane. D2's gadgets are not aligned. Large minimal traps exist (L9), which proves nothing either way. |
| orthogonal $c_u\perp a_u$ | **open** |

## 4. Failed constructions worth recording

| Intended gadget | Representation | Incompatibility | Proven? | Resolution |
|---|---|---|---|---|
| "not both" between literal clusters $X,Y$ | always-safe, one direction | $X,Y$ must be opposite caps (L10) | proven | keep the gadget, but only on single antipodal pairs |
| clause cap selecting $\ell_1,\ell_2,\ell_3$ directly | halfplane trace | on a circle, traces are arcs, so the literals must be contiguous | proven for convex position | private copies $\kappa_{ji}$ |
| implication $x\Rightarrow V$ with $x$ alone separated from everyone (Stage 1 $\mathsf O$-gadget) | one direction | needs every other point inside a slab of width $2\delta$ while $x$ lies outside; impossible for spread configurations | proven (L10-type argument) | separate $x$ from a *forced helper* only |
| Stage 2 paraboloid route in $d=3$ | disk traces | negated clusters forced onto the hull | observed, not proven | unnecessary after D2 |
| neighbourly polytopes in $\mathbb R^4$ (any pair isolable) | safety only | nothing failed: safety pairs are realizable. Arbitrary observation relations would also need realizing | — | unnecessary: D2 needs only adjacent pairs |
