# Stage 0 — Literature and novelty audit

*2026-11-20. This review is focused, not exhaustive. Every entry records how much of the source was actually read. A theorem is quoted only when its text was read. Where only an abstract or index page was seen, the entry says so and gives no theorem-level claims.*

**Access levels:**
- **F**: full text, or the relevant sections, read;
- **P**: partial (named sections);
- **A**: abstract or index page only;
- **M**: bibliographic metadata only;
- **X**: not obtained.

## 1. Sources examined

### 1.1 Safe exploration with a known safe seed (closest to "progressive expansion")

**Y. Sui, A. Gotovos, J. Burdick, A. Krause. *Safe Exploration for Optimization with Gaussian Processes.* ICML 2015, PMLR 37:997–1005.** <https://proceedings.mlr.press/v37/sui15.html> — **P** (text extracted locally from the proceedings PDF; the setup, the reachability operator and Theorem 1 were read).
- **Model.**
  - Unknown $f$ on a decision set $D$, with $\|f\|_k \le B$ in an RKHS and $L$-Lipschitz.
  - Noisy evaluations; safety means $f(x) \ge h$.
  - A nonempty seed $S_0$ with $f \ge h$ on $S_0$ is **assumed**.
- **Key object (verbatim, symbols restored).** The reachability operator is
  $$R_\epsilon(S) := S \cup \{x \in D \mid \exists x' \in S,\ f(x') - \epsilon - L\,d(x', x) \ge h\},$$
  with iterates $R^n_\epsilon$ and closure $\bar R_\epsilon(S) = \lim_n R^n_\epsilon(S)$. The paper states: "no algorithm that is able to learn $f$ only up to $\epsilon$ will ever be able to establish a decision $x \in D \setminus \bar R_\epsilon(S_0)$ as safe."
- **Theorem 1.** With high probability SafeOpt is safe at every round, and after $t^\*$ rounds it finds an $\epsilon$-optimal point of $\bar R_\epsilon(S_0)$.
- **Relation to us.**
  - $\bar R_\epsilon(S_0)$ is a fixed point of certified-safe expansion: exactly the "progressive expansion stops" phenomenon of Direction A.
  - Differences: Lipschitz propagation with a *given* seed, and probabilistic, approximate safety. There the information obtained from an experiment is a point evaluation, not tied to the risk of the experiment.
  - Our scalar model couples risk and information through the same intensity $x$. That is what produces thresholds in $(\delta, p, U_0)$.
- **Status.** The "unreachable safe region" idea is **previously established** in this form. Our deadlock phenomena must be positioned against it.

**M. Turchetta, F. Berkenkamp, A. Krause. *Safe Exploration in Finite Markov Decision Processes with Gaussian Processes.* NeurIPS (NIPS) 2016; arXiv:1606.04753.** — **A**. Extends safe exploration to MDPs with reachability and returnability constraints, and explores "the safely reachable part of the MDP". *Relation:* the dynamics/reachability analogue (Direction D). Not read beyond the abstract.

**F. Berkenkamp, M. Turchetta, A. Schoellig, A. Krause. *Safe Model-based Reinforcement Learning with Stability Guarantees.* NeurIPS 2017; arXiv:1705.08551.** — **A**. The safe set is an estimated region of attraction, which must never shrink, and is expanded through exploration. *Relation:* Direction D; safe-set expansion in a dynamical system.

### 1.2 Safe bandits: the role of a known safe action and slack

**S. Amani, M. Alizadeh, C. Thrampoulidis. *Linear Stochastic Bandits Under Safety Constraints.* NeurIPS 2019; arXiv:1908.05814.** — **P** (HTML v1 through §3.4, including Theorems 1–3).
- **Model.**
  - Loss $\mu^\top x + \eta$; safety $\mu^\top B x \le c$, with $B, c$ known and $\mu$ unknown.
  - $D_0$ is a convex body containing 0 in its interior, so 0 is safe (Assumption 3).
  - Sub-Gaussian noise.
- **Results.**
  - Theorem 2: $\tilde O(\sqrt T)$ regret when the safety gap $\Delta = c - \mu^\top B x^\* > 0$ is known. The exploration length $T_\Delta$ has $\Delta^2$ in the denominator.
  - Theorem 3: $\tilde O(T^{2/3})$ when $\Delta = 0$ or $\Delta$ is unknown.
  - No safe-setting lower bound in the sections read.
- **Relation.**
  - Their safety constraint is linear in the *same* unknown parameter that is observed. That is our Direction C model with $g = \theta^\top B u - c$.
  - Deadlock is excluded by design: there is an interior safe action and the noise is sub-Gaussian, so repetition averages the noise away.
  - With **bounded worst-case** noise, repetition does not help. The deadlock analysis of `research/scalar_analysis.md` shows exactly what is lost.

**A. Gangrade, T. Chen, V. Saligrama. *Safe Linear Bandits over Unknown Polytopes.* COLT 2024 (arXiv:2209.13694 v3).** — **P** (abstract, §§1–3.2 verbatim; later sections only via an automated summary, not used).
- **Model.** Unknown polytope constraints, with no known safe point. Safety is measured as cumulative violation, not as a hard per-round constraint.
- **Claims read.** Pessimistic–optimistic methods "usually assume a priori knowledge of a point $x^s$ in the interior of $S$ ... with positive safety margin". The authors state a "precision barrier" lower bound: $\Omega(\sqrt T)$ regret or safety violation for any algorithm on some instance.
- **Relation.** This is the soft-constraint regime (Direction E). It supports the view that hard safety without a safe margin is genuinely different. The lower-bound text itself (§5 and later) was not read, so no theorem is quoted.

### 1.3 Safe exploration hardness

**T. M. Moldovan, P. Abbeel. *Safe Exploration in Markov Decision Processes.* ICML 2012; arXiv:1205.4810.** — **P** (§§1–4 verbatim via ar5iv; the proof of Theorem 1 not read).
- **Model.**
  - Bayesian: a belief $\beta$ over MDPs.
  - $\delta$-safety means the agent can return to a home state $s_0$ with probability $\ge \delta$ under the belief.
- **Theorem 1 (verbatim).** "In general, it is NP-hard to decide whether there exist δ-safe policies with respect to a home state, s0, and a stopping time, T, for some belief, β."
- **Relation to our F4.** Both say that safety makes a decision problem hard. Theirs concerns the *existence of safe policies* under a probabilistic belief over dynamics. Ours concerns *worst-case identifiability* under robust safety without dynamics, and gives coNP-**completeness** with a contrasting polynomial unconstrained case.
- **Status of F4.** Related, not the same statement. **F4 must cite this.**

### 1.4 Set-membership identification and information-based complexity

**M. Milanese, A. Vicino. *Optimal estimation theory for dynamic systems with set membership uncertainty: an overview.* Automatica 27(6):997–1009, 1991. DOI 10.1016/0005-1098(91)90134-N.** — **A**. The unknown-but-bounded framework: the feasible parameter set and worst-case optimal estimation. *Relation:* our $\Theta_t$ is their feasible parameter set. Our notions of diameter and irreducible uncertainty are their worst-case estimation errors. **Use their vocabulary.**

**E. Novak. *On the power of adaption.* J. Complexity 12:199–237, 1996. DOI 10.1006/jcom.1996.0015.** — **A** (the author's page and search summaries). It surveys when adaptive information beats non-adaptive information. In the worst case, for linear problems over convex symmetric sets, adaption gains at most a factor of 2 (Traub–Wasilkowski–Woźniakowski; not read).
- **Relation.** In our setting the *admissible* information operators depend on the current uncertainty, through $\mathcal S(\Theta_t)$. The classical "adaption does not help" results assume a fixed admissible class.
- **Observation (ours).** In the scalar model the uniform worst case is achieved by the non-adaptive policy $x \equiv 1/U_0$ (S5): adaption does not help *uniformly*, but it does help instance-wise. Whether there is a uniform adaptivity gap in other safe-identification models is a clean question (register Q-C3).

**Not obtained (X), to check:**
- Schweppe 1968 (IEEE TAC; unknown-but-bounded state estimation);
- Walter & Piet-Lahanier 1990 (survey);
- the input-design literature for set-membership identification;
- Traub, Wasilkowski & Woźniakowski, *Information-Based Complexity* (book; radius of information).

### 1.5 Learning that stops because actions are uninformative (economics)

**D. Fudenberg, D. K. Levine. *Self-Confirming Equilibrium.* Econometrica 61(3):523–545, 1993. DOI 10.2307/2951716.** — **A**. Beliefs are correct on the equilibrium path but possibly wrong off it, because unreached information sets are never observed.
- *Relation:* the "self-confirming uncertainty" of the brief. The mechanism there is equilibrium play rather than a safety constraint, but the logical structure is the same: the actions taken never generate disconfirming data. A trap is the set-valued, worst-case analogue.

**D. Easley, N. M. Kiefer. *Controlling a Stochastic Process with Unknown Parameters.* Econometrica 56(5):1045–1064, 1988. JSTOR 1911358.** — **A**.
- Beliefs converge, but not necessarily to the truth. "Incomplete learning" can be optimal.
- *Relation:* the closest conceptual precedent for "learning stops short of the truth". The cause is the cost of experimentation (discounting), not a hard safety constraint.

**N. M. Kiefer, Y. Nyarko. *Optimal Control of an Unknown Linear Process with Learning.* International Economic Review 30(3):571–, 1989. DOI 10.2307/2526776.** — **M**. Associated with the notion of *confounding* actions, which reveal nothing at a limit belief. That association is not verified from the text.

**M. Rothschild. *A two-armed bandit theory of market pricing.* J. Economic Theory 9(2):185–202, 1974. DOI 10.1016/0022-0531(74)90066-0.** — **M**. Incomplete learning in bandits; not read.

### 1.6 Diagnosability (discrete-event systems)

**A. Paoli, S. Lafortune. *Safe diagnosability for fault-tolerant supervision of discrete-event systems.* Automatica 41(8):1335–1347, 2005. DOI 10.1016/j.automatica.2005.03.017.** — **A**. A fault must be detected before forbidden behaviour occurs. The paper gives necessary and sufficient conditions, and solves an "active safe diagnosis" controller-design problem.
- *Relation:* "safety constrains which observations can be generated" in a discrete-event setting.
- **This line, together with active diagnosis, is the most likely place where F1/F4-type statements already exist under other names.** Unresolved until read.

**M. Sampath, S. Lafortune, D. Teneketzis. *Active diagnosis of discrete-event systems.* IEEE TAC 43(7):908–929, 1998.** — **M**. Diagnosis by choosing the control. The complexity of active diagnosis in later work (e.g. Haar, Haddad and coauthors) was seen only as search hits — **X**.

### 1.7 Games of imperfect information

**J. H. Reif. *The complexity of two-player games of incomplete information.* JCSS 29(2):274–301, 1984. DOI 10.1016/0022-0000(84)90034-5.** — **A**. Knowledge-state constructions and complexity of imperfect-information games, which in general carry an exponential blow-up.
- *Relation:* our game is a reachability game on the knowledge-state lattice with monotone states. F1 is the standard attractor characterisation specialised to it.
- **F1 is not claimed as a contribution beyond its formulation.**

Not obtained (X): Chatterjee, Doyen, Henzinger & Raskin, *Algorithms for ω-regular games with imperfect information* (LMCS 2007).

### 1.8 Sequential design and hypothesis testing

**H. Chernoff. *Sequential design of experiments.* Ann. Math. Stat. 30(3):755–770, 1959. DOI 10.1214/aoms/1177706205.** — **M**.

**M. Naghshvar, T. Javidi. *Active sequential hypothesis testing.* Ann. Statist. 41(6):2703–2738, 2013. DOI 10.1214/13-AOS1144.** — **M**.

*Relation:* the stochastic, unconstrained version of choosing informative experiments. No safety constraint coupling the action set to the hypothesis.

### 1.8a Test cover

*Test cover / minimum test collection* — **A** (secondary sources only). Finding a *minimum* set of tests that separates all pairs is NP-hard (Garey & Johnson; de Bontridder et al., Math. Program. 98, 2003, inapproximability within $o(\log n)$).
- *Relation:* F3 shows that *feasibility* (does any separating strategy exist?) is polynomial without safety. F4 shows feasibility becomes coNP-complete with robust safety. This is a different axis from test-cover *minimality*. A minimum-experiments version of our problem inherits the test-cover hardness (Q-F4).

### 1.8b Leads from the generic searches (seen only as search summaries — **A** at best; authors unverified unless stated)

- **Experiment design for set-membership identification: from prior knowledge to universal inputs.** arXiv:2607.00844 (2026).
  - Per the search summary: safety-constrained experiment design "is left as future work". One prior-knowledge set does not enable universal experiment design.
  - **The closest current work in set-membership identification. Read in full before Stage 1.** If the summary is accurate, the safety-constrained version is open in that community.
- **S. Haar, S. Haddad, T. Melliti, S. Schwoon. *Optimal constructions for active diagnosis.* FSTTCS 2013 (LIPIcs, DOI 10.4230/LIPIcs.FSTTCS.2013.527); extended in JCSS 2017.**
  - Per the summaries: active diagnosability is **EXPTIME-complete**, with optimal-memory diagnoser synthesis. Active predictability is also EXPTIME-complete (FSTTCS 2020).
  - *Relation to F4:* these are dynamical (automaton) models with partial observation. Our static model sits lower, at coNP. The difference — static, worst-case, with safety the only source of coupling — must be made explicit. F4 could plausibly be derived as a special case of their hardness proofs, or be folklore there. **Unresolved.**
- ***Safe exploration for identifying linear systems via robust optimization.*** arXiv:1711.11165. Per the summary: a nominal safe action is assumed, and the paper notes that a one-step safe action can lead to states with no safe successors. Relevant to Direction D.
- ***Active learning with safety constraints.*** arXiv:2206.11183. Per the summary: safe best-arm identification interpolates between best-arm identification and level-set estimation. Stochastic, with a known safe set assumed (unverified).
- ***Identifiability and generalizability in constrained inverse reinforcement learning.*** arXiv:2306.00629. Per the summary: identifiability is lost under active inequality constraints. A different problem (IRL), with an analogous phenomenon.

### 1.9 Surveys

**L. Brunke, M. Greeff, A. W. Hall, Z. Yuan, S. Zhou, J. Panerati, A. P. Schoellig. *Safe Learning in Robotics: From Learning-Based Control to Safe Reinforcement Learning.* Annu. Rev. Control Robot. Auton. Syst. 5:411–444, 2022. DOI 10.1146/annurev-control-042920-020211.** — **M** (arXiv:2108.06266 not read). Use it to map the safe-RL landscape before Stage 1.

## 2. Comparison table

| Our item | Closest source | Assessment |
|---|---|---|
| Robust-safe action set $\mathcal S(\Theta_t)$, consistent sets | set-membership identification (Milanese–Vicino); pessimistic safe sets in safe bandits (Amani et al.) | **Previously established** as objects. |
| Expansion stopping at a fixed point | SafeOpt's $\bar R_\epsilon(S_0)$ | **Previously established** (Lipschitz/GP version). |
| Scalar thresholds ($\lambda_c$, $U_{\rm dead}$, one-shot trap) | none found | **Elementary.** Useful as a worked example. Not a headline contribution by itself. |
| Max-intensity domination (S2) | none found | **Elementary** coupling argument. Probably known in spirit. Not claimed. |
| F1 trap characterisation | attractor arguments in reachability games; Reif-style knowledge sets | **Follows from standard results.** The specific formulation is unresolved. Diagnosability literature unread. |
| Non-locality (pairwise-identifiable but globally deadlocked) | none found | **Potentially distinct.** Simple. Check DES diagnosability. |
| F4: coNP-completeness under robust safety; polynomial without it | Moldovan–Abbeel (Bayesian MDP, NP-hard existence of safe policies); active diagnosability, EXPTIME-complete (Haar et al.); test cover (minimality) | **Potentially distinct** as a sharp static statement; plausibly a special case of known techniques. **Unresolved** until Haar et al. are read. |
| Self-confirming / incomplete learning | Fudenberg–Levine; Easley–Kiefer | The conceptual precedent for the whole project. **The paper must frame against these.** |

## 3. Terminology recommendation

- Use **feasible parameter set** (set-membership) for $\Theta_t$.
- Use **certified-safe set** for $\mathcal S(\Theta_t)$.
- Reserve **trap** or **self-confirming set** for the deadlock object; the second echoes Fudenberg–Levine, so the parallel must be explicit or the name avoided.
- Avoid "informational deadlock" as a technical term until it has a theorem attached. **Irreducible uncertainty** conflicts with nothing, but compare "identified set" in partial identification (Manski; **X**, not checked).

## 4. Not yet examined (required before any novelty claim)

1. **Active diagnosis complexity** (Haar, Haddad, Melliti, Schwoon et al.) and safe diagnosability conditions in full (Paoli–Lafortune). This is the most likely home of F1/F4-type results.
2. **Set-membership input design** under constraints; persistence of excitation under input constraints (Åström–Wittenmark; adaptive-control texts).
3. **Dual control** (Feldbaum 1960s) and robust adaptive control (Ioannou–Sun).
4. **Viability theory** (Aubin 1991) and HJ reachability (Mitchell–Bayen–Tomlin 2005), for Direction D.
5. **Other safe-bandit work** — Khezeli & Bitar 2020; Moradipari et al.; Pacchiano et al. 2021 — specifically any **impossibility** result without a safe seed.
6. **Partial identification** (Manski); identified sets.
7. **Rényi–Ulam search with lies** (Pelc 2002 survey): adversarial bounded-error search; relevant to the finite model with $\delta > 0$.
8. **Imperfect-information game algorithms** (Chatterjee–Doyen–Henzinger–Raskin 2007).

## 5. Search log

- Web searches, 2026-11-20, one query per source, on titles and author names above.
- Generic queries run (the search tool was rate-limited for much of the session):
  - safe identifiability + set membership + experiment design;
  - active-diagnosis complexity;
  - safe-exploration impossibility without a known safe action.
  The leads are in §1.8b.
- Not yet run: "informational deadlock", "learning under endogenous constraints", "self-confirming uncertainty safety", "Rényi–Ulam with forbidden queries", "robust input design with state constraints". **Generic coverage is the most important remaining gap.**
- Crossref was rate-limited (HTTP 429). Metadata for Fudenberg–Levine and Easley–Kiefer comes from the Econometric Society and RePEc pages as returned by search.
- PDFs from proceedings and arXiv were returned as raw bytes. SafeOpt was read by local text extraction. The other arXiv papers were read through their HTML renderings.
