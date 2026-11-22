# Stage 3 — Safety, observation and joint geometric realizations

*2026-11-23. Checks: E006 §§B, C, E.*

**Definitions.** A combinatorial instance with interval-type observations is given by, for each experiment $u$, an unsafe set $B_u$ and a conflict graph $P_u$ (separated pairs).
- A **safety realization** in $\mathbb Q^{d_s}$: points $p_i$ and halfspaces $\{a_u^\top p>b_u\}$ with traces exactly $B_u$.
- An **observation realization** in $\mathbb Q^{d_o}$: points $q_i$, directions $c_u$ and radii $\delta_u$ with $\{ij : \lvert c_u^\top(q_i-q_j)\rvert>2\delta_u\}=P_u$.
- A **joint realization**: both at once, with one point set.

By 1-D Helly, preserving $P_u$ preserves the common-intersection property of every subset, so it preserves the whole trap structure. The exact observation centres need not be preserved, and this is the flexibility used below.

## 0. Summary

| ID | Statement | Status |
|---|---|---|
| R1 | A one-edge conflict graph $\{a,b\}$ is realizable on a fixed configuration iff $a,b$ are **strictly antipodal**: some $c$ has $a$ as unique minimizer and $b$ as unique maximizer. | proved |
| R2 | On a fixed $n$-point configuration in $\mathbb R^d$, the conflict graphs realizable by linear observations number $O(n^{2d})$. | proved |
| R3 | **Block sum.** Separate safety and observation realizations combine in dimension $d_s+d_o$ and preserve the instance exactly. Pairwise distances change, so this is valid for exact, not approximate, identification. | proved |
| R4 | Safety: any singleton (convex position); adjacent pairs (on a circle); *arbitrary* pairs in $\mathbb Q^4$ (moment curve, explicit integer halfspaces); arbitrary $k$-sets in $\mathbb Q^{2k}$. | proved |
| R5 | Observation, one-edge gadgets: perfect matchings in $\mathbb Q^2$ (antipodal points on a circle); any bipartite graph in $\mathbb Q^3$ (two orthogonal arcs). In the plane, at most $n$ strictly antipodal pairs exist. | proved / proved / cited |
| R6 | Joint: the D2 instances have joint realizations on the unit circle in $\mathbb Q^2$, because adjacency (safety) and antipodality (observation) impose independent constraints on an antipodally symmetric configuration. | proved |
| R7 | Binary patterns $\{0\},\{1\},\{0,1\}$ become intervals with centres $-1,1,0$ and $\delta=\tfrac12$. A fixed-dimensional *linear* realization of a pattern matrix needs the centre matrix, up to sign-preserving perturbations, to have rank $\le d$ plus a constant column. Arbitrary patterns need unbounded rank, which is why D2 avoids binary patterns. | proved / remark |

**Answer to the brief's questions 5 and 6.**
- **Q5.** The incompatibilities of Stage 2 are characterized by R1 together with the planar antipodality count. A lone forbidden pair must be a strictly antipodal pair, and a planar configuration has at most $n$ of them, so at most a linear number of independent negations.
- **Q6.** What governs joint realizability is the compatibility of two incidence structures on one configuration:
  - the **halfspace-trace hypergraph**, which in convex position consists of arcs;
  - the **strict antipodality graph**, which in the plane has at most $n$ edges.

  Hardness needs only singletons, adjacent pairs and a perfect antipodal matching, and these coexist on a circle.

## 1. Observation realizations

> **Lemma R1.** Let $Q$ be finite and $a\ne b\in Q$. There exist $c,\delta$ with conflict graph exactly $\{ab\}$ iff some $c$ has $c^\top a<c^\top z<c^\top b$ for all $z\in Q\setminus\{a,b\}$.

*Proof.*
- **(⇒)** This is Stage 2's L10 with $X=\{a\}$ and $Y=\{b\}$.
- **(⇐)** Put $\pi=c^\top\cdot$, $L=\pi(b)-\pi(a)$ and $M=\max(\pi(b)-\min_{\rm o}\pi,\ \max_{\rm o}\pi-\pi(a))<L$, where "o" ranges over the other points. Take $2\delta\in[M,L)$.
  - The pair $\{a,b\}$ conflicts, since $L>2\delta$.
  - Pairs involving one of $a,b$ and another point have gaps $\le M\le2\delta$.
  - Pairs of other points lie within an interval of length $<M$. ∎

*Check:* every one-edge conflict graph found among 300 random configurations, 20 directions each and all critical thresholds, joined the unique minimum and maximum (E006 §E).

> **Proposition R2.** For fixed $d$, the distinct conflict graphs realizable on an $n$-point $Q\subset\mathbb R^d$ number $O(n^{2d})$.

*Proof.*
- A conflict graph is determined by the order of the projections $\pi_c$ (with ties) and a threshold.
- The projection orders correspond to cells of the arrangement, on $S^{d-1}$, of the $\binom n2$ great spheres $\{c : c^\top(q_i-q_j)=0\}$. There are $O(n^{2(d-1)})$ such cells.
- For each order, the threshold matters only through which of the $O(n^2)$ gaps exceed it. ∎

So in fixed dimension the *observation alphabet* is polynomially bounded. Hardness in the plane therefore comes from combining polynomially many conflict shapes with the safety structure, not from an exponential variety of observations.

> **Proposition R5.**
> - (a) For any perfect matching $\{\{x_k,y_k\}\}$ there is a configuration in $\mathbb Q^2$ on which every pair is strictly antipodal: $x_k=v(k)$ and $y_k=-v(k)$ on the rational unit circle.
> - (b) For any bipartite graph between $A=\{a_1,\dots\}$ and $B=\{b_1,\dots\}$ there is a configuration in $\mathbb Q^3$ on which every $a_ib_j$ is strictly antipodal: $a_i=(t_i,0,1-t_i^2)$ and $b_j=(0,r_j,-1+r_j^2)$, with $\lvert t\rvert,\lvert r\rvert\le\tfrac14$ distinct rationals.
> - (c) In $\mathbb R^2$, a convex $m$-gon has $m-k$ strictly antipodal vertex pairs, where $k$ is its number of parallel side pairs (Nguyên–Soltan, as quoted in a secondary source, access level A). So at most $n$ lone-forbidden-pair gadgets exist on $n$ planar points.

*Proof.*
- **(a)** $c=v(k)$ attains its maximum 1 only at $v(k)$, and its minimum $-1$ only at $-v(k)$.
- **(b)** Take $c=(2t_i,-2r_j,1)$.
  - On $A$, $c^\top a(t)=2t_it-t^2+1$, maximized uniquely at $t=t_i$.
  - On $B$, $c^\top b(r)=-2r_jr+r^2-1$, minimized uniquely at $r=r_j$.
  - Values on $A$ are $\ge0.8$ and on $B$ are $\le-0.8$. So $a_i$ is the global unique maximum and $b_j$ the global unique minimum.
- In the plane the analogous two-arc configuration couples $t$ and $r$ through the single slope, so it gives only a matching. ∎

## 2. Safety realizations

> **Proposition R4.**
> - (a) In convex position, every singleton is a halfspace trace.
> - (b) On the unit circle, every pair of cyclically adjacent points is a trace, with normal $v_x+v_y$.
> - (c) On the moment curve $\mu(t)=(t,t^2,t^3,t^4)$ at integers $t_1<\dots<t_n$, every pair $\{t_i,t_j\}$ is the trace of $\{\theta : -\,p_{ij}(\theta)>-\tfrac12\}$, where $p_{ij}(\mu(t))=(t-t_i)^2(t-t_j)^2$, read as a linear function of $\mu(t)$ plus a constant. Coefficients are integers of polynomial size.
> - (d) Generally, $(t-t_{i_1})^2\cdots(t-t_{i_k})^2$ isolates any $k$-set on the moment curve in $\mathbb Q^{2k}$.

*Proof.*
- (a) Standard.
- (b) See D2.
- (c), (d) The polynomial is a nonnegative integer at integer points, and $0$ exactly at the chosen $t$. So "$<\tfrac12$" holds exactly there. ∎

**Consequence (the fixed-dimension route the brief suggested).** By R3, R4(c) and R5(b), every instance from the Stage 1 reduction H1(a) whose lone-pair graph is bipartite has a joint realization in $\mathbb Q^{4+3}$. I did not pursue this, because D2 does better.

## 3. Block sums and joint realizations

> **Lemma R3.** Given safety data $(p_i,a_u,b_u)$ in $\mathbb Q^{d_s}$ and observation data $(q_i,c_u,\delta_u)$ in $\mathbb Q^{d_o}$, put $\theta_i=(p_i,q_i)$, $\tilde a_u=(a_u,0)$, $\tilde c_u=(0,c_u)$. Then every unsafe set and every conflict graph is unchanged. Distinct indices stay distinct parameters if either block separates them. Bit lengths add.
>
> Distances become $\lVert\theta_i-\theta_j\rVert^2=\lVert p_i-p_j\rVert^2+\lVert q_i-q_j\rVert^2$, so $\varepsilon$-identification of the combined instance is a different problem.

*Proof.* $\tilde a_u^\top\theta_i=a_u^\top p_i$ and $\tilde c_u^\top\theta_i=c_u^\top q_i$. *Regression:* 200 random block pairs (E006 §C). ∎

> **Proposition R6.** Let $\mathcal I$ be an instance whose unsafe sets are singletons or pairs, and whose conflict graphs are complete or single edges. Suppose:
> - the single-edge pairs form a matching $\mathcal M$;
> - the unsafe pairs are disjoint;
> - each unsafe pair can be placed adjacently among the "upper" members of $\mathcal M$.
>
> Then $\mathcal I$ has a joint realization on the unit circle in $\mathbb Q^2$, with polynomial bit length.

*Proof.*
- Put the upper member of each matched pair at $v(k)$ and its partner at $-v(k)$, choosing the order of $k$ so that each required pair is consecutive.
- Unmatched points can be matched with fresh dummy partners that appear in no experiment.
- Then use R4(b) for adjacent pairs, R4(a) for singletons, R1/R5(a) for single edges, and a generic direction for complete conflict graphs. ∎

D2 is an instance of R6 in which every point is matched.

## 4. Binary patterns (R7)

- **The interval encoding.** For closed intervals with $\delta=\tfrac12$ and centres $-1,1,0$ (for $\{0\},\{1\},\{0,1\}$):
  - $[-\tfrac32,-\tfrac12]\cap[\tfrac12,\tfrac32]=\varnothing$;
  - each of these meets $[-\tfrac12,\tfrac12]$ in an endpoint.

  So a nonempty family has a common point iff it does not contain both $-1$ and $1$. That is exactly the binary rule. *(Stage 1 used $\delta=\tfrac35$, which works with slack; $\tfrac12$ works with touching endpoints.)*
- **Linear realization.** Realizing a whole pattern matrix *exactly* with centres $c_u^\top q_i$ requires the centre matrix $H$ to have rank $\le d$.
- **The flexibility.** By R1 and Helly, only each column's conflict graph matters, so any $H'$ with the same conflict graphs will do. For a column whose conflict graph is a single edge, the freedom is large. For general binary columns (conflicts = $\{-1\}\times\{1\}$, complete bipartite between two classes), R1 generalizes: the two classes must be *opposite caps* (L10).
- **Consequence.** Columns with large classes are expensive in fixed dimension, which is why D2 replaces them by single antipodal pairs and forced helpers. Whether every binary pattern matrix has an opposite-cap realization in fixed $d$ is a question about the "cap rank" of sign patterns. I did not pursue it, because D2 makes it unnecessary for hardness.
