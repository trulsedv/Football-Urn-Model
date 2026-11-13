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
- [ ] **Decide how the combined equations are handled.** Chapter 4 gives each step given the outcome of the step
  before, and combines them only once, numerically, in the running example (section 4.8). Open: whether the combined
  equations are needed in every chapter that uses them, or whether combining numerically (a weighted sum over the
  outcomes of earlier steps) is enough everywhere. If numerically is enough, reword the chapter 6 item below and drop
  its list of closed forms.
- [ ] **Consider a simpler who-shoots rule.** The tie-break in section 4.4 needs a recursion with a put-back when an
  urn runs empty. An alternative: on a tie, put all drawn balls back and both teams draw $K_s$ balls again. Then
  $q = P(k_{s,H} > k_{s,A}) / \big(1 - P(k_{s,H} = k_{s,A})\big)$, and a redraw can also give a big chance, so
  $\beta_H$ and $\beta_A$ are divided by the same factor. Both urns all red would still tie for ever. Decide, then
  change chapter 4, the README and the code together.
- [ ] **Unbreakable ties in phase 4.** Chapter 4 leaves out the case where a tie can never be broken: both match
  urns all red, or both all white, which needs $x_H = 0$. The simulator settles it with a fair draw. Decide whether
  the code keeps that, and whether chapter 9 mentions it.
- [ ] **Notation.** Chapter 4 uses a revised set of symbols: $K$ and $k$ for drawn balls and the red among them, $X$
  and $x$ for marked balls, subscripts $s$, $a$ and $d$ for the shot, attack and defence draws, $N$ for shots, $p_t$
  for the shot probability per round, and $H$ and $A$ for home and away. Rename the symbols in the README,
  `design.md`, `considerations.md` and the code comments to match, or drop them there.

## To do: material moved out of chapter 4

Chapter 4 was cut down to the rules and the moments of each step. The parts below were taken out and belong in
other chapters. The text as it was is in commits `8bb8053` (sections 4.1 to 4.8), `e8b314f` (the table and
comments on the moments) and `a508f78` (the stacked equations), in `docs/book/04-model-mechanics.md`.

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
- [ ] **Chapter 6, Inference.**
  - The exact computation of a whole match from the two skill pools. Chapter 4 gives each step's equations given a
    known outcome of the step before; chapter 6 stacks them, weighting each outcome by its probability from the step
    before, into the likelihood and the lookup table. Chapter 5 needs the same stacking to compare the model's
    moments with real matches. The stacked forms drafted earlier are in commit `a508f78`:
    - the home share of shots over the match urns, with $E[1/N]$ and the variance of $q$;
    - a team's xG per shot as a mix of ordinary and big chances, and its distribution over the match urns;
    - the per-round goal probability $\gamma$, with binomial goals given the match urns;
    - the result as a multinomial over the rounds, given the match urns.
  - The rule for assigning a continuous observed xG to one of the values the urns can produce.
