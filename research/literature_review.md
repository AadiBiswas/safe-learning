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
- **Relation to this project.**
  - $\bar R_\epsilon(S_0)$ is a fixed point of certified-safe expansion: exactly the "progressive expansion stops" phenomenon of Direction A.
  - Differences: Lipschitz propagation with a *given* seed, and probabilistic, approximate safety. There the information obtained from an experiment is a point evaluation, not tied to the risk of the experiment.
  - The scalar model here couples risk and information through the same intensity $x$. That is what produces thresholds in $(\delta, p, U_0)$.
- **Status.** The "unreachable safe region" idea is **previously established** in this form. The deadlock phenomena studied here must be positioned against it.

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
  - Their safety constraint is linear in the *same* unknown parameter that is observed. That is the Direction C model with $g = \theta^\top B u - c$.
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
- **Relation to F4.** Both say that safety makes a decision problem hard. Theirs concerns the *existence of safe policies* under a probabilistic belief over dynamics. F4 concerns *worst-case identifiability* under robust safety without dynamics, and gives coNP-**completeness** with a contrasting polynomial unconstrained case.
- **Status of F4.** Related, not the same statement. **F4 must cite this.**

### 1.4 Set-membership identification and information-based complexity

**M. Milanese, A. Vicino. *Optimal estimation theory for dynamic systems with set membership uncertainty: an overview.* Automatica 27(6):997–1009, 1991. DOI 10.1016/0005-1098(91)90134-N.** — **A**. The unknown-but-bounded framework: the feasible parameter set and worst-case optimal estimation. *Relation:* $\Theta_t$ here is their feasible parameter set. The diameter and irreducible-uncertainty notions used here are their worst-case estimation errors. **Use their vocabulary.**

**E. Novak. *On the power of adaption.* J. Complexity 12:199–237, 1996. DOI 10.1006/jcom.1996.0015.** — **A** (the author's page and search summaries). It surveys when adaptive information beats non-adaptive information. In the worst case, for linear problems over convex symmetric sets, adaption gains at most a factor of 2 (Traub–Wasilkowski–Woźniakowski; not read).
- **Relation.** In this setting the *admissible* information operators depend on the current uncertainty, through $\mathcal S(\Theta_t)$. The classical "adaption does not help" results assume a fixed admissible class.
- **Observation (mine).** In the scalar model the uniform worst case is achieved by the non-adaptive policy $x \equiv 1/U_0$ (S5): adaption does not help *uniformly*, but it does help instance-wise. Whether there is a uniform adaptivity gap in other safe-identification models is a clean question (register Q-C3).

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
- *Relation:* the identification game is a reachability game on the knowledge-state lattice with monotone states. F1 is the standard attractor characterisation specialised to it.
- **F1 is not claimed as a contribution beyond its formulation.**

Not obtained (X): Chatterjee, Doyen, Henzinger & Raskin, *Algorithms for ω-regular games with imperfect information* (LMCS 2007).

### 1.8 Sequential design and hypothesis testing

**H. Chernoff. *Sequential design of experiments.* Ann. Math. Stat. 30(3):755–770, 1959. DOI 10.1214/aoms/1177706205.** — **M**.

**M. Naghshvar, T. Javidi. *Active sequential hypothesis testing.* Ann. Statist. 41(6):2703–2738, 2013. DOI 10.1214/13-AOS1144.** — **M**.

*Relation:* the stochastic, unconstrained version of choosing informative experiments. No safety constraint coupling the action set to the hypothesis.

### 1.8a Test cover

*Test cover / minimum test collection* — **A** (secondary sources only). Finding a *minimum* set of tests that separates all pairs is NP-hard (Garey & Johnson; de Bontridder et al., Math. Program. 98, 2003, inapproximability within $o(\log n)$).
- *Relation:* F3 shows that *feasibility* (does any separating strategy exist?) is polynomial without safety. F4 shows feasibility becomes coNP-complete with robust safety. This is a different axis from test-cover *minimality*. A minimum-experiments version of the safe problem inherits the test-cover hardness (Q-F4).

### 1.8b Leads from the generic searches (seen only as search summaries — **A** at best; authors unverified unless stated)

- **Experiment design for set-membership identification: from prior knowledge to universal inputs.** arXiv:2607.00844 (2026).
  - Per the search summary: safety-constrained experiment design "is left as future work". One prior-knowledge set does not enable universal experiment design.
  - **The closest current work in set-membership identification. Read in full before Stage 1.** If the summary is accurate, the safety-constrained version is open in that community.
- **S. Haar, S. Haddad, T. Melliti, S. Schwoon. *Optimal constructions for active diagnosis.* FSTTCS 2013 (LIPIcs, DOI 10.4230/LIPIcs.FSTTCS.2013.527); extended in JCSS 2017.**
  - Per the summaries: active diagnosability is **EXPTIME-complete**, with optimal-memory diagnoser synthesis. Active predictability is also EXPTIME-complete (FSTTCS 2020).
  - *Relation to F4:* these are dynamical (automaton) models with partial observation. The static model here sits lower, at coNP. The difference — static, worst-case, with safety the only source of coupling — must be made explicit. F4 could plausibly be derived as a special case of their hardness proofs, or be folklore there. **Unresolved.**
- ***Safe exploration for identifying linear systems via robust optimization.*** arXiv:1711.11165. Per the summary: a nominal safe action is assumed, and the paper notes that a one-step safe action can lead to states with no safe successors. Relevant to Direction D.
- ***Active learning with safety constraints.*** arXiv:2206.11183. Per the summary: safe best-arm identification interpolates between best-arm identification and level-set estimation. Stochastic, with a known safe set assumed (unverified).
- ***Identifiability and generalizability in constrained inverse reinforcement learning.*** arXiv:2306.00629. Per the summary: identifiability is lost under active inequality constraints. A different problem (IRL), with an analogous phenomenon.

### 1.9 Surveys

**L. Brunke, M. Greeff, A. W. Hall, Z. Yuan, S. Zhou, J. Panerati, A. P. Schoellig. *Safe Learning in Robotics: From Learning-Based Control to Safe Reinforcement Learning.* Annu. Rev. Control Robot. Auton. Syst. 5:411–444, 2022. DOI 10.1146/annurev-control-042920-020211.** — **M** (arXiv:2108.06266 not read). Use it to map the safe-RL landscape before Stage 1.

## 2. Comparison table

| Item | Closest source | Assessment |
|---|---|---|
| Robust-safe action set $\mathcal S(\Theta_t)$, consistent sets | set-membership identification (Milanese–Vicino); pessimistic safe sets in safe bandits (Amani et al.) | **Previously established** as objects. |
| Expansion stopping at a fixed point | SafeOpt's $\bar R_\epsilon(S_0)$ | **Previously established** (Lipschitz/GP version). |
| Scalar thresholds ($\lambda_c$, $U_{\rm dead}$, one-shot trap) | none found | **Elementary.** Useful as a worked example. Not a headline contribution by itself. |
| Max-intensity domination (S2) | none found | **Elementary** coupling argument. Probably known in spirit. Not claimed. |
| F1 trap characterisation | attractor arguments in reachability games; Reif-style knowledge sets | **Follows from standard results.** The specific formulation is unresolved. Diagnosability literature unread. |
| Non-locality (pairwise-identifiable but globally deadlocked) | none found | **Potentially distinct.** Simple. Check DES diagnosability. |
| F4: coNP-completeness under robust safety; polynomial without it | Moldovan–Abbeel (Bayesian MDP, NP-hard existence of safe policies); active diagnosability, EXPTIME-complete (Haar et al.); test cover (minimality) | *Stage 1:* not subsumed by Haar et al. or Hierons–Türker. The deterministic case is polynomial and known. See §6.4. |
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

---

## 6. Stage 1 addendum (2026-11-21): the critical gaps

In Stage 1 I closed the gaps that Stage 0 marked as decisive for originality.

**Access.**
- PDFs were read through a local text extractor, since the fetch tool returned raw bytes.
- Where the extractor failed, I say so and quote nothing.
- Theorem statements are quoted only from text I read.

### 6.1 Sources read in Stage 1

**S. Haar, S. Haddad, T. Melliti, S. Schwoon. *Optimal constructions for active diagnosis.* FSTTCS 2013, LIPIcs 24:527–539, DOI 10.4230/LIPIcs.FSTTCS.2013.527. Extended version: J. Comput. Syst. Sci. (online 2016), DOI 10.1016/j.jcss.2016.04.007.** — **P**.
- *Read:* the JCSS preprint, §§1–3: the model, the definitions of controller, pilot and active diagnoser, and Theorem 1 with its proof.
- **Model.**
  - A finite *live, convergent* LTS. The observable events are partitioned into controllable and uncontrollable ones, and there is an unobservable fault event $f$.
  - A controller is a map from observation sequences to allowed event sets that always contains the uncontrollable events.
  - An *active diagnoser* is a controller + diagnoser pair whose controlled system is live, contains no ambiguous infinite observation sequence, and flags exactly the surely-faulty observations.
- **Theorem 1 (hardness):** "The active diagnosis decision problem is EXPTIME-hard." The proof is a reduction from safety games with imperfect information. A matching EXPTIME upper bound comes from a Büchi game on a $2^{O(n)}$ deterministic automaton.
- **Comparison with the static model.**
  - (i) *What is hidden.* Their hidden object is whether a fault *event* has occurred along an evolving run. Mine is a static parameter.
  - (ii) *What restricts the controller.* Their controllability set is fixed, the same in every state; the only constraint is liveness. Mine is uncertainty-dependent admissibility, the defining feature of this project.
  - (iii) *Observations.* Theirs are projections of events. Mine are bounded worst-case noise.
- **Verdict: their results do not subsume F4/H1 or T1.**
  - Embedding my static problem in theirs would require encoding hypothesis-dependent admissibility through liveness or forbidden states. That is plausible, but it gives only an EXPTIME upper bound, which is weaker than coNP.
  - Their EXPTIME-hardness relies on dynamics, so it does not transfer down to the static case.

**R. M. Hierons, U. C. Türker. *Distinguishing Sequences for Partially Specified FSMs.* NFM 2014, LNCS 8430:62–76, DOI 10.1007/978-3-319-06200-6_5.** — **F**.
- *Read:* the author manuscript, Brunel repository, §§1–4.
- **Model.** A PSFSM $(S,X,Y,\delta,\lambda,D)$ with *deterministic* outputs; $D\subseteq S\times X$ is the domain of defined inputs.
- **Definition 4 (ADS).** A tree whose node with state set $S'$ applies an input $x$ "defined in all states in $S'$", with further restrictions on merging states.
- **Results.**
  - Abstract: "it is possible to check the existence of an ADS in polynomial time but the corresponding problem for PDSs is PSPACE-complete".
  - The ADS result is proved by reduction to a completely specified FSM and Lee–Yannakakis.
- **Comparison.**
  - "Defined in all states of the current set" *is* robust safety.
  - A static instance with deterministic observations is a PSFSM with only self-loops, so ADS existence is exactly my exact identifiability. **My P2 (deterministic observations ⇒ polynomial), at $\varepsilon=0$, is a special case of their theorem.** I record it as known.
  - Their work does not treat nondeterministic outputs, which is where H1's hardness lives.

**U. C. Türker, R. M. Hierons, K. El-Fakih, G. Barlas. *Incomplete adaptive distinguishing sequences for non-deterministic FSMs.* IEEE TSE 49(9):4371–4389, 2023.** — **A**.
- The PDF text could not be extracted, so only search summaries were seen.
- Per those summaries:
  - machines may be partial and nondeterministic, and are assumed observable;
  - checking the existence of a set of $k$ incomplete ADSs separating all pairs is PSPACE-hard.
- *Relation:* the closest class that contains my static nondeterministic model. Its lower bound presumably uses dynamics, which is unverified. **This is the single most important paper still to read for H1.**

**R. Alur, C. Courcoubetis, M. Yannakakis. *Distinguishing tests for nondeterministic and probabilistic machines.* STOC 1995, 363–372, DOI 10.1145/225058.225161.** — **A**.
- Secondary sources only. Per those sources:
  - preset distinguishing is PSPACE-complete;
  - adaptive distinguishing is EXPTIME-complete;
  - the problem is polynomial for "observable" machines.
- *Relation:* the general dynamic, nondeterministic case. The same upper-bound-only relation as above.

**A. Shakouri, H. J. van Waarde, M. K. Camlibel. *Experiment design for set-membership identification: from prior knowledge to universal inputs.* arXiv:2607.00844, July 2026.** — **P**.
- *Read:* §§I–IV-A verbatim, and parts of the appendix proofs; the remaining sections only via summaries.
- **Model.**
  - LTI system $x^+=Ax+Bu+w$ with $\lVert w\rVert\le\epsilon$. The body uses the Euclidean norm, while the abstract says $\ell_\infty$; this is unresolved.
  - The prior is a set $\Sigma_{pk}$ of $(A,B)$.
  - An input is *universal* if every dataset it can generate from any system in $\Sigma_{pk}$ is informative, i.e. the consistent set has radius $\le\rho$.
- **Results read.**
  - Theorem 7 (single input, open prior, noiseless): universal iff persistently exciting of order $n+1$.
  - From the proof of Proposition 26: noisy *exact* identification requires a "uniformly discrete" prior set.
- **Constraints.**
  - Design is **offline**: the intro contrasts "online methods" with "offline methods" and the paper takes the latter.
  - The formulation in §§II–III has **no input or state constraints**. "safety considerations" appears only as motivation.
  - A future-work sentence on trajectory constraints is reported by a summary but not verified.
- **Verdict.** Different design class (offline, unconstrained), different system class (dynamic LTI) and a different question (universality of inputs). **It does not address uncertainty-dependent admissibility.** The uniform-discreteness result parallels my noise floor $D^\*$ (K2) and S5.

### 6.2 Search summaries only (A)

- *Paoli–Lafortune, Safe diagnosability (Automatica 2005).* Per summaries: fault detection must occur before any forbidden string in the failed mode, characterized by conditions on a "safe diagnoser". This is **passive** diagnosis with a deadline. It is not about admissibility of probing actions, and so is not a competitor to T1/H1.
- *Hyafil–Rivest 1976; Laber–Nogueira 2004* (DOI 10.1016/j.dam.2004.06.002). Per summaries: minimum-depth decision trees are NP-hard and hard to approximate within $\ln$ factors. Used only for §6 of `research/complexity_analysis.md`.
- *arXiv:2608.00215 (2026).* Per summary: a parameter component is identifiable from safe actions iff it lies in the span of the safe feature vectors. **The safe set is fixed and known there,** so there is no circularity. It is the unconstrained analogue of my G4.
- *arXiv:2601.08648, "Safe Language Generation in the Limit" (2026).* Per summary: impossibility of a "safe identification in the limit" notion in language learning. Different model (Gold-style).
- *Camilleri et al., Active Learning with Safety Constraints (NeurIPS 2022, arXiv:2206.11183)* is unchanged from Stage 0: stochastic, with a known safe set.
- *Optimal decision trees with noisy outcomes* (arXiv:2312.15357): approximation algorithms, without safety.

### 6.3 Assumption-by-assumption comparison

| | This project | Active diagnosis (Haar et al.) | PSFSM ADS (Hierons–Türker) | ND distinguishing (ACY 1995; Türker et al. 2023) | Set-membership design (Shakouri et al.) | SafeOpt (Sui et al.) | Self-confirming / incomplete learning |
|---|---|---|---|---|---|---|---|
| Hidden object | static parameter | evolving run (fault occurrence) | initial state of an evolving machine | initial state | static system matrices | static function | static parameter (belief) |
| Admissible actions | **depend on the current uncertainty** (robust safety) | fixed controllable set; liveness | input must be defined in all current states (**same as mine**) | partial inputs (2023) | unconstrained | depend on certified-safe set (GP, Lipschitz) | unconstrained; cost-driven |
| Identification notion | uniform, worst-case; also instance-wise (T3) | uniform (all runs) | uniform | uniform | uniform over prior | high-probability | asymptotic belief |
| Observations | bounded worst-case, set-valued | event projection | deterministic | nondeterministic | bounded noise | stochastic (sub-Gaussian) | stochastic |
| Horizon | finite, uniform (T1, K1) | infinite runs, bounded delay | finite tree | finite tree | finite offline | finite, high-probability | infinite |
| Policy class | adaptive, history-dependent | finite-memory controllers | adaptive tree | adaptive / preset | **offline (open-loop)** | adaptive | Bayesian optimal |
| Complexity | coNP-complete (H1); P for deterministic | EXPTIME-complete | P (ADS); PSPACE-complete (PDS) | EXPTIME-complete / PSPACE-hard | — | — | — |

### 6.4 Verdicts on the Stage 0 candidate contributions

| Item | Verdict after Stage 1 |
|---|---|
| T1 (trap characterization) | **Known in technique.** It is the finite-game attractor argument, and for deterministic outputs it is a special case of PSFSM ADS existence. The general set-valued formulation is a formulation, not a theorem to claim. |
| P2 (deterministic + safety ⇒ P) | **Known** (Hierons–Türker 2014), in the self-loop special case. |
| H1 / F4 (coNP-complete; binary observations with unsafe sets of size 2 suffice; P at size 1) | **Not found in the sources read.** Not subsumed by Haar et al., Hierons–Türker or ACY: those either have deterministic outputs (P) or dynamic hardness that does not transfer. **Remaining question:** does Türker et al. 2023, or the observable-NFSM testing literature, contain a static or self-loop hardness result? |
| T3 (one myopic policy is instance-optimal) | Not found; simple enough to be folklore. Low novelty weight. |
| T5, G1′ (σ governs minimal traps; exact local-to-global) | Not found. **Potentially original.** It is the natural structural statement behind H1 and P4. |
| G2b (realizable trap families under Helly-$h$ observations) | Not found. Potentially original, but minor. |
| K1–K3 (continuum, with (L)) | Not found as such. The technique is viability-kernel style. The (L) condition and the counterexamples X1–X3 are the substance. **Potentially original as a formulation**, with standard tools. |
| Self-confirming / incomplete learning | Remains the conceptual precedent (Stage 0). Unchanged. |

### 6.5 Remaining literature questions

Precise, in priority order:
1. **Türker–Hierons–El-Fakih–Barlas 2023, full text.** Is there a hardness result for observable nondeterministic *partial* FSMs that survives restricting all transitions to self-loops? If so, H1 is a corollary. Next: chase its references on "possibilistic" or "partial nondeterministic" ADS.
2. **El-Fakih, Yevtushenko et al.** on adaptive distinguishing test cases for nondeterministic FSMs (HAL hal-01815008), with the same question.
3. **Test sequencing in fault diagnosis** (Pattipati and co-authors): are there "test applicability depends on the fault hypothesis" models with complexity results?
4. **Viability theory** (Aubin 1991): find the exact lemma behind K1's Lemma 2, to cite rather than re-prove.
5. **Alur–Courcoubetis–Yannakakis 1995, full text.** Confirm the theorem statements quoted here from secondary sources.

**Search log, Stage 1.**
- Queries: Haar et al. PDF; Hierons–Türker partially specified FSM ADS; arXiv:2607.00844; Türker et al. 2023; ACY 1995; Paoli–Lafortune safe diagnosability; "adaptive identification with inapplicable tests"; "safe identifiability impossibility"; minimum-height decision trees.
- Downloads:
  - HAL returned an access-denied page.
  - CORE returned HTTP 403.
  - The Türker et al. 2023 PDF used fonts the extractor could not decode.

---

## 7. Stage 2 addendum (2026-11-21)

### 7.1 The partial nondeterministic FSM dependency: resolved

**U. C. Türker, R. M. Hierons, G. Barlas, K. El-Fakih. *Incomplete adaptive distinguishing sequences for non-deterministic FSMs.* IEEE TSE 49(9):4371–4389, 2023. DOI 10.1109/TSE.2023.3291137.** — **F**.
- *Read:* the author-accepted version (White Rose eprint 200869, CC-BY). Text was extracted with the macOS PDFKit framework; the earlier stdlib extractor failed on this file. I read the abstract, §§1–3, §5 and the references.

**Model.**
- An FSM is a tuple whose transition relation $h\subseteq S\times X\times Y\times S$ may be nondeterministic.
- It is **observable**: $(s,x,y)$ determines the next state (Def. 2.2).
- It may be **partial**: "input $x$ is defined for a set of states $S'$ if for every state $s\in S'$, $x$ is defined for $s$". Undefined inputs are motivated by environments where applying them "might lead to undesirable consequences such as damage to equipment or safety issues".
- An adaptive test case is "defined in $S'$" only if its first input is defined in $S'$ and the rest is defined on every successor set (Def. 3.2). States are separated iff $\mathrm{out}(s,\mu)\cap\mathrm{out}(s',\mu)=\varnothing$ (Def. 3.4).

**Results.**
- Theorem 5.1: "The K-Complete Forest problem is PSPACE-hard", where K-Complete Forest asks for at most $K$ *incomplete* ADSs separating all pairs.
- The proof takes $K=1$ on the deterministic FSM $M(\mathcal A)$ built from an FA-INT instance. That FSM's transitions are the automata's transitions plus a sink, so the machine has genuine dynamics. The construction is quoted from Hierons–Türker 2015 (*Computer Journal* 58(11)).
- No complexity result is stated for the existence of a single ADS for partial observable nondeterministic machines. The paper cites Kushik et al. 2016 and El-Fakih et al. 2018 for ADS existence algorithms and length bounds; their complexity status is reported as unknown in secondary sources.

**The seven questions of the Stage 2 brief.**
1. *Where is the nondeterminism?* In the output and the next state. Because the machine is observable, the next state is a function of the output. With self-loops ($s'=s$), only the output is nondeterministic.
2. *Can the hardness reduction be restricted to self-loops?* **No.** The FA-INT reduction encodes automaton runs in the state dynamics, and it is a deterministic machine besides. Under self-loops, $K=1$ forests for deterministic outputs are polynomial (Hierons–Türker 2014), so the reduction cannot survive.
3. *Does their admissibility coincide with robust safety?* **Yes, exactly.** "Defined in all states of the current set" is $u\in\mathcal S(K)$.
4. *Do their observation semantics coincide?* **Yes.** $\mathrm{out}(s,x)$ is a set-valued observation correspondence, and separation quantifies over all output traces, i.e. adaptive worst-case noise.
5. *Does their complexity result apply to static parameters?* The model *contains* the static case: an observable partial nondeterministic FSM with only self-loops. But the hardness is not proved there.
6. *Does it imply coNP-hardness under binary observations and unsafe sets of size $\le2$?* **No.**
7. *Does it have an analogue of the safety-witness number?* **No.** Its contributions are generation heuristics, invertible sequences and the forest-size hardness.

**Classification, in the brief's terms.**
- Türker et al. 2023 provides **an upper bound but not the necessary lower bound**, through the containing model. Its own hardness concerns a different problem (forest size) and uses dynamics.
- H1, P3, L6 and L7 concern the self-loop specialization, where the complexity drops from PSPACE-hard (forests) to coNP-complete (exact identifiability) and to P at unsafe size 1. **This is a specialization producing a substantially sharper classification.** Static models with safety are a natural sub-class of partial observable NFSMs that this literature has not singled out.
- **Hierons–Türker 2014 (§6.1) remains the one direct overlap:** deterministic outputs, P.

*Still unread:* Kushik et al., STTT 18(3) 2016; El-Fakih–Yevtushenko–Kushik, FAC 30(2) 2018 (abstract only, **A**: existence checking and exponential length bounds for complete observable machines); Hierons–Türker 2015, *Computer Journal*. These concern complete machines or forest size, so they do not bear on the static safety question, but they should be cited.

### 7.2 Geometric optimization and approximation (used in Stage 2)

All access levels are **A**, abstracts or citing papers, unless stated otherwise.

**Halfplane hitting set and cover.**
- Har-Peled–Lee, "Weighted geometric set cover problems revisited", JoCG 3(1) 2012: an exact polynomial algorithm for minimum-weight covering of points by halfplanes.
- arXiv:2506.16979, "Minimum-weight half-plane hitting set" (2025): $O(n^{5/2}\log^2n)$.
- *Use:* W4(c). Planar $\sigma$ is polynomial.

**Discrete unit disk cover.**
- Johnson 1982, the NP-hardness citation used in Claude–Dorrigiv–Durocher–Fraser–López-Ortiz–Salinger 2009 and later papers. I have not seen Johnson's statement itself.
- *Use:* W5, via lifting to the paraboloid. **Precise unresolved question:** confirm that Johnson's hardness holds for rational inputs with the discrete (given-centre) variant. The citing papers state it for DUDC.

**ε-nets for halfspaces.**
- Matoušek–Seidel–Welzl 1990, ε-nets for halfspaces in $\mathbb R^2$ and $\mathbb R^3$ of size $O(1/\varepsilon)$; Brönnimann–Goodrich 1995 for the reweighting approximation. **M**.
- *Use:* $O(1)$-approximation of $\sigma$ in $d\le3$ (`research/witness_geometry.md` §3).

**ε-kernels and coresets.**
- Agarwal–Har-Peled–Varadarajan, "Approximating extent measures of points", JACM 51(4) 2004. Confirmed: the definition of an ε-kernel as a subset preserving directional width to relative error ε.
- *Not confirmed from text:* the size bound $O(\varepsilon^{-(d-1)/2})$ and its origin in Dudley 1974 and Bronshteyn–Ivanov 1975.
- *Use:* `research/approximate_witnesses.md` A1–A2. I prove the weaker $O((R/\gamma)^{d-1})$ and a matching lower bound in the exponent $(d-1)/2$. The sharp upper bound is attributed, not claimed.

**Set cover inapproximability.** Dinur–Steurer 2014, $(1-o(1))\ln n$. **M**.

**Parameterized complexity.** Multicolored clique is W[1]-hard (standard; e.g. Cygan et al., *Parameterized Algorithms*, 2015). **M**.

**Targeted searches with no direct hits**, for the specific combination of safety-dependent admissibility with identification:
- geometric active learning under hard constraints;
- safe experimental design with bounded errors;
- halfspace-constrained identification;
- adaptive decision trees with restricted tests;
- support-function approximation for identification;
- finite discretization of uncertainty sets.

The adaptive decision tree literature with noisy outcomes (arXiv:2312.15357) studies approximation without admissibility constraints.

### 7.3 Updated verdicts

| Item | Verdict |
|---|---|
| H1, P3 (static, safety, nondeterministic: coNP-complete; P at unsafe size 1) | **Not subsumed.** Türker et al. 2023 contains the model but proves hardness only for forest size, with dynamics. Hierons–Türker 2014 covers only deterministic outputs. |
| L1–L3 (support-function trap characterization; hull invariance; convex-position minimal traps) | Elementary consequences of the definitions. Not found stated. Low novelty weight, high expository value. |
| L6 (NP-complete for laminar size-$\le2$ unsafe sets, convex position, common noise) | Not found. A strengthening of H1. |
| L7 (W[1]-hard in the number of safety directions) | Not found. **Potentially original.** |
| W4(b), W5 ($\sigma$ polynomial in the plane, NP-hard in space) | Direct consequences of known geometric hitting-set results. **Not a contribution.** The contribution is only the connection. |
| A1–A4, Q1–Q2 (approximate witnesses, certificates, packing horizons) | The tools are classical: support-function sampling, covering numbers. The certificate soundness and completeness (A3–A4) and the packing horizon (Q1) for safe identification were not found. **Potentially original as formulations.** |

---

## 8. Stage 3 addendum (2026-11-21): novelty check for the fixed-dimension results

### 8.1 Searches

Queries run in Stage 3:
- the Johnson 1982 NP-completeness column with unit disk cover;
- strictly antipodal pairs of convex polygons;
- satisfiability or hardness for points on a circle with halfplane ranges combined with identification or adaptive testing under safety constraints.

Results:
- **Johnson, "The NP-completeness column: an ongoing guide", J. Algorithms 3(2):182–195, 1982.** **M**. The citation was confirmed from the reference list of arXiv:1411.6810 and from Waterloo DUDC papers, which attribute DUDC NP-hardness to it. The column itself was not obtained.
  - Fowler–Paterson–Tanimoto, "Optimal packing and covering in the plane are NP-complete", IPL 12(3), 1981, is the usual source for the continuous unit-disk cover. **M**.
  - **W5's dependency is therefore on a citation chain, not on a read theorem.** The exact question: does the hardness hold for the discrete variant with rational inputs? The citing papers state it for discrete unit disk cover.
- **Strictly antipodal pairs.** A convex $m$-gon has $m-k$ strictly antipodal vertex pairs, $k$ being the number of pairs of parallel sides. This is attributed to Nguyên–Soltan in an appendix of arXiv:1406.2052. **A**. Used only as an upper bound remark in R5(c).
- **No source found** combining halfplane ranges on points in convex position with satisfiability-type hardness of *identification* or *adaptive testing* under safety constraints.
  - The closest hits are geometric hitting-set and cover problems, e.g. arXiv:2506.16979, which reduces halfplane hitting set to circular arc covering.
  - Densest-hemisphere NP-completeness holds when the dimension is not fixed (Johnson–Preparata 1978, as cited; **M**).

### 8.2 Verdict on D2 (planar coNP-completeness)

- **Not found in the sources read, nor in the targeted searches.**
- It is **not implied** by the partial-FSM literature (§7.1), which gives only upper bounds for the static case.
- It is **not implied** by geometric hitting-set hardness either, which concerns optimization of a hitting set. W4(c) shows that the planar hitting-set version, computing $\sigma$, is polynomial, while D2 shows that planar TRAP is coNP-complete. These are different problems with opposite complexity in the plane.
- D2 is the strongest candidate for an original contribution so far. The precise novelty question for a future check is whether any "geometric CSP with halfplane scopes" or "geometric decision tree with forbidden tests" result already contains a planar NP-hardness of this form. I found none.

### 8.3 Still unread

- Johnson 1982 (the column itself).
- The Dudley / Bronshteyn–Ivanov / AHPV coreset size statements (§7.2).
- Kushik et al. 2016 and El-Fakih et al. 2018 (complete observable machines; not on the critical path).

---

## 9. Stage 4: final theorem-level originality audit (2026-11-21)

### 9.1 Primary-source status

**Johnson 1982 ("The NP-completeness column: an ongoing guide", J. Algorithms 3(2):182–195).** **M**. Not obtained.
- Citing papers state "discrete unit disk cover is NP-hard [Joh82]".
- Fowler–Paterson–Tanimoto 1981 (IPL 12(3)) is the usual source for the continuous version. **M**.
- **Resolution:** W5 ($\sigma$ NP-hard in $\mathbb Q^3$) remains citation-dependent. The new **W5′** ($\sigma$ NP-hard in $\mathbb Q^4$) is self-contained: vertex cover on moment-curve pairs. No principal theorem depends on Johnson 1982.

**The sharp coreset exponent.** Secondary statements, **A**:
- Mount et al. (SoCG 2012): any convex body $K$ is $\varepsilon$-approximable by a polytope with $O((\operatorname{diam}K/\varepsilon)^{(d-1)/2})$ facets (Dudley 1974), and the same number of vertices suffices (Bronshteyn–Ivanov 1975).
- Arya–da Fonseca–Mount (SoCG 2016) and the survey arXiv:2512.02379 say the same.
- The original papers were not obtained. Bronshtein's 2007 survey ("Approximation of convex sets by polytopes", J. Math. Sci. / Contemp. Math. Fundam. Directions 22) is the reliable alternative to consult.
- **Resolution:** A2 proves the weaker $O((R/\gamma)^{d-1})$ upper bound and the matching-exponent lower bound $\Omega((R/\gamma)^{(d-1)/2})$ independently. The sharp upper exponent is used only as a cited remark. No principal theorem depends on it.

### 9.2 Theorem-level assessment

The underlying static model **is a specialization of observable partial nondeterministic FSMs** (Türker et al. 2023, §7.1). Nothing below claims otherwise. Categories:
- **(K)** known;
- **(S)** a new specialization of known theory;
- **(D)** an independently derived consequence;
- **(O)** potentially original, not found in the sources read. Not finding a theorem is not proof that it is new.

| # | Result | Category | Precise basis |
|---|---|---|---|
| 1 | Deterministic vs. ambiguous safe identification: P2 versus H1 | P2 is **K** (Hierons–Türker 2014). H1, the coNP-completeness of the static nondeterministic case, is **O**. | Türker et al. 2023 and ACY 1995 give only upper bounds for the static case. Their hardness uses dynamics, or concerns forest size. |
| 2 | Unsafe-set cardinality transition: P at size 1, NP-complete at size 2, even laminar | **O** (statement). The technique is standard (Horn-SAT; Schaefer). | — |
| 3 | Planar and fixed-dimensional dichotomy D2/D3 | **O** | not implied by geometric hitting-set hardness, which concerns a different problem and is polynomial in the plane; no match in targeted searches (§8) |
| 4 | Unit-circle rational realization of D2; lone pair ⇔ strict antipodality (R1) | R1 is **D** (elementary). The realization is **O** as part of D2. | strict antipodality counts are **K** (Nguyên–Soltan, as cited) |
| 5 | Safety-witness number $\sigma$; $\sigma(K)=\lvert K\rvert$ for minimal traps | **O** as a formulation; elementary proof | computing $\sigma$ is hitting set (**K**) |
| 6 | Local-to-global principle G1′ | **O** | — |
| 7 | Compact-space characterization K1–K3 and counterexamples X1–X4 | **D/O**: the technique is viability-kernel style (**K** in spirit); the statement with condition (L) and the counterexamples were not found | Aubin's viability theory is the template (not checked against a specific theorem) |
| 8 | Certified discretization A3–A4; packing horizon Q1′; necessity Q2 | **D/O**. The covering and coreset tools are **K**; the safe-learning consequences were not found. | — |
| 9 | Aligned classification AL1–AL4 | AL1 is **D**; AL2 and AL3 are **O** | — |

**Strongest defensible original contributions, in order:**
1. **The complexity map of static safe identification.** It has three parts:
   - the coNP-completeness of the ambiguous-observation static case, set against the known polynomial deterministic case;
   - the size-1 / size-2 transition;
   - the dimensional dichotomy (P at $d=1$, coNP-complete at every fixed $d\ge2$, already on the unit circle), with the alignment refinement.
2. **The structural theory:** traps, $\sigma$, minimal-trap cardinality and local-to-global principles.
3. **The compact-space theory with (L),** and its certified and quantitative versions.

All three remain subject to a final pre-submission novelty search in the geometric-CSP and testing literatures, using the queries recorded in §§6.5, 7.2 and 8.1.

---

## 10. Final pre-manuscript verification (2026-11-21)

*A last primary-source-driven search, aimed at mathematical equivalence rather than terminology. Bibliographic data for everything the manuscript may cite is in `research/references.bib`, with access levels.*

### 10.1 Searches

Queries covered:
- adaptive distinguishing for partial nondeterministic FSMs, the self-loop or static restriction, and forbidden or undefined inputs;
- adaptive identification and diagnosis with forbidden, dangerous or uncertainty-dependent tests;
- geometric identification with halfplane constraints, points on a circle and interval measurements;
- deciding safe identifiability or safe exploration with NP- or coNP-hardness;
- recent work by the partial-FSM authors (2024–2026).

### 10.2 New items

**H. Yenigün, N. Yevtushenko, N. Kushik, J. López. *The effect of partiality and adaptivity on the complexity of FSM state identification problems.* Proc. ISP RAS 30(1):7–24, 2018. DOI 10.15514/ISPRAS-2018-30(1)-1.** **F** (text extracted from the journal PDF).
- *Model.* Partial observable nondeterministic FSMs. An input may be applied only if it is **defined at every current candidate state**. This is exactly the robust-safety rule here ($u\in\mathcal S(\Theta_t)$), so it is the nearest existing framework, together with Türker et al. 2023.
- *Results for distinguishing experiments.*
  - Preset distinguishing: PSPACE-complete for complete and partial observable nondeterministic machines.
  - Adaptive distinguishing: P for complete and partial deterministic machines, the latter citing Hierons–Türker 2014.
  - Adaptive distinguishing for nondeterministic machines: claimed PSPACE-hard and "out of P". The argument is a family of 2-input machines with prime-length cycles, in which every adaptive distinguishing test case has exponential height.
- *Relation to this project.*
  - The hardness argument lives entirely in the **state dynamics**. With self-loops only, every reachable candidate set is a subset of $\Theta_0$, and some distinguishing test case has height $\le\lvert\Theta_0\rvert-1$ (T1, T2). So the argument does not apply to the static model, which is in coNP (Proposition M).
  - The paper says nothing about the static case, unsafe-set cardinality, or geometric realizations.
  - **It does not establish or subsume H1, P3, D2 or D3.** It strengthens the framing that the static model is the self-loop case of a known family whose dynamic versions are PSPACE-hard.
  - Separately, an exponential-height argument by itself shows a lower bound on test-case size, not hardness of the existence question. I do not rely on that claim.

**T. Lu, M. Zinkevich, C. Boutilier, B. Roy, D. Schuurmans. *Safe exploration for identifying linear systems via robust optimization.* arXiv:1711.11165, 2017.** **A**. This is the entry listed without authors in §1.8b. It is stochastic, PAC-style, with a nominal safe action and no complexity-class result. It is not comparable.

**"Identification of points using disks"** (Discrete Math. 2019; arXiv:1705.11116). **A**. Identifying codes: a *non-adaptive* minimum set of disks separating all points, NP-complete for fixed radius. There are no safety constraints and no adaptivity. Its closest analogue here is computing $\sigma$, not deciding TRAP. Not equivalent.

**Moldovan–Abbeel 2012** (already §1.3) is the only safe-exploration paper with a hardness result. It concerns existence of ergodicity-safe policies in MDPs, not identification.

### 10.3 Primary-source verification

**Bronshtein's survey.** E. M. Bronshtein, *Approximation of convex sets by polytopes*, Sovremennaya Matematika. Fundamental'nye Napravleniya 22 (2007) 5–37; J. Math. Sci. 153(6):727–762, 2008, DOI 10.1007/s10958-008-9144-x. **F**, Russian original.
- §4.1, inequality (6): for every convex body $U\subset\mathbb E^d$, $\delta_H(U,\mathfrak R^d_n)\le c(U)\,n^{-2/(d-1)}$, where $\mathfrak R^d_n$ are the polytopes with at most $n$ vertices. The same bound holds for the inscribed and circumscribed classes, with vertices and with facets.
- It attributes the result to [5] Bronshteyn–Ivanov, Sib. Mat. Zh. 16 (1975) 1110–1112, and [103] Dudley, J. Approx. Theory 10 (1974) 227–236, independently.
- *Metric:* Hausdorff. *Exponent:* $2/(d-1)$ in $n$, i.e. $n=O(\varepsilon^{-(d-1)/2})$ at accuracy $\varepsilon$.
- *Constant:* $c(U)$, unspecified in that passage.

**The uniform constant.**
- Hoehner, arXiv:2512.02379 (**P**, Thm. 4.1) states it: at most $(\operatorname{diam}K/\varepsilon)^{(d-1)/2}$ vertices for an inscribed polytope, and the same number of facets for a circumscribed one, for every convex body and $\varepsilon\in(0,1]$.
- The original papers remain unread, so the uniform form is **A**.

**Consequence for the documents.**
- `research/approximate_witnesses.md` now records what is primary, and closes two small gaps in applying the classical theorem to $\sigma_\gamma$:
  - vertices lie in $\operatorname{conv}K$, fixed by Carathéodory at a factor $d+1$;
  - empty interior, fixed by fattening and projection.
- No theorem changes. A2's own bounds are proved there, and the sharp upper exponent is a remark.

**Johnson 1982.** Unchanged: **M**, not obtained.
- **W5** ($\sigma$ NP-hard in $\mathbb Q^3$) depends on it.
- **W5′** ($\sigma$ NP-hard in $\mathbb Q^4$) does not: vertex cover on moment-curve pairs, proved in `research/witness_geometry.md`.
- The manuscript should state W5′ as the theorem, and W5 as a remark citing Johnson.

### 10.4 Conclusion

**No prior result found establishes or subsumes D2, its unit-circle restriction, H1, the size-1/size-2 transition, $\sigma$ and G1′, or K1–K3.** The assessment in §9.2 stands unchanged. As before, an unsuccessful search is not proof of priority.

**Remaining cited-only statements, none on a principal theorem's critical path:**
- Johnson 1982 (W5);
- the uniform Dudley / Bronshteyn–Ivanov constant (A2 remark);
- Har-Peled–Lee 2012 and arXiv:2506.16979 (W4(c));
- Hyafil–Rivest and Laber–Nogueira (OPTCOUNT);
- Nguyên–Soltan (R5(c));
- the ACY 1995 theorem statements.
