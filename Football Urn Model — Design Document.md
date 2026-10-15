# Football Urn Model — Design Document

Oct 15, 2026 · @Truls Edvardsen Aarønes

## Purpose and goals

The model treats a football match as a lottery: each team's skill is a count of red balls, red draws become shots, and each shot's xG decides whether it becomes a goal. Because every step is an explicit probability, the same model can both simulate matches and compute exact likelihoods for observed data.

The model must:

1. Simulate realistic match results and xG data (number of shots,  xG-values, result).
2. Answer, with a clear probabilistic meaning: *given this xG data, how likely is it that team A has N more red balls than team B** **in** the **s**k**ill p**o**o**l**?*
3. Keep underlying skill slow-moving, with match-to-match form as a separate, faster source of randomness.
4. Stay simple enough that every probability can be written down and computed exactly on a grid.

## Model structure

&#91;embedded content: model layers · skill pool to observed data\]

Simulation runs top to bottom. Inference runs the same chain backwards, from observed data to the red-ball counts.

## Mathematical specification

Each layer is a standard distribution, so the full likelihood is a product of known terms. Notation: team i has a pool of M balls, of which R\_i are red.

**Layer 1 — Underlying skill.** Skill is the red share of the pool, θ\_i = R\_i / M. R\_i is an integer and changes slowly (see drift under Calibration).

**Layer 2 — Matchday form.** Before each match, team i draws m balls from its pool without replacement. The number of red match balls is hypergeometric:

```latex
k_i \sim \mathrm{Hypergeometric}(M,\ R_i,\ m), \qquad p_i = k_i / m
```

p\_i is the team's strength on the day. Smaller m means more matchday variation.

**Layer 3 — The match.** The match has n attacking phases. In each phase both teams draw one ball (with replacement) from their match bowls:

- A red, B white → A gets a shot
- B red, A white → B gets a shot
- Same colour → nothing happens

Shot counts are therefore multinomial:

```latex
(S_A,\ S_B,\ S_0) \sim \mathrm{Multinomial}\big(n;\ p_A(1-p_B),\ p_B(1-p_A),\ 1 - p_A(1-p_B) - p_B(1-p_A)\big)
```

**Layer 4 — Shot quality and goals.** Each shot j gets an xG value x\_j drawn from a shot-quality distribution f (fitted to league data), and becomes a goal with probability x\_j:

```latex
x_j \sim f(x), \qquad G_j \sim \mathrm{Bernoulli}(x_j)
```

**Likelihood of one match.** Given matchday strengths, the probability of the observed shots, their xG values and the goals is:

```latex
L(D \mid k_A, k_B) = \mathrm{Mult}(S_A, S_B, S_0;\ n, q_A, q_B, q_0) \prod_{j} f(x_j)\, x_j^{G_j} (1 - x_j)^{1 - G_j}
```

Important consequence: if f does not depend on skill, the second factor is the same for every value of R and cancels in the posterior. Then only shot *counts* tell you anything about red balls, and the xG values themselves carry no skill information. See Open design decisions.

## Inference: how likely is a red-ball difference?

The headline question is a Bayesian posterior, computed exactly by enumerating every possible pair of red-ball counts. With M = 100 that is 101 × 101 ≈ 10,000 cells per team pair, which is trivial to compute.

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

1. Several teams playing each other: estimate all R\_i jointly. Start by holding opponents fixed at their current best estimate and updating one team at a time.
2. Skill drift over a season: treat R\_i as a hidden Markov chain that can move ±1 ball between matches, and run forward filtering on the same grid.

## Calibration

Calibration means choosing the global parameters so that simulated leagues look like real ones; team red-ball counts are then estimated on top. Six parameters need fixing:

| Parameter | What it controls | Calibrated against | Method |
| --- | --- | --- | --- |
| M (pool size) | Resolution of the skill scale | Not identifiable from data | Choose it (e.g. 100); it only sets the units of "one ball" |
| f(x) (shot quality) | Distribution of xG per shot | All shots in the league | Fit directly, e.g. a Beta or an empirical histogram |
| n (phases per match) | Match tempo, total shot volume | Mean and variance of total shots per match | Maximum likelihood, jointly with m |
| m (match balls) | Size of matchday form swings | Extra variance in a team's shot counts beyond binomial | Maximum likelihood, jointly with n |
| Prior P(R) | Spread of skill across teams | Spread of team shot shares over a season | Empirical Bayes: fit to the league |
| Drift rate | How fast R changes | Correlation of a team's form across matches and seasons | Maximum likelihood in the hidden Markov model |
| h (home balls) | Extra red match balls for the home team | Home vs away difference in shots and xG | Maximum likelihood, jointly with n and m |

**Procedure:**

1. Fix M.
2. Fit f(x) from per-shot league data. Check that total xG ≈ total goals, which confirms the xG provider's numbers behave as probabilities.
3. Fit n, m and the prior jointly by maximising the marginal likelihood of a full season (EM works well: alternate between posteriors over R and k, and re-estimating parameters).
4. Fit drift using several consecutive seasons.
5. Validate (next section). Recalibrate if checks fail.

The key identification point: m is learned from how much a team's shot share varies between matches *more than* binomial noise alone would cause. Without matchday form, the model would be overconfident about skill.

## Validation and accuracy metrics

"Accurate" has two meanings here, and each has its own test.

**Does it simulate realistic football?** Simulate whole seasons with the calibrated parameters and compare against real data:

- Distribution of shots and xG per team per match
- Goals per match, 0–0 rate, draw rate, common scorelines
- Spread of final league points

**Are its probabilities honest?** Test on matches the model was not fitted to:

- Win/draw/loss forecasts scored with log loss and ranked probability score, compared against a baseline (e.g. a Poisson or Dixon–Coles model, or bookmaker odds)
- Reliability: events forecast at 30% should happen about 30% of the time

**Is "X% likely that A has N more red balls" correct?** This is checked by simulation, since true red balls are never observed:

1. Pick known R values, simulate matches, run the inference.
2. Repeat many times. An 80% credible interval for R\_A − R\_B should contain the true difference in about 80% of runs.
3. If coverage is too low, the model is overconfident (usually m or drift is wrong).

## Data analysis: shots and xG vs skill

Before fixing the layer-3 draw rule and the shot-quality distribution f(x), one Premier League season is used to measure how shot counts and shot quality depend on skill difference.

**Data.** One season of Premier League matches with per-shot xG, fetched with [soccerdata](https://github.com/probberechts/soccerdata). Per shot: match, team, home or away, xG, goal. Per team: final points.

**Skill proxy.** For each match, d = final points of the home team − final points of the away team. Caveats: final points include the match itself, and points are a noisy measure of skill. Both are acceptable for a first look.

**Analyses:**

1. **Shot counts vs d.** Bin d (e.g. 10-point bins). In each bin, look at the full distribution of home shots and away shots: mean, variance and histogram. This is the "3D landscape" P(k shots | d). Variance above what a binomial predicts indicates matchday form and informs m.
2. **Shot quality vs d.** Compare the per-shot xG distribution across bins of the shooting team's point advantage. Does the whole distribution shift, or only its mean? This decides whether f(x) must depend on skill.
3. **Coupling of shot counts.** Within each bin of d, correlate home shots with away shots. A negative correlation supports a coupled draw rule, where one team's chance is the other team's missed chance.
4. **Home advantage, by paired fixtures.** Every pair of teams meets twice, once at each ground. Skill difference flips sign between the two matches, but home advantage does not, so averaging cancels skill:

```latex
H = \tfrac{1}{2}\big[(s_A^{\text{home}} - s_B^{\text{away}}) + (s_B^{\text{home}} - s_A^{\text{away}})\big]
```

Here s is shots in that match. Averaging H over all 190 pairs gives the home effect on shots. The same works for xG. Half the difference of the two brackets gives the skill effect for that pair.

5. **Sanity check.** Total xG over the season should be close to total goals, confirming xG behaves as a probability.

**Results so far** (Premier League 2025/26, Understat, own goals excluded; code in `src/football_urn_model/shot_counts.py` and `shot_quality.py`):

- **Analysis 1 — shot counts vs d. Conclusion:** the total number of shots in a match varies randomly around ~25 and does not depend on d. The skill difference decides how those shots are split: the better team gets the larger share (home shots rise from ~9 at d ≈ −40 to ~17 at d ≈ +30, away shots fall from ~14 to ~8). Home teams shoot more at equal skill (~14 vs ~10 at d ≈ 0). There are many ways to model the split, coupled or not; this is left open, and no more shot-count analysis is planned for now.
- **Analysis 2 — shot quality vs d. Conclusion:** better teams get better chances, and the whole xG distribution shifts, not only its mean. Binning shots (penalties excluded) by the shooting team's points advantage, from < −30 to > 30: mean xG per shot rises from 0.101 to 0.131, every quantile rises by roughly 20–35% (median 0.054 → 0.066, 90th percentile 0.33 → 0.41), and the share of shots with xG > 0.3 goes from 11% to 15.5%. The effect is much smaller than for shot counts (a team's shot share roughly doubles across d, xG per shot rises by about a third), so most skill information is in how many shots a team gets, and some is in how good they are. Caveats: game state (a leading team may get better chances on the counter), home and away mixed, and final points as a noisy skill proxy.
- **Analysis 5 — sanity check, xG vs goals. Conclusion: fails.** Understat's xG is too high for 2025/26. Non-penalty shots: 1,114 xG but 927 goals (17% fewer). Penalties: 70 xG, 77 goals. Shots with xG between 0.1 and 0.7 convert clearly below their xG (e.g. 0.4–0.7: mean xG 0.52, goal rate 0.39). The reason is unknown; comparing with earlier seasons would show whether it is Understat's model or an unusual season.

## Correcting the xG data

In the model, x is the *true* probability that a shot becomes a goal. A data source's xG is only a measurement of it, so each data source has to be adjusted before it can be used to assess skill differences accurately. Analysis 5 shows this is needed for Understat.

- **Finishing is part of skill.** A better team should not only create more and better chances, it should also convert them better. Understat's xG does not know who shoots or who is in goal, so in the model, chance quality should depend more strongly on skill than Understat's xG does.
- **The correction has up to three parts:**
  1. League-wide calibration of the source's xG (the 17% overestimate above), e.g. logit P(goal) = a + b·logit(x).
  2. A skill effect, so that better teams convert better, e.g. + β·(θ_shooter − θ_opponent). One global β, no extra parameter per team.
  3. Optionally a small, team-specific residual, heavily shrunk towards zero, since most over- or under-performance is noise.
- Estimating the correction inside the model, together with skill, keeps its uncertainty in the posterior. Since the correction should be small, a fixed adjustment applied beforehand is also an acceptable approximation.

## Open design decisions

- [x] **One bowl or two per team?** The current draw rule uses one bowl, so attack and defence are the same skill. Separate attack and defence bowls are more realistic but double the parameters. Decided: one skill bowl per team.
- [ ] **Should shot quality depend on skill?** If not, xG values carry no information about red balls, only shot counts do. Letting better teams draw from a better f(x) makes xG informative but adds parameters. Data (analysis 2): the whole xG distribution shifts with skill, so the data supports a skill-dependent f(x).
- [ ] **Per-shot xG or match totals?** Per-shot data gives the exact likelihood above. Match totals require approximating the distribution of summed xG.
- [x] **Home advantage:** ignore, or add extra red balls for the home team? Decided: the home team gets extra matchday red balls, a parameter to calibrate.
- [x] **Game state:** teams that lead tend to shoot less. Ignore in version 1, or let p change with the score? Decided: ignore in version 1; every phase has the same probabilities regardless of score.
- [ ] **Pool size M:** 100 is a convenient default; confirm or pick another.

* [ ] **Shot-count distribution:** layer 3 may need an extra variable so that P(k shots) = f(k, p\_i − p\_j) matches real matches. Check against data.
* [ ] **Later:** walk through the multinomial shot-count equation in layer 3, and the one-match likelihood equation.

- [ ] **Data check — does skill affect shot quality?** Per team and season, collect shots per match and mean xG per shot, and correlate both with a skill proxy (e.g. final table position). The result decides whether f(x) must depend on skill.

* [ ] **Redesign the layer-3 draw rule to depend only on differences.** The current rule gives A a shot with probability p\_A(1 − p\_B), which depends on both values, not only on p\_A − p\_B (goal 5).
* [ ] **Teams that outperform (or underperform) their xG.** Some teams score more, or concede fewer, goals than their xG says. Layer 4 currently turns every shot into a goal with probability exactly x, so the model has no room for this. The end goal is to account for it; see Correcting the xG data for the current thinking.
