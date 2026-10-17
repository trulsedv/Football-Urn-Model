# Football Urn Model — Data Analysis

Real data used to design the model and to set what it must reproduce. The model itself is described in
[design.md](design.md); the decisions drawn from this data are in [considerations.md](considerations.md).

## Data

One season of Premier League matches (2025/26) with per-shot xG from Understat, fetched with
[soccerdata](https://github.com/probberechts/soccerdata). Per shot: match, team, home or away, xG, goal. Per team:
final points. Own goals are excluded from shots. Run with `uv run shot-counts` and `uv run shot-quality`; code in
`src/football_urn_model/`.

**Skill proxy.** For each match, d = final points of the home team − final points of the away team. Caveats: final
points include the match itself, and points are a noisy measure of skill. Both are acceptable for a first look.

## Analyses

1. **Shot counts vs d.** Bin d (e.g. 10-point bins). In each bin, look at the full distribution of home shots and
   away shots: mean, variance and histogram. This is the "3D landscape" P(k shots | d). Variance above what a
   binomial predicts indicates matchday form and informs m.
2. **Shot quality vs d.** Compare the per-shot xG distribution across bins of the shooting team's point advantage.
   Does the whole distribution shift, or only its mean?
3. **Coupling of shot counts.** Within each bin of d, correlate home shots with away shots. A negative correlation
   supports a coupled draw rule, where one team's chance is the other team's missed chance.
4. **Home advantage, by paired fixtures.** Every pair of teams meets twice, once at each ground. Skill difference
   flips sign between the two matches, but home advantage does not, so averaging cancels skill:

   ```latex
   H = \tfrac{1}{2}\big[(s_A^{\text{home}} - s_B^{\text{away}}) + (s_B^{\text{home}} - s_A^{\text{away}})\big]
   ```

   Here s is shots in that match. Averaging H over all 190 pairs gives the home effect on shots. The same works for
   xG. Half the difference of the two brackets gives the skill effect for that pair.
5. **Sanity check.** Total xG over the season should be close to total goals, confirming xG behaves as a
   probability.

## Results

- **Analysis 1 — shot counts vs d (`shot_counts.py`).** The total number of shots in a match varies randomly
  around ~25 and does not depend on d. The skill difference decides how those shots are split: the better team gets
  the larger share (home shots rise from ~9 at d ≈ −40 to ~17 at d ≈ +30, away shots fall from ~14 to ~8). Home
  teams shoot more at equal skill (~14 vs ~10 at d ≈ 0). The total does not depend on the sum of the two teams'
  final points either (correlation 0.02; mean ≈ 24–27 shots from 60 to 140 points), so the number of shots in a
  match seems independent of the teams' skill altogether. No more shot-count analysis is planned for now.
- **Analysis 2 — shot quality vs d (`shot_quality.py`).** Better teams get better chances, and the whole xG
  distribution shifts, not only its mean. Binning shots (penalties excluded) by the shooting team's points
  advantage, from < −30 to > 30: mean xG per shot rises from 0.101 to 0.131, every quantile rises by roughly 20–35%
  (median 0.054 → 0.066, 90th percentile 0.33 → 0.41), and the share of shots with xG > 0.3 goes from 11% to
  15.5%. The effect is much smaller than for shot counts (a team's shot share roughly doubles across d, xG per shot
  rises by about a third), so most skill information is in how many shots a team gets, and some is in how good they
  are. Caveats: game state (a leading team may get better chances on the counter), home and away mixed, and final
  points as a noisy skill proxy.
- **Analysis 5 — sanity check, xG vs goals. Fails.** Understat's xG is too high for 2025/26. Non-penalty shots:
  1,114 xG but 927 goals (17% fewer). Penalties: 70 xG, 77 goals. Shots with xG between 0.1 and 0.7 convert
  clearly below their xG (e.g. 0.4–0.7: mean xG 0.52, goal rate 0.39). The reason is unknown; comparing with
  earlier seasons would show whether it is Understat's model or an unusual season.

## What the model must reproduce

1. **Total shots per match:** mean ≈ 25 (24.96), variance ≈ 29 (29.46), range 11–42 over 380 matches. The total
   does not depend on the teams' skill, and its distribution should look like the real one.
2. **Split between the teams:** depends on each team's matchday red balls; the better team gets the larger share.
3. **xG per shot:** random, with higher values for the better team. The distribution should look like the real one
   (most shots below 0.1, median ≈ 0.06, about 13% above 0.3).
