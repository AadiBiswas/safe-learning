# Stage 2 report — Geometric and computational limits of safe identifiability

*2026-11-21. This is a self-contained handoff. Proofs are in the files cited, every ID is in `research/theorem_register.md`, and the computations are ledger entry E005.*

## 1. Where Stage 2 started

Stage 1 showed three things:
- safe identifiability of a finite static model is characterized by **traps**;
- it is coNP-complete exactly when robust safety meets overlapping observations;
- the **safety-witness number** $\sigma$ governs the size of minimal traps.

Stage 2 asked:
- whether the 2023 nondeterministic-FSM literature already contains the hardness;
- whether hardness survives *linear* geometry;
- whether $\sigma$ has a geometric theory;
- whether the continuum theorem can be made finite and quantitative.

## 2. Answers to the six questions

1. **Does safe identification stay hard under simple linear geometry?**
   - **In unbounded dimension, yes, in its most restrictive form.** Hardness holds even with all of: parameters in convex position (affinely independent), one common noise radius, and unsafe traces of size $\le2$ forming a laminar family (L6).
   - **Parameterized by the number $r$ of safety directions, it is W[1]-hard** (L7). *(Corrected 2026-11-21: W[1]-hardness rules out $f(r)\,\mathrm{poly}(n,m)$ algorithms unless FPT $=$ W[1]. It does not show that the exponent $r+2$ of the XP algorithm $O(n^{r+2}m)$ is optimal; an exponent lower bound would need, e.g., ETH. The earlier wording "essentially optimal in form" overstated this.)*
   - **In fixed dimension $d\ge2$ it is open.** I could not prove hardness or find an algorithm. Lemma L10 identifies the exact obstruction (§5).
2. **Which structures restore tractability?**
   - **Restore it:**
     - one dimension (pairs, L5);
     - all safety normals on one line (L8);
     - a bounded number of safety rays (XP, L7);
     - unsafe traces of size $\le1$ (Horn closure, Stage 1 P3);
     - nested traces (Stage 1 P4);
     - homogeneous shared-functional models with full scaling (Stage 1 G4).
   - **Do not restore it:**
     - convex position;
     - a common noise radius;
     - laminarity;
     - aligned observations with finite menus (L9).
3. **Is $\sigma$ governed by directional or extremal geometry?**
   - **Yes.** $\sigma\le r$ (W1, sharp), $\sigma\le\lvert V(K)\rvert$, and minimal traps lie in convex position, so their size is $\le c(\Theta_0)$ (L3). Dimension alone bounds nothing.
   - **Computing $\sigma$** is polynomial in the plane and NP-hard in space (W4, W5). It is a separate problem from identifiability.
   - **Minimum witnesses are not hull-invariant** (L4), even though traps are.
4. **Do approximate witnesses give finite quantitative certificates for continuum problems?** Yes.
   - $\sigma_\gamma$ is an additive support-function coreset on the experiment normals, of size $\Theta((R/\gamma)^{(d-1)/2})$ for round bodies (A2, with the sharp upper bound cited).
   - **Two-sided net certificates are always sound** (A3). They are complete exactly away from tangential safety and zero-margin traps (A4, X5).
5. **Can qualitative guarantees become explicit horizons?** Yes:
   - $T(\varepsilon)\le M(\Theta_0,\mu(\varepsilon)/4L_h)$, where $\mu(\varepsilon)>0$ is the worst best-experiment margin (Q1′);
   - both the exponent $d$ and the dependence on the margin are necessary (Q2);
   - **no bound without a margin exists**, even in $d=1$ with fixed Lipschitz constants.
6. **What is substantive beyond the literature?** See §6.

## 3. The literature dependency, resolved

**Türker–Hierons–Barlas–El-Fakih, IEEE TSE 2023** (full text, `research/literature_review.md` §7.1).

**The match is exact.** Their observable partial nondeterministic FSMs contain the static model as the self-loop case:
- "Input defined in all states of the current set" is robust safety. They even motivate undefined inputs by "safety issues".
- $\mathrm{out}(s,x)$ is a set-valued observation correspondence.
- Separation quantifies over all output traces, i.e. adaptive worst-case noise.

**But their hardness does not apply.** Their PSPACE-hardness (Theorem 5.1) concerns the *number* of incomplete ADSs, the K-Complete Forest problem. It is proved by an FA-INT reduction on a **deterministic machine with genuine dynamics**.
- Restricted to self-loops, the deterministic case is polynomial (Hierons–Türker 2014), so that reduction cannot survive.
- They state no complexity result for single-ADS existence in partial nondeterministic machines.

**Classification:**
- the existing work gives an **upper bound** for the static problem (PSPACE/EXPTIME), not the lower bound;
- the Stage 1 and Stage 2 results are **a specialization with a substantially sharper classification**: coNP-complete, P at unsafe size 1, and so on;
- the only direct overlap remains Hierons–Türker 2014: deterministic outputs, P.

## 4. Principal theorems

| ID | Statement | Proof idea |
|---|---|---|
| L1 | Trap ⇔ every experiment is blocked, $h_K(a_u)>b_u$, or blind, $w_K(c_u)\le2\delta_u$. | Robust safety is a support-function inequality; closed intervals intersect iff their centre spread is $\le2\delta$. |
| L2–L3 | Traps are determined by $\operatorname{conv}K$. Minimal traps are in convex position, of size $\le c(\Theta_0)$. | Deleting a non-vertex keeps the hull. |
| L6 | NP-complete in unbounded $d$, with convex position, common $\delta$, laminar size-$\le2$ unsafe sets. | 3-SAT with private literal copies tied by singleton-unsafe implications; basis-vector embedding. |
| L7 | W[1]-hard in the number of safety rays. | Multicolored clique: one ray per colour class, always-safe "not both" experiments for conflicts. |
| W1 | $\sigma\le r$. | One maximizer per positive ray reproduces every blocked experiment. |
| W5 | $\sigma$ NP-hard in $d=3$, convex position. | Paraboloid lifting turns disks into halfspaces; discrete unit-disk cover. |
| A2 | $\sigma_\gamma\le N(S^{d-1},\gamma/2R)$; $\ge\Omega((R/\gamma)^{(d-1)/2})$ on the sphere. | Support sampling; caps of depth $\gamma$ subtend angle $\approx\sqrt{2\gamma/R}$. |
| A3–A4 | Net certificates: sound; complete under density (upper) and margin-robust traps (lower). | Hausdorff-limit compactness, as in K1. |
| Q1′ | $T(\varepsilon)\le M(\Theta_0,\mu(\varepsilon)/4L_h)$. | Each informative experiment removes a ball of radius $\mu/2L_h$ around an extreme point; the centres are separated. |
| Q2 | The exponent $d$ and margin dependence are necessary; no margin-free bound exists. | Bump experiments; the X2 family with the trap moving toward $\varepsilon$. |

## 5. The fixed-dimension question: the precise obstacle

**Lemma L10.** An always-safe experiment that kills exactly the sets meeting both $X$ and $Y$ forces $X$ and $Y$ to be **opposite caps** in its observation direction, with everything else in the slab between. Every reduction from SAT needs such "not both" constraints, together with clause caps that pick one point from each of three literal sets.

**Why the reductions fail in low dimension.**
- *Planar convex position.* Caps are arcs, so clause caps can only touch cyclically consecutive literal arcs. The realizable formulas have bounded cyclic bandwidth and are easy.
- *General planar position.* The literal caps spread around the configuration, and I could not make a clause cap pick out three of them.
- *$d=3$ via the paraboloid.*
  - **What works:** clause caps become empty circles, and "not both" becomes a nearest/farthest pair from a centre.
  - **What breaks:** the "farthest" cluster must sit on the hull. Empty circles through hull and interior clusters then capture other clusters.
  - **What would complete it:** a Delaunay-structured 3-SAT variant with negations on the hull. I do not know whether such a variant is NP-complete.

**What is established in fixed $d$:**
- XP in $r$;
- $O(n^{c(\Theta_0)}m)$;
- polynomial $\sigma$ in the plane;
- unbounded minimal traps in the plane (G3(c), L9).

## 6. Contributions after Stage 2

**Strongest potentially original contribution: the complexity map of safe identification.** It has two parts:
- **The combinatorial classification** (Stage 1 H1, P3, B1, P2, plus L6). Hardness exactly when safety and overlapping observations combine; P at unsafe size 1 and NP-complete at size 2 even when laminar; P for nested.
- **Its geometric refinement.** Linear models are hard in unbounded dimension. The governing parameter is the number of safety directions, which is XP but W[1]-hard. One dimension and single-line safety are polynomial.

The 2023 literature confirms the static problem is a natural, previously unsingled-out subclass whose complexity is much lower than the general partial-NFSM bounds.

**Second: $\sigma$ and $\sigma_\gamma$ as one structural thread.**
- In finite models $\sigma$ governs minimal traps and local-to-global principles (Stage 1).
- In linear models it is bounded by directional and extremal geometry (W1, L3).
- In the continuum its approximate version $\sigma_\gamma$ bounds the size of trap certificates (A2′) and has the classical $(R/\gamma)^{(d-1)/2}$ growth.

**Third: the certified continuum theory** (A3–A4, Q1′–Q2). The qualitative K1 becomes a sound semi-decision procedure with a clean failure set, plus an explicit covering-number horizon.

**Not contributions** (known or immediate):
- W4 and W5 follow from known geometric hitting-set results;
- A1 and the sharp exponent in A2 are classical coreset results;
- L1–L2 are elementary.

## 7. Counterexamples and examples added in Stage 2

| ID | Shows |
|---|---|
| L4 | A minimum witness needing a non-vertex (triangle and centroid side point). |
| L9 | Aligned safety and sensing (finite menu) still give minimal traps of every size. |
| X5 | Net certificates failing forever, by tangential safety or by a zero-margin trap. |
| Q2 | Bump experiments, which need $\sim(L_h/\mu)^d$ steps; X2 variants with unbounded horizons at fixed constants. |
| Q3 | Arbitrary approach rates to an asymptotic obstruction. |
| Q4 | Attainable accuracy jumping from $\ge\tfrac12$ to $\le0.02$ under an arbitrarily small safety relaxation. |

## 8. Verification

- **`scripts/linear.py`.** Exact rational linear models, compiled to the combinatorial instances of `scripts/traps.py`, whose exhaustive solver is the reference.
- **`scripts/stage2_checks.py`** (E005, about 45 s) covers:
  - the support-function characterization on 48,520 subsets, including collinear, repeated, rational-circle, equality and touching cases, and $a=0$, $c=0$, $\delta=0$;
  - hull invariance;
  - the ray bound;
  - the interior-witness example;
  - the 1-D algorithm (1,500/1,500);
  - the planar convex $\sigma$ algorithm (12,647/12,647);
  - the clique reduction (150/150);
  - the laminar reduction (63/63);
  - aligned instances;
  - the support-sampling bound;
  - the circle witness count ($\sqrt\gamma\,\sigma_\gamma=2.227$ against $\pi/\sqrt2=2.221$);
  - the net perturbations (33,056 pairs).
- **Bugs found.** The checks themselves had three: a wrong halfplane, indices used as coordinates, and half-circle sampling. Each was caught by a failing comparison and fixed. No mathematical claim had to change.
- **Weak evidence.** Only 2 minimal traps of size $\ge3$ arose in the random planar instances, so L3 rests on its proof.
- **Tests.** 40 tests, all passing (10 new).

## 9. Recommended Stage 3

1. **G-O1, fixed-dimensional hardness.** The single most valuable open problem. Attempt it in this order:
   - **$d=3$ first,** via the paraboloid route: find, or prove NP-complete, a planar SAT variant whose clauses are empty-circle triangles with negated literals on the hull;
   - **then $d=2$,** where L10 and the arc structure suggest looking for a *polynomial* algorithm in convex position first.

   A dichotomy "polynomial for $d\le d_0$, NP-complete for $d>d_0$" would be the cleanest possible theorem for the paper.
2. **W-O1: FPT in $r$ for fixed $d$.** The profile approach reduces it to a multicolored compatibility problem in the observation projections. Decide whether that problem is tractable for linear projections.
3. **Q-K5: bound $\mu(\varepsilon)$ from a quantitative (L).** This would make Q1′ fully explicit in the data.
4. **Begin consolidating the manuscript structure,** once G-O1 is settled either way.

**Not recommended:** further restricted classes without a structural reason, stochastic noise, or RL.
