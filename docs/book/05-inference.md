# 5. Inference

This chapter shows how the red balls in each team's skill pool are inferred from observed matches. The model is only
ever run forwards. For every possible pair of skill pools, chapter 4 gives the probability of the match that was
observed; multiplied by what was believed before the match and normalised, this gives what is believed after it.

## 5.1 What is observed

A match is observed as its list of shots: for each shot, the team that took it and its xG. This is all the inference
uses, and the rest of the match adds nothing, for two reasons that follow from chapter 4.

The number of shots says nothing about skill. It comes from the tempo urn (section 4.3), which is the same for every
pair of teams, so its probability is the same for every pair of skill pools and cancels when the result is
normalised. Which team took each shot does carry information, and it enters through the probability $q$ of section
4.4.

The goals say nothing about skill once the xG is known. A goal is a single draw that succeeds with probability xG
(section 4.6), whoever the teams are. The goals, and the result, are outcomes of the model; they are not inputs to
the inference.

The observed match is written $D = \big((t_1, v_1), \dots, (t_N, v_N)\big)$, where $t_i$ is $H$ or $A$ for the team
that took shot $i$ and $v_i$ is its xG. Real xG is a continuous number, while the urns produce only a few values;
section 5.5 deals with the difference.

## 5.2 One shot, given the match urns

Given the two match urns, every shot is drawn the same way and independently of the others. With $j$ red balls drawn
into the home team's match urn and $k$ into the away team's (section 4.2), one shot has four possible kinds, with the
probabilities $q$, $\beta_H$ and $\beta_A$ of section 4.4, all computed for the match urns $j$ and $k$.

The probability of one observed shot combines the kind of shot with its xG. Let $P_H^o(v \mid j, k)$ and
$P_H^b(v \mid j, k)$ be the probabilities from section 4.5 that a home ordinary chance and a home big chance have
xG $v$, and $P_A^o$ and $P_A^b$ the same for the away team. The probability that a shot is taken by the home team and
has xG $v$, and the same for the away team, are

$$
\ell_H(v \mid j, k) = (q - \beta_H)\, P_H^o(v \mid j, k) + \beta_H\, P_H^b(v \mid j, k)
$$

$$
\ell_A(v \mid j, k) = (1 - q - \beta_A)\, P_A^o(v \mid j, k) + \beta_A\, P_A^b(v \mid j, k)
$$

Summed over every value $v$, the two add up to $q + (1 - q) = 1$. A value that only one kind of shot can produce gets
its probability from that kind alone. If the marked sets keep the values of the two kinds apart, an observed xG
also tells which kind of shot it was; if not, both kinds add to the same value.

## 5.3 One match, given the match urns

Given the match urns, the likelihood of the whole match is a product over its shots. The shots are independent given
$j$ and $k$, and their order does not matter:

$$
L(D \mid j, k) = \prod_{i:\, t_i = H} \ell_H(v_i \mid j, k) \prod_{i:\, t_i = A} \ell_A(v_i \mid j, k)
$$

The home share of shots needs no term of its own. Each home shot contributes a factor that sums to $q$ over its
values and each away shot one that sums to $1 - q$, so the product holds the binomial of section 4.4 without its
binomial coefficient, which is the same for every pair of match urns and cancels.

## 5.4 One match, given the skill pools

The match urns are not observed, so the likelihood given the skill pools sums over every pair of match urns. The
match urns are drawn once and used for every shot of the match. With $m_{s,H}$ and $m_{s,A}$ red balls in the two
skill pools and the hypergeometric probabilities of section 4.2:

$$
L(D \mid m_{s,H}, m_{s,A}) = \sum_{j} \sum_{k} P(m_{u,H} = j \mid m_{s,H})\, P(m_{u,A} = k \mid m_{s,A})\, L(D \mid j, k)
$$

The order of the sum and the product matters. The product over the shots is taken inside each pair of match urns,
and the sum over the pairs outside. Taking the sum inside, shot by shot, would give every shot its own match-day
form, and the inference would treat form as noise that averages out within a match instead of something shared by
all its shots. It would then be too sure of a team's skill after a single good or bad day.

The likelihood is computed exactly from the equations of chapter 4, without simulation; appendix A shows how. One
pair of match urns is left out. When both hold only red balls, who shoots is never decided (section 4.4), and that
pair is given a likelihood of zero.

## 5.5 Observed xG and model xG

An observed xG has to be matched to the values the urns can produce before its probability can be found. Real xG is a
continuous number, often given to two decimals, and the urns produce a finite set of values, so an observed xG of,
say, 0.137 usually has no value of its own.

The values the urns can produce depend only on the parameters. They are set by the ball counts of section 4.5: the
balls drawn and the x-marked balls of each kind of shot. The match urns only change how likely each value is, and a
value that a weak match urn cannot reach has probability zero for those match urns. So the values form one sorted list,
$u_1 < u_2 < \dots < u_V$, the same for both teams, every match and every pair of match urns. Ordinary and big chances
share the list, since real data does not say which kind a shot was, and $\ell_H$ and $\ell_A$ already add the two
kinds.

An observed xG is split between its two neighbours in the list. With $u_r \le v \le u_{r+1}$, the shot counts as
$u_r$ with weight $w$ and as $u_{r+1}$ with weight $1 - w$, where

$$
w = \frac{u_{r+1} - v}{u_{r+1} - u_r}
$$

and its factor for match urns $j$ and $k$ is the weighted sum $w\,\ell_H(u_r \mid j, k) + (1 - w)\,\ell_H(u_{r+1}
\mid j, k)$ for a home shot, and the same with $\ell_A$ for an away shot. An observed xG below $u_1$ counts as $u_1$,
and one above $u_V$ as $u_V$.

**Assumption (observed xG).** An observed xG is the model's xG, split between its two neighbouring values in the
list, and counted as the end value when it falls outside the list.

The split keeps each shot's xG right on average, since $w\,u_r + (1 - w)\,u_{r+1} = v$. Counting a shot as its
nearest value would throw away where it lies between the two. The split still widens the spread of xG a little, by
spreading each shot over two values.

The larger distortion is at the ends of the list. A real xG far above the top of the list, counted as the top value,
loses much of its size, and so does a real xG far below the bottom. The fit of chapter 7 should therefore make the
list cover nearly all real xG. Setting up the urns so that they produce every two-decimal value within the range
makes the split matter less, but the ends remain.

## 5.6 The update after a match

Before a match, each team's skill is held as a probability distribution over the red balls in its skill pool. Let
$\pi_H(s)$ and $\pi_A(s)$ be the home and away team's distributions before the match, for $s$ from 0 to $M_s$.

**Assumption (independent skills).** Before each match, the two teams' skill distributions are independent, so the
probability of a pair of skill pools is their product.

The distribution after the match follows from Bayes' rule. For each pair of skill pools, the probability before the
match is multiplied by the likelihood of section 5.4 and the result is normalised:

$$
P(m_{s,H} = s_H,\, m_{s,A} = s_A \mid D) = \frac{\pi_H(s_H)\, \pi_A(s_A)\, L(D \mid s_H, s_A)}
{\sum_{s_H'} \sum_{s_A'} \pi_H(s_H')\, \pi_A(s_A')\, L(D \mid s_H', s_A')}
$$

Each team keeps only its own distribution, which is the sum over the other team's skill pool:

$$
\pi_H'(s_H) = \sum_{s_A} P(m_{s,H} = s_H,\, m_{s,A} = s_A \mid D), \qquad
\pi_A'(s_A) = \sum_{s_H} P(m_{s,H} = s_H,\, m_{s,A} = s_A \mid D)
$$

Keeping only each team's own distribution is what the assumption of independent skills costs. After the match, a
strong home team against a strong away team can explain the same shots as a weaker home team against a weaker away
team, so the two teams' skills are correlated, and the next match starts as if they were not. The joint distribution
of a whole league is not kept because it is too large: $T$ teams give $(M_s + 1)^T$ combinations. In a league the
teams share opponents, so the correlations do not simply fade. The effect is expected to be small, and the check on
simulated matches in chapter 7 tests it.

## 5.7 Between matches: skill drift

The red balls in a skill pool may change between matches (section 4.2), and the inference has to allow for it.
Whoever runs the model sets how skill changes, while an observer of real matches does not know it. Before each
match, the observer widens each team's distribution with an assumed drift: a probability $G(s \mid s')$ that a skill
pool with $s'$ red balls has $s$ red balls at the next match:

$$
\pi(s) = \sum_{s'} G(s \mid s')\, \pi'(s')
$$

The drift is a spread around the current count, since red balls may change by more than one between matches.

**Assumption (drift).** Between two matches of a team, the red balls in its skill pool move by a rounded normal step
with standard deviation $\sigma M_s$, kept inside the skill pool and normalised there:

$$
G(s \mid s') = \frac{\exp\!\big(-(s - s')^2 / 2 (\sigma M_s)^2\big)}{\sum_{r=0}^{M_s} \exp\!\big(-(r - s')^2 / 2 (\sigma M_s)^2\big)},
\qquad s = 0, \dots, M_s
$$

The spread $\sigma$ is a constant, the same between every pair of matches, whatever the time between them. A longer
gap, such as an international break, is by choice not given a wider spread. The spread is a share of the skill pool,
so it keeps its meaning when $M_s$ changes. With $\sigma = 0$
the distribution narrows with every match and in the end becomes as certain as one likes. With $\sigma > 0$ it
stops narrowing at a width where the widening between matches balances what each match reveals.

The drift is an assumption of the inference, not a part of the model, and it does not have to equal the change used
when matches are simulated. Too little drift makes the inference slow to follow a real change in skill and too sure
of an old estimate; too much makes it more uncertain than it needs to be. Choosing $\sigma$ is the main setting of
the inference. Chapter 7 sets it, by a check on simulated matches run with the fitted parameters; the same check
tests the assumption of independent skills.

## 5.8 Before the first match

Before a team's first match, its distribution is a starting choice and not a result of the inference.

**Assumption (starting distribution).** Before its first match, a team's skill has a chosen distribution, for
example spread evenly over a range of red balls, or carried over from an earlier season.

Its influence fades with each match the team plays, at a rate set by the drift of section 5.7.
