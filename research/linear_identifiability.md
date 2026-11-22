# Stage 2 — Safe identifiability under linear safety and linear observations

*2026-11-21. Definitions follow `research/finite_trap_theory.md`. Code: `scripts/linear.py`. Exhaustive checks: `scripts/stage2_checks.py`, output `results/stage2_checks.txt` (ledger E005). Agreement with brute force is a regression check, never part of a proof.*

## 0. Summary

| ID | Statement | Status |
|---|---|---|
| L1 | $K$ is a trap iff every experiment is **blocked** ($h_K(a_u)>b_u$) or **blind** ($w_K(c_u)\le2\delta_u$). | proved |
| L2 | The trap property, the far property, $\mathcal S(K)$ and $\operatorname{diam}K$ depend only on the vertex set of $\operatorname{conv}K$. | proved |
| L3 | Every minimal far trap is in convex position. Hence minimal traps have size $\le c(\Theta_0)$, the largest convex-position subset. This improves G3's $c+2$. | proved |
| L4 | The minimum safety witness is **not** hull-invariant: $\sigma(K)$ can require a non-extreme point. | example |
| L5 | $d=1$: $K$ is a trap iff $\{\min K,\max K\}$ is. $O(n^2m)$. | proved |
| L6 | $d$ part of the input: NP-complete, even with all of the following at once: parameters in convex position (affinely independent); a common noise radius; every unsafe trace of size $\le2$; and the unsafe traces forming a **laminar** family. | proved |
| L7 | Parameterized by the number $r$ of distinct safety rays: XP, $O(n^{r+2}m)$, and **W[1]-hard** ($d$ unbounded). So no $f(r)\,\mathrm{poly}$ algorithm unless FPT $=$ W[1]. | proved |
| L8 | Safety normals on at most two opposite rays ($\pm a$): pairs suffice at $\varepsilon=0$, $O(n^2m)$. | proved |
| L9 | Aligned observations ($c_u=a_u$) do not bound minimal traps: the aligned parabola has minimal traps of every size $n\ge4$ in the plane. | proved |
| L10 | A negative ("not both") constraint from an always-safe experiment forces **opposite caps**. This is the exact geometric obstruction that defeats the *direct* planar reductions. | proved (lemma). Fixed-$d$ complexity: **resolved in Stage 3**, coNP-complete for $d\ge2$ (D2–D3) |

**Answers to the brief's questions 1 and 2.**
- **Hardness survives linear geometry in unbounded dimension.** It survives even in its most restrictive form: convex position, common noise, laminar unsafe sets of size $\le2$ (L6). It also survives parameterization by the number of safety directions (L7).
- **Tractability is restored by:**
  - one dimension (L5);
  - a bounded number of safety rays (XP only, L7);
  - opposite-ray safety (L8);
  - unsafe traces of size $\le1$ (Stage 1, P3);
  - nested traces (P4).
- **Not by:** convex position, aligned observations, common noise radius, or laminarity.
- **Open at Stage 2; resolved in Stage 3:** fixed dimension $d\ge2$. *Stage 3 (`research/fixed_dimension_complexity.md`, D2–D3) proves coNP-completeness already in $\mathbb Q^2$, with all parameters on the unit circle. So the critical dimension is 2.* The Stage 2 text below is kept as the record of why the *direct* reductions fail.

## 1. The model

- **Parameters.** $\Theta_0=\{\theta_1,\dots,\theta_n\}\subset\mathbb Q^d$.
- **Experiments.** $u=(a_u,b_u,c_u,\delta_u)\in\mathbb Q^d\times\mathbb Q\times\mathbb Q^d\times\mathbb Q_{\ge0}$.
  - *Safety.* $u$ is safe for $\theta$ iff $a_u^\top\theta\le b_u$, so it is safe at equality.
  - *Observation.* $\mathcal Y(\theta,u)=[c_u^\top\theta-\delta_u,\ c_u^\top\theta+\delta_u]$, closed.
- **Degenerate cases** are allowed and tested (E005 §A):
  - $a_u=0$ (constant safety);
  - $c_u=0$ (a blind experiment);
  - $\delta_u=0$ (exact observation);
  - collinear and repeated parameters.
- **Repeated parameters.** Two parameters with identical coordinates are observationally equivalent. They always form a trap, so identification is understood up to this equivalence.
- **Encoding.** Rationals in binary. All arithmetic here is exact, and every predicate below is a comparison of rational linear forms. So complexity statements are in the Turing model, with no real-arithmetic issues.

Write $h_K(v)=\max_{\theta\in K}v^\top\theta$ for the support function and $w_K(v)=h_K(v)+h_K(-v)$ for the width.

## 2. Geometric characterization

> **Theorem L1.** For finite nonempty $K\subseteq\Theta_0$:
> $$K\text{ is a trap}\iff\forall u:\quad h_K(a_u)>b_u\ \ \lor\ \ w_K(c_u)\le2\delta_u .$$

*Proof.*
- $u\in\mathcal S(K)$ iff $a_u^\top\theta\le b_u$ for all $\theta\in K$, i.e. iff $h_K(a_u)\le b_u$.
- Closed intervals of common half-width $\delta$ centred at $x_1,\dots,x_k$ have a common point iff $\max x_i-\delta\le\min x_i+\delta$. This is Helly in dimension 1, with the common point $\max x_i-\delta$.
- With $x_i=c_u^\top\theta_i$, the condition is $w_K(c_u)\le2\delta_u$. ∎

**Boundary conventions.**
- Safety at equality and closed noise intervals are both "inclusive". So a set with $h_K(a)=b$ is not blocked, and touching intervals ($w_K(c)=2\delta$) are uninformative.
- With strict safety ($a^\top\theta<b$), "blocked" becomes $h_K(a)\ge b$; nothing below changes.
- With open noise intervals, "blind" becomes $w_K(c)<2\delta$.
- Both variants appear in E005 through the equality cases.

> **Corollary L2 (hull invariance).** Let $V(K)$ be the vertex set of $\operatorname{conv}K$. Then $h_K=h_{V(K)}$ and $\operatorname{diam}K=\operatorname{diam}V(K)$. Consequently:
> - $\mathcal S(K)=\mathcal S(V(K))$;
> - $K$ is a trap iff $V(K)$ is;
> - $K$ is far iff $V(K)$ is.

*Proof.* Linear functionals and the convex function $\lVert\theta-\theta'\rVert$ attain their maxima over $\operatorname{conv}K$ at vertices. ∎

So **a trap is a lattice polytope of $\Theta_0$**: a convex polytope $P$ with vertices in $\Theta_0$. The only conditions are linear support inequalities at the safety normals, and width bounds at the observation directions. Arbitrary subsets enter only through their hulls.

> **Corollary L3.** Every minimal far trap $K$ with $\lvert K\rvert\ge3$ is in convex position. Hence every minimal far trap has size at most
> $$c(\Theta_0)=\max\{\lvert X\rvert : X\subseteq\Theta_0\text{ in convex position}\}.$$

*Proof.*
- If $\theta\in K$ is not a vertex of $\operatorname{conv}K$, then $K\setminus\{\theta\}$ has the same hull, hence is a far trap (L2).
- It has at least 2 elements, because $\lvert V(K)\rvert\ge2$ when $K$ is far. This contradicts minimality. ∎

**Remarks.**
- This sharpens Stage 1's G3, which gave $c+2$ through $\sigma$.
- It holds for every $\varepsilon\ge0$.
- In E005 §B the convex-position property held for every minimal trap of size $\ge3$. Random small planar instances rarely have such traps (only 2 were seen), so the evidence for L3 is the proof.

> **Example L4 (minimum witnesses are not hull-invariant).**
> - **Setup.** $\Theta_0=\{v_0,v_1,v_2,g\}$ with $v_0=(0,0)$, $v_1=(6,0)$, $v_2=(0,6)$, and centroid-side point $g=(2,2)$. Three experiments with unsafe sets $x+y<5$, $x>\tfrac32$ and $y>\tfrac32$.
> - **Traces.** $\{v_0,g\}$, $\{v_1,g\}$ and $\{v_2,g\}$.
> - **Witnesses.** $\sigma(\Theta_0)=1$, witnessed by $g$. Every witness made of hull vertices needs all three (E005 §D).

So $\sigma(K)\le\sigma(V(K))$, and the inequality can be strict. The trap property is a property of the hull. The *optimization* of witness sets is not. This is the distinction the brief asked to keep (see `research/witness_geometry.md` §3).

## 3. Complexity

### 3.1 Dimension one

> **Theorem L5.** For $d=1$ and every $\varepsilon\ge0$, a far trap exists iff some pair $\{\theta_i,\theta_j\}$ is a far trap. Decidable in $O(n^2m)$.

*Proof.* By L2, a trap $K$ in one dimension has hull $[\min K,\max K]$, so $\{\min K,\max K\}$ is a trap with the same diameter. *Regression:* 1500/1500 (E005 §E). ∎

This covers the scalar model, and any model whose parameters lie on a line in $\mathbb R^d$, since restricted to a line every functional is affine in the line coordinate.

### 3.2 Dimension part of the input

> **Theorem L6.** $\mathrm{TRAP}_0$ for the linear model is NP-complete, and $\mathrm{SAFEID}_0$ coNP-complete, already when all of the following hold:
> 1. the parameters are the standard basis vectors of $\mathbb Q^n$, so they are in convex position;
> 2. every experiment has the same $\delta=\tfrac35$;
> 3. every unsafe trace has size $\le2$;
> 4. the unsafe traces form a laminar family.

*Proof.*
- **Membership:** Proposition M.
- **Hardness.** Take the Stage 1 encoding H1(d) of the reduction `sat_laminar` (`scripts/traps.py`):
  - parameter $i$ becomes $e_i$;
  - an unsafe set $V$ becomes the halfspace $\langle\mathbf 1_V,\theta\rangle\le\tfrac12$, whose trace is exactly $V$;
  - binary symbol patterns become linear observations $\langle c_u,\theta\rangle$ with $(c_u)_i\in\{-1,0,1\}$ and $\delta=\tfrac35$.
- **The laminar reduction.** It is `sat_u2` with every clause using *private copies* $\kappa_{j,1},\kappa_{j,2},\kappa_{j,3}$ of its literals. Its unsafe sets are:
  - $\{T_v,F_v\}$, $\{s_j,s'_j\}$ and $\{\kappa_{j,1},\kappa_{j,2}\}$, which are pairwise disjoint;
  - singletons $\{\kappa_{j,3}\}$, $\{\ell\}$ and $\{\kappa\}$, each contained in one of the pairs or disjoint from all of them.
- **Gadgets.**
  - The clause constraints are $s'_j\Rightarrow\kappa_{j,1}\vee\kappa_{j,2}$ and $s_j\Rightarrow\kappa_{j,3}$.
  - Copies are tied to originals by the two implications $\kappa\Rightarrow\ell$ (unsafe set $\{\ell\}$) and $\ell\Rightarrow\kappa$ (unsafe set $\{\kappa\}$). Both are $\mathsf O$-gadgets of Stage 1.
- **Correctness.** A set of size $\ge2$ is a trap iff it encodes a satisfying assignment, together with all copies of true literals and one choice of $s_j/s'_j$ per clause. The argument is that of H1(a) with copies substituted.
- *Regression:* 63/63 formulas, including degenerate ones (E005 §H). ∎

**Contrast.** Nested unsafe families are polynomial ($\sigma\le1$, Stage 1 P4). Laminar ones are hard. So the tractability of nested safety is a *chain* phenomenon, not a tree phenomenon.

### 3.3 Parameterization by safety directions

The **safety rays** of an instance are the distinct positive rays $\mathbb R_{>0}a_u$, for $a_u\ne0$.
- Positively collinear normals ($a'=\lambda a$, $\lambda>0$) share a ray.
- Opposite normals ($a$ and $-a$) do not.

> **Theorem L7.** Let $r$ be the number of safety rays.
> - (a) $\mathrm{TRAP}_\varepsilon$ is decidable in $O(n^{r+2}m)$ time, i.e. in XP in $r$.
> - (b) $\mathrm{TRAP}_0$ parameterized by $r$ is W[1]-hard, with the dimension unbounded.

*Proof.*
- **(a)** By `research/witness_geometry.md` W1, $\sigma(K)\le r$. Lemma W of Stage 1 then gives a far trap of size $\le r+2$ whenever a far trap exists. Enumerate.
- **(b)** Reduction from MULTICOLORED CLIQUE, parameter $k$: a graph with color classes $V_1,\dots,V_k$; is there a clique with one vertex per class?
  - **Parameters.** One per vertex, in $\mathbb Q^D$ with $D=k+\lvert C\rvert+1$, where $C$ is the set of *conflicts*: pairs in the same class, or non-adjacent pairs in different classes. Vertex $v\in V_i$ has:
    - coordinate $i$ equal to 1;
    - for each conflict $(p,q)\in C$, $\pm1$ if $v\in\{p,q\}$ (sign $+$ for $p$) and $0$ otherwise;
    - a last coordinate equal to $10\cdot\mathrm{index}(v)$.
  - **Class experiments** $u_i$: $a=e_i$, $b=\tfrac12$, so the unsafe trace is $V_i$; $c=e_D$ and $\delta=1$, which separates every pair. $u_i$ kills exactly the sets of size $\ge2$ avoiding $V_i$.
  - **Conflict experiments** $u_{pq}$: always safe ($a=0$, $b=0$); $c=e_{k+j}$ and $\delta=\tfrac35$. They kill exactly the sets containing both $p$ and $q$.
  - **Correctness.** A set of size $\ge2$ is a trap iff it meets every class and contains no conflict, i.e. iff it is a multicolored clique. Here $k\ge2$, and the safety rays are $e_1,\dots,e_k$, so $r=k$. The size is polynomial.
  - *Regression:* 150/150, with at most $k$ rays (E005 §G). ∎

**Reading.**
- XP is the right complexity for the safety-direction parameter. A bounded number of directions makes safe identification polynomial, but the degree of the polynomial must grow with the number of directions, unless FPT $=$ W[1].
- In (b) the dimension grows with the number of conflicts. Whether TRAP is FPT in $r$ **for fixed $d$** is open.

### 3.4 Restricted classes

> **Theorem L8 (opposite rays).** If every nonzero $a_u$ lies on $\pm a$ for one vector $a$, then at $\varepsilon=0$ a trap of size $\ge2$ exists iff a trap pair exists. Decidable in $O(n^2m)$.

*Proof.*
- $\mathcal S(K)$ depends only on $\max_K a^\top\theta$ and $\min_K a^\top\theta$.
- Let $W=\{\theta^+,\theta^-\}$ be a maximizer and a minimizer. If they are distinct, $W$ is a trap pair: it has the same safe set, and smaller widths.
- If every point of $K$ has the same value of $a^\top\theta$, then any pair from $K$ has the same safe set. ∎

> **Proposition L9 (aligned observations do not help).** Take $\theta_i=(i,i^2)$, $i=0,\dots,n-1$, and experiments $a_k=c_k=(2k,-1)$, $b_k=k^2-\tfrac12$, $\delta=\tfrac14$. For $n\ge4$, $\Theta_0$ is the only trap of size $\ge2$.

*Proof.*
- $a_k^\top\theta_i=k^2-(i-k)^2$. This exceeds $b_k$ only at $i=k$, so $a_k$ is unsafe exactly at $\theta_k$, and $\Theta_0$ is a trap.
- Observations are integers, so two parameters are separated by $a_k$ iff $(i-k)^2\ne(j-k)^2$, i.e. iff $i+j\ne2k$.
- **Pairs.** A proper subset $\{i,j\}$ misses $n-2\ge2$ indices, and at most one of them equals $(i+j)/2$.
- **Larger sets.** A proper subset with $\ge3$ elements misses some $k$. Among three of its elements at most one pair sums to $2k$, so $a_k$ separates some pair.
- Verified for $n\le8$ (E005 §I). At $n=3$ the pair $\{0,2\}$ is a trap, as predicted. ∎

On random aligned instances, traps fail to be closed under subsets in 630 of 1500 cases (E005 §I). Stage 1's homogeneity theorem G4 needs **full scaling** of the experiments, not just alignment. With finite menus, alignment is not a structural restriction.

**Other restrictions examined.**
- **Common noise radius.** No effect on hardness (L6(2)).
- **Unsafe traces of size $\le1$.** Polynomial (P3) in any geometry. Size 2 is NP-complete (L6(3)).
- **Points on a line.** Same as $d=1$.
- **Points on a convex curve in the plane.** Same as planar convex position, which is open (§5).
- **Orthogonal safety and observation directions.** I have no result for this restriction.

## 4. What fixed dimension does give

For fixed $d$ with no other restriction, the strongest results I can prove are:
1. witness enumeration in $O(n^{c(\Theta_0)}m)$ (L3), which is polynomial when $c(\Theta_0)$ is bounded, e.g. points on boundedly many lines;
2. $O(n^{r+2}m)$ in the number of safety rays (L7);
3. **computing $\sigma$ is polynomial for $d=2$ and NP-hard for $d=3$** (`research/witness_geometry.md` W4, W5). This does **not** transfer to TRAP: trap existence never requires computing $\sigma$.

## 5. Fixed dimension $d\ge2$: the obstruction

> **Lemma L10 (negative constraints are opposite caps).** Let $u$ be safe for all of $\Theta_0$, and let $X,Y\subseteq\Theta_0$ be disjoint and nonempty. Suppose $u$ kills a set $K$, i.e. $w_K(c_u)>2\delta_u$, exactly when $K$ meets both $X$ and $Y$. Then, possibly after swapping $X$ and $Y$:
> - there are $t_1<t_2$ with $X=\{\theta : c_u^\top\theta<t_1\}\cap\Theta_0$ and $Y=\{\theta : c_u^\top\theta>t_2\}\cap\Theta_0$;
> - every other parameter lies in the slab $t_1\le c_u^\top\theta\le t_2$.
>
> In other words, $X$ and $Y$ are opposite caps.

*Proof.* Write $\pi=c_u^\top\theta$.
- Every pair inside $X\cup Y$ that is not an $X$–$Y$ pair has $\lvert\pi(p)-\pi(q)\rvert\le2\delta_u$.
- Pick $x\in X$ and $y\in Y$ with $\pi(y)-\pi(x)>2\delta_u$. For $z\notin X\cup Y$, compatibility with both gives $\pi(y)-2\delta_u\le\pi(z)\le\pi(x)+2\delta_u$, and $\pi(x)+2\delta_u<\pi(y)$.
- The same holds for every $x'\in X$ and $y'\in Y$. So $\max_X\pi<\min\pi(\text{rest})$ and $\max\pi(\text{rest})<\min_Y\pi$. Take $t_1,t_2$ in the gaps. ∎

**Why the natural reductions fail in the plane.** Every hardness proof above uses three ingredients:
- (i) "not both" constraints between literal sets, which by L10 must be opposite caps;
- (ii) "at least one" clause constraints, whose unsafe traces are caps that meet exactly the chosen literal points;
- (iii) copies, to keep clause traces simple.

In the plane, caps are halfplane traces.

- **Convex position.** Caps are contiguous arcs of the cyclic order. A clause cap meeting three literal arcs must contain every arc between them. Together with the antipodal structure of opposite caps, the realizable formulas are those whose clauses touch cyclically consecutive literal arcs. Formulas of bounded cyclic bandwidth like these are solvable by dynamic programming. **This reduction strategy therefore cannot prove hardness in planar convex position.** That is not a proof of tractability: other constraint shapes are possible, since a general experiment kills $K$ iff $K$ avoids a cap *and* contains a pair far apart in $c_u$.
- **General planar position.** The literal sets of (i) are caps in directions $\pm c_v$, which spread around the configuration. A clause cap that takes one point from three such caps, while excluding everything else, needs the three caps to be nearly contiguous in angular order. I could not make this precise as an impossibility, nor circumvent it.
- **$d=3$, the most promising route.** Lift a planar configuration to the paraboloid $z=x^2+y^2$. Halfspace traces become disk traces in the plane, so clause caps become *empty circles* through three literal clusters. Linear observations become radial functions $c_3\lvert q-q_0\rvert^2+c'^\top q$.
  - *What works.* "Not both" constraints are then realizable as nearest/farthest clusters from a centre $q_0$.
  - *What breaks.* The farthest cluster must be a vertex of the planar hull. That forces each variable's negative-literal cluster onto the hull, and empty circles through hull clusters and interior clusters then contain other clusters. A Delaunay-structured (planar) 3-SAT variant in which every clause is an empty-circle triangle *and* negations sit on the hull would complete the reduction. I do not know whether such a variant is NP-complete.

**Precise open problem (Stage 2), now resolved.** Is $\mathrm{TRAP}_0$ for the linear model in $\mathbb Q^2$, or $\mathbb Q^3$, decidable in polynomial time? *Stage 3 answer: no, unless P $=$ NP.* D2 shows coNP-completeness in $\mathbb Q^2$, on the unit circle. The obstruction above (L10, and arcs in convex position) is real but rules out only reductions that put literal points directly into clause traces. Private copies and forced helpers avoid it.
- minimal traps are unbounded in both: G3(c) and L9 give planar examples;
- $\sigma$ is polynomial in $\mathbb Q^2$ and NP-hard in $\mathbb Q^3$;
- by L10, every "not both" gadget is a pair of opposite caps.
