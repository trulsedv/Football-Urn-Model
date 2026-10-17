# Football Urn Model — Design

Oct 15, 2026 · @Truls Edvardsen Aarønes

This document describes the model as it is. Why it looks this way, open questions and future ideas are in
[considerations.md](considerations.md); the data behind it is in [data-analysis.md](data-analysis.md).

## Purpose and goals

The model treats a football match as a lottery: each team's skill is a count of red balls, red draws decide who
gets the shots, and drawn chance balls decide each shot's xG and whether it becomes a goal. Because every step is
an explicit probability, the same model can both simulate matches and compute exact likelihoods for observed data.

The model must:

1. Simulate realistic match results and xG data (number of shots, xG values, result).
2. Answer, with a clear probabilistic meaning: *given this xG data, how likely is it that team A has N more red
   balls than team B in the skill pool?*
3. Keep underlying skill slow-moving, with match-to-match form as a separate, faster source of randomness.
4. Stay simple enough that every probability can be written down and computed exactly on a grid.
5. Be physically playable: every random step is a draw of balls from an urn, so a match could be played with real
   urns and balls. No step may use a fitted function or continuous distribution.

## Model structure

Simulation runs top to bottom. Inference runs the same chain backwards, from observed data to the red-ball counts.

1. **Skill pool** (M balls, R red): true underlying skill, drifts slowly across matches and seasons.
2. **Match urn** (m balls drawn from the pool): matchday form, redrawn every match.
3. **Match rounds** (n per match): a tempo urn decides whether there is a shot; the match urns decide who gets it.
4. **Chance balls** (c per shot): their red share is the shot's xG; one drawn from them decides the goal.

Observed: number of shots, xG values, result.

Real data enters through a correction step: data source → correction → model inference → skill difference.

## Mathematical specification

Each layer is a standard distribution, so the full likelihood is a product of known terms. Notation: team i has a
pool of M balls, of which R\_i are red.

**Layer 1 — Underlying skill.** Skill is the red share of the pool, θ\_i = R\_i / M. R\_i is an integer and
changes slowly (see drift under Calibration).

**Layer 2 — Matchday form.** Before each match, team i draws m balls from its pool without replacement. The number
of red match balls is hypergeometric:

```latex
k_i \sim \mathrm{Hypergeometric}(M,\ R_i,\ m), \qquad p_i = k_i / m
```

p\_i is the team's strength on the day. Smaller m means more matchday variation. The home team gets h extra red
match balls.

**Layer 3 — The match.** The match has n match rounds. In each round:

1. **Is there a shot?** A ball is drawn (with replacement) from a tempo urn of N balls, s of them red. A red ball
   means there is a shot this round. The tempo urn is independent of the match urns. With μ the average number of
   shots per match, the tempo urn has s = μN/n red balls (N and n chosen so that s is a whole number; n ≥ μ).
2. **Who gets the shot?** Both teams draw one ball (with replacement) from their match urns. A red, B white → A
   gets the shot; B red, A white → B gets it. Same colour: redraw or flip a coin (not decided yet).

The total number of shots T and A's shots S\_A are therefore:

```latex
T \sim \mathrm{Binomial}(n,\ s/N), \qquad S_A \mid T \sim \mathrm{Binomial}(T,\ q_A), \qquad S_B = T - S_A
```

where q\_A is the probability that A gets a shot: q\_A = p\_A(1−p\_B) / [p\_A(1−p\_B) + p\_B(1−p\_A)] with
redraw, or q\_A = ½ + ½(p\_A − p\_B) with a coin flip.

**Layer 4 — Chance quality and goals.** When a team gets a shot, it draws c balls (e.g. c = 10) from its match urn
(or from a separate chance urn; not decided yet). The share of red balls among them is the shot's xG. The c balls
are put in a shot urn and the player draws one: red is a goal.

```latex
r_j \sim \mathrm{Hypergeometric}(m,\ k_i,\ c), \qquad x_j = r_j / c, \qquad G_j \sim \mathrm{Bernoulli}(x_j)
```

xG can therefore only take the values 0, 1/c, …, 1. A better team gets better chances, and finishing is part of
skill.

**Likelihood of one match.** Given matchday strengths, the probability of the observed shots, their xG values and
the goals is:

```latex
L(D \mid k_A, k_B) = \mathrm{Bin}(T;\ n, s/N)\, \mathrm{Bin}(S_A;\ T, q_A) \prod_{j} \mathrm{Hyp}(r_j \mid m, k_{(j)}, c)\, x_j^{G_j} (1 - x_j)^{1 - G_j}
```

Here k\_(j) is the match-red count of the team that took shot j. Both shot counts and xG values carry information
about red balls.

## Inference: how likely is a red-ball difference?

The headline question is a Bayesian posterior, computed exactly by enumerating every possible pair of red-ball
counts. With M = 100 that is 101 × 101 ≈ 10,000 cells per team pair, which is trivial to compute.

**Step 1 — Marginalise matchday form.** For one match, sum over all possible match draws:

```latex
P(D \mid R_A, R_B) = \sum_{k_A=0}^{m} \sum_{k_B=0}^{m} \mathrm{Hyp}(k_A \mid R_A)\, \mathrm{Hyp}(k_B \mid R_B)\, L(D \mid k_A, k_B)
```

**Step 2 — Combine matches and prior.** Matches are independent given skill, so the posterior is:

```latex
P(R_A, R_B \mid D) \propto P(R_A)\, P(R_B) \prod_{\text{matches}} P(D_{\text{match}} \mid R_A, R_B)
```

**Step 3 — Answer the question.** Sum the posterior along the diagonal where the difference is N:

```latex
P(R_A - R_B = N \mid D) = \sum_{R_A - R_B = N} P(R_A, R_B \mid D)
```

The same table also gives P(R\_A > R\_B), credible intervals for the difference, and so on.

**Extensions, in order of difficulty:**

1. Several teams playing each other: estimate all R\_i jointly. Start by holding opponents fixed at their current
   best estimate and updating one team at a time.
2. Skill drift over a season: treat R\_i as a hidden Markov chain that can move ±1 ball between matches, and run
   forward filtering on the same grid.

## Correcting the xG data

The correction is not part of the model. It is a transformation step between a data source and model inference:

data source → correction → model inference → skill difference

In the model, xG is the red share of the drawn chance balls. A data source's xG comes from its own model, so each
data source has its own correction that turns its xG into model xG. Since the correction is outside the model, it
does not have to be playable and may use fitted functions. Its form is not decided yet.

## Calibration

Calibration means choosing the global parameters so that simulated leagues look like real ones; team red-ball
counts are then estimated on top. These parameters need fixing:

| Parameter | What it controls | Calibrated against | Method |
| --- | --- | --- | --- |
| M (pool size) | Resolution of the skill scale | Not identifiable from data | Choose it (e.g. 100); it only sets the units of "one ball" |
| n (match rounds), N and s (tempo urn) | Total shot volume | Mean total shots per match, μ ≈ 25 | s = μN/n |
| c (chance balls) | Distribution of xG per shot | All shots in the league, after correction | Maximum likelihood |
| m (match balls) | Size of matchday form swings | Extra variance in a team's shot counts beyond binomial | Maximum likelihood, jointly with the prior |
| Prior P(R) | Spread of skill across teams | Spread of team shot shares over a season | Empirical Bayes: fit to the league |
| Drift rate | How fast R changes | Correlation of a team's form across matches and seasons | Maximum likelihood in the hidden Markov model |
| h (home balls) | Extra red match balls for the home team | Home vs away difference in shots and xG | Maximum likelihood, jointly with m |

**Procedure:**

1. Fix M, and set n, N and s from μ.
2. Correct the data source's xG, then fit c from the per-shot data.
3. Fit m, h and the prior jointly by maximising the marginal likelihood of a full season (EM works well: alternate
   between posteriors over R and k, and re-estimating parameters).
4. Fit drift using several consecutive seasons.
5. Validate (next section). Recalibrate if checks fail.

The key identification point: m is learned from how much a team's shot share varies between matches *more than*
binomial noise alone would cause. Without matchday form, the model would be overconfident about skill.

## Validation and accuracy metrics

"Accurate" has two meanings here, and each has its own test.

**Does it simulate realistic football?** Simulate whole seasons with the calibrated parameters and compare against
real data:

- Distribution of shots and xG per team per match
- Goals per match, 0–0 rate, draw rate, common scorelines
- Spread of final league points

**Are its probabilities honest?** Test on matches the model was not fitted to:

- Win/draw/loss forecasts scored with log loss and ranked probability score, compared against a baseline (e.g. a
  Poisson or Dixon–Coles model, or bookmaker odds)
- Reliability: events forecast at 30% should happen about 30% of the time

**Is "X% likely that A has N more red balls" correct?** This is checked by simulation, since true red balls are
never observed:

1. Pick known R values, simulate matches, run the inference.
2. Repeat many times. An 80% credible interval for R\_A − R\_B should contain the true difference in about 80% of
   runs.
3. If coverage is too low, the model is overconfident (usually m or drift is wrong).
