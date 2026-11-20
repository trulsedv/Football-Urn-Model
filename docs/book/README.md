# The urn model of football

*Theory, mechanics and inference*

This folder holds the book, one file per chapter. The book is meant to become the source of truth for the model: the
rules, the reasoning behind them, the inference and the fit to real data. The rest of the documentation should end up
following it or pointing to it.

## Chapters

| # | Chapter | File | Status |
| --- | --- | --- | --- |
| 1 | Introduction | – | Not started |
| 2 | A theory of football | – | Not started |
| 3 | From theory to model | – | Not started |
| 4 | Model mechanics | [04-model-mechanics.md](04-model-mechanics.md) | First draft |
| 5 | Inference | [05-inference.md](05-inference.md) | First draft |
| 6 | Fitting method | [06-fitting-method.md](06-fitting-method.md) | First draft |
| 7 | Fitting to real data | [07-fitting-to-real-data.md](07-fitting-to-real-data.md) | Stub: planned sections |
| 8 | Use | – | Not started |
| 9 | Known limitations | – | Not started |
| A | Appendix: computation | [A-computation.md](A-computation.md) | First draft |
| B | Appendix: starting point and checks on simulated data | [B-starting-point-and-checks.md](B-starting-point-and-checks.md) | Stub: plan and values now |

The order after chapter 4 was changed in [issue #4](https://github.com/trulsedv/football-urn-model/issues/4).
Simulated matches cannot fit the model to real football, so the parameters are fitted to real data, and that has to
come after the inference, since skill is not observed. Chapter 5 is the inference. Chapter 6 is the method of the fit:
the error function and how to minimise it. Chapter 7 runs it on real data and reports the numbers. Appendix B holds the rough
fit of the mean, variance and skewness of each step, which is the starting point (B.1), a test on simulated data of
which parameters the fit can recover (B.2), and the check of the inference on simulated matches, run with the fitted
parameters (B.3).

## Conventions

- **No values in the theory.** Chapters 4 to 6 are written in symbols and hold for any parameter values. Concrete
  values first appear in chapter 7, where they are fitted.
- **What, not how.** The theory chapters say what is computed. How it is computed exactly and cheaply is in
  appendix A.
- **Assumptions.** Each assumption is stated once, as a paragraph starting "**Assumption (name).**". Chapter 9 lists
  them all, with how each is checked.
- **Every number is reproducible.** Every number in chapter 7 and the appendix comes from a command in the repo.
  The equations of chapter 5 are checked by `uv run python scripts/check_chapter5.py`, which uses the parameters in
  `model_settings()` and so reruns when they change.
- **Theory, then doing.** Chapter 6 decides how the fit works and which parameters are fixed by design; chapter 7
  only runs it, states the fixed values and reports the numbers.

## To do: revise the documentation around the book

The documentation was written before the book existed, so parts of it duplicate the book or disagree with it. Each
item below is to be decided or done as the chapters are written.

- [ ] **Decide which documentation files are needed.** With the book as the source of truth, the likely set is:
  the root README for what the project is and how to run it, the book, and at most one file of working notes. Decide
  whether `docs/design.md`, `docs/considerations.md` and `docs/data-analysis.md` survive, merge into chapters or
  become working notes.
- [ ] **One place for the rules.** The root README ("How to play") and chapter 4 both state the rules. Make the
  README a short summary that points to chapter 4, or drop the rules from it, so they cannot drift apart.
- [ ] **`docs/design.md`.** Its phase chapters (Shot, Attack/defend, xG, Goal, Result) are the material for chapter
  7, and its equations overlap chapter 4. Decide whether it becomes part of chapter 7 or stays as working notes that
  chapter 7 draws on, and remove the equations that chapter 4 now defines.
- [ ] **Fix the inference scope in `docs/considerations.md`.** The section "Future: inference" opens with "Not part
  of this project, perhaps a later one", which contradicts goal 4 in `design.md`. Rename the section (for example to
  "Inference") and replace that sentence with one saying that inference is part of this project.
- [ ] **`docs/considerations.md`, the rest.** Its decided choices and accepted simplifications are material for
  chapters 3 and 9, and its inference notes for chapter 5. Move them as those chapters are written.
- [ ] **`docs/data-analysis.md`.** The data and figures behind chapter 7. Decide whether chapter 7 cites it or
  absorbs it.
- [ ] **Outline, discussion notes and minutes** (`docs/report-outline.md`, `docs/discussion-notes-2026-11-12.md`,
  `docs/meeting-minutes-2026-11-12.md`, in `docs/`). These are working material for the book. Decide whether
  they stay in `docs/` as a record once the chapters exist, or move to an archive folder.
- [x] **Update the outline** (`docs/report-outline.md`). Done for the new chapter order of issue #4: chapters 3 to
  7 rewritten, and "neutral urn" renamed to "tempo urn".
- [ ] **Decide how the combined equations are handled.** Chapter 4 gives each step given the outcome of the step
  before, and never combines them. Chapter 5 combines them numerically: the likelihood is a weighted sum over the
  match urns of products over the shots (sections 5.3 and 5.4). Open: whether closed-form combined equations are
  needed anywhere else, for the rough fit of chapter 7 or the result probabilities of chapter 8, or whether combining
  numerically is enough everywhere. If numerically is enough, drop the list of closed forms under chapter 7 below.
- [ ] **Rerun `uv run calibrate` after the redraw rule.** The redraw raises the big-chance share (about 1.7 times
  in the former running example of chapter 4, commit `2481745`), which moves xG and goals per
  match, and `calibrate` fits `marked_white` against goals per match. `uv run chapters` can wait: the figures it gives `docs/design.md` (total shots, home share
  of shots) barely move, so rerun it when the xG and goal chapters are filled in.
- [ ] **Notation.** Chapter 4 uses a revised set of symbols: $K$ and $k$ for drawn balls and the red among them, $X$
  and $x$ for marked balls, subscripts $s$, $a$ and $d$ for the shot, attack and defence draws, $N$ for shots, $p_t$
  for the shot probability per round, and $H$ and $A$ for home and away. Rename the symbols in the README,
  `design.md`, `considerations.md` and the code comments to match, or drop them there. Chapter 5 adds $D$, $\ell_H$,
  $\ell_A$, $L$, $\pi$, $u_r$, $w$, $G$ and $\sigma$, and appendix A adds $W$ and $\Lambda$; include them in the
  sweep. The drift kernel is $G$, so that it does not clash with $K_s$, $K_a$ and $K_d$.

## To do: open points from chapter 5 onwards

- [x] **Rule for observed xG** (section 5.5). Decided: split between the two neighbouring values, weighted by
  distance; values outside the range count as the nearest end value.
- [ ] **The simulated check** (appendix B.3). Needs inference code: the lookup table of appendix A, the update and
  the drift. $\sigma$ is now trained with the other parameters (section 6.7), so the check only verifies it, and
  tests the assumption of independent skills of section 5.6. Section 5.7 still says the check sets $\sigma$; see the
  comment on pull request #5.
- [x] **What the error function measures** (chapter 6). Decided: the ranked probability score of each team's shot
  count and each shot's xG, predicted before the match, on fixed xG bins, with a weight $\lambda$ between the two
  tuned on results (sections 6.3 to 6.5 and 6.9).
- [ ] **Code for the proper fit** (chapter 6, run in chapter 7). The prediction of section 6.2, the score, and the
  search of section 6.8 on top of the inference code. `calibrate.py` stays as the rough fit of appendix B.1.
- [ ] **Rerun the rough fit** (appendix B.1). Replace the values now with the output of `uv run calibrate`, so that
  B.2 and chapter 7 start from it.
- [ ] **Trainability study** (appendix B.2). Simulate as many matches as the real data has from B.1's values, fit
  from several random starts, and report which parameters come back. Rerun with chapter 7's fitted values.
- [ ] **Bookmaker odds in the data** (section 6.9). The Understat data has no odds; find a source of home, draw and
  away odds for the same matches.
- [ ] **Chapter 6 settings left to chapter 7.** The xG bin width, the matches left out at the start, the grid for
  $\lambda$, the step and smallest step for $\sigma$, and the sizes of the three data sets.
- [ ] **Tempo pool** (chapter 9). The fixed tempo urn cannot give a shot-count variance above the mean; drawing each
  match's tempo urn from a larger pool, as in `docs/considerations.md`, could. Kept as a known limitation for now.
- [ ] **Assumption list** (chapter 9). List every "**Assumption (name).**" paragraph of the book, with how each is
  checked. Chapter 5 has four: observed xG, independent skills, drift and starting distribution. Chapters 3 and 4
  should mark theirs the same way when they are revised.
- [x] **Where resolution against variance goes.** Its own section in chapter 7. It is a design trade-off, so it is
  kept apart from the mismatch section, which takes the variance gaps found by the fit and feeds chapter 9.
- [ ] **xG for every two decimals.** Set up the shot urns so that they can produce every two-decimal xG value within
  a range. Belongs with resolution against variance, and makes the rule of section 5.5 matter less.
- [ ] **xG of 0.00** (chapter 7). Real data has many shots with an xG of 0.00, which the rule of section 5.5 counts
  as the lowest model value. Check how many there are, and make the model's list of values reach close to zero.

## To do: material moved out of chapter 4

Chapter 4 was cut down to the rules and the moments of each step. The parts below were taken out and belong in
other chapters. The text as it was is in commits `8bb8053` (sections 4.1 to 4.8), `e8b314f` (the table and
comments on the moments) and `a508f78` (the stacked equations), in `docs/book/04-model-mechanics.md`. The running
example (the examples in sections 4.2 to 4.5, and section 4.8) was removed later; it is in commit `2481745`.

The chapter numbers below follow the order of issue #4: the items once planned for "Fitting the structure" are
under chapter 7, and those for "Inference" under chapter 5.

- [ ] **Chapter 3, From theory to model.**
  - How the urn chain maps onto chapter 2's three layers of randomness. The skill pool is skill, the draw into the
    match urn is match-day form, and the rounds are chance within the game: the tempo urn sets how often there is a
    shot, the grab decides who creates it, the attack-versus-defence draw sets how good it is, and the shot urn
    decides whether it goes in.
  - The assumption that teams do not play differently with the score, and its consequence: every round of a match
    is identical and independent given the two match urns. Chapter 4's equations use this.
  - The tempo urn not depending on the teams, stated as a modelling choice.
  - Finishing as pure chance given the xG: no team converts better than its xG says.
- [ ] **Chapter 7, Fitting to real data.**
  - The data reason for the tempo urn: total shots per match were the one observable whose mean did not move with
    the skill proxy.
  - Resolution against variance, in full:
    - The number of balls in a container sets the resolution, and the number drawn sets the variance.
    - The match urn couples the resolution and the size of form, and $M_s$ loosens that coupling.
    - Raising the shot-urn counts together makes the xG grid finer but narrows the spread.
    - The ceilings: binomial shots, the single-ball goal draw, and the with-replacement limit on form.
    - The cost of more balls for the inference table (appendix A.3).
    - Why the variance decides how confident the inference is.
  - The findings so far, from three Premier League seasons, for the mismatch section:
    - Real total shots have a standard deviation of 6.0 against the model's 4.3, a variance above the mean, which
      no binomial can give.
    - The model's home share of shots varies more than the real one: 0.23 against 0.17.
  - That the model records the same quantities per shot as real data does, which is what makes the comparison
    possible.
  - What the moments in chapter 4 mean for fitting:
    - The match-urn variance is zero when $M_s = M_u$ and rises towards $M_u p_s (1 - p_s)$ as $M_s$ grows.
    - The binomial shot count has its variance below its mean; with the starting values, 25 shots, a standard
      deviation of 4.33 and a skewness of 0.12.
    - The home share's variance has two parts: noise from the limited number of shots, and how much $q$ varies
      between matches.
    - How $K_s$ and the two red shares set the probability of attacking. The table from chapter 4 had this for
      match urns of 20 balls and no home advantage; for example, red shares 0.55 against 0.45 give 0.64 with
      $K_s = 3$ and 0.77 with $K_s = 10$.
    - The xG resolution: with the starting values, each kind of shot can take 11 values, from 0.04 to 0.23 for an
      ordinary chance and from 0.32 to 0.52 for a big chance.
  - The size of the skill pool. The starting values give about 16 skill levels, too few for real teams; a larger
    pool only grows $W$ (appendix A) but changes match-day form, so it is fitted with the rest.
  - The check of the inference on simulated matches, moved from section 5.10, now appendix B.3. About twenty teams play
    thousands of matches by chapter 4's rules, each team's skill pool changing slowly along its own curve (for
    example a sine wave with its own period, amplitude and phase). The inference is run on the simulated shots alone.
    Measured: whether the centre of each distribution follows the true red balls; whether an 80% interval holds the
    truth in about 80% of matches; and how many matches a team needs before its distribution stops narrowing. It
    sets $\sigma$, tests the assumption of independent skills, and cannot show whether the model describes real
    football. The text as it was is in commit `3c787bf`.
  - The model's moments over the match urns, to compare with real matches. The stacked closed forms drafted
    earlier are in commit `a508f78`:
    - the home share of shots over the match urns, with $E[1/N]$ and the variance of $q$;
    - a team's xG per shot as a mix of ordinary and big chances, and its distribution over the match urns;
    - the per-round goal probability $\gamma$, with binomial goals given the match urns;
    - the result as a multinomial over the rounds, given the match urns.
- [x] **Chapter 5, Inference.**
  - The likelihood of a whole match from the two skill pools: sections 5.2 to 5.4; the lookup table: appendix A.
  - The rule for assigning a continuous observed xG to one of the values the urns can produce: section 5.5.
- [ ] **Chapter 8, Use.**
  - The probability of a result from the two skill pools. It sums over every path through the chain; the stacked
    result above gives it given the match urns.
