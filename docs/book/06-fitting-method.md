# 6. Fitting method

This chapter sets out how the parameters of chapter 4 and the drift spread of chapter 5 are fitted to real matches.
The fit chooses the parameters whose predictions of real matches score best, with each match predicted before it is
played. The chapter defines the error, says which parameters are trained and which are fixed by design, and gives
the search that minimises the error. Chapter 7 runs the method on real data.

## 6.1 Two levels

The fit works on two levels. The outer level chooses the parameters shared by all teams: the ball counts of chapter
4 and the drift spread $\sigma$ of section 5.7, the only parameter of the inference. The inner level runs the
inference of chapter 5 through every match, for the parameters being tried, and gives the error.

The teams' skills are not parameters of the fit. Each team's red balls $m_s$ come out of the inference for whatever
parameters are being tried, and so does the range they fall in. If the other parameters change, the red balls needed
to produce real-looking shots change with them, and the inferred skills move to wherever fits. The starting
distribution of section 5.8 only has to be wide enough to cover where they end up.

## 6.2 What is predicted

Each match is predicted from the skill distributions as they stand just before it, and only then used to update
them. The inference runs through the matches in time order. Before each match it widens both teams' distributions by
the drift (section 5.7), predicts the match, scores the prediction against what happened, and updates the
distributions with the match (section 5.6). Every prediction therefore uses only earlier matches.

Two things are predicted for each match: each team's number of shots, and the xG of each shot. Goals and results
are not part of the fit. They are much noisier than shots and xG, and they are used to tune and test the fit instead
(section 6.9).

A team's number of shots, given the match urns, is binomial. Each round gives a home shot with probability $p_t q$
and an away shot with probability $p_t (1 - q)$, with $p_t$ of section 4.3 and $q$ of section 4.4, so $N_H$ is
binomial with $n$ rounds and probability $p_t q$, and $N_A$ with $p_t (1 - q)$. The prediction mixes this over the
match urns and over the skill distributions:

$$
P(N_H = c) = \sum_{s_H} \sum_{s_A} \pi_H(s_H)\, \pi_A(s_A) \sum_j \sum_k P(m_{u,H} = j \mid s_H)\,
P(m_{u,A} = k \mid s_A)\, \binom{n}{c} \big(p_t q\big)^c \big(1 - p_t q\big)^{n - c}
$$

with $q$ computed for the match urns $j$ and $k$, and the same for $N_A$ with $1 - q$.

The xG of a home shot is predicted the same way, from $\ell_H$ of section 5.2. Given that a shot is taken by the home
team, the match urns are weighted by how likely they make a home shot:

$$
P_H(v) = \frac{\sum_{s_H, s_A} \pi_H(s_H)\, \pi_A(s_A) \sum_{j, k} P(m_{u,H} = j \mid s_H)\, P(m_{u,A} = k \mid s_A)\,
\ell_H(v \mid j, k)}{\sum_{s_H, s_A} \pi_H(s_H)\, \pi_A(s_A) \sum_{j, k} P(m_{u,H} = j \mid s_H)\,
P(m_{u,A} = k \mid s_A)\, q(j, k)}
$$

and $P_A(v)$ the same with $\ell_A$ and $1 - q$. Each shot is scored against this distribution on its own. The shots
of one match share their match urns, so they are not independent in the prediction; scoring each against the
distribution before the match ignores that, which suits a score, since it asks only how well each shot was foreseen.

## 6.3 Bins

The predictions are scored on fixed bins of xG, the same for every set of parameters. The values the urns can
produce depend on the parameters (section 5.5), so two sets of parameters would otherwise be scored on different
values, and a set with finer values would spread its probability thinner and look worse for that reason alone. With
fixed bins, the model's probability of a bin is the sum of $P_H(v)$ over the model values $v$ in it, and each real
shot falls into one bin. The bins run from the lowest to the highest xG in the data; their width is a choice made in
chapter 7.

A bin that holds no model value gets probability zero, and the score of the next section handles this without any
special rule. The shot counts need no bins of their own: each count, from 0 to $n$, is its own bin.

The bins are used only for scoring. The update after the match still uses the split of section 5.5, which matches
each observed xG to the model's own values.

## 6.4 The ranked probability score

Each prediction is scored by the ranked probability score, which compares the predicted and the observed cumulative
distribution over ordered bins. With bins $1, \dots, B$ in order, predicted probabilities $P_1, \dots, P_B$, and the
observation in bin $o$:

$$
\mathrm{RPS} = \sum_{b=1}^{B} \big(F_b - O_b\big)^2, \qquad F_b = \sum_{i \le b} P_i, \qquad
O_b = \begin{cases} 0 & b < o \\ 1 & b \ge o \end{cases}
$$

$F_b$ is the predicted probability of landing in bin $b$ or lower, and $O_b$ the same for what happened. A lower
score is better.

The score has three properties the fit needs:

- **It rewards honest probabilities.** Over many predictions, the lowest expected score goes to the distribution
  that matches how often each bin really occurs, so the fit cannot gain by being overconfident.
- **A near miss costs less than a far miss.** The bins are ordered, and probability placed next to the observed bin
  lowers the score more than probability placed far from it. A score that treats the bins as unrelated, such as the
  Brier score, gives every miss the same cost.
- **It is bounded.** A bin the model gave probability zero raises the score by a finite amount, at most $B - 1$ for
  one prediction.

The last property is the reason the logarithmic score is not used. The logarithmic score, minus the log of the
probability given to what happened, is infinite for an observation the model gave probability zero, and very large
for one it gave very little. The structure of chapter 4 has known limits, such as its range of xG and the spread of
its shot counts (chapter 9). Under the logarithmic score, the few shots the structure can barely produce would steer
the parameters at the cost of fitting the common shots worse. The ranked probability score fits the parameters to
what the structure can describe, and leaves the rest to the known limitations.

## 6.5 The error

The error of one match adds the scores of its two shot counts and of its shots:

$$
E_{\text{match}} = \mathrm{RPS}(N_H) + \mathrm{RPS}(N_A) + \lambda \sum_{i=1}^{N} \mathrm{RPS}(v_i)
$$

where each $\mathrm{RPS}(v_i)$ scores shot $i$ against $P_H$ or $P_A$, by the team that took it. The home and away
counts together carry which team shot, so who shoots needs no term of its own. The error of the fit is the sum over
the matches that count (section 6.6).

The weight $\lambda$ sets how much the xG of the shots counts against the shot counts. The two kinds of score are not
parts of one probability, so nothing in the scores themselves fixes their balance. $\lambda$ is a hyperparameter: a
setting of the fit that the error cannot choose, since the error depends on it. It is tuned on the results (section
6.9).

## 6.6 The starting distribution

The starting distribution of section 5.8 is a choice, not a result, and it should not pull the fit. A team's first
matches are predicted mostly from that choice, so their scores say more about the choice than about the parameters.

The error therefore leaves out each team's first matches, or the inference starts a season before the matches the
error counts. Either way, the matches the error counts are predicted from distributions the data has already shaped.
How many matches are left out is set in chapter 7.

## 6.7 What is trained and what is fixed

Most parameters are searched not as ball counts but as shares, so that each search direction changes one thing about
the model. A share is turned back into balls by rounding, within the limits the rules of chapter 4 set: a draw cannot
take more balls than its urn holds, and $x_H$ is at least 1. Parameters that only set a resolution are fixed by
design, since the fit would push them without limit.

| Parameters | How they are fitted | Why |
| --- | --- | --- |
| $n$ | Fixed by design | The fit would push it without limit (below) |
| $M_s$ | Fixed by design | It sets the number of skill levels, and the fit would push it without limit |
| $M_t$, $m_t$ | $M_t$ fixed by design; $m_t$ trained, as the mean shot count $n p_t$ | One ball is drawn and put back, so only $p_t$ matters |
| $M_u$ | Trained directly | It sets match-day form |
| $x_H$ | Trained as the home share $x_H / M_u$ | Its effect depends on $M_u$ |
| $K_s$ | Trained directly | It sets how strongly skill decides who shoots |
| $b$ | Trained as the share $b / K_s$ | Its effect depends on $K_s$ |
| $K_a$ | Trained directly | It sets the resolution of xG, bounded by $M_u$ |
| $K_d$ | Trained as the share $K_d / K_a$ | It acts only through the attacker's red balls it cancels |
| $X_o$, $x_o$ | Trained as the red share $x_o / X_o$ and the attacker's share $K_a / (X_o + K_a)$ | Level and sensitivity of xG |
| $X_b$, $x_b$ | The same, for a big chance | Level and sensitivity of xG |
| $\sigma$ | Trained directly | It sets how fast the inference follows a change in skill |

**The rounds.** With the mean shot count $\mu = n p_t$ held fixed, the variance of the shot count is
$\mu (1 - \mu / n)$, which grows with $n$ towards the ceiling $\mu$. Real shot counts vary more than their mean, so the
fit would push $n$ towards infinity and $p_t$ towards zero. The rounds are kept, since the game is played round by
round, and fixed at a value chosen in chapter 7; near the ceiling, a larger value changes the shot counts little.

**The skill pool.** A larger skill pool gives more skill levels, and slightly more match-day form, since the match
urn is drawn from it without replacement. Both make the fit a little better, so it would grow without limit. Fixing
it also bounds the rest: $M_u$ cannot exceed $M_s$, and $K_s$, $K_a$ and $K_d$ cannot exceed $M_u$.

**The marked sets.** The red share of a marked set sets the level of the xG. Its size matters too, unlike the tempo
urn's, because the attacker's balls are added to the same shot urn: the attacker's share of the shot urn sets how
much a team's skill moves the xG. Searched as red balls and white balls, a level and a sensitivity are mixed in every
step, and the error forms long valleys along which many combinations score nearly the same. Searched as the two
shares, they are separate directions. With the shares fixed, $K_a$ mostly sets how fine the xG values are, which the
fixed bins of section 6.3 do not reward for its own sake.

Some links remain. The margin share removes most of the dependence of $b$ on $K_s$ but not all, since more draws also
make the difference in red balls less noisy. A strong who-shoots draw with little match-day form can look a little
like a weak draw with more form, though $M_u$ also affects the xG, which should tell them apart.

Appendix B.2 tests, on simulated data, which of these parameters the data can pin down. A parameter it cannot recover
is fixed by design as well.

## 6.8 The search

The error is minimised by a search over whole steps, since most parameters are ball counts and the error has no
gradient. Each try rebuilds the tables of appendix A and runs the inference through every match, so the search has
to make few tries.

The search starts from the rough fit of appendix B.1 and repeats one round until no step lowers the error:

1. For each parameter in the table of section 6.7, try one step up and one step down, and note the change in the
   error. For a share, a step is the smallest change that moves a ball; for $\sigma$, a step of a chosen size.
2. Try the combined step: every parameter whose step lowered the error moves at once.
3. Keep the combined step if it lowers the error more than the best single step; otherwise keep the best single step.

When no single step lowers the error, the step for $\sigma$ is halved and the search goes on, until the step reaches
a chosen smallest size.

A search by single steps stops wherever no single step helps, even if two parameters moved together would. The
search is therefore run from several starting points. If they end in the same place, local minima do not matter in
practice. If they do not, diagonal steps, in which two parameters move together, are added for the pairs of section
6.7 that are still linked.

## 6.9 Tuning and testing on results

The matches are split in time order into three sets: one to train on, one to tune the weight $\lambda$, and one held
out for the final test. The inference runs through all three in order, so the skills keep updating, but the
parameters are fitted on the first set alone.

**Tuning.** For each value of $\lambda$ on a grid, the parameters are fitted on the training set. Each match of the
tuning set is then predicted as a result, home win, draw or away win, from the skill distributions before it
(chapter 8), and scored by the ranked probability score over those three ordered outcomes. The value of $\lambda$
with the lowest total score is kept.

**Testing.** The fitted model predicts the results of the held-out set, scored the same way, and is compared with two
baselines on the same matches:

- **Bookmaker odds.** One over each of the three odds, scaled so the three add up to one, which removes the
  bookmaker's margin. This is a strong benchmark; coming close to it is already a good result.
- **League averages.** The share of home wins, draws and away wins in the training set, the same for every match.
  This shows whether the model beats guessing.

A single match says little, since a result is mostly chance. The comparison is the difference in mean score per
match over the held-out set, with its standard error, so that a real difference can be told from noise.

Goals and results are used only here. The fit itself is on shots and xG, so the test also checks the assumption of
section 4.6 that finishing is chance given the xG: if it holds, a model that predicts xG well also predicts results
well.
