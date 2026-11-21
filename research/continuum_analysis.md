# Stage 1 — Continuum trap characterization

*2026-11-21. This answers Stage 0's Q-F3. Everything here is proved analytically; no computation is involved.*

## 0. Summary

| ID | Statement | Status |
|---|---|---|
| K1 | Under compactness, continuity of safety, closed-graph observations, and **lower semicontinuity of the certified-safe correspondence** (L): for every $\varepsilon>0$, if every closed trap has diameter $<\varepsilon$, then **one horizon $T$ works uniformly**. Conversely, a trap of diameter $>\varepsilon$ blocks every policy forever. | proved |
| K2 | Under the same hypotheses the closed traps form a closed family. The minimax asymptotic diameter equals $D^\*=\max\{\operatorname{diam}K : K\text{ a closed trap}\}$, and it is reached within finite time for every $\varepsilon>D^\*$. | proved |
| K3 | Under the same hypotheses, eventual identification ($\forall\theta^\*\,\forall\eta\,\exists T$) implies uniform identification ($\exists T\,\forall\theta^\*\,\forall\eta$). | proved |
| X1 | Without (L), K1 fails. Safety and observations are continuous and everything is compact, yet the agent is stuck at diameter $\ge\tfrac12$ while every trap has diameter $\le0.02$. The mechanism is an informative experiment that becomes admissible only in the limit. | counterexample |
| X2 | K1's strict/non-strict gap is sharp. With all hypotheses holding, the worst-case diameter decreases to $D^\*$ but never reaches it, and the horizon $T(\varepsilon)$ diverges as $\varepsilon\downarrow D^\*$. | counterexample |
| X3 | Without the closed-graph property, the supremum of closed-trap diameters is not attained, and K1(a) fails at that value. | counterexample |
| X4 | Without joint continuity, eventual does not imply uniform. | counterexample |
| S | The scalar model satisfies all the hypotheses. K2 recovers Stage 0's S5 value $\min(U_0-L_0,2\delta U_0^p)$. | check |

**Answer to the brief's question 4.** The finite characterization extends to compact spaces, but not unconditionally. The condition that makes it work is (L). Its failure mode is exactly the one the brief anticipated: experiments that become safe only once a boundary is reached. The corrected theorem is K1–K3, and X1–X4 show which hypotheses matter.

## 1. Setting

- **Spaces.** $\Theta_0$ and $\mathcal U$ are compact metric spaces, and $\mathsf Y$ is a compact metric observation space. Bounded ranges of continuous $h$ make intervals fit this.
- **Safety.** $g:\Theta_0\times\mathcal U\to\mathbb R$ is continuous, and $u$ is safe for $\theta$ iff $g(\theta,u)\le0$.
- **Observations.** $\mathcal Y(\theta,u)\subseteq\mathsf Y$ is nonempty, and the graph $\{(\theta,u,y) : y\in\mathcal Y(\theta,u)\}$ is closed. For $[h-\delta,h+\delta]$ with continuous $h$ this holds.
- **Hyperspace.** $\mathcal K$ is the set of nonempty closed subsets of $\Theta_0$, with the Hausdorff metric; it is compact. Write
  - $G(K,u)=\max_{\theta\in K}g(\theta,u)$, which is jointly continuous on $\mathcal K\times\mathcal U$;
  - $\mathcal S(K)=\{u : G(K,u)\le0\}$, a closed set;
  - $K_y^u=\{\theta\in K : y\in\mathcal Y(\theta,u)\}$, closed by the closed graph.
- **The game.** As in the finite case, $\Theta_{t+1}=(\Theta_t)^{u_t}_{y_t}$, with $u_t\in\mathcal S(\Theta_t)$ and $y_t\in\mathcal Y(\theta^\*,u_t)$ chosen adaptively. Starting from a closed $\Theta_0$, every $\Theta_t$ is closed.
- **Trap.** A set $K$ such that $\bigcap_{\theta\in K}\mathcal Y(\theta,u)\ne\varnothing$ for every $u\in\mathcal S(K)$.

**(L) — lower semicontinuity of $\mathcal S$.** If $K_n\to K$ in $\mathcal K$ and $u\in\mathcal S(K)$, then there are $u_n\in\mathcal S(K_n)$, for all large $n$, with $u_n\to u$.

> **Lemma 0 (a checkable sufficient condition).** Suppose every $K\in\mathcal K$ has $\mathcal S(K)=\overline{\{u : G(K,u)<0\}}$, i.e. strictly safe experiments are dense in the safe ones. Then (L) holds.

*Proof.*
- Fix $u'$ with $G(K,u')<0$. By continuity of $G$, $G(K_n,u')<0$ for large $n$, so $u'\in\mathcal S(K_n)$.
- Approximate $u$ by such $u'$ and diagonalize. ∎

(L) fails precisely when an experiment is safe for $K$ only "tangentially". Some $u\in\mathcal S(K)$ has a neighbourhood containing no experiment that is safe for slightly larger sets.

## 2. The characterization

Fix $\varepsilon>0$. Define $W_0=\{K\in\mathcal K : \operatorname{diam}K\ge\varepsilon\}$ and
$$W_{t+1}=\{K\in W_0 : \forall u\in\mathcal S(K)\ \exists y\ \ K^u_y\ne\varnothing,\ K^u_y\in W_t\}.$$
By induction on $t$, $K\in W_t$ iff the adversary can keep $\operatorname{diam}\ge\varepsilon$ through $t$ more experiments from $K$. Unwinding the definition when $K\notin W_t$ gives the agent's strategy.

> **Lemma 1.** Each $W_t$ is up-closed under inclusion, and $W_{t+1}\subseteq W_t$.

*Proof.*
- **Up-closure**, by induction. If $K\subseteq K'$, then $\mathcal S(K')\subseteq\mathcal S(K)$ and $K'^u_y\supseteq K^u_y$, so the adversary's answer for $K$ works for $K'$.
- **Decrease.** $W_1\subseteq W_0$ by definition. If $W_t\subseteq W_{t-1}$, the definitions give $W_{t+1}\subseteq W_t$. ∎

> **Lemma 2.** Under (L), each $W_t$ is closed in $\mathcal K$.

*Proof.* By induction on $t$. $W_0$ is closed because $\operatorname{diam}$ is continuous on $\mathcal K$. Assume $W_t$ is closed, and let $K_n\in W_{t+1}$ with $K_n\to K$; then $K\in W_0$.
- Let $u\in\mathcal S(K)$. By (L), choose $u_n\in\mathcal S(K_n)$ with $u_n\to u$, and $y_n$ with $M_n:=(K_n)^{u_n}_{y_n}\in W_t$.
- By compactness of $\mathsf Y$ and $\mathcal K$, pass to a subsequence with $y_n\to y$ and $M_n\to M$. Then $M\in W_t$, because $W_t$ is closed.
- **$M\subseteq K^u_y$.** Each $\theta\in M$ is a limit of points $\theta_n\in M_n\subseteq K_n$, so $\theta\in K$. Since $y_n\in\mathcal Y(\theta_n,u_n)$, the closed graph gives $y\in\mathcal Y(\theta,u)$.
- By Lemma 1, $K^u_y\in W_t$. Hence $K\in W_{t+1}$. ∎

> **Lemma 3 (no (L) needed).** Let $L=\bigcap_tW_t$. If $K\in L$ and every $W_t$ is closed, then every $u\in\mathcal S(K)$ has some $y$ with $K^u_y\in L$.

*Proof.*
- For each $t$ choose $y_t$ with $K^u_{y_t}\in W_t$. Pass to a subsequence with $y_t\to y$ and $K^u_{y_t}\to M$.
- For each $s$, $K^u_{y_t}\in W_s$ for all $t\ge s$, so $M\in W_s$ by closedness. Hence $M\in L$.
- As in Lemma 2, $M\subseteq K^u_y$, and $L$ is up-closed. ∎

> **Theorem K1.** Assume compactness, continuity of $g$, a closed observation graph, and (L). Let $\varepsilon>0$.
> - (a) If every closed trap has $\operatorname{diam}<\varepsilon$, there is $T$ and a policy with $\operatorname{diam}\Theta_T<\varepsilon$ for all $\theta^\*$ and all admissible reports.
> - (b) Without any hypotheses: if some trap has $\operatorname{diam}>\varepsilon$, no policy ever achieves $\operatorname{diam}\Theta_t\le\varepsilon$, for some $\theta^\*$ and reports.

*Proof.*
- **(b)** As in finite T1: the adversary holds the trap.
- **(a)** Suppose $\Theta_0\in W_t$ for every $t$, so $L\ne\varnothing$. By Lemma 2 each $W_t$ is closed, so $L$ is closed in $\mathcal K$.
  - **$L$ has a minimal element**, by Zorn's lemma. A chain in $L$ is a family of compact sets totally ordered by inclusion. Its intersection is nonempty, by the finite-intersection property, and it is the Hausdorff limit of the chain viewed as a net. So the intersection lies in $L$.
  - **The minimal element $K$ is a trap.** By Lemma 3, every $u\in\mathcal S(K)$ has $K^u_y\in L$ with $K^u_y\subseteq K$, so $K^u_y=K$ by minimality, i.e. $y\in\bigcap_K\mathcal Y(\cdot,u)$.
  - So $K$ is a closed trap with $\operatorname{diam}K\ge\varepsilon$, since $K\in W_0$. This contradicts the hypothesis.
  - Hence $\Theta_0\notin W_T$ for some $T$, which is (a). ∎

> **Theorem K2.** Under the hypotheses of K1, the closed traps form a closed subset of $\mathcal K$, so $D^\*=\max\operatorname{diam}$ over closed traps is attained. Moreover:
> $$\inf_\pi\ \sup_{\theta^\*,\eta}\ \lim_t\operatorname{diam}\Theta_t\;=\;D^\*,$$
> and for every $\varepsilon>D^\*$ some finite $T(\varepsilon)$ achieves $\operatorname{diam}\Theta_{T(\varepsilon)}<\varepsilon$ uniformly.

*Proof.*
- **Closedness.** Let $K_n\to K$ with each $K_n$ a trap, and let $u\in\mathcal S(K)$.
  - Use (L) to get $u_n\in\mathcal S(K_n)$ with $u_n\to u$, and pick $y_n\in\bigcap_{K_n}\mathcal Y(\cdot,u_n)$.
  - For a limit point $y$ of $(y_n)$, the closed graph gives $y\in\mathcal Y(\theta,u)$ for every $\theta\in K$, using approximating $\theta_n\in K_n$.
- **The value.** The rest follows from K1(a) applied to each $\varepsilon>D^\*$, and from K1(b) at the maximizing trap. Note that $\operatorname{diam}\Theta_t$ is non-increasing, so the limit exists. ∎

> **Theorem K3 (compactness bridges the quantifiers).** Under the hypotheses of K1, suppose some policy guarantees that, for every $\theta^\*$ and every report sequence, $\operatorname{diam}\Theta_t<\varepsilon$ eventually. Then some policy guarantees it by a fixed time $T$.

*Proof.*
- If no uniform $T$ exists, then $\Theta_0\in L$, and the proof of K1(a) produces a closed trap $K$ with $\operatorname{diam}K\ge\varepsilon$.
- The adversary holds $K$, with $\theta^\*\in K$, against *any* policy. That contradicts eventual success. ∎

**Remarks.**
- $\varepsilon>0$ is essential. At $\varepsilon=0$, "$\operatorname{diam}<0$" is impossible, and exact identification of a continuum parameter in finite time requires zero noise and essentially injective observations.
- The proofs use only the order structure and compactness. This is the viability-kernel argument, specialised to the hyperspace and with the safe-action correspondence playing the role of the constraint map.

## 3. Counterexamples

**X1 — admissibility in the limit ((L) fails, everything else holds).**

*The instance.*
- $\Theta_0=[0,1]$, $\mathcal U=[-1,1]\cup[2,3]$, and $\delta=\tfrac1{10}$.
- **"Sharp" experiments**, $u\in[-1,1]$:
  - safety $g=\theta-\tfrac12+\lvert u\rvert$;
  - observation $h=10\theta$.
- **"Probe" experiments**, $u=2+s$ with $s\in[0,1]$:
  - safety $g=\theta-\tfrac12-s$;
  - observation $h=\max\bigl(0,\,2\delta+10(\theta-\tfrac12-\tfrac s2)\bigr)$.
- $g$ and $h$ are continuous, all spaces are compact, and $\mathcal Y=[h-\delta,h+\delta]$.

*Every trap has diameter $\le2\delta/10=0.02$.* Let $K$ be a trap with $m=\max K$.
- *Case $m\le\tfrac12$.* The sharp experiment $u=0$ is safe, and it resolves $K$ to width $2\delta/10$.
- *Case $m>\tfrac12$.* No sharp experiment is safe. The probe $s=m-\tfrac12$ is safe. It has $h(m)=2\delta+5s>2\delta$, and is flat at 0 below $\tfrac12+\tfrac s2-2\delta/10$. So any point of $K$ below that threshold makes the spread exceed $2\delta$, while points above it must lie within $2\delta/10$ of $m$.

*Yet the adversary keeps $\Theta_t\supseteq[0,\tfrac12]$ forever.*
- It reports $y=\delta$ to every probe, which is consistent with any $\theta^\*\le\tfrac12$, since $h\in[0,2\delta]$ there. The response to $y=\delta$ is $[0,\tfrac12+\tfrac s2]$.
- From $\Theta_t=[0,m_t]$ with $m_t>\tfrac12$, the agent may only probe with $s\ge m_t-\tfrac12$. So $m_{t+1}-\tfrac12\ge(m_t-\tfrac12)/2>0$.
- The sharp experiment becomes safe only at $m=\tfrac12$ exactly, which is never reached. So $\operatorname{diam}\Theta_t\ge\tfrac12$ for all $t$, and K1(a) fails for every $\varepsilon\in(0.02,\tfrac12)$.

*Where (L) fails.* At $K=[0,\tfrac12]$: $\mathcal S(K)\ni0$, but $K_n=[0,\tfrac12+\tfrac1n]$ has no safe sharp experiment. $G(K,u)=\lvert u\rvert$ has no strict sublevel set near 0.

*The mechanism* is the brief's anticipated failure. There are infinitely many strictly decreasing consistent sets, and the informative experiment becomes admissible only in their limit. The limit $[0,\tfrac12]$ is **not** a trap and is never reached. In the finite case this cannot happen, because strict decreases end after $n-1$ steps.

**X2 — the boundary case is not attained ((L) holds).** Remove the sharp experiments from X1.
- Now $[0,\tfrac12]$ is a closed trap, and $D^\*=\tfrac12$.
- (L) holds, since $\mathcal S(K)=[2+\max(0,\max K-\tfrac12),\,3]$ varies continuously.
- The optimal play $s_t=m_t-\tfrac12$ gives $m_t-\tfrac12=2^{-t}(m_0-\tfrac12)$. So $\operatorname{diam}\Theta_t\downarrow\tfrac12$ but stays $>\tfrac12$ for all $t$.
- Hence K1(a) cannot be strengthened to "$\le\varepsilon$" at $\varepsilon=D^\*$, and $T(\varepsilon)\ge\log_2\frac{1/2}{\varepsilon-1/2}\to\infty$ as $\varepsilon\downarrow D^\*$. These are the brief's "arbitrarily long learning horizons". They appear exactly at the critical tolerance, never above it (K2).

**X3 — the closed graph matters.** $\Theta_0=[0,1]$, $\delta=\tfrac1{10}$, two always-safe experiments.
- $u_1$ reports $\mathcal Y=\{0\}$ for $\theta<\tfrac12$ and $\{1\}$ for $\theta\ge\tfrac12$. Its graph is not closed at $\theta=\tfrac12$.
- $u_2$ has interval observations with $h=10\max(0,\theta-\tfrac12)$. These are continuous, with a closed graph.
- **Closed traps.** $u_1$ forces a trap to lie in $[0,\tfrac12)$ or in $[\tfrac12,1]$. $u_2$ then restricts traps in $[\tfrac12,1]$ to diameter $\le0.02$. So the closed traps are the closed subsets of $[0,\tfrac12)$ and these small sets. Every closed trap has diameter $<\tfrac12$, and the supremum $\tfrac12$ is not attained.
- **The adversary's play.** Reporting $y=0$ to $u_1$ leaves the non-closed set $[0,\tfrac12)$. That set is a trap of diameter $\tfrac12$, and the adversary holds it forever.
- **Conclusion.** K1(a) fails at $\varepsilon=\tfrac12$ and K2's maximum does not exist. Closed graphs are what keep the consistent sets closed. Without that, the relevant traps can be non-closed, and compactness of $\mathcal K$ no longer applies.

**X4 — eventual ≠ uniform without joint continuity.**

*The instance.*
- $\Theta_0=\{0\}\cup\{p_{k,i}: k\ge1,\ 0\le i\le k\}$, with block $k$ inside $(2^{-k},2^{-k+1})$. This is compact and countable, and its only accumulation point is 0.
- Exact observations ($\delta=0$) and $\varepsilon=0$; the isolated points make exact identification meaningful.
- **Experiments:**
  - $w$: always safe, reports $2^{-k}$ on block $k$ and $0$ at $0$. This is continuous on $\Theta_0$.
  - $a_{k,i}$: safe exactly on block $k$, reports $[\theta=p_{k,i}]$.
  - $a_\infty$: the limit of the $a_{k,i}$, unsafe everywhere.

*The behaviour.*
- Every $\theta^\*$ is identified: $w$ first, then at most $k$ equality tests. No uniform bound exists.
- $g$ and $h$ are continuous in $\theta$ for each experiment, but not jointly at $(0,a_\infty)$.
- **Whether joint continuity alone, without (L), suffices for K3 is open (Q-K1).** Neither X1 nor X4 settles it. In X1, eventual identification also fails.

## 4. The scalar model satisfies the hypotheses

Take $\Theta_0=[L_0,U_0]$ with $L_0>0$, $\mathcal U=[0,1/L_0]$, $g=\theta x-1$ and $h=\theta x^p$.
- **Lemma 0 holds:** $\mathcal S(K)=[0,1/\max K]$ is the closure of $[0,1/\max K)$.
- **Closed traps.** A closed $K$ with endpoints $a<b$ is a trap iff $(b-a)x^p\le2\delta$ for all $x\le1/b$, i.e. iff $b-a\le2\delta b^p$.
- **The value.** Maximizing over $b\le U_0$ gives $D^\*=\min(U_0-L_0,\,2\delta U_0^p)$. This is exactly Stage 0's uniform value S5, here derived from K2.
- K2 predicts that the value is approached within finite time for every $\varepsilon>D^\*$. S5 is sharper: it is attained at $T=1$.

## 5. Open questions

- **Q-K1.** Does K3 (eventual ⇒ uniform) hold under compactness and joint continuity alone, without (L)?
- **Q-K2 (continuum analogue of T3).** Is there one policy that achieves, for each $\theta^\*$, the instance-wise optimum $\lim\operatorname{diam}\Theta_t=D(\theta^\*)$, the largest closed trap containing $\theta^\*$?
  - In the scalar model, maximum safe intensity does this, asymptotically (S2, S8).
  - In general the myopic argument of T3 breaks, since strictly shrinking moves need not terminate. X2 shows the instance-wise limit may be approached but not reached.
- **Q-K3.** Under (L), is $T(\varepsilon)$ bounded by a modulus of continuity of $g$ and $h$ and the covering numbers of $\Theta_0$? This would give quantitative horizons. *Answered in Stage 2 (§7): yes, through the margin $\mu(\varepsilon)$ (Q1′), and no margin-free bound exists (Q2). Q-K5 asks to bound $\mu(\varepsilon)$ itself.*
- **Q-K4.** Is there a "robust" variant without (L): define traps using the closure of the graph of $\mathcal S$ (i.e. relaxing safety by an infinitesimal), and prove a characterization that holds always? X1 suggests that the relaxed traps are what the adversary can actually hold.

## 6. Relation to the literature

- **SafeOpt** (Sui et al. 2015): the reachability closure $\bar R_\epsilon(S_0)$ is the Lipschitz/GP analogue of the limit of the $\Theta_t$ dynamics. Its fixed-point property corresponds to K1(b).
- **Set-membership experiment design** (Shakouri–van Waarde–Camlibel, arXiv:2607.00844; partly read). They show that exact identification under bounded noise is possible only for "uniformly discrete" prior sets. This parallels the positive noise floor $D^\*$ here and Stage 0's S5. Differences:
  - their inputs are designed offline;
  - there is no safety constraint;
  - the system is linear and dynamic.

  No characterization of the kind of K1 appeared in the sections I read.
- **Viability theory** (Aubin) provides the template for Lemmas 1–3 (closedness of capture/viability kernels under upper semicontinuity), but I have not checked a specific theorem against this statement.

---

## 7. Stage 2: quantitative learnability (2026-11-22)

K1 gives a uniform horizon $T(\varepsilon)$, but no estimate of it. This section gives one, explains why it must involve a margin, and records how the deadlock boundary behaves under perturbation. Hypotheses and notation are those of §§1–2. Observations are scalar, $\mathcal Y(\theta,u)=[h(\theta,u)-\delta_u,h(\theta,u)+\delta_u]$, with $h(\cdot,u)$ uniformly $L_h$-Lipschitz, and $w_K(u)=\max_Kh(\cdot,u)-\min_Kh(\cdot,u)$.

**Distinguishability margin.** For a closed set $K$,
$$\Delta(K)=\sup_{u\in\mathcal S(K)}\bigl[w_K(u)-2\delta_u\bigr].$$
- $K$ is a trap iff $\Delta(K)\le0$, by Helly in dimension 1.
- **$\Delta(K)>0$ alone does not give progress in diameter.** An informative experiment may only shave a thin sliver off $K$.

> **Theorem Q1 (packing horizon).** Suppose there is $\mu>0$ such that every closed $K\subseteq\Theta_0$ with $\operatorname{diam}K\ge\varepsilon$ has a safe $u$ with $w_K(u)\ge2\delta_u+\mu$. Then the policy "play such a $u$" achieves $\operatorname{diam}\Theta_T<\varepsilon$ uniformly, with
> $$T\le M\!\left(\Theta_0,\tfrac{\mu}{2L_h}\right)\le\left(1+\tfrac{4L_hD}{\mu}\right)^{d}\qquad(\Theta_0\subset\mathbb R^d,\ \operatorname{diam}\Theta_0\le D),$$
> where $M(\cdot,r)$ is the largest cardinality of an $r$-separated subset (the packing number).

*Proof.*
- Fix a step with current set $K$, the chosen $u$, and the report $y$. Let $m=\min_Kh$ and $M=\max_Kh$, so $M-m\ge2\delta_u+\mu$.
- **One extreme is excluded with margin.** The retained set is $\{\theta\in K : \lvert h(\theta,u)-y\rvert\le\delta_u\}$, whose $h$-values lie in $[y-\delta_u,y+\delta_u]$. One of $y-\delta_u\ge m+\mu/2$ or $y+\delta_u\le M-\mu/2$ must hold; otherwise $2\delta_u>M-m-\mu\ge2\delta_u$.
- **A ball is removed.** Say the first holds, and let $\theta_t$ attain $m$. Every $\theta\in K$ with $\lVert\theta-\theta_t\rVert<\mu/(2L_h)$ has $h(\theta,u)<m+\mu/2$, so it is removed. The other case is symmetric.
- **Counting.** So step $t$ removes from the current set the open ball of radius $r=\mu/(2L_h)$ around a point $\theta_t$ of that set. Later centres lie in later sets, hence outside all earlier balls. The centres are therefore pairwise $\ge r$ apart, so there are at most $M(\Theta_0,r)$ of them.
- The volume bound is the standard one. ∎

> **Corollary Q1′ (K1 made quantitative).** Under the hypotheses of K1, with $h$ jointly continuous and $L_h$-Lipschitz in $\theta$: if every closed trap has diameter $<\varepsilon$, then
> $$\mu(\varepsilon):=\min\{\Delta(K) : K\text{ closed},\ \operatorname{diam}K\ge\varepsilon\}>0,$$
> and $T(\varepsilon)\le M(\Theta_0,\mu(\varepsilon)/(4L_h))$.

*Proof.*
- **$\Delta$ is lower semicontinuous** on $\mathcal K$. Given $K_n\to K$, take a near-optimal $u\in\mathcal S(K)$, use (L) to get $u_n\in\mathcal S(K_n)$ with $u_n\to u$, and use joint continuity of $w$ and $\delta$.
- The family $\{K : \operatorname{diam}K\ge\varepsilon\}$ is compact, so $\Delta$ attains its minimum there. That minimum is positive, because no member is a trap.
- Apply Q1 with margin $\mu(\varepsilon)/2$. ∎

> **Proposition Q2 (the bound has the right shape).**
> - (a) *Exponent $d$ and scale $L_h/\mu$ are necessary.*
>   - **Instance.** $\Theta_0=[0,1]^d$, with always-safe "bump" experiments $h_q(\theta)=A\max(0,1-\lVert\theta-q\rVert/r)$ for $q\in\Theta_0$, amplitude $A=2\delta+\mu$, so $L_h=A/r$.
>   - **The margin hypothesis holds** for every $\varepsilon>r$. A set of diameter $\ge\varepsilon$ contains $q$ and a point at distance $\ge r$ from $q$, so $w=A$.
>   - **The adversary.** It always reports $y=\delta$. Each experiment then removes at most the ball of radius $r\mu/A=\mu/L_h$ around its centre.
>   - **Lower bound.** Reaching diameter $<\varepsilon$ requires removing all of $[0,1]^d$ except a set of diameter $<\varepsilon$, so $T\ge(1-\omega_d\varepsilon^d)/(\omega_d(\mu/L_h)^d)$. This matches Q1 up to constants depending on $d$.
> - (b) *A margin is necessary.* With $d=1$, $\operatorname{diam}\Theta_0=1$ and fixed Lipschitz constants, horizons can be arbitrarily long.
>   - **Instance.** X2 with the trap moved to $[0,\beta]$ for $\beta\uparrow\varepsilon$.
>   - **Horizon.** $T(\varepsilon)\ge\log_2\frac{1-\beta}{\varepsilon-\beta}$, while $L_g$ and $L_h$ are fixed.
>   - **Margin.** Here $\mu(\varepsilon)\to0$.
>
> So no bound $F(d,\varepsilon,L_g,L_h)$ without a margin parameter exists, and covering numbers replace cardinality exactly when a uniform informativeness margin is available.

*Proof.*
- (a) The volume argument as stated.
- (b) The computation of X2, with threshold $\tfrac12$ replaced by $\beta$. ∎

**Answer to the brief's question 5.**
- Yes. The qualitative K1 horizon becomes $T(\varepsilon)\le M(\Theta_0,\mu(\varepsilon)/4L_h)$, a covering-number bound in place of Stage 1's cardinality bound $\lvert\Theta_0\rvert-1$.
- The margin $\mu(\varepsilon)$ is positive under the K1 hypotheses but uncontrolled near the critical tolerance $D^\*$. Both the exponent $d$ and the dependence on the margin are necessary (Q2).
- Safety slack enters only through (L), i.e. through whether $\mu(\varepsilon)>0$. A quantitative form of (L), such as a modulus for the strictly safe approximation, would be needed to bound $\mu(\varepsilon)$ from the data of $g$ and $h$. That is open (Q-K5).

### 7.1 The boundary of informational deadlock

> **Proposition Q3 (no universal rate).**
> - **Instance.** In X2, replace the probe response $\tfrac12+\tfrac s2$ by $\tfrac12+f(s)$, for any continuous increasing $f$ with $0<f(s)<s$ on $(0,1]$ and $f(0)=0$. Use $h=\max(0,2\delta+c(\theta-\tfrac12-f(s)))$, which is continuous and Lipschitz in $\theta$.
> - **Result.** The worst-case excess $m_t-\tfrac12$ follows the iteration $x_{t+1}=f(x_t)$.
>   - $f(x)=x/2$ gives geometric decay.
>   - $f(x)=x-x^2$ gives $x_t\sim1/t$.
>   - Any decreasing sequence $x_t\downarrow0$ arises, by interpolating $f(x_t)=x_{t+1}$.
>
> So the approach to an asymptotic obstruction has **no universal rate**. Rates are a property of the probe family, not of the trap structure.

*Proof.* As in X2: the adversary's report $y=\delta$ leaves $[0,\tfrac12+f(s)]$, and the optimal probe is $s=m_t-\tfrac12$. ∎

> **Proposition Q4 (discontinuity under safety relaxation).** For $\gamma\ge0$, let $V(\gamma)$ be the minimax limiting diameter when safety is relaxed to $g\le\gamma$. $V$ is non-increasing. In X1, $V(0)\ge\tfrac12$ but $V(\gamma)\le0.02$ for every $\gamma>0$: once $m_t<\tfrac12+\gamma$, the sharp experiment $u=0$ is safe. So **the attainable accuracy can jump under an arbitrarily small relaxation of the safety standard**.
>
> Conversely, under the density condition of Lemma 0, closed traps of the relaxed models converge to traps of the original. That is, $\limsup_{\gamma\downarrow0}D^\*(\gamma)\le D^\*(0)$, by the argument of A4(a) with $G\le\gamma_n$ in place of $G\le-L_gh_n$.

*Proof.* Monotonicity holds because relaxation enlarges every $\mathcal S(K)$. The X1 computation is in §3. The limit argument follows A4(a) verbatim. ∎

**Status of the remaining question.** $D^\*(\gamma)\le D^\*(0)$ always holds, by monotonicity. Under density, is $\lim_{\gamma\downarrow0}D^\*(\gamma)=D^\*(0)$? Relaxation can unblock experiments with $0<G(K,u)\le\gamma$. These are informative on a trap $K$ only with margins that tend to 0, but they are still informative. I have neither a proof nor a counterexample (Q-K4′).

**Terminology.** I introduce no new object. An "asymptotic obstruction", as in X1, is exactly a set that is a trap of the *limit* (closure) safety correspondence but not of $\mathcal S$ itself. The precise version is Q-K4: the relaxed-trap characterization of §5. Q4 shows that relaxed traps, not exact traps, govern what is attainable once safety is allowed any slack at all.
