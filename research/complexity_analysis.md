# Stage 1 — Complexity of safe identifiability

*2026-11-21. Definitions follow `research/finite_trap_theory.md`.*
- *Algorithms and reductions:* `scripts/traps.py`.
- *Exhaustive regression checks:* `scripts/stage1_finite.py`, §§B–G of `results/stage1_finite.txt` (ledger E003).
- *Proofs:* given here in full. Agreement with brute force is a regression check, not part of any proof.

## 0. Summary — the classification

All problems below are on explicitly represented finite instances (§1).

| Restriction | Trap existence (non-identifiability) | Reference |
|---|---|---|
| none | NP-complete; identifiability coNP-complete | H1 |
| no safety constraints, any observations | P, by a pairwise test | B1 |
| any safety, **deterministic** (partition) observations | P, split recursion, $O(n^2m)$ | P2 (known: Hierons–Türker 2014) |
| every experiment unsafe for **at most one** parameter | P, closure, $O(n^3m)$ | P3 |
| unsafe sets of size $\le2$, **binary** observations | **NP-complete** | H1(a) |
| unsafe sets of size $\le3$, binary observations, $\le n+m\lceil\log_2 2n\rceil$ experiments | NP-complete | H1(b) |
| interval observations of one common width | NP-complete | H1(c) |
| linear safety and linear interval observations in $\mathbb R^d$, $d$ unbounded | NP-complete | H1(d) |
| safety-witness number $\sigma\le k$ (includes nested safety, $k=1$; one-dimensional thresholds, $k=2$; $\le k$ experiments) | P for fixed $k$, $O(n^{k+2}m)$ | P4 |
| promise: minimal traps have size $\le k$ | P for fixed $k$, $O(n^km)$ | P5 |
| linear safety, fixed dimension $d\ge2$ | **open** | `research/geometric_obstructions.md` §5 |
| least worst-case number of experiments | NP-hard even without safety; in PSPACE | §6 |

**Answer to the brief's question 1.**
- Yes: safety creates a computational obstruction absent without it. Without safety, every explicit static instance is decided by a pairwise test (B1). With safety, the problem is coNP-complete (H1).
- **The obstruction is an interaction.** It needs both robust safety and *overlapping* observations, i.e. noise that can be consistent with two hypotheses that are themselves separable:
  - safety alone, with deterministic observations, is polynomial (P2);
  - overlap alone, without safety, is polynomial (B1);
  - hardness appears with binary observations and unsafe sets of size 2, but not size 1 (P3).
- The two mechanisms are exact:
  - safety destroys heredity: a subset of a non-trap can be a trap, so local tests fail;
  - overlap destroys laminarity: the responses of one experiment cover the current set non-disjointly, so the split recursion branches.

## 1. Representation and decision problems

**An instance** $\mathcal I=(\Theta_0,\mathcal U,U,\mathcal Y,d,\varepsilon)$ is given by:
- $n=\lvert\Theta_0\rvert$ and $m=\lvert\mathcal U\rvert$, in unary, i.e. the parameters and experiments are listed explicitly;
- the **safety matrix**: an $n\times m$ Boolean matrix, entry $1$ iff $\theta\in U(u)$;
- **observations**, in one of two encodings:
  - *explicit*: for each $(\theta,u)$, a nonempty list of symbols from a finite alphabet;
  - *interval*: for each $(\theta,u)$, rational endpoints $\ell\le r$ in binary, with $\mathcal Y=[\ell,r]$. The common-width case $[h-\delta,h+\delta]$ is a special case;
- the **metric**: a rational $n\times n$ distance matrix in binary, and a rational $\varepsilon\ge0$.

Input size is polynomial in $n$, $m$, the total list length, and the bit length of the rationals.

**Problems.**
- $\mathrm{TRAP}_\varepsilon$: does a far trap exist?
- $\mathrm{SAFEID}_\varepsilon$: is $\Theta_0$ uniformly $\varepsilon$-identifiable? By Theorem T1 this is the complement of $\mathrm{TRAP}_\varepsilon$.
- $\mathrm{OPTCOUNT}$: given $k$, can identification be guaranteed within $k$ experiments?

> **Proposition M (membership).** $\mathrm{TRAP}_\varepsilon\in\mathrm{NP}$ and $\mathrm{SAFEID}_\varepsilon\in\mathrm{coNP}$ for both encodings.

*Proof.* The certificate is a set $K$.
- Compute $\operatorname{diam}K$ and compare it with $\varepsilon$: $O(n^2)$ rational comparisons.
- Compute $\mathcal S(K)$ from the matrix.
- For each $u\in\mathcal S(K)$, decide $\bigcap_{K}\mathcal Y(\cdot,u)\ne\varnothing$:
  - explicit lists: intersect the lists;
  - intervals: test $\max\ell\le\min r$.
- All of this is polynomial. ∎

**The game is not the problem.** Solving the identification game directly ranges over up to $2^n$ knowledge states. Theorem T1 replaces the game by a single existential question about subsets, which is why the problem drops to NP/coNP. For comparison, imperfect-information games in general are EXPTIME-complete (Reif 1984; used by Haar et al. 2013/2016).

## 2. The unrestricted baseline

> **Theorem B1.** Suppose no experiment is unsafe for any parameter. Then, for any metric, any $\varepsilon$ and arbitrary set-valued observations, a far trap exists iff some far *pair* is a trap. With explicit or interval observations this is decidable in $O(n^2m)$ intersection tests.

*Proof.*
- **Traps are closed under subsets.** For $K'\subseteq K$, $\mathcal S(K')=\mathcal S(K)=\mathcal U$ and $\bigcap_{K'}\mathcal Y\supseteq\bigcap_K\mathcal Y$.
- A far trap $K$ contains a pair $\{a,b\}$ with $d(a,b)=\operatorname{diam}K>\varepsilon$, which is a far trap.
- The converse is immediate. ∎

**Audit of the Stage 0 statement F3.**
- F3 attributed pairwise-ness to Helly's theorem for intervals. **That was unnecessary.** Downward closure alone gives it, for every observation correspondence. Helly matters for a different question (`research/geometric_obstructions.md`, G2).
- *Hypotheses that do matter:*
  1. the goal is diameter-type, so that failure is witnessed by a pair. For a general goal "the consistent set lies in some member of a down-closed family $\mathcal D$", the witnesses are the minimal sets outside $\mathcal D$, which may be large;
  2. pairwise intersection $\mathcal Y(a,u)\cap\mathcal Y(b,u)\ne\varnothing$ is decidable in polynomial time. That holds for both encodings, but not for implicitly given sets, e.g. sets defined by circuits, where the pair test can itself be NP-hard;
  3. the claim concerns *feasibility*. The least number of experiments is NP-hard even here (§6).

## 3. Hardness

**Gadgets.** All use binary observations. The *symbol pattern* of an experiment is $\mathcal Y(\theta,u)\in\{\{0\},\{1\},\{0,1\}\}$.
- $\mathsf N(a,b)$: always safe, with $\mathcal Y(a)=\{0\}$, $\mathcal Y(b)=\{1\}$ and $\{0,1\}$ for everyone else. *It kills $K$* (is safe and informative on $K$) iff $\{a,b\}\subseteq K$.
- $\mathsf{Bits}(V)$: $\lceil\log_2 n\rceil$ deterministic binary experiments, all with unsafe set $V$. Experiment $k$ reports bit $k$ of the parameter's index.
  - If $K$ meets $V$, all are unsafe.
  - If $K\cap V=\varnothing$ and $\lvert K\rvert\ge2$, two distinct indices differ in some bit.
  - So $\mathsf{Bits}(V)$ kills exactly the $K$ with $\lvert K\rvert\ge2$ and $K\cap V=\varnothing$.
- $\mathsf O(V,x)$: one deterministic binary experiment with unsafe set $V$ that reports whether $\theta=x$, for $x\notin V$. It kills $K$ iff $K\cap V=\varnothing$, $x\in K$ and $\lvert K\rvert\ge2$.

> **Theorem H1.** $\mathrm{TRAP}_0$ is NP-complete, and $\mathrm{SAFEID}_0$ coNP-complete, already for instances with:
> - (a) binary observations and every unsafe set of size $\le2$;
> - (b) binary observations, every unsafe set of size $\le3$, and only $n+m\lceil\log_2 2n\rceil$ experiments;
> - (c) interval observations $[h-\delta,h+\delta]$ with a common $\delta=3/5$ and $h\in\{-1,0,1\}$;
> - (d) $\Theta_0\subset\mathbb R^d$ the standard basis vectors, linear safety $\langle a_u,\theta\rangle\le\tfrac12$, and linear interval observations $[\langle c_u,\theta\rangle-\tfrac35,\langle c_u,\theta\rangle+\tfrac35]$, with $d$ part of the input.

*Proof.*

**Construction (b), from 3-SAT.** Variables $x_1,\dots,x_n$ and clauses $C_1,\dots,C_m$, each a *set* of literals.
- If $n=1$, add an unused dummy variable. This is needed: without it, the satisfiable formula $(x_1)$ would have only the trap $\{T_1\}$, which is not far.
- **Parameters:** $T_v,F_v$ for each $v$, so $2n$ in all.
- **Experiments:** $\mathsf N(T_v,F_v)$ for each $v$, and $\mathsf{Bits}(C_j)$ for each $j$, identifying literals with parameters.

*Claim: $K$ with $\lvert K\rvert\ge2$ is a trap iff $K$ contains no complementary pair and meets every $C_j$.* The gadget behaviours above give this directly.
- *If $K$ is such a trap,* set $x_v$ true if $T_v\in K$, false if $F_v\in K$, and arbitrarily otherwise. This is well defined because there is no complementary pair. Each $C_j$ contains a literal in $K$, which is true, so the formula is satisfied.
- *If $\alpha$ satisfies the formula,* the set $K_\alpha$ of true literals has $n\ge2$ elements, contains no complementary pair, and meets every clause.

**Degenerate inputs.**
- *Repeated literals* are absorbed by the set semantics. The code must OR the bitmasks: my first implementation summed them, and the exhaustive check caught it (E003).
- *A tautological clause* $\{x_v,\neg x_v,\dots\}$ is met by every $K_\alpha$. It may be avoided by partial sets, but the claim only uses "meets", so the equivalence is unaffected.
- *Unused variables* are harmless.
- *The empty conjunction* $m=0$: every consistent pair is a trap, and the formula is satisfiable.
- *An empty clause* gives $\mathsf{Bits}(\varnothing)$, which kills every $K$ with $\lvert K\rvert\ge2$. There is no trap, and the formula is unsatisfiable.
- All of these, together with random formulas both sparse and dense, are in the regression set: E003 §F, 309/309 agreements, 166 satisfiable.

*Size:* $2n$ parameters and $n+m\lceil\log_2 2n\rceil$ experiments.

**Construction (a): unsafe sets of size $\le2$.** Same literals, plus two auxiliary parameters $s_j,s'_j$ for each clause $C_j=(\ell_1\vee\ell_2\vee\ell_3)$. Shorter clauses are padded by repeating a literal; an empty clause contributes $\mathsf{Bits}(\varnothing)$.
- **Experiments:**
  - $\mathsf N(T_v,F_v)$ and $\mathsf{Bits}(\{T_v,F_v\})$: *exactly one* of $T_v,F_v$;
  - $\mathsf N(s_j,s'_j)$ and $\mathsf{Bits}(\{s_j,s'_j\})$: exactly one of $s_j,s'_j$;
  - $\mathsf O(\{\ell_1,\ell_2\},s'_j)$: $s'_j\in K\Rightarrow K\cap\{\ell_1,\ell_2\}\ne\varnothing$;
  - $\mathsf O(\{\ell_3\},s_j)$: $s_j\in K\Rightarrow\ell_3\in K$.
- All of these use $\lvert K\rvert\ge2$, which every candidate satisfies since $\lvert K\rvert\ge n\ge2$. So a set of size $\ge2$ is a trap iff it encodes an assignment $\alpha$ together with, for each $j$, a choice of $s'_j$ (requiring $\ell_1$ or $\ell_2$ true) or $s_j$ (requiring $\ell_3$ true).
- Such a choice exists iff $\alpha$ satisfies $C_j$. Every unsafe set has size $\le2$.
- *Regression:* E003 §F, 146/146, on instances with at most 12 parameters.

**Encoding (c).** Map the symbol pattern $\{0\}\mapsto h=-1$, $\{1\}\mapsto h=1$, $\{0,1\}\mapsto h=0$, with $\delta=3/5$.
- $[-\tfrac85,-\tfrac25]$ and $[\tfrac25,\tfrac85]$ are disjoint, and both meet $[-\tfrac35,\tfrac35]$.
- So for every set $K$ the interval intersection is nonempty iff the symbol-set intersection is. Traps are unchanged.
- Verified on 1500 random binary instances (E003 §G).

**Encoding (d).** Identify parameter $i$ with the basis vector $e_i\in\mathbb R^{n'}$, where $n'$ is the number of parameters.
- *Safety:* an unsafe set $V$ becomes the halfspace $\langle\mathbf 1_V,\theta\rangle\le\tfrac12$, which excludes exactly $V$.
- *Observations:* an observation $h(\theta,u)\in\{-1,0,1\}$ becomes $\langle c_u,\theta\rangle$ with $(c_u)_i=h(e_i,u)$.

*Membership* is Proposition M. ∎

**How restrictive are the hard instances?**
- *Interpretation.* Observations take three values in effect: "low", "high", and "can't tell". Each experiment is dangerous under at most two hypotheses.
- *Geometry (d).* High dimension is needed: the parameters are affinely independent, so every subset is cut off by some halfspace. In fixed dimension the realizable families of unsafe sets have bounded VC dimension, and I do not know whether hardness survives (open, geometric doc §5).
- *Monotone or ordered structure kills the hardness* (P4).

## 4. Tractable classes

> **P2 (deterministic observations; split recursion).** If the responses of every experiment are pairwise disjoint, $\mathrm{TRAP}_\varepsilon$ is decidable in $O(n^2m)$ time, with the bitmask word size treated as constant.

*Proof.*
- **Invariant.** If $u\in\mathcal S(K)$ and $K'\subseteq K$ is a trap, then $u\in\mathcal S(K')$. So $K'$ lies in a single response $K\cap\{\theta : y\in\mathcal Y(\theta,u)\}$.
- **Recursion** `find_trap_split`:
  - if $K$ is not far, return none;
  - if no safe experiment is informative on $K$, return $K$;
  - otherwise take any safe informative $u$ and recurse on its responses.
- **Correctness.** By the invariant, every far trap inside $K$ lies inside some response. This holds for arbitrary observations.
- **Complexity.** With disjoint responses, the recursion tree is laminar. Its leaves are disjoint and its internal nodes have at least two children, so it has at most $2n-1$ nodes. Finding a safe informative experiment costs $O(mn)$.
- *Regression:* exact in 3000/3000 deterministic and 3000/3000 general instances; the maximum node count was $0.46(2n-1)$ (E003 §B).
- *Known:* this is the static case of Hierons–Türker's polynomial ADS-existence result for partially specified FSMs (§7). ∎

> **P3 (unsafe sets of size $\le1$).** $\mathrm{TRAP}_\varepsilon$ is decidable in $O(n^3m)$ intersection tests.

*Proof.*
- For each far pair $P$, compute the least trap containing it: start with $K=P$, and while some safe $u$ is informative on $K$:
  - if $U(u)=\varnothing$, stop: no trap contains $P$;
  - otherwise add the single element of $U(u)$ to $K$.
- **Invariant:** $K$ is contained in every trap $K'\supseteq P$.
  - If $u\in\mathcal S(K)$ is informative on $K$, it is informative on $K'\supseteq K$.
  - So $u\notin\mathcal S(K')$, which means $U(u)\cap K'\ne\varnothing$, i.e. $U(u)\subseteq K'$.
- A far trap contains a far pair, so the search is complete. Each closure adds at most $n$ elements.
- *Regression:* 3000/3000 (E003 §C).

*Why this is the boundary.* A constraint of the form "$K$ meets $U(u)$, or $K$ lies in a response of $u$" is Horn-like when $\lvert U(u)\rvert\le1$: at most one positive literal. That is why a least model exists. Size 2 gives non-Horn clauses, and H1(a) uses exactly that. ∎

> **P4 (bounded safety-witness number).** If $\sigma(K)\le k$ for every far trap $K$, then a far trap exists iff one of size $\le k+2$ does. For $\varepsilon=0$, size $\le\max(2,k)$ suffices. Enumeration costs $O(n^{k+2}m)$.

$\sigma(K)\le k$ holds in each of the following cases:
- **at most $k$ experiments are unsafe for anything.** This places $\mathrm{TRAP}$ in XP parameterized by the number of experiments; its FPT status is open;
- **nested safety** ($U(u)$ totally ordered by inclusion): $\sigma\le1$, witnessed by the most dangerous member;
- **one-dimensional thresholds** (every $U(u)$ an up-set or a down-set of a line): $\sigma\le2$, witnessed by $\{\min K,\max K\}$. In fact $\{\min K,\max K\}$ is itself a trap of the same diameter, so pairs suffice for every $\varepsilon$, in $O(n^2m)$;
- **safety through $k$ fixed functionals** ($\theta\in U(u)$ iff $\phi_{i(u)}(\theta)>b_u$, for $i(u)\in\{1..k\}$): $\sigma\le k$, witnessed by the maximizers of each $\phi_i$ on $K$.

*Proof.* Lemma W of the finite theory, plus the witnesses listed. Regressions: the witness bound on 1500 instances; nested safety, 2000/2000; thresholds, 2000/2000 (E003 §E). ∎

> **P5 (promise of small minimal traps).** If every minimal far trap has size $\le k$, enumerating $k$-subsets decides $\mathrm{TRAP}_\varepsilon$. By T5, at $\varepsilon=0$ this promise is equivalent to $\sigma(K)\le k$ on minimal traps of size $\ge3$.

## 5. The scalar model as a member of the tractable class

The scalar model is the intended motivating example: safe iff $\theta x\le1$, with $x\ge0$. Its unsafe sets are up-sets of $\theta$, so it lies in P4 (thresholds). This explains structurally why its analysis reduces to two endpoints, the one-sided deadlock of Stage 0 S3. The hardness of H1 needs unsafe sets that are not monotone in any single order.

## 6. Optimal experiment counts

- **Hardness.** $\mathrm{OPTCOUNT}$ is NP-hard *even without safety and with deterministic observations*. This is the minimum-height decision tree problem, NP-hard by Hyafil–Rivest 1976 and hard to approximate within $O(\log n)$ (Laber–Nogueira 2004).
  - *Access:* both seen only through secondary sources. I have not read the theorem statements, so this is to be confirmed.
  - With safety, $\mathrm{OPTCOUNT}$ at $k=n-1$ is $\mathrm{SAFEID}$, so it is also coNP-hard.
- **Membership.** $\mathrm{OPTCOUNT}\in\mathrm{PSPACE}$: an alternating polynomial-time machine plays $k\le n-1$ rounds, existentially choosing experiments and universally choosing responses.
- **Exact complexity: open.** It is probably $\Sigma_2^p$-hard or PSPACE-hard with safety; I have not attempted it. It is secondary to the feasibility classification.

## 7. Literature comparison (detailed in `research/literature_review.md` §6)

The static model embeds into **partially specified FSMs** with self-loops only:
- states are parameters;
- inputs are experiments, *undefined* exactly where unsafe;
- outputs are observations.

What this implies:
- **Hierons–Türker (NFM 2014), full text read.** Their ADS definition requires the input to be "defined in all states" of the current node, which is robust safety. Their main theorem gives polynomial ADS existence for deterministic outputs. **P2 at $\varepsilon=0$ is therefore a special case of a published result.** My split recursion is a simpler proof for the static case, not a contribution.
- **Nondeterministic outputs: no lower bound transfers.**
  - The nondeterministic static case sits inside classes shown EXPTIME-complete (Alur–Courcoubetis–Yannakakis 1995, adaptive distinguishing for nondeterministic machines; secondary sources only) or PSPACE-hard (Türker et al. 2023, partial observable nondeterministic FSMs; not read: PDF text not extractable).
  - Those *upper* bounds apply to the static case. Their *lower* bounds do not transfer down, since their hardness uses state dynamics.
  - H1 shows the static case is coNP-complete — strictly lower unless NP = PSPACE, while still hard.
- **Haar–Haddad–Melliti–Schwoon (FSTTCS 2013; JCSS 2016), full text read.**
  - *Their setting:* active diagnosis of a fault *event* in a live LTS under partial observation. The controller may disable controllable events, subject to liveness. Admissibility does not depend on the hidden state.
  - *Their result:* EXPTIME-hardness by reduction from safety games with imperfect information.
  - *Comparison:* different hidden object (an evolving trajectory, not a static parameter) and different admissibility, so **not subsuming.**
- **Still to check.** The specific statement "static hypotheses, nondeterministic (possibilistic) test outcomes, test applicability depends on the hypothesis: coNP-complete" could exist in:
  - the testing literature on *observable nondeterministic FSMs with partial inputs*, restricted to "self-loop" machines;
  - *test-sequencing* work in fault diagnosis.

  This is the precise remaining originality question for H1.
