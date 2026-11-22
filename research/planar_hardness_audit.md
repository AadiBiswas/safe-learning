# Stage 4 — Independent audit of the planar hardness theorem D2

*2026-11-21.*
- *Scope:* I reconstruct D2 from the definitions, without relying on the Stage 3 text, and record every check.
- *Verifier:* `scripts/verify_d2.py`, output `results/verify_d2.txt` (ledger E007). It re-derives every intended experiment from the formula and recomputes every geometric quantity with its own exact arithmetic.

**Verdict.** D2 survives the audit. One defect was found and corrected: the "always safe" experiments had no strict safety margin. Their constant safety $0\le0$ was tight at every parameter. They now use $0\le1$; no unsafe set changes. Two statements are sharpened:
- the experiment count is $\le5n+12m$, not $\le7n+13m$;
- the ETH statement is now precise in terms of parameters, experiments and bit length.

## 1. Definitions used

- **Instance.** Parameters $\theta_i\in\mathbb Q^2$; experiments $(a_u,b_u,c_u,\delta_u)$; $u$ unsafe for $\theta$ iff $a_u^\top\theta>b_u$; observation interval $[c_u^\top\theta-\delta_u,c_u^\top\theta+\delta_u]$, closed.
- **Trap** (Stage 1, T1): $K\ne\varnothing$ such that every experiment either meets $K$ in its unsafe set, or has a common observation on $K$.
- **Results relied on.**
  - T1: no trap of size $\ge2$ ⇔ exact identifiability, under adaptive noise.
  - L1: for intervals, "common observation on $K$" ⇔ $\max_Kc^\top\theta-\min_Kc^\top\theta\le2\delta$.
- **Consequence.** An experiment *kills* $K$ (shows that $K$ is not a trap) iff $K$ misses its unsafe set and contains a **separated pair** $\{i,j\}$, one with $\lvert c^\top(\theta_i-\theta_j)\rvert>2\delta$.

## 2. The reduction

**Source.** A 3-CNF $\phi$ with variables $x_1,\dots,x_n$ ($n\ge1$) and clauses $C_1,\dots,C_m$. Clauses have length 1–3; repeated literals and tautologies are allowed; the empty clause is allowed. Each nonempty clause is padded to $(\ell_{j1},\ell_{j2},\ell_{j3})$ by repeating its last literal.

### 2.1 Parameters and their roles

| Parameter | Role | Number |
|---|---|---|
| $T_v,F_v$ | literal points; $T_v\in K$ means $x_v$ true | $2n$ |
| $T'_v,F'_v$ | primed literals, used only to forbid $T_v,F_v$ together | $2n$ |
| $s_j,s'_j$ | clause selectors: $s'_j$ "satisfied by $\ell_{j1}$ or $\ell_{j2}$", $s_j$ "by $\ell_{j3}$" | $2m'$ |
| $\kappa_{j1},\kappa_{j2},\kappa_{j3}$ | private copies of the clause's literals | $3m'$ |
| $w_x$ | helper of each antecedent $x\in\{T_v,F_v,s_j,s'_j,\kappa_{ji}\}$ | $2n+5m'$ |

Here $m'\le m$ is the number of nonempty clauses. In total there are $N=6n+10m'$ parameters.

### 2.2 Experiments

Write $\mathbf 1$ for "every pair separated". Each experiment is listed with its intended unsafe set $B$ and separated-pair set $P$.

| # | Experiment | $B$ | $P$ | Count |
|---|---|---|---|---|
| E1 | force$(w)$, each helper | $\{w\}$ | $\mathbf 1$ | $2n+5m'$ |
| E2 | imply$(T_v\to T'_v)$, imply$(F_v\to F'_v)$ | $\{T'_v\}$, $\{F'_v\}$ | $\{T_v,w_{T_v}\}$, $\{F_v,w_{F_v}\}$ | $2n$ |
| E3 | notboth$(T'_v,F'_v)$ | $\varnothing$ | $\{T'_v,F'_v\}$ | $n$ |
| E4 | some$(s_j,s'_j)$ | $\{s_j,s'_j\}$ | $\mathbf 1$ | $m'$ |
| E5 | imply$(s'_j\to\kappa_{j1}\vee\kappa_{j2})$ | $\{\kappa_{j1},\kappa_{j2}\}$ | $\{s'_j,w_{s'_j}\}$ | $m'$ |
| E6 | imply$(s_j\to\kappa_{j3})$ | $\{\kappa_{j3}\}$ | $\{s_j,w_{s_j}\}$ | $m'$ |
| E7 | imply$(\kappa_{ji}\to\ell_{ji})$ | $\{$literal point of $\ell_{ji}\}$ | $\{\kappa_{ji},w_{\kappa_{ji}}\}$ | $3m'$ |
| E8 | each empty clause | $\varnothing$ | $\mathbf 1$ | $m-m'$ |

In total there are $5n+11m'+(m-m')\le5n+11m$ experiments. Stage 3's bound $\le7n+13m$ was loose but correct; the precise count is used below.

### 2.3 What each experiment forbids

An experiment kills exactly the sets $K$ with $K\cap B=\varnothing$ that contain a pair of $P$. Hence, for $K$ with $\lvert K\rvert\ge2$:
- **E1:** $w\notin K$ ⇒ killed. So *every trap of size $\ge2$ contains every helper.*
- **E2, E5–E7:** killed iff $K\cap B=\varnothing$, $x\in K$ and $w_x\in K$.
- **E3:** killed iff $T'_v,F'_v\in K$.
- **E4:** killed iff $s_j,s'_j\notin K$.
- **E8:** always killed.

## 3. Both implications

**(⇐) A trap gives a satisfying assignment.** Let $K$ be a trap with $\lvert K\rvert\ge2$. Nothing beyond the trap property is assumed.
1. *Helpers.* By E1, every helper lies in $K$.
2. *Implications.* Since each $w_x\in K$, E2 and E5–E7 give:
   - $T_v\in K\Rightarrow T'_v\in K$ and $F_v\in K\Rightarrow F'_v\in K$;
   - $s'_j\in K\Rightarrow\{\kappa_{j1},\kappa_{j2}\}\cap K\ne\varnothing$;
   - $s_j\in K\Rightarrow\kappa_{j3}\in K$;
   - $\kappa_{ji}\in K\Rightarrow$ (literal point of $\ell_{ji}$) $\in K$.
3. *Consistency.* If $T_v,F_v\in K$, then $T'_v,F'_v\in K$, and E3 kills $K$. So for each $v$ at most one of $T_v,F_v$ is in $K$.
4. *Assignment.* Define $\alpha(x_v)=\mathrm{true}$ iff $T_v\in K$.
   - If a literal point is in $K$, its literal is true under $\alpha$. For $T_v$ this is immediate. For $F_v\in K$, step 3 gives $T_v\notin K$, so $\neg x_v$ is true.
5. *Clauses.*
   - No clause is empty, since otherwise E8 kills every $K$ with $\lvert K\rvert\ge2$.
   - For each $j$, E4 gives $s_j\in K$ or $s'_j\in K$. Step 2 then yields a copy $\kappa_{ji}\in K$, hence its literal point in $K$, hence a true literal of $C_j$ by step 4.
   - So $\alpha\models\phi$.

**(⇒) A satisfying assignment gives a trap.** Let $\alpha\models\phi$. Then $\phi$ has no empty clause. Define $K$ to contain:
- all helpers;
- every literal point whose literal is true, together with its primed copy ($T'_v$ with $T_v$, $F'_v$ with $F_v$);
- every copy $\kappa_{ji}$ whose literal $\ell_{ji}$ is true;
- $s'_j$ if $\ell_{j1}$ or $\ell_{j2}$ is true, and $s_j$ otherwise (then $\ell_{j3}$ is true).

$\lvert K\rvert\ge2$, since there are at least two helpers. Check each experiment:

| Experiment | Why it does not kill $K$ |
|---|---|
| E1 | every helper is in $K$ |
| E2 | $T_v\in K$ only if true, and then $T'_v\in K$; likewise for $F_v$ |
| E3 | $T'_v,F'_v$ are both in $K$ only if $T_v,F_v$ are both true, which is impossible |
| E4 | one selector is chosen per clause |
| E5 | $s'_j\in K$ only if $\ell_{j1}$ or $\ell_{j2}$ is true, so the matching copy is in $K$ |
| E6 | $s_j\in K$ only if $\ell_{j3}$ is true, so $\kappa_{j3}\in K$ |
| E7 | a copy is in $K$ only if its literal is true, so the literal point is in $K$ |
| E8 | no empty clause |

So $K$ is a trap. ∎

**Unintended traps.** The (⇐) direction derived every property from the trap condition alone, so no trap of size $\ge2$ escapes the correspondence.

## 4. The rational geometric realization

**Points.** Put $v(k)=\bigl(\frac{1-k^2}{1+k^2},\frac{2k}{1+k^2}\bigr)$, $k\in\mathbb Z_{\ge1}$, which lies at angle $2\arctan k\in[\tfrac\pi2,\pi)$.
- The **upper** points are the antecedents and the $T'_v$, in order $k=1,\dots,M$ with $M=3n+5m'$:
  - $T_v,F_v,T'_v$ for each $v$;
  - then $s_j,s'_j,\kappa_{j1},\kappa_{j2},\kappa_{j3}$ for each nonempty clause.
- Each upper point's **partner** is its antipode $-v(k)$: the helper $w_x$ for an antecedent $x$, and $F'_v$ for $T'_v$.

**Membership, distinctness and order.**
- $\lVert v(k)\rVert^2=\frac{(1-k^2)^2+4k^2}{(1+k^2)^2}=1$, exactly.
- Distinct $k$ give distinct angles in $[\tfrac\pi2,\pi)$. Their antipodes lie in $[\tfrac{3\pi}2,2\pi)$. So all $N$ points are distinct.
- The cyclic order is the upper points in increasing $k$, then the lower points in increasing $k$. So $s_j,s'_j$ are cyclically adjacent, and so are $\kappa_{j1},\kappa_{j2}$.

**Unsafe sets.**
- *$B=\{y\}$.* Take $a=v_y$ and $b=(1+\max_{z\ne y}v_y^\top z)/2$.
  - $v_y^\top z<1$ for every unit $z\ne v_y$, so the trace is exactly $\{y\}$, with margin $1-b>0$.
- *$B=\{x,y\}$, adjacent.* Take $a=v_x+v_y$.
  - $a^\top z=2\cos(\alpha/2)\cos(\angle z-\mu)$, where $\mu$ is the bisector and $\alpha<\pi$ the angle between $x$ and $y$.
  - No point lies strictly between $x$ and $y$ in the short arc, so every other point is angularly farther from $\mu$. Thus $x,y$ are the strict top two.
  - Take $b$ as the midpoint between the second and third largest values.
- *$B=\varnothing$.* Take $a=0$, $b=1$. *(Corrected from $b=0$, which was safe only at equality.)*
- *Margins.* Every threshold is a midpoint of distinct values, or 1 for the constant constraint. So no parameter lies on any threshold. Verified exactly (E007).

**Separated pairs.**
- *Lone pair $\{v(k),-v(k)\}$.* Take $c=v(k)$. Then $c^\top v(k)=1$, $c^\top(-v(k))=-1$, and every other point has $\lvert c^\top z\rvert<1$.
  - Put $M_k=\max(1-\min_{\rm o},\ 1+\max_{\rm o})<2$ and $\delta=(M_k+2)/4$, so that $M_k<2\delta<2$.
  - Then exactly that pair is separated (R1), with strict margins on both sides.
- *All pairs, $\mathbf 1$.* Take $c^\*=(1,\tfrac17)$ and $\delta^\*=\gamma/3$, with $\gamma$ the smallest gap between projections. This needs **all projections distinct**:
  - $c^{\*\top}z=\sqrt{50/49}\cos(\angle z-\theta_0)$ with $\theta_0=\arctan\tfrac17$.
  - Two points have equal projection iff their angles sum to $2\theta_0$ modulo $2\pi$.
  - *Two upper angles* sum into $[\pi,2\pi)$, and *two lower angles* into $[3\pi,4\pi)$. Neither range contains $2\theta_0\approx0.284$, $2\theta_0+2\pi\approx6.57$ or $2\theta_0+4\pi\approx12.85$, since $4\pi\approx12.57$.
  - *An upper and a lower angle* sum to $\pi+2(\arctan k+\arctan l)\in[2\pi,3\pi)$, so the only candidate is $2\theta_0+2\pi$. That requires $\arctan k+\arctan l=\theta_0+\tfrac\pi2$, i.e. $\frac{k+l}{1-kl}=\tan(\theta_0+\tfrac\pi2)=-7$ (for $kl\ne1$), i.e. $7kl-k-l=7$.
    - $k=1$: $6l=8$, no integer solution.
    - $k=2$: $13l=9$, none.
    - $k,l\ge2$: the left side is $\ge24$.
    - $k=l=1$: the equation reads $\tfrac\pi2=\theta_0+\tfrac\pi2$, false.

    So there is no solution.
  - *The antipodal pair itself*, $k=l$, has opposite nonzero projections.

  So projections are pairwise distinct, analytically, for every formula.
- *Common noise radius.* Replace $(c_u,\delta_u)$ by $(c_u/\delta_u,1)$. Every comparison $\lvert c^\top(\theta_i-\theta_j)\rvert>2\delta$ scales identically.

**Structural restrictions asserted by D2.**
- Unit circle: ✓.
- Strict convex position: ✓, since distinct points of a circle are.
- Unsafe sets: singletons or adjacent pairs, ✓; and laminar, ✓. The pairs $\{s_j,s'_j\}$ and $\{\kappa_{j1},\kappa_{j2}\}$ are pairwise disjoint, and every singleton is inside one of them or disjoint from all.
- Separated-pair sets: $\mathbf 1$ or one antipodal pair, ✓.
- Common $\delta$: ✓.

E007 checks all of these exactly on 48 formulas, up to 176 parameters, with $n\le6$ and $m\le24$, including degenerate formulas.

## 5. Encoding length

**Per-number bit length.**
- Coordinates of $v(k)$: $O(\log M)$ bits.
- An inner product of two such points: denominator $(1+k^2)(1+l^2)$, so $O(\log M)$ bits.
- Thresholds are means of two such values: $O(\log M)$ bits.
- Sums $v_x+v_y$: $O(\log M)$ bits.
- $\delta$ for a lone pair: rational in $O(\log M)$-bit quantities.
- $\delta^\*$: the minimum of $O(N^2)$ differences of $O(\log M)$-bit rationals, which is still $O(\log M)$ bits.

Every number therefore has $O(\log(n+m))$ bits. E007 observed at most $5.14\log_2N$ bits.

**Total.** The input has $O((n+m)\log(n+m))$ bits, and the construction runs in polynomial time. Computing $\delta^\*$ is the costliest step at $O(N\log N)$ comparisons, after sorting.

## 6. Complexity statements, precisely

- **Languages.**
  - $\mathrm{TRAP}^{(2)}_0$: does a trap of size $\ge2$ exist? **NP-complete.**
    - *Membership:* certify by $K$; the safe experiments and the widths are computable in polynomial time.
    - *Hardness:* D2.
  - $\mathrm{SAFEID}^{(2)}_0$: is $\Theta_0$ exactly identifiable? This is its complement by T1, hence **coNP-complete.**
- **In every fixed $d\ge2$**, by zero-padding (D1).
- **ETH, stated exactly.** Assume ETH. By the sparsification lemma, 3-SAT with $n$ variables and $m=O(n)$ clauses has no $2^{o(n)}$ algorithm. D2 maps such formulas to instances with $N=6n+10m'=O(n)$ parameters, $\le5n+11m=O(n)$ experiments and $L=O(n\log n)$ input bits. Hence:
  - no $2^{o(N)}$ algorithm and no $2^{o(\lvert\mathcal U\rvert)}$ algorithm for $\mathrm{TRAP}^{(2)}_0$;
  - no $2^{o(L/\log L)}$ algorithm in terms of bit length.

  Nothing stronger is claimed. In particular, no bound on the XP exponents of L7 or D5 follows.

## 7. Approximate identification ($0\le\varepsilon<1$)

**Conventions** (Stage 1). Identification to tolerance $\varepsilon$ succeeds when $\operatorname{diam}\Theta_t\le\varepsilon$. A trap is *far* if $\operatorname{diam}>\varepsilon$. By T1, $\varepsilon$-identifiable iff no far trap exists. $\varepsilon=0$ is exact identification.

**Claim.** If $n\ge2$, then for every $0\le\varepsilon<1$: $\phi$ is satisfiable iff a far trap exists. For $n=1$, add one unused variable; satisfiability is unchanged.

*Proof.*
- **The helper diameter.** With $n\ge2$, helpers $w_{T_1}=-v(1)$ and $w_{T_2}=-v(4)$ exist; $T_2$ sits at $k=4$ in the order $T_1,F_1,T'_1,T_2$. Here $v(1)=(0,1)$ and $v(4)=(-\tfrac{15}{17},\tfrac8{17})$, so
  $$\lVert v(1)-v(4)\rVert^2=\tfrac{225}{289}+\tfrac{81}{289}=\tfrac{306}{289},$$
  and the distance is $\sqrt{306}/17\approx1.029>1$.
- **(⇒)** If $\phi$ is satisfiable, the trap of §3 contains all helpers. So its diameter is $>1>\varepsilon$: it is far.
- **(⇐)** A far trap has size $\ge2$, so §3(⇐) applies. This uses only the trap property and $\lvert K\rvert\ge2$, which far traps satisfy.

The exact theorem is not used as a black box in the forward direction: the diameter of the constructed trap is computed directly. ∎

For the continuum-style convention "$\operatorname{diam}<\varepsilon$", the same holds for every $\varepsilon\le1$.

## 8. What the verifier does, and what it does not do

**What it does** (`scripts/verify_d2.py`):
- re-derives the intended multiset of (unsafe labels, separated-pair labels) from the formula, using its own code;
- recomputes unsafe sets and separated pairs with its own inner products;
- checks unit-circle membership, distinctness, cyclic adjacency (with its own exact angular order), antipodality, strict margins, laminarity and bit lengths.

**What it shares with the builder:** only the builder's output and the point labels.

**What it does not do:** decide satisfiability. Correctness of the equivalence is §3. E006 separately confirmed satisfiable ⇔ trap on 58 formulas.

**Results:** 48/48 formulas pass. The constant-safety margin defect was found by this verifier, and fixed in `scripts/planar_hardness.py`. E006's output is unchanged by the fix.
