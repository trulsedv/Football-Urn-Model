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
- [ ] **`docs/considerations.md`.** "Future: inference" still says inference is not part of this project, which
  contradicts goal 4 in `design.md`. Its decided choices and accepted simplifications are material for chapters 3 and
  9, and its inference notes for chapter 6. Update the scope sentence now; move the rest as those chapters are
  written.
- [ ] **`docs/data-analysis.md`.** The data and figures behind chapter 5. Decide whether chapter 5 cites it or
  absorbs it.
- [ ] **Outline, discussion notes and minutes** (`docs/report-outline.md`, `docs/discussion-notes-2026-11-12.md`,
  `docs/meeting-minutes-2026-11-12.md`, in pull request 1). These are working material for the book. Decide whether
  they stay in `docs/` as a record once the chapters exist, or move to an archive folder.
- [ ] **Unbreakable ties in phase 4.** Chapter 4 states a provisional rule (a fair draw). Replace it with a final
  rule, or list it under known limitations, and make the code and the README match.
