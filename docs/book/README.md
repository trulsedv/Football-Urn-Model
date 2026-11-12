# The urn model of football

*Theory, mechanics and inference*

This folder holds the book, one file per chapter. The book is meant to become the source of truth for the model: the
rules, the reasoning behind them, the inference and its validation. The rest of the documentation should end up
following it or pointing to it.

## Chapters

| # | Chapter | File | Status |
| --- | --- | --- | --- |
| 1 | Introduction | – | Not started |
| 2 | A theory of football | – | Not started |
| 3 | From theory to model | – | Not started |
| 4 | Model mechanics | [04-model-mechanics.md](04-model-mechanics.md) | First draft |
| 5 | Fitting the structure | – | Not started |
| 6 | Inference | – | Not started |
| 7 | Validation | – | Not started |
| 8 | Use | – | Not started |
| 9 | Known limitations | – | Not started |

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
  5, and its equations overlap chapter 4. Decide whether it becomes chapter 5 or stays as working notes that chapter 5
  draws on, and remove the equations that chapter 4 now defines.
- [ ] **Fix the inference scope in `docs/considerations.md`.** The section "Future: inference" opens with "Not part
  of this project, perhaps a later one", which contradicts goal 4 in `design.md`. Rename the section (for example to
  "Inference") and replace that sentence with one saying that inference is part of this project.
- [ ] **`docs/considerations.md`, the rest.** Its decided choices and accepted simplifications are material for
  chapters 3 and 9, and its inference notes for chapter 6. Move them as those chapters are written.
- [ ] **`docs/data-analysis.md`.** The data and figures behind chapter 5. Decide whether chapter 5 cites it or
  absorbs it.
- [ ] **Outline, discussion notes and minutes** (`docs/report-outline.md`, `docs/discussion-notes-2026-11-12.md`,
  `docs/meeting-minutes-2026-11-12.md`, in pull request 1). These are working material for the book. Decide whether
  they stay in `docs/` as a record once the chapters exist, or move to an archive folder.
- [ ] **Update the outline** (`docs/report-outline.md`, pull request 1). Chapter 4 now only describes how the game
  is played and how the mean, variance and skewness of each step follow from the step before. Resolution against
  variance is in chapter 5, and the independence of rounds in chapter 3. Change the descriptions of chapters 3, 4 and
  5 to match.
- [ ] **Unbreakable ties in phase 4.** Chapter 4 states a provisional rule (a fair draw). Replace it with a final
  rule, or list it under known limitations, and make the code and the README match.

## To do: material moved out of chapter 4

Chapter 4 was cut down to the rules and the moments of each step. The parts below were taken out and belong in
other chapters. The text as it was is in commit `8bb8053`, `docs/book/04-model-mechanics.md`, sections 4.1 to 4.8.

- [ ] **Chapter 3, From theory to model.**
  - How the urn chain maps onto chapter 2's three layers of randomness. The skill pool is skill, the draw into the
    match urn is match-day form, and the rounds are chance within the game: the tempo urn sets how often there is a
    shot, the grab decides who creates it, the attack-versus-defence draw sets how good it is, and the shot urn
    decides whether it goes in.
  - The assumption that teams do not play differently with the score, and its consequence: every round of a match
    is identical and independent given the two match urns. Chapter 4's equations use this.
  - The tempo urn not depending on the teams, stated as a modelling choice.
  - Finishing as pure chance given the xG: no team converts better than its xG says.
- [ ] **Chapter 5, Fitting the structure.**
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
- [ ] **Chapter 6, Inference.**
  - The exact computation of a whole match from the two skill pools: the outcomes of one round, the enumeration of
    the attack-versus-defence draw, and the weighting over match urns. Chapter 4 now gives the pieces (sections 4.2
    to 4.7); chapter 6 should put them together as the likelihood and the lookup table.
  - The rule for assigning a continuous observed xG to one of the values the urns can produce.
