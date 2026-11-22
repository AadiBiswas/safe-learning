# Stage 2 — Approximate safety witnesses and certified discretization

*2026-11-21. This connects the finite witness theory (`research/witness_geometry.md`) to the continuum theorem K1–K3 (`research/continuum_analysis.md`). Checks are in E005 §§J–K.*

## 0. Summary

| ID | Statement | Status |
|---|---|---|
| A0 | $\sigma_\gamma$ is defined for unit safety normals. It is exactly an additive $\gamma$-coreset of the support function on the experiment normals. | definition / observation |
| A1 | Maximizers over a $\rho$-net of directions approximate $h_K$ to within $2R\rho$. | proved (classical) |
| A2 | Every compact $K\subset B(x_0,R)$ has $\sigma_\gamma(K)\le N(S^{d-1},\gamma/2R)$, the covering number of the sphere at scale $\gamma/2R$. Conversely, for the sphere and all-direction cap experiments, $\sigma_\gamma\ge c_d(R/\gamma)^{(d-1)/2}$. In $d=2$ the exact asymptotic is $\pi/\sqrt{2\gamma/R}$. | proved; the sharp upper exponent $(d-1)/2$ is cited |
| A2′ | **Robust Lemma W.** Every far trap contains a far trap of the $\gamma$-*tightened* model with at most $\sigma_\gamma+2$ points. | proved |
| A3 | **Two-sided net certificates (soundness).** A finite trap in a perturbed net instance certifies: (upper) "no closed trap of diameter $\ge\varepsilon$", or (lower) "a closed trap of diameter $\ge\varepsilon$ exists". | proved |
| A4 | **Completeness.** If strictly safe experiments are dense (Lemma 0) and $D^\*<\varepsilon$, the upper certificate succeeds for every sufficiently fine net. If a trap of diameter $>\varepsilon$ has positive blocking and blindness margins, the lower certificate succeeds. Without these conditions the certificates can fail forever (X5). | proved; counterexample |
| CandA | The brief's Candidate A holds, for nets $F\subseteq K$. | proved |
| CandB | The brief's Candidate B holds, for nets $F\subseteq K$. | proved |

**Answer to the brief's question 4.**
- Approximate witnesses give finite, quantitative certificates for continuum problems.
- **Soundness holds always.** Completeness holds exactly away from the boundary cases identified in Stage 1: tangential safety (X1) and zero-margin traps (X2).
- The number of points needed is the covering number of the direction sphere at the scale (safety margin)/(radius), up to the classical improvement of the exponent from $d-1$ to $(d-1)/2$. It degenerates as the margin goes to 0, unavoidably.

## 1. Approximate witnesses

**Normalization.** Linear safety $a_u^\top\theta\le b_u$ with $\lVert a_u\rVert_2=1$. Without normalization, rescaling $(a,b)\mapsto(\lambda a,\lambda b)$ would multiply every margin by $\lambda$.

**Definition (approximate safety-witness number).** For compact $K$ and a margin $\gamma\ge0$:
$$\sigma_\gamma(K)=\min\{\lvert F\rvert : F\subseteq K\text{ finite},\ \forall u:\ h_K(a_u)>b_u+\gamma\ \Rightarrow\ h_F(a_u)>b_u\}.$$
Every experiment blocked by $K$ with margin more than $\gamma$ must be blocked by $F$.

**Observation A0.**
- *At zero margin.* For finite $K$, $\sigma_0=\sigma$. For compact $K$, $\sigma_0$ may be infinite: take the disk and all tangent caps.
- *As a coreset.* When the thresholds $b_u$ range over all reals for each normal in a set $A$, the condition is equivalent to $h_F(a)\ge h_K(a)-\gamma$ for all $a\in A$. Then $\sigma_\gamma$ is the size of the smallest **additive $\gamma$-coreset for the support function restricted to $A$**.
- *Literature.* Directional-width coresets ($\varepsilon$-kernels, Agarwal–Har-Peled–Varadarajan 2004) are therefore exactly the right literature. No novelty is claimed for A1–A2.

> **Theorem A1 (support-function sampling).** Let $K\subseteq B(x_0,R)$ be compact and $D_\rho$ a $\rho$-net of $S^{d-1}$. Let $F_\rho=\{\theta_v : v\in D_\rho\}$ with $\theta_v\in\arg\max_K v^\top\theta$. Then for every unit $a$,
> $$0\le h_K(a)-h_{F_\rho}(a)\le2R\rho .$$

*Proof.*
- Translate so that $x_0=0$. Both sides shift by $a^\top x_0$, so the gap is unchanged. Now $\lVert\theta\rVert\le R$ on $K$.
- Pick $v\in D_\rho$ with $\lVert a-v\rVert\le\rho$, and let $\theta_a$ attain $h_K(a)$. Then
  - $h_K(a)=a^\top\theta_a\le v^\top\theta_a+\rho R\le v^\top\theta_v+\rho R$;
  - $h_{F_\rho}(a)\ge a^\top\theta_v\ge v^\top\theta_v-\rho R$.
- Subtracting gives the bound. The lower bound $0\le$ holds because $F_\rho\subseteq K$. ∎

*Check:* on random sets in $d=2,3$, the worst observed gap was 1.5% of $2R\rho$ (E005 §J). The bound is pessimistic for typical sets.
- **Sharper for round sets.** For a ball, $h_K(a)-h_{F_\rho}(a)\le R(1-\cos\rho)\approx R\rho^2/2$. Quadratic dependence on $\rho$ is what makes the Dudley exponent $(d-1)/2$ possible.

> **Theorem A2 (witness counts).**
> - (a) $\sigma_\gamma(K)\le N(S^{d-1},\gamma/(2R))\le(1+4R/\gamma)^d$.
> - (b) If $K$ lies in an affine subspace of dimension $k$, the same holds with $S^{k-1}$ in place of $S^{d-1}$ (intrinsic dimension).
> - (c) *Lower bound.* Let $K=R\,S^{d-1}$, and include an experiment $(a,\,R-\gamma-\tau)$ for every unit $a$, with small $\tau>0$. Then $\sigma_\gamma(K)\ge M(S^{d-1},2\arccos(1-\gamma/R))$, a packing number of order $(R/\gamma)^{(d-1)/2}$. In $d=2$: $\sigma_\gamma(K)=\lceil\pi/\arccos(1-\gamma/R)\rceil\sim\pi/\sqrt{2\gamma/R}$.

*Proof.*
- **(a)** Take $F_\rho$ with $2R\rho\le\gamma$. If $h_K(a)>b+\gamma$, then $h_{F_\rho}(a)\ge h_K(a)-\gamma>b$. Covering numbers of the sphere are standard.
- **(b)** For $a\in\mathbb R^d$, write $a=a_\parallel+a_\perp$ relative to the subspace's direction space. On $K$, $a^\top\theta=a_\parallel^\top\theta+\mathrm{const}$ with $\lVert a_\parallel\rVert\le1$. Apply A1 in the subspace.
- **(c)** A point $\theta\in K$ blocks experiment $a$ iff $a^\top\theta>R-\gamma-\tau$, i.e. iff the angle between $\theta$ and $a$ is less than $\alpha=\arccos(1-(\gamma+\tau)/R)$.
  - So $F$ must have a point within angle $\alpha$ of every direction. That is an $\alpha$-covering of the sphere, so $\lvert F\rvert\ge N(S^{d-1},\alpha)\ge M(S^{d-1},2\alpha)$.
  - Letting $\tau\to0$, and using $\arccos(1-x)\sim\sqrt{2x}$, gives order $(R/\gamma)^{(d-1)/2}$.
  - In $d=2$ the covering of a circle by arcs of half-angle $\alpha$ needs exactly $\lceil\pi/\alpha\rceil$ points. ∎

*Check:* the exact circular-arc solver on 1439 rational points of the unit circle gives $16,32,63$ witnesses at $\gamma=1/50,1/200,1/800$, so $\sqrt\gamma\cdot\sigma_\gamma=2.263,2.263,2.227$ against the predicted $\pi/\sqrt2=2.221$ (E005 §J).

**The sharp upper exponent is classical.**
- For every compact $K\subseteq B(R)$, $O((R/\gamma)^{(d-1)/2})$ points suffice for an additive $\gamma$-approximation of $h_K$ in all directions (Dudley 1974; Bronshteyn–Ivanov 1975; used for $\varepsilon$-kernels in Agarwal–Har-Peled–Varadarajan).
- Access level: definition confirmed, size bound not confirmed from text. I cite rather than prove it.
- *Source check (2026-11-21, pre-manuscript verification).*
  - **What the primary-level source states.** Bronshtein's survey, read in full (Russian original, §4.1, inequality (6)): for every convex body $U\subset\mathbb R^d$, the Hausdorff distance from $U$ to the polytopes with at most $n$ vertices is $\le c(U)\,n^{-2/(d-1)}$. The same holds for polytopes *inscribed* in $U$. It attributes this to Bronshteyn–Ivanov 1975 and Dudley 1974, proved independently.
  - **What it leaves out.** In that passage the constant $c(U)$ depends on $U$; the survey does not state it as $C_d\operatorname{diam}U$. The uniform form, at most $(\operatorname{diam}K/\varepsilon)^{(d-1)/2}$ vertices for every convex body (arXiv:2512.02379, Thm. 4.1), remains secondary (**A**).
  - **Two gaps between the classical statement and the use here, both closed below.**
    1. *Vertices.* An inscribed polytope $Q\subseteq\operatorname{conv}K$ with Hausdorff distance $\le\gamma$ has $h_Q\ge h_K-\gamma$, but its vertices lie in $\operatorname{conv}K$, not in $K$. Write each vertex as a convex combination of at most $d+1$ points of $K$ (Carathéodory). The resulting $F\subseteq K$ has $\operatorname{conv}F\supseteq Q$, so $h_F\ge h_K-\gamma$, with $\lvert F\rvert\le(d+1)n$.
    2. *Empty interior.* If $\operatorname{conv}K$ has empty interior, apply the bound to the body $U=\operatorname{conv}K+\tfrac\gamma2B\subseteq B(R+\tfrac\gamma2)$ at accuracy $\tfrac\gamma2$: since $h_U=h_K+\tfrac\gamma2$, the inscribed $Q$ has $h_Q\ge h_K$. Replace each vertex by its nearest point of $\operatorname{conv}K$, at distance $\le\tfrac\gamma2$, which costs at most $\tfrac\gamma2$ in every support value. Then apply step 1. (A2(b) already gives the intrinsic-dimension version.)
  - **Consequence.** Since $h_F\ge h_K-\gamma$ is exactly the coreset condition of A0, for each fixed compact $K$, $\sigma_\gamma(K)=O(\gamma^{-(d-1)/2})$ follows from the survey's statement. The uniform $O((R/\gamma)^{(d-1)/2})$ over all $K\subseteq B(R)$ rests on the uniform constant, which is cited. Only this remark uses either; A2 proves its own bounds.
- With (c), **the exponent $(d-1)/2$ is exactly right.** The approximate witness number of a round body grows like $(R/\gamma)^{(d-1)/2}$ and is infinite at $\gamma=0$. That is the unavoidable deterioration near zero margin.

> **Theorem A2′ (robust Lemma W).** Let $K$ be a far trap of the linear model with compact parameter space, $F$ a set realizing $\sigma_\gamma$, and $\{p,q\}\subseteq K$ a far pair. Then $F'=F\cup\{p,q\}$ is a far trap of the **$\gamma$-tightened** model, in which $u$ counts as safe for a set $L$ iff $h_L(a_u)\le b_u-\gamma$.

*Proof.*
- **Note on the definition.** This proof uses $\sigma_\gamma$ in the form "$h_K(a)>b\Rightarrow h_F(a)>b-\gamma$". That is the defining condition applied to the shifted threshold $b-\gamma$. For the maximizer construction of A2 both forms hold.
- Let $u$ be tightened-safe for $F'$, so $h_{F'}(a_u)\le b_u-\gamma$.
- Then $h_F(a_u)\le b_u-\gamma$, so the defining property gives $h_K(a_u)\le b_u$, i.e. $u\in\mathcal S(K)$.
- Hence $w_K(c_u)\le2\delta_u$, and $w_{F'}(c_u)\le w_K(c_u)$. ∎

**Reading.**
- In the finite theory, exact witnesses ($\sigma$) give *exact* small traps.
- In the continuum, exact witnesses may not exist. Approximate witnesses give small traps of a *slightly more conservative* model. The finite search needed to detect a trap then has size $\sigma_\gamma+2=O((R/\gamma)^{(d-1)/2})$, independent of $\lvert\Theta_0\rvert$.
- **This is how $\sigma_\gamma$ functions as a complexity parameter.** It bounds the size of trap certificates for continuum problems, at the price of a safety margin $\gamma$.

## 2. Perturbation statements: the brief's Candidates A and B

**Setting.**
- $K$ compact, with safety $g(\cdot,u)$ uniformly $L_g$-Lipschitz in $\theta$, and scalar observations $h(\cdot,u)$ uniformly $L_h$-Lipschitz, with interval noise $\delta_u$.
- $F\subseteq K$ is an *$h$-net*: every $\theta\in K$ has some $\theta'\in F$ with $\lVert\theta-\theta'\rVert\le h$.
- $w_L(u)=\max_Lh(\cdot,u)-\min_Lh(\cdot,u)$.

**The elementary bounds.**
- $\max_Kg(\cdot,u)\le\max_Fg(\cdot,u)+L_gh$.
  - This is the correct reading of the brief's garbled inequality. In particular, $\max_Fg\le-L_gh$ implies $\max_Kg\le0$.
- $0\le w_K(u)-w_F(u)\le2L_hh$, since the maximum rises and the minimum falls by at most $L_hh$ each.

> **Proposition CandA.** If $K$ is a trap of the original model, then $F$ is a trap of the model with safety tightened to $g(\theta,u)\le-L_gh$, and observations unchanged.

*Proof.*
- If $\max_Fg(\cdot,u)\le-L_gh$, then $\max_Kg\le0$, so $u\in\mathcal S(K)$.
- Hence $w_K(u)\le2\delta_u$, and $w_F\le w_K$. ∎

> **Proposition CandB.** If $F$ is a trap of the original model, then $K$ is a trap of the model with noise $\delta'_u=\delta_u+L_hh$, and safety unchanged.

*Proof.*
- If $u\in\mathcal S(K)$, then $u\in\mathcal S(F)$ since $F\subseteq K$, so $w_F(u)\le2\delta_u$.
- Then $w_K(u)\le w_F(u)+2L_hh\le2\delta'_u$. ∎

**Which model changes.** Candidate A perturbs **safety**: a stricter certification standard for the sample. Candidate B perturbs **observations**: worse sensors for the whole set. Neither changes both.

*Check:* exact, using $L^\infty$ nets and $L^1$ Lipschitz constants $\lVert a\rVert_1$, $\lVert c\rVert_1$, on 33,056 (set, subnet) pairs of random planar instances (E005 §K).

**Caveat.** Both statements assume $F\subseteq K$. Nets of the *initial* space $\Theta_0$ do not, in general, lie inside a given uncertainty set $K$. §3 handles that.

## 3. Certified discretization of the identification problem

Let $\Theta_0$ be compact and $N_h\subseteq\Theta_0$ a finite $h$-net of $\Theta_0$. Consider two finite instances on $N_h$:
- the **upper instance** $\mathcal I^+_h$: safety tightened to $g\le-L_gh$, noise enlarged to $\delta+L_hh$;
- the **lower instance** $\mathcal I^-_h$: safety relaxed to $g\le L_gh$, noise shrunk to $\delta-L_hh$, assuming $\delta>L_hh$.

> **Theorem A3 (soundness).**
> - (a) If $\mathcal I^+_h$ has no trap of diameter $\ge\varepsilon-2h$, then $\Theta_0$ has no closed trap of diameter $\ge\varepsilon$. Under the hypotheses of K1, $\Theta_0$ is then uniformly identifiable to accuracy $<\varepsilon$.
> - (b) If $\mathcal I^-_h$ has a trap $F$ with $\operatorname{diam}F>\varepsilon$, then $\hat F=\{\theta\in\Theta_0 : \operatorname{dist}(\theta,F)\le h\}$ is a closed trap of $\Theta_0$ with diameter $>\varepsilon$, so $\Theta_0$ is not $\varepsilon$-identifiable by any policy.

*Proof.*
- **(a)** Let $K$ be a closed trap with $\operatorname{diam}K\ge\varepsilon$, and set $F=\{q\in N_h : \operatorname{dist}(q,K)\le h\}$.
  - **Density.** Every $\theta\in K$ has a net point within $h$, and that point lies in $F$. So $F$ is $h$-dense in $K$, and every point of $F$ is within $h$ of $K$.
  - **Safety.** If $u$ is safe for $F$ in $\mathcal I^+_h$, then $\max_Kg\le\max_Fg+L_gh\le0$, so $u\in\mathcal S(K)$.
  - **Blindness.** $w_K(u)\le2\delta$, so $w_F(u)\le w_K(u)+2L_hh\le2(\delta+L_hh)$. Hence $F$ is a trap of $\mathcal I^+_h$.
  - **Diameter.** $\operatorname{diam}F\ge\operatorname{diam}K-2h\ge\varepsilon-2h$. This contradicts the hypothesis.
- **(b)** $\hat F$ is closed and contains $F$, so $\operatorname{diam}\hat F>\varepsilon$.
  - **Safety.** If $u\in\mathcal S(\hat F)$, then $\max_Fg\le0\le L_gh$, so $u$ is safe for $F$ in $\mathcal I^-_h$.
  - **Blindness.** So $w_F(u)\le2(\delta-L_hh)$. Every point of $\hat F$ is within $h$ of $F$, so $w_{\hat F}(u)\le w_F(u)+2L_hh\le2\delta$. ∎

Both certificates are finite trap-existence questions, decidable by the finite theory. With linear models they are covered by the algorithms of `research/linear_identifiability.md`.

> **Theorem A4 (completeness).** Assume the hypotheses of K1, with $h(\theta,u)$ jointly continuous and Lipschitz in $\theta$.
> - (a) Suppose strictly safe experiments are dense in $\mathcal S(K)$ for every closed $K$ (Lemma 0), and $D^\*<\varepsilon$. Then for all sufficiently small $h$, $\mathcal I^+_h$ has no trap of diameter $\ge\varepsilon-2h$. So the upper certificate succeeds.
> - (b) Suppose some closed trap $K$ with $\operatorname{diam}K>\varepsilon+2h_0$ is **margin-robust**: there is $\mu>0$ such that every experiment either has $\max_Kg(\cdot,u)\ge\mu$ or has $w_K(u)\le2\delta-\mu$. Then for all sufficiently small $h$, $\mathcal I^-_h$ has a trap of diameter $>\varepsilon$. So the lower certificate succeeds.

*Proof.*
- **(a)** Otherwise there are $h_n\to0$ and traps $F_n$ of $\mathcal I^+_{h_n}$ with $\operatorname{diam}F_n\ge\varepsilon-2h_n$. Pass to a Hausdorff limit $F_n\to F$; $F$ is closed and $\operatorname{diam}F\ge\varepsilon$.
  - Let $u\in\mathcal S(F)$ be strictly safe, $G(F,u)<0$. Then $G(F_n,u)\to G(F,u)$, so eventually $G(F_n,u)\le-L_gh_n$. So $u$ is upper-safe for $F_n$.
  - Hence $w_{F_n}(u)\le2\delta+2L_hh_n$, and in the limit $w_F(u)\le2\delta$.
  - Density and continuity of $w_F(\cdot)$ in $u$ extend this to every $u\in\mathcal S(F)$. So $F$ is a closed trap of diameter $\ge\varepsilon>D^\*$, a contradiction.
- **(b)** Let $F=\{q\in N_h : \operatorname{dist}(q,K)\le h\}$, as in A3(a), so $\operatorname{diam}F\ge\operatorname{diam}K-2h>\varepsilon$ once $h<h_0$. Let $u$ be lower-safe for $F$, i.e. $\max_Fg\le L_gh$. Then $\max_Kg\le\max_Fg+L_gh\le2L_gh<\mu$ once $h$ is small.
  - So, by margin-robustness, $w_K(u)\le2\delta-\mu$.
  - Then $w_F(u)\le w_K(u)+2L_hh\le2\delta-\mu+2L_hh\le2(\delta-L_hh)$ once $4L_hh\le\mu$.
  - Hence $F$ is a trap of $\mathcal I^-_h$. ∎

**Example X5 (where certification fails).**
- **Tangential safety blocks the upper certificate.** Take $\Theta_0=[0,\tfrac12]$ with the single sharp experiment of X1, $g=\theta-\tfrac12+\lvert u\rvert$ and $h=10\theta$.
  - The agent identifies in one step, since $u=0$ is exactly safe.
  - But every net contains $\tfrac12$, and tightening makes $u=0$ unsafe for it. So $N_h$ itself is a trap of $\mathcal I^+_h$ of diameter $\tfrac12$, for every $h$. The upper certificate never succeeds, although the problem is identifiable.
  - Density fails here, as it must by A4(a).
- **Zero-margin traps block the lower certificate.** In X2, the maximal trap $[0,\tfrac12]$ is blind with zero margin: the probe $s=0$ has width exactly $2\delta$. Margin-robustness fails, and the lower instance shrinks the noise, which makes the probe informative on the net. So the lower certificate cannot certify the true value $D^\*=\tfrac12$ by this route, although it does certify slightly smaller values whenever robust sub-traps exist.

**Reading.** A3–A4 turn K1–K2 into a **semi-decision procedure with a clean failure set**.
- Refine $h$ until either certificate succeeds.
- Success is guaranteed except at instances that are boundary cases in exactly the senses of Stage 1: tangential safety, or zero-margin traps.
- The finite instances can be large. The approximate witness bounds of §1 say that the trap searches need only subsets of size $O((R/\gamma)^{(d-1)/2})$ in the linear case, with $\gamma=L_gh$.
- Note that the uncertainty sets reachable in the finite instance are subsets of $N_h$, not discretizations of reachable continuum sets. The certificates are statements about traps, via T1/K1, not about simulating the continuum game.
