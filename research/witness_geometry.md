# Stage 2 — Geometry of the safety-witness number

*2026-11-22. Notation follows `research/linear_identifiability.md`.*

**Conventions** (unchanged from Stage 1).
- For an uncertainty set $K$ and experiment $u$, the **trace** is $T_u(K)=\{\theta\in K : g(\theta,u)>0\}$.
- $u$ is **blocked** by $K$ if $T_u(K)\ne\varnothing$, and $B(K)$ is the set of blocked experiments.
- $\sigma(K)=\min\{\lvert S\rvert : S\subseteq K,\ B(S)=B(K)\}$.
- Since $S\subseteq K$ always gives $B(S)\subseteq B(K)$, $\sigma(K)$ is the minimum size of a set of points hitting every nonempty trace. By convention $\sigma(\varnothing)=0$, and $\sigma(K)=0$ iff nothing is blocked.

**Checks.** E005 §§C, D, F (`results/stage2_checks.txt`).

## 0. Summary

| ID | Statement | Status |
|---|---|---|
| W1 | $\sigma(K)\le r(K)$, the number of positive rays among blocked nonzero normals, plus one if the only blocked experiments have constant safety. Sharp. One maximizer per ray is an explicit witness, computable in $O(nr)$. | proved |
| W2 | $\sigma(K)\le\min\{r(K),\ \lvert V(K)\rvert,\ \lvert B(K)\rvert\}$. No bound in terms of the dimension. A minimum witness may need non-vertices. | proved |
| W3 | Computing $\sigma$ is minimum hitting set. NP-hard in general, even for linear safety with $d$ unbounded. | proved (reduction) |
| W4 | $d=1$: $\sigma\le2$, computed in $O(nm)$. $d=2$ with $K$ in convex position: circular-arc hitting set, exact, in $O(k\,m\log m)$. $d=2$ in general: polynomial, by the half-plane hitting-set literature. | proved / proved / cited |
| W5 | $d=3$: computing $\sigma$ is NP-hard, **even with $K$ in convex position** (on a paraboloid). | proved from a cited NP-hardness |
| W6 | Four different bounds, kept distinct: minimal-trap size; $\sigma$ of arbitrary sets; witnesses needed to *detect* non-identifiability; *efficient* witness construction. | §4 |

**Answer to the brief's question 3.**
- Yes. In the linear model, $\sigma$ is controlled by **directional complexity**, the number of safety rays $r$, and by **extremal geometry**: the vertex count and the convex-position number $c(\Theta_0)$.
- Dimension alone controls nothing, because planar configurations already reach $\sigma=n$.
- The directional parameter gives XP algorithms, and is W[1]-hard as a parameter (L7).
- The cost of *computing* $\sigma$ jumps from polynomial in the plane to NP-hard in space. It is a separate problem from identifiability.

## 1. Directional complexity

> **Theorem W1.** Let $K$ be finite and nonempty, and let $\mathcal R$ be the set of positive rays $\{\mathbb R_{>0}a_u : u\in B(K),\ a_u\ne0\}$, with $r=\lvert\mathcal R\rvert$. For each ray $\rho\in\mathcal R$ pick any $\theta_\rho\in\arg\max_K a^\top\theta$, with $a\in\rho$. Then $S=\{\theta_\rho\}$ satisfies $B(S)\supseteq B(K)\cap\{a_u\ne0\}$. Hence:
> - $\sigma(K)\le r$ if $r\ge1$;
> - $\sigma(K)\le1$ if $r=0$ and some blocked experiment has $a_u=0$.

*Proof.*
- Let $u\in B(K)$ with $a_u\ne0$ on ray $\rho$, so $a_u=\lambda a$ with $\lambda>0$.
- The maximizer of $a$ maximizes $a_u$ as well, because positive scaling preserves argmax. So $a_u^\top\theta_\rho=h_K(a_u)>b_u$, and $u\in B(S)$.
- Ties are harmless: every maximizer works.
- An experiment with $a_u=0$ is blocked iff $b_u<0$, and then it is blocked by any nonempty set. ∎

**Remarks.**
- *Opposite normals.* $a$ and $-a$ are maximized at different points, so the bound counts them as two rays. The two-point example with normals $\pm1$ in $\mathbb Q^1$ has $\sigma=2=r$ (E005 §C).
- *Sharpness.* In the convex-position trap (G3(c)) and the aligned parabola (L9), each experiment blocks exactly one parameter, along its own ray, so $\sigma(\Theta_0)=n=r$. On random instances with 1–3 rays, $\sigma=r\ge2$ occurred in 359 subsets, and $\sigma>r$ never (E005 §C).
- *Explicit witness.* Computing the maximizers takes $O(nr)$. This gives a witness of size $\le r$ in linear time, though not a minimum one.

**Algorithmic consequence.** Lemma W gives, from any far trap, a far trap of size $\le\sigma+2\le r+2$. This is L7(a), $O(n^{r+2}m)$.
- That is XP, not FPT.
- L7(b) shows that an $f(r)\,\mathrm{poly}(n,m)$ algorithm would imply FPT $=$ W[1], at least when the dimension is unbounded.
- With $d$ fixed, the question is open. The natural route is to guess the support profile $(h_K(a_\rho))_\rho$, which has at most $n^r$ possibilities, and then solve a multicolored compatibility problem in the observation projections. The second step is itself a clique-type problem, so the profile route does not obviously give FPT.

## 2. Extremal geometry

> **Proposition W2.**
> - (a) $\sigma(K)\le\min\{r(K),\ \lvert V(K)\rvert,\ \lvert B(K)\rvert\}$. More precisely, $\sigma(K)$ is at most the number of distinct faces $\arg\max_{\operatorname{conv}K}a_u$, for $u\in B(K)$ with $a_u\ne0$, that are needed to cover the traces.
> - (b) For every $d\ge2$ and $n$, there are $K\subset\mathbb Q^2\subseteq\mathbb Q^d$ with $\sigma(K)=n$. So no bound in terms of affine dimension exists.
> - (c) $\sigma(K)\le\sigma(V(K))$, and the inequality can be strict (Example L4).

*Proof.*
- (a) Each blocked trace contains a maximizer of its normal, which can be chosen as a vertex of $\operatorname{conv}K$. So $V(K)$ is a witness, and so is any choice of one point per blocked experiment.
- (b) Points in convex position, each cut off by its own halfplane: G3(c).
- (c) $B(K)=B(V(K))$, and a witness for $V(K)$ is a witness for $K$. ∎

**What the bounds measure.** None of them alone is the "right" geometric invariant:
- the vertex count measures extremal complexity, and is large for round configurations;
- the ray count measures directional complexity, and is large for rich experiment menus;
- $\sigma$ is the minimum of the true hitting problem. Example L4 shows that an interior point can serve three directions at once.

**What bounds minimal traps.** Minimal traps are in convex position (L3). So the parameter that bounds *trap size* is the convex-position number $c(\Theta_0)$, or $r+2$, whichever is smaller. It is not $\sigma$ of arbitrary sets.

## 3. Computing $\sigma$

**As hitting set.** $\sigma(K)$ is the minimum hitting set of the hypergraph $\{T_u(K) : u\in B(K)\}$ on vertex set $K$. Equivalently, it is the minimum set cover of $B(K)$ by the sets $\{u : \theta\in T_u\}$, for $\theta\in K$.

> **Proposition W3.** Deciding $\sigma(K)\le k$ is NP-complete for the linear model with $d$ unbounded. It is not approximable within $(1-o(1))\ln\lvert B(K)\rvert$ unless P $=$ NP.

*Proof.*
- **Membership** is trivial.
- **Hardness.** Any hypergraph $\{V_j\}$ on $[n]$ is the trace hypergraph of the standard basis $\{e_i\}$ under the halfspaces $\langle\mathbf 1_{V_j},\theta\rangle>\tfrac12$ (as in L6). Hitting set is NP-complete.
- **Inapproximability.** Hitting set is equivalent to set cover under duality, which carries the set-cover threshold. I cite Dinur–Steurer (2014) for that threshold (access level A: secondary statement only). ∎

> **Proposition W4.**
> - (a) $d=1$: $\sigma(K)\le2$, witnessed by $\{\min K,\max K\}$ and computed in $O(\lvert K\rvert m)$.
> - (b) $d=2$, $K$ in convex position, $k=\lvert K\rvert$: $\sigma(K)$ is computed exactly in $O(k\,m\log m)$.
> - (c) $d=2$, $K$ arbitrary: $\sigma(K)$ is computable in polynomial time.

*Proof.*
- **(a)** In one dimension the unsafe sets are up-sets and down-sets.
- **(b)** For points in convex position, a halfplane's trace is a contiguous arc of the cyclic hull order: a line meets the boundary of a convex polygon in at most two points. This makes $\sigma$ a circular-arc hitting set.
  - Some point $p$ of the first arc lies in an optimal solution. For each of its $\le k$ choices, delete the arcs containing $p$ and cut the cycle just after $p$.
  - The remaining arcs are intervals, and the interval-stabbing greedy (sort by right endpoint, stab when unstabbed) is optimal for intervals.
  - Take the best of the $\le k$ runs.
  - `sigma_convex_planar` implements this. It agreed with brute-force minimum hitting set on 12,647 (instance, subset) pairs (E005 §F).
- **(c)** Point–line duality turns hitting halfplanes with points into covering points with halfplanes. Polynomial algorithms are in the literature:
  - Har-Peled–Lee 2012, weighted cover by halfplanes, $O((m+n)^6)$;
  - arXiv:2506.16979 (2025), "Minimum-weight half-plane hitting set", $O(n^{5/2}\log^2n)$, per its abstract.

  Access level A: I have not checked these proofs. (b) is the convex-position special case, proved here. ∎

> **Proposition W5.** For $d=3$, deciding $\sigma(K)\le k$ is NP-complete, even with $K$ in convex position.

*Proof.*
- Reduce from discrete unit disk cover (DUDC): given points $C$ and candidate centres $P$ in $\mathbb Q^2$, can $k$ unit disks centred in $P$ cover $C$? This is NP-hard (Johnson 1982, cited by later DUDC papers; access level A).
- **Symmetry.** $\lvert p-q\rvert\le1$ is symmetric. So the DUDC instance is the same as: choose $k$ points of $P$ hitting every disk $D(q,1)$ for $q\in C$.
- **Lifting.** Lift $p\mapsto\hat p=(p,\lvert p\rvert^2)$. Then $\lvert p-q\rvert^2<\rho^2$ iff $2q^\top p-\lvert p\rvert^2>\lvert q\rvert^2-\rho^2$, i.e. iff $\hat p$ lies in the open halfspace with normal $(2q,-1)$ and threshold $\lvert q\rvert^2-\rho^2$.
- **Open versus closed.** Choose $\rho$ slightly above 1, between 1 and the next distance in the finite instance, so that open and closed disks agree. Rationality is preserved by working with squared distances.
- **Result.** $\sigma(\hat P)$ under these experiments is the DUDC optimum.
- The lifted points lie on the paraboloid, hence are in convex position. ∎

> **Proposition W5′ (Stage 4; self-contained).** For $d=4$, deciding $\sigma(K)\le k$ is NP-complete, even with $K$ in convex position.

*Proof.*
- Reduce from vertex cover. Place the vertices of $G$ at integers $t_i$ on the moment curve $(t,t^2,t^3,t^4)$.
- For each edge $\{i,j\}$, take the experiment unsafe on $\{\theta : -(t-t_i)^2(t-t_j)^2>-\tfrac12\}$. The expression is linear in $\theta$ (R4(c)), so the experiment is a halfspace, and its trace is exactly $\{i,j\}$.
- A witness set is then a vertex cover. Coefficients are integers of polynomial size. ∎

This removes the dependence on the unread Johnson (1982) for dimension 4. Dimension 3 still rests on the citation.

**Approximation.**
- For halfspaces in $\mathbb R^2$ and $\mathbb R^3$, hitting sets admit $O(1)$-approximation via $\varepsilon$-nets of size $O(1/\varepsilon)$ (Matoušek–Seidel–Welzl 1990) and the Brönnimann–Goodrich reweighting method. Access level M: metadata only.
- An LP relaxation gives a certified lower bound, the fractional hitting number, and a rounded solution gives an upper bound within a constant factor.

**Do the bounds yield efficient identification certificates?**
- **Non-identifiability.** The certificate is a trap, checkable in polynomial time (Proposition M). It needs no $\sigma$ at all.
- **Identifiability.** The bounds give *algorithms*: enumerate subsets of size $\le\min(r,c(\Theta_0))+2$. They do not give succinct certificates.
- An upper bound $\hat\sigma(K)\ge\sigma(K)$ on one set $K$ bounds the traps inside that $K$, not the traps of $\Theta_0$. A global bound needs a parameter that bounds $\sigma$ on every subset, e.g. $r$ or $c$.

## 4. Four statements kept apart

1. **Minimal-trap size.**
   - $\le\max(2,\sigma(K))$ at $\varepsilon=0$, using $\sigma$ of the trap itself (Stage 1, T5);
   - $\le c(\Theta_0)$ (L3);
   - $\le r+2$ (W1 together with Lemma W).
2. **$\sigma$ of an arbitrary set:** W1/W2. This may be large on sets that are nowhere near traps.
3. **Witnesses needed to detect non-identifiability:** the maximum size of a minimal far trap, which is bounded by item 1. It can be much smaller than $\max_K\sigma(K)$, since a large-$\sigma$ set need not be a trap.
4. **Efficient construction.**
   - *Per-set witnesses.* Maximizers give a size-$\le r$ witness in $O(nr)$ (W1). A *minimum* witness is polynomial in $d\le2$ and NP-hard in $d=3$ (W4, W5).
   - *Detecting identifiability.* This needs neither: it enumerates candidate traps up to the size bound in item 1.
   - *Generally.* The complexity of TRAP and of computing $\sigma$ are unrelated in general. TRAP in $d=3$ is open, while $\sigma$ there is NP-hard. In unbounded $d$ both are hard.

## 5. Open questions

- **W-O1.** Is TRAP FPT in $r$ for fixed $d$?
- **W-O2.** Do points in planar convex position admit an algorithm polynomial in both $n$ and $r$ for TRAP? *Answered in Stage 3: no, unless P $=$ NP (D2, unit circle).*
- **W-O3.** A continuum $\sigma$: `research/approximate_witnesses.md` replaces it by the approximate witness number $\sigma_\gamma$, which is finite.
