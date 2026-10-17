# Football Urn Model — Design Considerations

What we have considered while designing the model, and what we concluded. [design.md](design.md) describes the
system itself; this file records why it looks the way it does, what is still open, and ideas for later. Data
results are in [data-analysis.md](data-analysis.md).

## Decided

### The model must be physically playable

Every random step is a draw of balls from an urn, so a match could be played with real urns and balls. No step may
use a fitted function or a continuous distribution. This replaced the earlier layer 4, where xG was drawn from a
fitted distribution f(x).

### Correcting xG data is outside the model

A data source's xG comes from its own model and can be biased: Understat's xG is 17% too high for 2025/26
(analysis 5). Each data source therefore needs its own correction that turns its xG into model xG:

data source → correction → model inference → skill difference

The correction is not part of the model, so it does not have to be playable and may use fitted functions.

### Finishing is part of skill

A better team should create more and better chances, and also convert them better. This is why xG in the model
comes from the team's own balls, and why model xG should depend more strongly on skill than Understat's xG does
(Understat does not know who shoots or who is in goal).

### Shot quality depends on skill

Analysis 2 shows the whole xG distribution shifts with skill. Without this, xG values would carry no information
about red balls, only shot counts would. Drawing chance balls from the team's own urn (layer 4) makes shot quality
depend on skill by construction.

### The total number of shots comes from a tempo urn

The data shows that the total number of shots in a match (mean ≈ 25, variance ≈ 29) depends neither on the
difference nor on the sum of the two teams' final points. Options considered:

- **Combined urn:** pour both match urns together and draw; a red ball is a shot for its owner. Rejected: the
  total then depends on the sum of red balls, so strong pairs of teams would shoot more than weak ones, which the
  data does not show.
- **Red phases and white phases:** n₁ phases where either team drawing red gives a shot, then n₂ phases where
  either drawing white gives a shot. With n₁ = n₂ the sum of red balls cancels, but a term depending on the product
  remains: expected total n·(1.5 − 2ab), where the urns are ½ + a and ½ + b red. Small if the match urns are near
  50% red (≈ 1.3% at 40–60%), large if they are far from it (≈ 20% at 10–30%). Rejected: it only approximates a
  tempo urn, and the red share of the match urns is not settled.
- **Counting red balls to set n₁ and n₂:** would make only the average exact, not the spread, and needs the players
  to count balls. Rejected.
- **Exactness from match urns alone is impossible:** the probability of any event built from match-urn colours
  depends on p_A and p_B, unless the event ignores the colours entirely.

Conclusion: a tempo urn, independent of the match urns, decides whether a round gives a shot. It has s = μN/n red
balls, so the average total is μ.

### The split only has to depend on red balls, initially

Which team gets a shot should depend on the teams' matchday red balls. Depending only on the *difference* is not
required initially; it can be adjusted once the model works. Options for deciding who gets a shot (both teams draw
from their match urns):

- **Redraw on same colour:** P(A) = p_A(1−p_B) / [p_A(1−p_B) + p_B(1−p_A)]. Depends on both values, not only the
  difference, but uses only the match urns.
- **Coin flip on same colour:** P(A) = ½ + ½(p_A − p_B), so it depends only on the difference, but adds a coin.

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

## Open

- **Split rule:** redraw or coin flip on same colour.
- **Where chance balls come from, and how many (c):** the match urn or a separate chance urn. Real xG is mostly
  below 0.1, which would need match urns of about 10% red if chance balls come from the match urn. With a tempo urn
  for the total, layer 3 no longer needs match urns near 50% red, so this is not ruled out. Check against the
  per-shot xG data.
- **Form of the xG correction.** Possible parts:
  1. League-wide calibration, e.g. logit P(goal) = a + b·logit(x).
  2. A skill effect: model xG should depend more strongly on skill than Understat's xG does.
  3. Optionally a small, team-specific residual, heavily shrunk towards zero, since most over- or under-performance
     is noise.
- **Teams that outperform (or underperform) their xG.** Some teams score more, or concede fewer, goals than their
  xG says. The end goal is to account for it, through the correction above.
- **Per-shot xG or match totals?** Per-shot data gives the exact likelihood. Match totals require approximating the
  distribution of summed xG.
- **Pool size M:** 100 is a convenient default; confirm or pick another.
- **Per-team check of shot quality:** per team and season, correlate shots per match and mean xG per shot with a
  skill proxy (e.g. final table position). Partly answered by analysis 2.
- **Later:** walk through the one-match likelihood equation together.

## Future ideas

### Tempo pool for the tempo urn

To add the missing match-to-match variation in total shots, fill the tempo urn before each match by drawing N balls
(without replacement) from a larger tempo pool, the same way layer 2 draws match balls from the skill pool.

Example: n = 100 rounds, a tempo pool with 25% red balls, and N ≈ 170 balls drawn for each match gives mean 25 and
variance ≈ 29.5. The variance of the total is n·Q(1−Q) + n(n−1)·Var(s/N), where Q is the pool's red share.

### Split depending only on the difference

Once the model works, the split could be made to depend only on p_A − p_B, e.g. with the coin flip on same colour.
