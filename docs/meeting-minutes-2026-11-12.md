# Meeting minutes: urn model design discussion

**Date:** 12 November 2026  
**Form:** voice call, Truls thinking aloud with Claude responding; followed by a text session to file the results  
**Present:** Truls Edvardsen Aarønes, Claude  
**Purpose:** set the structure of a written account of the urn model, and settle the inference approach

Full reasoning for each item is in [discussion-notes-2026-11-12.md](discussion-notes-2026-11-12.md). The chapter outline is in [report-outline.md](report-outline.md).

## How the conversation went

1. **Opening.** Truls set out what he wanted: a monologue on the model, checked for consistency, then a dialogue, then something written down as the start of a pamphlet or book. The arc was: a theory of football, its simplification into a model, inference of skill from observations, probabilities for future matches and seasons, betting as an application.
2. **Theory of randomness.** He named injuries and between-game change as the first source of uncertainty, then in-game randomness, then added match-day form as a third. He gave the tactical-mismatch example; Claude flagged it as a pairwise effect rather than noise, and he agreed to state it as a simplification.
3. **xG as the observable.** He gave his hypothesis that xG converges faster than goals. Claude raised the two caveats (xG-model error, finishing as skill); he agreed both should be written down and said both can be corrected statistically.
4. **Result probabilities from xG.** He described removing a shot's outcome and simulating the rest of the game. Claude connected it to expected points and noted his version adds game-state effects, which he then said the first model excludes.
5. **Inference, first attempt.** He proposed going from prior skill and xG to win/draw/loss probabilities, then inferring red balls from those. Claude pushed back: the three probabilities lose the totals. He asked how to use the xG data directly and was not sure how.
6. **Inference, worked through.** Claude explained the forward-only Bayesian update in steps: likelihood of the observed xG given a ball count, times prior, normalised. He rephrased it back twice, landed on "I only need to calculate all possible outcomes given a set of red balls", and asked for the formula. He said the formula was the point where it became understandable.
7. **Observables.** Claude proposed four (shots and xG per team); he pointed out total shots carry no skill information in his model, leaving three. He asked whether summing xG loses information (yes) and whether shot-by-shot needs a bigger table (no); Claude walked through the per-shot histogram with a four-shot example.
8. **Resolution against variance.** He raised that the early model had few balls to get the variance right and that he wants higher resolution. Claude separated the two dials; he confirmed the direction and asked about the limits. He marked this as an important design section.
9. **Fitting done so far.** He described the Claude Code session: mean, variance and skew per observable on a sum/difference grid, Premier League, three seasons, final points as proxy. He corrected Claude from position to points. He said shot count was the one observable that did not move with skill, which is why the neutral urn exists. Claude suggested attacker/defender axes for xG per shot; he leaned towards home/away for everything.
10. **Structure versus calibration, and validation.** He said the fitting only set structure and calibration needs its own design. He described the synthetic-season validation plan. Claude distinguished tuning the inference from validating the mechanics; he accepted it. He said parameters are frozen for the first year and, after Claude's caution about chasing noise, dropped the xG corrections from the first version.
11. **Form and title.** He rejected "report" and "further work"; after several candidates, the title does the work and the last chapter is "Known limitations". He checked the chapter order and agreed Inference stays before Validation, with one worked cell in chapter 6 and full tables in chapter 7.
12. **Tooling.** He asked about Cowork, then Claude Code from the phone with GitHub access. Agreed: a text session writes the notes, Claude Code drafts chapters from the repo.
13. **Text session.** Claude wrote the discussion notes and the outline, found the repo, and opened pull request 1. Truls asked the Claude Code brief to state the scope increase to include inference, then asked for these minutes.

## Decisions

| # | Decision | Section in notes |
| --- | --- | --- |
| D1 | The written account will be a finished, self-contained document, not a growing report. Working title "The urn model of football", subtitle along the lines of "Theory, mechanics and inference". No genre word in the title. | 12 |
| D2 | The last chapter is "Known limitations", not "Further work". | 12 |
| D3 | Nine chapters in the order: Introduction, A theory of football, From theory to model, Model mechanics, Fitting the structure, Inference, Validation, Use, Known limitations. Inference stays before Validation. | 12 |
| D4 | The theory chapter names three layers of randomness: between-game skill drift, match-day form, in-game chance. Tactical mismatch between specific opponents is treated as noise, stated as a deliberate simplification. | 2 |
| D5 | xG, not goals, is the observable the model is fitted to. | 3 |
| D6 | The first version applies no corrections to observed xG: neither per-team finishing nor xG-provider error. Measured xG is taken as true xG. Both corrections go under known limitations. | 3 |
| D7 | The first model has no game-state effects: teams do not play differently depending on the score. | 5 |
| D8 | Inference is a forward-only Bayesian update. For every candidate pair of red-ball counts, compute the likelihood of the observed match, multiply by the prior, normalise. Outcome probabilities (win, draw, loss) are an output of the model, not an input to inference. | 6 |
| D9 | The per-match observation is three numbers: home shot share, home xG, away xG. Total shot count is dropped because tempo is independent of skill in the model. Shot-by-shot xG is the refinement. | 6.4, 6.5 |
| D10 | Likelihoods come from a precomputed lookup table indexed by home and away red balls, computed exactly from the urn mechanics rather than by simulation. | 6.6, 8 |
| D11 | The resolution-versus-variance tension (ball count sets resolution, number drawn sets variance) gets its own treatment in the design chapter. | 9 |
| D12 | Each phase of the model gets the same chapter template: mean, variance and skew of the observable, and how they change with skill. | 10 |
| D13 | The document will say up front that the data fitting done so far set the model's structure only; parameter calibration is a separate, later step. | 11 |
| D14 | Validation is a synthetic study: about twenty teams, thousands of matches, known red-ball counts drifting along slow curves; the inference is judged by how well it recovers them. | 11 |
| D15 | Model parameters are frozen for roughly the first year of use. | 11 |
| D16 | Project scope widens to include inference, which `design.md` currently excludes. | (text session) |

## Points noted, not decided

| # | Point | Section in notes |
| --- | --- | --- |
| N1 | Skill axes for the fitting chapter: switch from sum/difference to home/away points for all observables, or only to attacker/defender for xG per shot. | 10 |
| N2 | Whether a finishing correction, when added, belongs inside the model as an inferred parameter or outside as preprocessing. | 3 |
| N3 | Concrete urn and draw sizes that raise xG resolution while keeping variance; whether real variance exceeds the single-draw ceiling. | 9 |
| N4 | Binning rule for continuous observed xG onto the discrete ratios the urns produce. | 6.5 |
| N5 | Skill drift model between matches: how the next prior is formed from the last posterior. | 13 |
| N6 | The formula treats the two teams' priors as independent; the correlation introduced by each update is dropped. | 13 |
| N7 | Design of the parameter calibration step. | 11 |

## Corrections made during the discussion

- Inference by way of outcome probabilities was proposed, then dropped in favour of the direct likelihood of the xG data (D8).
- Four observables per match were proposed; total shot count was removed, leaving three (D9).
- Total xG was noted to lose information relative to shot-by-shot xG; the table does not grow when going shot-by-shot, since each cell holds a per-shot histogram and shots are independent.
- Several seasons were pooled in the fitting (three) after noting that the corner cells of the skill grid were thin.
- The spoken description of the mechanics used "neutral urn" for what the README calls the tempo urn, and was from memory; the README and `design.md` are the authority.

## Actions

| # | Action | Owner | Status |
| --- | --- | --- | --- |
| A1 | Write the chapter outline. | Claude | Done: `docs/report-outline.md` |
| A2 | Write up the full discussion. | Claude | Done: `docs/discussion-notes-2026-11-12.md` |
| A3 | Put both files in the repo. | Claude | Done: pull request 1, branch `docs/urn-model-book-outline` |
| A4 | Review and merge pull request 1. | Truls | Open |
| A5 | Start a Claude Code session with the agreed brief: update the scope line in `design.md`, then draft chapter 4 from the README and `design.md`. | Truls | Open |
| A6 | Decide N1 before chapter 5 is drafted. | Truls | Open |
| A7 | Add these minutes to `docs/` as `meeting-minutes-2026-11-12.md`. | Claude | Done: pull request 1 |
