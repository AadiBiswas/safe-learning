# Stage 1 — Geometric structure and local-to-global principles

*2026-11-21. Definitions follow `research/finite_trap_theory.md`. Exhaustive checks are in `results/stage1_finite.txt` §§E, H, J (ledger E003).*

## 0. Summary

There are two different local-to-global questions. Stage 1 shows that they are governed by two different structures.

| Question | Governing structure | Result |
|---|---|---|
| Does trap *existence* have small witnesses? Equivalently: is $\Theta_0$ identifiable iff all small subsets are? | **safety**: the safety-witness number $\sigma$ | G1: witnesses of size $\le\sigma+2$. **Exact characterization** at $\varepsilon=0$ (G1′). |
| Does *non*-trap-ness of a given set have small witnesses? | **observations**: the Helly number $h$ | G2: a set is a trap if all its $\le h$-subsets are. G2b characterizes which trap families are realizable. |
| Does geometry bound minimal traps? | convex position of $\Theta_0$, relative to halfspace safety | G3: one-dimensional thresholds give pairs. In the plane, minimal traps of every size occur, with linear safety and linear observations. In general, $\sigma\le$ the largest subset in convex position. |
| When do traps become hereditary? | homogeneous experiments in which safety and sensing share a functional | G4: traps are closed under subsets, so pairwise tests suffice. This explains Stage 0's C1. |

**The warning in the brief is borne out exactly.** A Helly bound on observations gives small witnesses that a set is *not* a trap. It gives nothing for trap *existence*. The cycle trap has deterministic binary observations, the smallest Helly number possible, and still has minimal traps of every size. Small witnesses for existence come only from safety structure.

**Answer to the brief's question 5.** Yes, there is a meaningful local-to-global principle, and it is sharp:
- $\Theta_0$ is identifiable iff every subset of size $\le k$ is;
- this holds for all sub-instances iff every minimal trap has safety-witness number $\le k$;
- it holds in particular whenever $\sigma\le k$ globally, as with nested, threshold or $k$-functional safety.

When it fails, the obstruction is a set whose every member individually blocks a distinct experiment.

## 1. Safety witnesses: small traps

Recall $\sigma(K)=\min\{\lvert W\rvert : W\subseteq K,\ \mathcal S(W)=\mathcal S(K)\}$.

> **Theorem G1.** Every far trap $K$ contains a far trap of size $\le\sigma(K)+2$; at $\varepsilon=0$, of size $\le\max(2,\sigma(K))$. Consequently, if $\sigma(K)\le k$ for all $K$, then $\Theta_0$ is uniformly $\varepsilon$-identifiable iff every subset of size $\le k+2$ is, each subset taken as the restricted instance.

*Proof.*
- The first part is Lemma W of the finite theory.
- For the second: by T4(1), the traps of a restriction $\Theta'$ are the traps of $\Theta_0$ contained in $\Theta'$. Then apply T1 to $\Theta_0$ and to each small restriction. ∎

> **Theorem G1′ (exact local-to-global; $\varepsilon=0$, $k\ge2$).** The following are equivalent:
> - (i) for every $\Theta'\subseteq\Theta_0$, if all $k$-subsets of $\Theta'$ are identifiable then $\Theta'$ is;
> - (ii) every minimal trap of $\Theta_0$ has size $\le k$;
> - (iii) every minimal trap $K$ with $\lvert K\rvert\ge3$ has $\sigma(K)\le k$.

*Proof.*
- **(i)⇒(ii).** Let $K$ be a minimal trap with $\lvert K\rvert>k$. Every $k$-subset of $K$ is identifiable, since its traps are traps strictly inside $K$, of which there are none of size $\ge2$. But $K$ itself is not identifiable, contradicting (i) with $\Theta'=K$.
- **(ii)⇒(i).** If $\Theta'$ is not identifiable, it contains a minimal trap, of size $\le k$, which lies inside some $k$-subset.
- **(ii)⇔(iii).** By T5(a), $\sigma(K)=\lvert K\rvert$ for minimal traps of size $\ge3$. ∎

**Sharpness.** The cycle trap and the convex-position trap (§3) have $\sigma(\Theta_0)=n$. All of their $(n-1)$-subsets are identifiable, but $\Theta_0$ is not. So no local-to-global principle holds at any scale below $\sigma$.

**Where $\sigma$ is bounded** (proofs in `research/complexity_analysis.md`, P4):
- nested safety: $\sigma\le1$;
- one-dimensional threshold safety: $\sigma\le2$;
- safety through $k$ fixed functionals with experiment-dependent thresholds: $\sigma\le k$;
- at most $k$ experiments unsafe anywhere: $\sigma\le k$.

## 2. Observation Helly numbers: small killing witnesses

Say the observations have **Helly number $\le h$** if, for every experiment $u$, every finite subfamily of $\{\mathcal Y(\theta,u)\}_\theta$ with empty intersection contains an empty-intersection subfamily of size $\le h$. Examples:
- intervals in $\mathbb R$ have $h=2$;
- convex sets in $\mathbb R^q$ have $h=q+1$ (Helly's theorem);
- deterministic observations have $h=2$.

> **Theorem G2 (upward local-to-global).** If the observations have Helly number $\le h$, then a set $K$ is a trap whenever all its subsets of size $\le h$ are.

*Proof.*
- If $K$ is not a trap, some $u\in\mathcal S(K)$ has $\bigcap_K\mathcal Y(\cdot,u)=\varnothing$.
- Helly gives $K'\subseteq K$ with $\lvert K'\rvert\le h$ and $\bigcap_{K'}\mathcal Y(\cdot,u)=\varnothing$.
- Since $u\in\mathcal S(K)\subseteq\mathcal S(K')$, $K'$ is not a trap. ∎

**This is the wrong direction for identification.** G2 says traps are "determined from below", but identification asks whether *any* trap exists. The cycle trap of size $n$ has $h=2$, and its only trap of size $\ge2$ is $\Theta_0$. It is consistent with G2, since its 2-subsets are not traps. So G2 places no bound on minimal trap size.

> **Theorem G2b (realizable trap families).** Let $\mathcal N$ be a family of subsets of $\Theta_0$, each of size $\ge2$. $\mathcal N$ is the family of non-traps of size $\ge2$ for some instance with observation Helly number $\le h$ iff:
> - every $N\in\mathcal N$ contains some $P$ with $2\le\lvert P\rvert\le h$ such that every $K$ with $P\subseteq K\subseteq N$ lies in $\mathcal N$.
>
> For $h=2$, the realization uses interval observations.

*Proof.*
- **(⇒)** Let $N$ be killed by $u$. Then $N\cap U(u)=\varnothing$, and Helly gives $P\subseteq N$, with $\lvert P\rvert\le h$ and an empty intersection. Every $K$ between $P$ and $N$ avoids $U(u)$ and has an empty intersection, so it is killed too.
- **(⇐)** For each $N$, take an experiment unsafe outside $N$, with alphabet $P$ and $\mathcal Y(\theta)=P\setminus\{\theta\}$ for $\theta\in P$, $\mathcal Y(\theta)=P$ otherwise.
  - It kills exactly the interval $[P,N]$ of sets, and its Helly number is $\lvert P\rvert$.
  - For $\lvert P\rvert=2$ this is the $\mathsf N$ gadget, which is realizable by intervals (H1(c)). ∎

**Verification.** For all $2^{11}$ families on 4 points:
- universality (T6) holds in every case;
- the 1218 families satisfying the $h=2$ condition are realized by intervals, and the realized trap families match exactly (E003 §J).

So with interval observations, 830 of the 2048 families on 4 points are *not* trap families. The simplest is "every 2- and 3-subset is a trap, $\Theta_0$ is not". Killing $\Theta_0$ with intervals always kills a pair as well.

## 3. Geometric safety

**Setting.** $\Theta_0\subset\mathbb R^d$ is finite. Safety is linear in the parameter: $U(u)=\{\theta : \langle a_u,\theta\rangle>b_u\}$, an open halfspace. The experiment set is finite.

> **Proposition G3.**
> - (a) $\sigma(K)\le\lvert\operatorname{ext}\operatorname{conv}K\rvert$.
> - (b) For $d=1$, $\sigma\le2$, and $\{\min K,\max K\}$ is a trap with the same diameter as $K$. Trap existence is decided by pairs, for every observation model.
> - (c) For $d=2$, every $n\ge3$, linear safety and linear interval observations, there is an instance whose unique trap of size $\ge2$ is $\Theta_0$, and whose proper subsets are each identified by one experiment.
> - (d) For $d$ unbounded, trap existence is NP-complete with linear safety and linear interval observations (H1(d)).

*Proof.*
- **(a)** A linear functional attains its maximum over $K$ at an extreme point of $\operatorname{conv}K$. So every halfspace meeting $K$ contains an extreme point, and the extreme points hit every trace.
- **(b)** In $d=1$, halfspaces are up-sets and down-sets, and $\mathcal S(\{\min K,\max K\})=\mathcal S(K)$.
- **(c)** Take $\theta_i=(i,i^2)$ and experiment $a_k$:
  - $a_k$ is unsafe iff $2kx-y-k^2+\tfrac12>0$. For $\theta_i$ this quantity is $\tfrac12-(i-k)^2$, so the halfspace contains only $\theta_k$.
  - $a_k$ observes $x$ with $\delta=\tfrac14$, which separates every pair.
  - $\Theta_0$ is a trap, vacuously. A proper subset misses some $k$, so $a_k$ is safe for it and identifies it in one step.
  - Verified for $n\le8$ in exact rational arithmetic (E003 §H).
- **(d)** By H1(d). ∎

**Reading.**
- One-dimensional ordered structure gives pairwise witnesses.
- In the plane the obstruction is **convex position**. Each extreme point can be the unique hypothesis blocking "its" experiment. This is the geometric form of T5's "every member blocks a distinct experiment".
- Classical tools play these roles:
  - **Carathéodory / extreme points** bound $\sigma$ by the convex-position size, $\sigma\le c(\Theta_0)=\max\{\lvert X\rvert : X\subseteq\Theta_0\text{ in convex position}\}$. Hence minimal traps have size $\le c(\Theta_0)+2$, and trap existence is decidable in $O(n^{c+2})$.
  - **Erdős–Szekeres** shows that large planar point sets in general position always contain large convex-position subsets. So this bound is weak unless $\Theta_0$ is degenerate, e.g. points on few lines.
  - **Helly** controls only the observation side (G2).
  - **Radon** played no role that I could find.

**Open (G-O1).** What is the complexity of trap existence for halfspace safety in fixed dimension $d\ge2$, with finitely many explicitly listed experiments?
- Minimal traps are unbounded (G3(c)), so witness enumeration fails.
- The H1 reduction needs arbitrary unsafe-set systems. Halfplane traces on a planar point set have bounded VC dimension, which may or may not prevent the encoding.
- I have no conjecture with real evidence either way.

## 4. Homogeneous experiments: when traps are hereditary

The natural linear model of Stage 0 (C1) had only small traps despite unbounded $\sigma$. The reason is structural.

> **Theorem G4.** Suppose:
> - the experiment set is closed under scaling $u\mapsto tu$ for $t\in(0,1]$;
> - $\varphi(\theta,u)\ge0$ with $\varphi(\theta,tu)=t^q\varphi(\theta,u)$;
> - safety is $\varphi(\theta,u)\le1$;
> - observations are $\varphi(\theta,u)+[-\delta,\delta]$.
>
> Then $K$ is a trap iff, for every $u$ with $\max_K\varphi(\cdot,u)>0$, $\min_K\varphi(\cdot,u)\ge(1-2\delta)\max_K\varphi(\cdot,u)$. Traps are therefore closed under subsets, and trap existence is decided by pairs.

*Proof.*
- Along the ray through $u$, the safe scales are $t^q\le1/\max_K\varphi$.
- The spread is $t^q(\max_K\varphi-\min_K\varphi)$, which is maximal at the largest safe scale. That maximum is $(\max-\min)/\max$.
- Subsets raise the minimum and lower the maximum, so they preserve the inequality. ∎

**Reading.**
- When safety and sensing are *the same functional*, and the agent may always choose a safe intensity along any direction, the safety constraint normalizes itself away. It costs exactly a factor $(1-2\delta)$ of relative resolution, and it creates no combinatorial obstructions.
- C1 is the case $\varphi=\langle\theta,u\rangle$ with $u\ge0$ and $q=1$.
- The scalar model with $p\ne1$ is *not* homogeneous in this sense, since safety is linear in $x$ and sensing is $x^p$. Its traps $[a,b]$ with $b-a\le2\delta b^p$ are not hereditary for $p>1$, but they are threshold-ordered (G3(b)).

**Hence the brief's Direction C diagnosis is confirmed and made precise.** Genuinely multidimensional obstructions need one of:
- safety and observation functionals that differ;
- finite or otherwise non-scalable experiment menus;
- non-homogeneous sensing.

The convex-position trap (G3(c)) uses a finite menu. A natural open question is whether two different functionals with full scaling (Q-C2) already produce large minimal traps.

## 5. Open questions

- **G-O1.** Complexity for halfspace safety in fixed dimension $d\ge2$.
- **G-O2 (Q-C2 sharpened).** With full scaling, safety $\langle a(u),\theta\rangle\le1$ and sensing $\langle c(u),\theta\rangle$, where $a\ne c$: are minimal traps bounded in terms of $d$?
- **G-O3.** For continuum $\Theta_0$, an analogue of $\sigma$ via the support function of $\operatorname{conv}K$ restricted to the experiment normals. Does a finite-$\sigma$ condition give a continuum local-to-global theorem in the setting of `research/continuum_analysis.md`?
