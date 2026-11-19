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
section 5.6 deals with the difference.

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
its probability from that kind alone. With the starting values, ordinary chances lie between 0.04 and 0.23 and big
chances between 0.32 and 0.52, so an observed xG also tells which kind of shot it was.

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

The sum can be written as a product of three matrices. Let $W$ be the matrix with $W_{s j} = P(m_u = j \mid m_s = s)$,
one row per possible skill pool and one column per possible match urn, and $\Lambda$ the matrix with
$\Lambda_{j k} = L(D \mid j, k)$. The likelihood for every pair of skill pools at once is then

$$
L = W\, \Lambda\, W^\mathsf{T}, \qquad L_{s_H s_A} = L(D \mid m_{s,H} = s_H,\, m_{s,A} = s_A)
$$

## 5.5 The lookup table

Everything the inference needs from chapter 4 fits in one table, computed once from the equations and without
simulation. The table has one cell for each pair of match urns $j$ and $k$, from 0 to $M_u$ red balls each, so
$(M_u + 1)^2$ cells, 441 with the starting values. Each cell holds $\ell_H(v \mid j, k)$ and $\ell_A(v \mid j, k)$
for every value $v$ the urns can produce, 22 values per team with the starting values. The matrix $W$ of section 5.4
is a second, smaller table.

One cell is left out of the table. When both match urns hold only red balls, every draw of section 4.4 is a tie and
the redraw never ends. This needs $j = M_u$ and $k = M_u$, so it only happens when both skill pools hold at least
$M_u$ red balls; for skill pools with far fewer, as section 4.4 assumes, the cell's weight is negligible, and it is
given a likelihood of zero.

Each match is then priced by lookups, multiplications and the matrix product. For every cell, the factors of the
shots in the match are looked up and multiplied, which gives $\Lambda$; the matrix product of section 5.4 then gives
the likelihood for every pair of skill pools. The products of many small factors are best taken as sums of
logarithms, scaled before the matrix product so that the largest entry of $\Lambda$ is one; the scale cancels when
the posterior is normalised.

The table depends on the parameters of chapter 4 and not on the teams. It is recomputed whenever the parameters
change, as they do during the fitting of chapters 6 and 7.

## 5.6 Observed xG and model xG

An observed xG has to be matched to the values the urns can produce before it can be looked up. Real xG is a
continuous number, often given to two decimals, and the urns produce a finite set of values: with the starting
values, 11 for ordinary chances and 11 for big chances. A shot with an observed xG of 0.137 has no value of its own
in the table.

Two rules are the natural candidates. The observed value can count as the nearest value the urns can produce, or
it can be split between the two neighbouring values, with weights that fall linearly with the distance, so that the
shot's factor in a cell is the weighted sum of the two lookups. The rule matters most for values outside the range
the urns cover, and for values in the gap between the two kinds of shot, from 0.23 to 0.32 with the starting values.

Which rule the model uses is not decided yet. Setting up the urns so that they can produce every two-decimal value
within the range would make the rule matter less, but not remove it, since real xG still falls outside the range or
in the gap.

## 5.7 The update after a match

Before a match, each team's skill is held as a probability distribution over the red balls in its skill pool. Let
$\pi_H(s)$ and $\pi_A(s)$ be the home and away team's distributions before the match, for $s$ from 0 to $M_s$. The
two are taken as independent, so the probability of a pair of skill pools is their product.

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

Keeping only each team's own distribution drops the link between the two teams. After the match, a strong home team
against a strong away team can explain the same shots as a weaker home team against a weaker away team, so the joint
distribution has the two teams' skills correlated. Keeping the joint distribution of every team in a league is not
possible on a grid, since twenty teams of 101 values each give $101^{20}$ combinations. The approximation is that
the correlation fades as each team meets other opponents.

## 5.8 Between matches: skill drift

The red balls in a skill pool may change between matches (section 4.2), and the inference has to allow for it.
Whoever runs the model sets how skill changes, while an observer of real matches does not know it. Before each
match, the observer widens each team's distribution with an assumed drift: a probability $K(s \mid s')$ that a skill
pool with $s'$ red balls has $s$ red balls at the next match:

$$
\pi(s) = \sum_{s'} K(s \mid s')\, \pi'(s')
$$

A simple drift moves the red balls one up or one down, each with probability $\delta$, and leaves them as they are
otherwise; at 0 and at $M_s$ the move out of the range is not made. With $\delta = 0$ the distribution narrows with
every match and in the end becomes as certain as one likes. With $\delta > 0$ it stops narrowing at a width where
the widening between matches balances what each match reveals.

The drift is an assumption of the inference, not a part of the model, and it does not have to equal the change used
when matches are simulated. Too little drift makes the inference slow to follow a real change in skill and too sure
of an old estimate; too much makes it more uncertain than it needs to be. Choosing it is the main setting of the
inference, and section 5.10 sets it.

## 5.9 Before the first match

Before a team's first match, its distribution is a starting choice and not a result of the inference. It can be
spread evenly over a range of red balls, or carried over from an earlier season. Its influence fades with each match
the team plays, at a rate set by the drift of section 5.8.

## 5.10 Checking the inference on simulated matches

The inference is checked on simulated matches, since only there is the true skill known. About twenty teams play
thousands of matches by the rules of chapter 4. Each team's skill pool changes slowly along its own curve, for
example a sine wave with its own period, amplitude and phase. The inference is run on the simulated shots alone,
match by match, and its distributions are compared with the true red balls.

Three things are measured. The first is whether the centre of each team's distribution follows its true red balls.
The second is whether the distributions are as certain as they should be: the true red balls should lie inside an
80% interval in about 80% of the matches. The third is how many matches a team needs before its distribution stops
narrowing, which says how early in a season the estimates can be used.

The check sets the drift of section 5.8. The value of $\delta$ that gives the right coverage, while still following
the changes in skill, is the one the inference uses.

The check cannot show whether the model describes real football. The simulated matches come from the same model the
inference assumes, so a good result shows that the inference recovers skill when the model is right, and nothing
more. How well the model fits real matches is the subject of chapters 6 and 7.
