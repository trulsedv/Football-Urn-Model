# Football Urn Model — Design Considerations

What we have considered while designing the model, and what we concluded. [design.md](design.md) describes the
system itself; this file records why it looks the way it does, what is still open, and ideas for later. Data
results are in [data-analysis.md](data-analysis.md).

## Decided

### The model must be physically playable

Every random step is a draw of balls from an urn, so a match could be played with real urns and balls. No step may
use a fitted function or a continuous distribution. This replaced an earlier version where xG was drawn from a
fitted distribution f(x).

### Correcting xG data is outside the model

A data source's xG comes from its own model and can be biased: Understat's xG is 17% too high for 2025/26
(analysis 5). Each data source therefore needs its own correction that turns its xG into model xG:

data source → correction → comparison with simulated data (and, later, inference)

The correction is not part of the model, so it does not have to be playable and may use fitted functions.

### Finishing is part of skill

A better team should create more and better chances, and also convert them better. This is why xG in the model
comes from the team's own balls, and why model xG should depend more strongly on skill than Understat's xG does
(Understat does not know who shoots or who is in goal).

### Shot quality depends on skill

Analysis 2 shows the whole xG distribution shifts with skill. Without this, xG values would carry no information
about red balls, only shot counts would. Drawing the chance balls from the team's own match urn (phase 5) makes shot quality
depend on skill by construction.

### The total number of shots comes from a tempo urn

The data shows that the total number of shots in a match (mean ≈ 25, variance ≈ 29) depends neither on the
difference nor on the sum of the two teams' final points. Options considered:

- **Combined urn:** pour both match urns together and draw; a red ball is a shot for its owner. Rejected: the
  total then depends on the sum of red balls, so strong pairs of teams would shoot more than weak ones, which the
  data does not show.
- **Red rounds and white rounds:** n₁ rounds where either team drawing red gives a shot, then n₂ rounds where
  either drawing white gives a shot. With n₁ = n₂ the sum of red balls cancels, but a term depending on the product
  remains: expected total n·(1.5 − 2ab), where the urns are ½ + a and ½ + b red. Small if the match urns are near
  50% red (≈ 1.3% at 40–60%), large if they are far from it (≈ 20% at 10–30%). Rejected: it only approximates a
  tempo urn, and the red share of the match urns is not settled.
- **Counting red balls to set n₁ and n₂:** would make only the average exact, not the spread, and needs the players
  to count balls. Rejected.
- **Exactness from match urns alone is impossible:** the probability of any event built from match-urn colours
  depends on p_A and p_B, unless the event ignores the colours entirely.

Conclusion: a tempo urn, independent of the match urns, decides whether a round gives a shot. It has m\_t = μM\_t/n red
balls, so the average total is μ.

### The split only has to depend on red balls, initially

Which team gets a shot should depend on the teams' matchday red balls. Depending only on the *difference* is not
required initially; it can be adjusted once the model works. Options for deciding who gets a shot (both teams draw
from their match urns):

- **Redraw on same colour:** P(A) = p_A(1−p_B) / [p_A(1−p_B) + p_B(1−p_A)]. Depends on both values, not only the
  difference, but uses only the match urns.
- **Coin flip on same colour:** P(A) = ½ + ½(p_A − p_B), so it depends only on the difference, but adds a coin.

### Skill change is a simulation input

Phase 1 is not a random step of the model (this matters mostly for the later inference). Whoever runs the simulation sets how the red balls in each skill pool
change between matches: not at all, randomly, or by a rule. An observer who only sees shots, xG values and goals
infers m\_s with Bayes. If m\_s never changes, the posterior can get as certain as you like (e.g. 99.999%) with enough
matches. If m\_s changes, the observer must widen the posterior between matches with an assumed drift; this
assumption belongs to the inference, not to the model, and need not equal the rule the simulation used.

### Who shoots: grab k\_w balls, most red wins (phase 4)

Each team grabs k\_w balls from its match urn; the team with more red balls shoots, ties broken one ball at a time.
k\_w = 1 equals the redraw rule; a larger k\_w gives the better team a bigger share of the shots. Chosen over the
redraw and coin rules because k\_w gives a knob for how strongly skill decides the split.

### xG: the defender cancels red balls (phase 5)

The xG must depend on the defender too, since the data shows xG rising with the skill *difference*. The shooting
team draws k\_c chance balls from its match urn and the defender k\_d; the defender's red balls are removed from
the shooter's before the shot urn is filled. Considered:

- **Defender draws as many balls as the attacker:** about 60% of shots get xG = 0, and mean xG differs by a factor
  10–30 between strong and weak attackers (data: about 1.3). Rejected.
- **Defender draws fewer balls (k\_d < k\_c):** skill effect about 1.2–1.5, close to the data. Chosen. Mean xG is
  roughly the red share × (1 − k\_d/k\_c), so a mean of about 0.1 needs match urns of roughly 10–15% red.

Chance balls come from the match urn, not a separate chance urn.

### Two kinds of shots: ordinary and big chances

Real non-penalty xG has two groups: ordinary shots (about 83% between 0 and 0.15, peak near 0.03) and a second bump
of big chances at 0.3–0.6 (about 13%). Shots with xG ≥ 0.2 are only 16% of shots but carry more than half of the
total xG, so leaving them out would halve the goals. We first assumed one smooth peak; the first simulation (35% of
shots with xG = 0) made us add big chances now.

A shot is a big chance when the shooting team wins phase 4 by at least a set margin of red balls. This ties big
chances to skill: in the data, the share of shots with xG > 0.3 rises from 11% for the weakest teams to 15.5% for
the strongest. Ordinary shots and big chances differ only in their marked balls (below).

### Marked balls in the shot urn (phase 5)

Marked balls are added to the shot urn and taken out again before the other balls go back into the match urn. A
marked red ball counts as red. They avoid xG = 0 and set each kind of shot's level: marked red gives a floor, marked
white lowers the level. Caveats:

- Marked white balls lower the spread together with the mean; the drawn red balls still give the variation.
- With one marked red ball, the spread relative to the mean (sd/mean) stays below about 0.5. Real ordinary shots have
  0.64, all shots 1.34; the big chances provide the rest.
- A plain green (marked red) ball alone in a small shot urn gives a floor of about 0.17, far above the real median of
  0.06; hence the marked white balls.

### Earlier decisions

- **One skill urn per team:** attack and defence are the same skill. Separate urns would be more realistic but
  double the parameters.
- **Home advantage:** the home team gets extra matchday red balls, a parameter to calibrate.
- **Game state:** teams that lead tend to shoot less. Ignored in version 1; every round has the same probabilities
  regardless of the score.

## Accepted simplifications

### The tempo urn is fixed

A fixed tempo urn gives a binomial total with variance μ(1 − μ/n), always below the mean. The data has mean 25 and
variance 29.5; the excess is real but modest (dispersion test z ≈ 2.5 over 380 matches). Accepted for simplicity;
see "Tempo pool" under Future ideas.

### Coarse xG resolution

Only a few chance balls are drawn, so xG takes few distinct values. Marked balls removed xG = 0 and big chances add a
second peak, but within each kind of shot the values are still coarse. Accepted for the MVP.

## Open

- **Unbreakable ties in phase 4:** when both match urns hold only one colour (all red or all white), the tie-break
  can never end. The simulator currently lets a fair draw (one red, one white ball) decide; a proper rule is open.
- **Form of the xG correction.** Possible parts:
  1. League-wide calibration, e.g. logit P(goal) = a + b·logit(x).
  2. A skill effect: model xG should depend more strongly on skill than Understat's xG does.
  3. Optionally a small, team-specific residual, heavily shrunk towards zero, since most over- or under-performance
     is noise.
- **Teams that outperform (or underperform) their xG.** Some teams score more, or concede fewer, goals than their
  xG says. The end goal is to account for it, through the correction above.
- **Skill pool size M\_s:** 100 is a convenient default; confirm or pick another.
- **Per-team check of shot quality:** per team and season, correlate shots per match and mean xG per shot with a
  skill proxy (e.g. final table position). Partly answered by analysis 2.

## Future ideas

### Tempo pool for the tempo urn

To add the missing match-to-match variation in total shots, fill the tempo urn before each match by drawing M\_t balls
(without replacement) from a larger tempo pool, the same way phase 2 fills the match urn from the skill pool.

Example: n = 100 rounds, a tempo pool with 25% red balls, and M\_t ≈ 170 balls drawn for each match gives mean 25 and
variance ≈ 29.5. The variance of the total is n·Q(1−Q) + n(n−1)·Var(m\_t/M\_t), where Q is the pool's red share.

### Split depending only on the difference

Once the model works, the split could be made to depend only on p_A − p_B, e.g. with the coin flip on same colour.

## Future: inference

Not part of this project, perhaps a later one: using Bayesian inference on observations (shots, xG values, goals)
to get probability distributions over the red balls in every team's skill pool, and predictions from them. The model
must stay simple enough for this (goal 4). Notes kept from earlier design work, in the old notation (R = m\_s,
m = M\_u, k = m\_u, c = k\_c, N = M\_t, s = m\_t, M = M\_s):

**Likelihood of one match.** Given matchday strengths, the probability of the observed shots, their xG values and
the goals is:

```latex
L(D \mid k_A, k_B) = \mathrm{Bin}(T;\ n, s/N)\, \mathrm{Bin}(S_A;\ T, q_A) \prod_{j} \mathrm{Hyp}(r_j \mid m, k_{(j)}, c)\, x_j^{G_j} (1 - x_j)^{1 - G_j}
```

Here k\_(j) is the match-red count of the team that took shot j. Both shot counts and xG values carry information
about red balls.

### How likely is a red-ball difference?

The headline question is a Bayesian posterior, computed exactly by enumerating every possible pair of red-ball
counts. With M = 100 that is 101 × 101 ≈ 10,000 cells per team pair, which is trivial to compute.

**Step 1 — Marginalise matchday form.** For one match, sum over all possible match draws:

```latex
P(D \mid R_A, R_B) = \sum_{k_A=0}^{m} \sum_{k_B=0}^{m} \mathrm{Hyp}(k_A \mid R_A)\, \mathrm{Hyp}(k_B \mid R_B)\, L(D \mid k_A, k_B)
```

**Step 2 — Combine matches and prior.** If R is assumed not to change, matches are independent given skill, and
the posterior is:

```latex
P(R_A, R_B \mid D) \propto P(R_A)\, P(R_B) \prod_{\text{matches}} P(D_{\text{match}} \mid R_A, R_B)
```

With enough matches it then becomes as narrow as you like around the true red-ball counts.

If R may change, older matches say less about today's R. Before each new match, the posterior is widened with an
assumed drift kernel K (e.g. R moves ±1 ball with probability δ), and then updated with the match (forward
filtering on the same grid):

```latex
P(R_t \mid D_{<t}) = \sum_{R'} K(R_t \mid R')\, P(R' \mid D_{<t}), \qquad P(R_t \mid D_{\le t}) \propto P(R_t \mid D_{<t})\, P(D_t \mid R_t)
```

The posterior then stops narrowing at a width set by how fast R is assumed to move compared with how much each match
reveals. K is the observer's assumption, not necessarily the rule used in the simulation: too little widening makes
the inference overconfident, too much makes it more uncertain than needed.

**Step 3 — Answer the question.** Sum the posterior along the diagonal where the difference is N:

```latex
P(R_A - R_B = N \mid D) = \sum_{R_A - R_B = N} P(R_A, R_B \mid D)
```

The same table also gives P(R\_A > R\_B), credible intervals for the difference, and so on.

**Extension:** several teams playing each other: estimate all R\_i jointly. Start by holding opponents fixed at their current
best estimate and updating one team at a time.

### Open questions for inference

- **Per-shot xG or match totals?** Per-shot data gives the exact likelihood. Match totals require approximating the
  distribution of summed xG.
- Walk through the one-match likelihood equation together.

### Checking the inference

**Are its probabilities honest?** Test on matches the model was not fitted to:

- Win/draw/loss forecasts scored with log loss and ranked probability score, compared against a baseline (e.g. a
  Poisson or Dixon–Coles model, or bookmaker odds)
- Reliability: events forecast at 30% should happen about 30% of the time

**Is "X% likely that A has N more red balls" correct?** This is checked by simulation, since true red balls are
never observed:

1. Pick known R values, simulate matches, run the inference.
2. Repeat many times. An 80% credible interval for R\_A − R\_B should contain the true difference in about 80% of
   runs.
3. If coverage is too low, the model is overconfident (usually m or the assumed drift K is wrong).
