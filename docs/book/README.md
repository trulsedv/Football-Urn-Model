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
| 6 | Fitting method | – | Not started |
| 7 | Fitting to real data | – | Not started |
| 8 | Use | – | Not started |
| 9 | Known limitations | – | Not started |

The order after chapter 4 was changed in [issue #4](https://github.com/trulsedv/football-urn-model/issues/4).
Simulated matches cannot fit the model to real football, so the parameters are fitted to real data, and that has to
come after the inference, since skill is not observed. Chapter 5 is the inference. Chapter 6 is the method of the fit:
the error function and how to minimise it. Chapter 7 applies it to real data, starting from a rough fit of the mean,
variance and skewness of each step, and ends with the check of the inference on simulated matches, run with the
fitted parameters (moved there from chapter 5 in pull request #5, for now).

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
  `design.md`, `considerations.md` and the code comments to match, or drop them there.

## To do: open points from chapter 5 onwards

- [x] **Rule for observed xG** (section 5.6). Decided: split between the two neighbouring values, weighted by
  distance; values outside the range count as the nearest end value.
- [ ] **The simulated check** (chapter 7). Needs inference code: the lookup table, the update and the drift. It
  sets the drift spread $\sigma$ of section 5.8. Its loop: the fit runs through the inference, which needs a drift,
  so chapter 7 starts from a guessed $\sigma$ and refines it after the fit.
- [ ] **What the error function measures** (chapter 6). For example the result probabilities or the xG of the next
  match, scored against what happened.
- [ ] **Where resolution against variance goes.** It was planned for the old chapter 5, "Fitting the structure",
  which no longer exists; it is listed under chapter 7 below for now.
- [ ] **xG for every two decimals.** Set up the shot urns so that they can produce every two-decimal xG value within
  a range. Belongs with resolution against variance, and makes the rule of section 5.6 matter less.

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
    - The cost of more balls for the inference table.
    - Why the variance decides how confident the inference is.
  - The findings so far, from three Premier League seasons:
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
    pool only grows $W$ (section 5.5) but changes match-day form, so it is fitted with the rest.
  - The check of the inference on simulated matches, moved from section 5.10 for now. About twenty teams play
    thousands of matches by chapter 4's rules, each team's skill pool changing slowly along its own curve (for
    example a sine wave with its own period, amplitude and phase). The inference is run on the simulated shots alone.
    Measured: whether the centre of each distribution follows the true red balls; whether an 80% interval holds the
    truth in about 80% of matches; and how many matches a team needs before its distribution stops narrowing. It
    sets $\sigma$, and cannot show whether the model describes real football. The text as it was is in commit
    `3c787bf`.
  - The model's moments over the match urns, to compare with real matches. The stacked closed forms drafted
    earlier are in commit `a508f78`:
    - the home share of shots over the match urns, with $E[1/N]$ and the variance of $q$;
    - a team's xG per shot as a mix of ordinary and big chances, and its distribution over the match urns;
    - the per-round goal probability $\gamma$, with binomial goals given the match urns;
    - the result as a multinomial over the rounds, given the match urns.
- [x] **Chapter 5, Inference.**
  - The likelihood of a whole match from the two skill pools, and the lookup table: sections 5.2 to 5.5.
  - The rule for assigning a continuous observed xG to one of the values the urns can produce: section 5.6.
- [ ] **Chapter 8, Use.**
  - The probability of a result from the two skill pools. It sums over every path through the chain; the stacked
    result above gives it given the match urns.
