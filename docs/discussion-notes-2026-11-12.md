# Discussion notes: voice session, 12 November 2026

These notes record a spoken design discussion between Truls and Claude about the urn model of football. They are written for whoever drafts the document outlined in [report-outline.md](report-outline.md), and they keep the reasoning, the corrections made along the way, and the points that are still unsettled. Where something was Claude's suggestion and not Truls's decision, it is marked as such.

## 1. What the document is for

The document should explain the model from first principles to practical use. The arc Truls described is: a theory of how football works; how that theory is simplified into a model; how the model is used on real match observations to estimate each team's skill over time, with uncertainty; and how those estimates give probabilities for future matches and final league standings. Betting is one possible application.

## 2. Theory: where randomness enters

The theory must say at which steps randomness occurs. Three layers were identified.

- **Between games: skill drift.** A team's true skill changes slowly through injuries, improvement and form. Truls noted this is perhaps better called unmeasurable than random; either way it has to be approximated.
- **Match-day form.** For each match, a team's effective strength is a random draw around its underlying skill. A good team can look bad, and be bad on the day, without being a bad team on average. Causes include a player having an off day or a late injury.
- **Within the game.** Given the match-day strength, the events of the game are themselves random.

Match-day form and in-game randomness are distinct in theory but hard to separate in data. Only one result per game is observed, so the model may not be able to tell them apart. The document can state the distinction anyway.

Tactical mismatch is treated as noise, by choice. Truls's example: a team that is much better on average may not show it against a specific opponent because the two game plans are incompatible. Claude pointed out that this differs in kind from a bad day: it is a pairwise effect depending on the opponent, not noise around a team's own level. Truls agreed it is important to state explicitly that folding it into noise is a simplification.

The principle that follows: a single match is a noisy measurement of skill, not a revelation of it.

## 3. xG as the observable

The model is fitted to xG data and not to goals. Truls's hypothesis is that xG gives the estimation loop far more signal per match, so the skill estimate converges faster. Goals give one outcome per match, and that outcome is mostly randomness layered on top of the xG.

Two caveats were agreed as important to write down.

1. **xG is itself a model's output.** Errors and provider differences in the xG model are inherited unless accounted for.
2. **Finishing may be partly skill.** Higher-skill teams may convert chances better than their xG says. Fitting only to xG assumes finishing is random and discards that part.

Truls's view is that both can be corrected statistically. Claude's sketch: xG error as a measurement-noise term with its own variance, and finishing as a per-team conversion factor estimated from goals against xG. A design choice was raised but not made: whether a finishing correction lives inside the model as an inferred parameter (cleaner, gives uncertainty) or outside as preprocessing on the xG (simpler, leaves the urn model untouched).

Decision for the first version: no corrections. Claude cautioned that over a season, finishing over- or underperformance is mostly noise, and a correction that chases it does more harm than good. Truls decided to skip both corrections for now. The first version therefore has one clear assumption, that measured xG is taken as true xG, and the corrections are listed as known limitations.

## 4. Result probabilities from xG

Truls wants the probability of each result given a match's xG, not only the result that happened. His idea: take an observed shot, remove the fact that it did or did not go in, and simulate the rest of the game with the opposite outcome.

This is close to the existing "expected points" method, with an extension. In expected points, each shot is a coin flip with its xG as probability; resampling all shots many times gives a distribution of results. A simpler baseline when only totals are known is a Poisson distribution on each team's total xG. Truls's version goes further by letting the game continue differently after a flipped shot, which would capture game-state effects.

In the first model the extension collapses to the simple version. Because game state does not affect play (section 5), the rest of the game is unaffected by a flipped shot. The resimulated version only becomes different once game-state effects are added.

## 5. No game-state effects in the first model

Teams do not play differently depending on the score. Truls stated this as a deliberate property of the initial model. It is also what makes exact computation possible (section 9), since every round is then identical and independent.

## 6. Inference: how the skill estimate is updated

This was the longest thread, and the approach changed during it.

### 6.1 The first idea, and why it was dropped

Truls's initial pipeline went through outcome probabilities. Use the prior skill estimates and the match's xG to compute the probabilities of home win, draw and away win, then use those three numbers to infer how likely a given red-ball count is.

Claude argued this throws away most of the information xG was chosen for. Many different xG pairs give similar outcome probabilities, so the totals cannot be recovered from them. Truls restated it with his own example: 1.0 against 0 xG and 5 against 4 xG could give similar result probabilities, and the information about totals is then lost. (Under Poisson the two are not identical, since 1 against 0 gives far more draws, but the principle holds.) A team creating five xG says something that a team creating one does not. The three outcome probabilities are a product of the model, not an input to the inference.

### 6.2 The approach settled on: forward-only Bayesian update

The inference only ever runs the model forwards. The question asked is not "given this match, what is the skill?" directly. It is: "if the home team has $h$ red balls and the away team has $a$, how likely is this observed match?" That is asked for every combination. Each answer is multiplied by how likely that combination was believed to be before kick-off, and the results are normalised. Truls's own summary: no reverse mathematical simulation is needed, only the forward calculation for every set of red balls.

Several observations are combined in one update, not several. Truls asked how to weight four observables that might each pull the distribution differently. The answer: the model predicts all of them together, and the likelihood is the probability of seeing all of them at once. Treating them as conditionally independent given skill, this is the product of the individual likelihoods. Weighting then needs no hand-chosen numbers: an observable the model predicts sharply moves the posterior a lot, a noisy one barely moves it.

### 6.3 The formula

With $h$ and $a$ the home and away red-ball counts, and $D$ the observed match:

$$
P(h=6 \mid D) = \frac{\pi_H(6)\,\sum_{a} \pi_A(a)\,L(6,a)}{\sum_{h}\sum_{a} \pi_H(h)\,\pi_A(a)\,L(h,a)}
$$

- $\pi_H(h)$, $\pi_A(a)$: each team's prior probability of that ball count before the match.
- $L(h,a) = P(D \mid h,a)$: the likelihood of the observed match given that pair, read from the lookup table.

The numerator is the "six" row weighted by the away team's prior; the denominator is the same sum over the whole table. A correction made during the call: the distributions held before the match are the prior, and the posterior is what comes out. Because the teams are separate, the prior for a pair is the product of the two teams' priors (2% and 2% gives 0.04% for six against six).

### 6.4 Which observables

The observables form a ladder, each rung using more of the data.

1. Results only.
2. Total xG per team.
3. Shots plus xG per team.
4. Shot by shot.

Total shot count was dropped as an observable. Claude first proposed four numbers: shots and xG for each team. Truls pointed out that in this model the total number of shots does not depend on skill, because the neutral urn sets tempo. So the observation for one match is three numbers: home shot share, home xG and away xG. This is a known simplification, since in real football total shots do vary with the teams.

Shot count and xG together separate volume from quality. Ten shots of 0.1 and two shots of 0.5 have the same total xG, but the model treats them differently: the macro level decides how often a team shoots, the micro level how good the shot is.

### 6.5 Shot-by-shot likelihood

Summing xG loses some information, and the shot-by-shot version recovers it without a larger table. Truls asked whether the sum loses information (yes: five shots at 0.2 and one at 1.0 have the same total) and whether a much larger table would be needed (no). Each table cell holds, per team, a histogram of per-shot xG values: the probability that a shot by that team has each possible xG. Shots are independent in the model, so the likelihood of a list of shots is the product of each shot's probability under the histogram, times the shot-share term. Longer lists mean more multiplications, not bigger tables.

A worked example, with invented numbers. In the six-against-six cell, suppose the home histogram gives 0.03 xG a probability of 0.2, 0.1 a probability of 0.3, 0.3 a probability of 0.15, and 0.7 a probability of 0.05. Home shots of 0.03, 0.3, 0.1 and 0.7 then have likelihood 0.2 × 0.15 × 0.3 × 0.05. The away list is treated the same way against the away histogram, and the two are multiplied with the shot-share probability to give $L(6,6)$.

The histogram comes straight from the mechanics. For a given pair of match urns, enumerate every way the attack-versus-defence draw can go. Each path has a known probability and ends in a specific shot urn with a specific red-to-white ratio, which is the xG. Group the paths by ratio and add the probabilities. Real xG values are continuous, so an observed value has to be binned to the nearest ratio the urns can produce.

### 6.6 The lookup table

Truls wants a mathematical representation of the model so that the table can be computed, not simulated. The table is indexed by home red balls and away red balls. Each cell holds what is needed to price a match: the shot-share distribution and the xG distribution for each team (totals, or per-shot histograms). With ball counts from 1 to 20 that is 400 cells, computed once; each match update is then lookups and multiplications.

## 7. Model mechanics as currently stated

Truls described the current mechanics from memory and said he did not remember the later steps exactly. The exact rules are in the [README](../README.md) ("How to play") and [design.md](design.md); where this list differs, those are right. The "neutral urn" of this conversation is the tempo urn there.

1. **Skill pool.** Each team has a pool of red balls representing its true underlying skill.
2. **Match urn.** Before the match, a draw from the skill pool fills the team's match urn. This is the match-day form layer.
3. **Home advantage.** The home team gets a few extra red balls in its match urn, marked as home advantage so they can be removed cleanly afterwards.
4. **Shot or no shot.** Each round, a ball is drawn from a neutral urn that decides whether there is a shot that round. This is independent of skill.
5. **Who gets the shot.** Each team draws from its match urn to decide which team gets it.
6. **Chance quality.** The attacking team then draws more balls than the defending team, and these fill a shot urn. Attacker red balls may be removed depending on how well the defence did. A standard number of balls is added depending on whether it is a "big chance" or a "normal chance": a big chance, from a poor defence or a very good attack, gives a higher share of red balls (possibly also by controlling the number of white balls).
7. **xG.** The red-to-white ratio in the shot urn is the shot's xG.
8. **Goal.** A draw from the shot urn decides whether it is a goal.

Claude's mapping onto the theory: the neutral urn is tempo, the match-urn contest is who creates, the attack-versus-defence draw is chance quality, and the shot urn is the xG.

## 8. Computing the model without simulation

The model can be computed exactly from the two skill-pool counts. Truls first thought each round would have to be simulated. It does not, precisely because game state is excluded: every round is identical and independent. Only one round needs working out: the probability that it produces a home shot, an away shot or nothing, and for each shot the distribution over shot-urn ratios. That is a finite enumeration of urn draws. A full match is then a fixed number of independent rounds, giving a binomial on shot counts and a sum of independent per-shot xG values. The match-urn draw is summed over as one more layer: for each possible match urn, compute the above, and weight by the probability of that match urn given the skill pool.

## 9. Resolution against variance

This is to be an important part of the design chapter. The first version of the model had few balls in the match urns and shot urns, so the resolution of xG values was low. Truls believes that was chosen to get the right amount of variance. He wants to raise the resolution while keeping the variance.

The two can be controlled separately. The number of balls in an urn sets the resolution, meaning which ratios are possible. The number of balls drawn sets the variance: drawing one ball from a fixed ratio is a coin flip with maximal variance, while drawing many and taking the proportion converges on the true ratio. Truls confirmed the direction: more balls drawn, less variance.

There are limits in both directions.

- **Variance has a ceiling.** One ball drawn is as noisy as it gets. If real football is noisier than that, another mechanism is needed, such as randomising the ratio itself.
- **Resolution has a cost.** More balls means more paths to enumerate for the table.

The reason this matters: the model's variance must match what real football shows, or the inference will be over- or under-confident.

## 10. Structure fitting done so far

In an earlier Claude Code session, real data was used to shape the model phase by phase. Claude could not see that session; this is Truls's account of it.

- **Method.** For each observable, look at its mean, variance and skew, and build mechanics that reproduce them. Then look at how those three moments change with skill.
- **Data.** Premier League matches, three seasons (expanded from one for sample size).
- **Skill proxy.** Each team's final points total for the season. (Not league position.)
- **Skill axes.** The sum of the two teams' points and the difference, each split into three buckets, giving a three-by-three grid: nine means, nine variances and nine skews per observable.
- **Observables fitted.** Total shots per game; home and away shot share; the xG distribution.

The shot count did not move with skill, and that is why there is a neutral urn. It was the one observable whose moments were flat across the grid. The data drove the design choice.

Caveats on this analysis, raised by Claude and accepted as minor:

- Final points include the matches being fitted, so the proxy is slightly circular, and points are noisy themselves.
- Corner cells of the grid are thin (few matches between two top or two bottom teams). A smooth trend across the grid would be more robust than nine independent cells.
- Points are not strictly comparable across seasons when pooled into one bucket. The difference is less affected than the sum. With three seasons of one league this is a sentence in the caveats, not a redesign.

Possible change to the axes, not yet decided. Every observable was examined against sum and difference only. Claude noted that sum and difference span the same space as home and away points, so nothing is lost, but that for xG per shot the natural split is attacking team against defending team, since the mechanics have the attacker drawing and the defender removing balls. Claude suggested redoing only that one, grouped by the shooting team's points and the conceding team's points. Truls then leaned towards using home and away points for all observables, for a uniform template. Which of the two to do is open.

Chapter template. Truls wants one section per model phase, each showing the same things: the observable's mean, variance and skew, and how they change with skill.

## 11. Structure, calibration and validation

The fitting so far set the structure of the model, not its parameters. Truls wants this said clearly at the start of the design chapter. The moments against a crude skill proxy show which mechanics to include; fine-tuning the parameters is a separate step that still needs a design.

The validation plan is a synthetic study. Truls's plan:

1. Simulate thousands of matches between about twenty teams. Not seasons, only a large number of matches.
2. Give each team a known number of red balls in its pool, changing slowly: probably sinusoids with different periods, amplitudes and phase shifts.
3. Run the skill inference on the simulated matches to get skill distributions per team.
4. Tune the inference so that it best recovers the known red-ball counts.

What this does and does not show. Claude's distinction, which Truls accepted: the study tunes the inference (the drift model, how fast beliefs move, how uncertainty is handled) under conditions where the forward model is correct by construction. It cannot show whether the urn mechanics match real football. That is a separate question, answered only against real matches.

Parameters are frozen for the first year. Truls does not plan to recalibrate the model parameters during roughly the first year of use. The only calibration against real matches he had considered was the xG corrections, which are now deferred (section 3).

Claude's suggestion for later calibration, not adopted or discussed further: the structural parameters could be fitted by maximising the likelihood of all observed matches across a league with skill integrated out, which would not need the points proxy at all.

## 12. Form and title of the document

It is a finished, self-contained account, not a report that keeps growing. Truls rejected "report" because it implies reporting on an event, and rejected a "further work" framing because the document should not argue that work must continue. "Design document", "model specification", "model description" and "monograph" were all considered and set aside.

- **Title:** "The urn model of football", with a subtitle such as "Theory, mechanics and inference". No genre word.
- **Last chapter:** "Known limitations": what someone continuing the work could look into.

Chapter order was checked. Truls asked whether Inference (6) and Validation (7) should swap. They stay as they are: the validation tests the inference, so the reader needs the inference first. The document alternates idea and evidence: mechanics (4) then fitting (5), inference (6) then validation (7). Chapter 6 shows that the table can be built and how, with one small worked cell (six against six). Full example tables belong in chapter 7.

Writing preference for all drafted prose: the first sentence of each paragraph tells the reader what to expect, so the text can be skimmed.

## 13. Open questions

These points were raised and not settled, or need checking.

1. **Exact mechanics after "who gets the shot".** Section 7 is from memory. How many balls each side draws, how defender success removes attacker balls, and how big and normal chances set the shot urn must be taken from the README and design.md, not from section 7.
2. **Number of rounds per match.** Ninety was used in conversation as shorthand; the actual number is the n of design.md.
3. **Skill axes for the fitting chapter.** Home and away points for everything, or attacker and defender points for xG per shot only (section 10).
4. **How to raise resolution while keeping variance.** The principle is agreed (section 9); the concrete urn sizes and draw sizes are not.
5. **Whether real match variance exceeds the single-draw ceiling.** If so, a further mechanism is needed.
6. **Binning of observed xG.** Observed xG is continuous and the urns produce a discrete set of ratios; the binning rule is undecided.
7. **Skill drift model for the inference.** How the prior for the next match is formed from the last posterior was not discussed beyond "skill changes slowly".
8. **Parameter calibration design.** Acknowledged as needed, not designed (section 11).
9. **Independence of the two teams' priors.** The formula multiplies the two teams' priors. This was assumed, not discussed. (Note from Claude: after an update the two teams' beliefs are correlated, and keeping only each team's own distribution drops that. Probably fine, but worth a sentence.)
10. **Game-state effects.** Excluded from the first model; Truls has an outcome calculation for changing game states from an older project that could be used later.
