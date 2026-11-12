# 4. Model mechanics

This chapter defines the model: how a match is played with urns and balls, and how the mean, variance and skewness
of each step follow from the step before.

## 4.1 Containers and symbols

The model uses four kinds of urn and two kinds of marked ball, and every ball is red or white.

| Container | What it holds | Lifetime |
| --- | --- | --- |
| Skill pool | One per team; its red balls are the team's skill | Changes only between matches |
| Match urn | One per team, drawn from the skill pool; the home team's also holds h-marked balls | One match |
| Tempo urn | One, shared by both teams | Fixed |
| Shot urn | The attacking team's remaining balls and a set of x-marked balls | One shot |

The symbols follow one pattern. $M$ and $m$ count the balls and the red balls an urn holds, $K$ and $k$ the balls
and the red balls a team draws, and $X$ and $x$ the marked balls and the red marked balls. The starting values are
the model's current values and are not fitted.

| Symbol | Meaning | Starting value |
| --- | --- | --- |
| $M_s$, $m_s$ | Balls and red balls in a skill pool | 100; $m_s$ from 10 to 25 by team |
| $M_u$, $m_u$ | Balls drawn from the skill pool into a match urn, and red balls among them | 20; $m_u$ is drawn |
| $M_t$, $m_t$ | Balls and red balls in the tempo urn | 4 and 1 |
| $n$ | Rounds per match | 100 |
| $N$, $N_H$, $N_A$ | Shots in a match: total, home, away | drawn |
| $K_s$, $k_s$ | Balls each team draws to decide who shoots, and red balls among them | 3; $k_s$ is drawn |
| $b$ | Big-chance margin | 2 |
| $K_a$, $k_a$ | Balls drawn by the attacking team, and red balls among them | 5; $k_a$ is drawn |
| $K_d$, $k_d$ | Balls drawn by the defending team, and red balls among them | 1; $k_d$ is drawn |
| $c$ | Red balls cancelled, $c = \min(k_a, k_d)$ | drawn |
| $x_H$ | Red h-marked balls in the home team's match urn | 1 |
| $X_o$, $x_o$ | x-marked balls and red x-marked balls for an ordinary chance | 21 and 1 |
| $X_b$, $x_b$ | x-marked balls and red x-marked balls for a big chance | 20 and 8 |
| $X$, $x$ | Whichever x-marked set the shot uses | – |

The subscripts $H$ and $A$ mark the home and away team, and $U_H$ and $U_A$ are their match urns. The lowercase $a$
is the attacking team, whichever side it is on.

## 4.2 Before the match: skill pool and match urn

Skill change is the first step of a match, and it is not random. Whoever runs the model may change the number of red
balls in each team's skill pool between matches.

Each team then fills its match urn by drawing $M_u$ balls from its skill pool without replacement. The number of red
balls $m_u$ in the match urn is hypergeometric. With $p_s = m_s / M_s$:

$$
P(m_u = j) = \frac{\binom{m_s}{j}\binom{M_s - m_s}{M_u - j}}{\binom{M_s}{M_u}}
$$

- Mean: $E[m_u] = M_u p_s$
- Variance: $\operatorname{Var}(m_u) = M_u p_s (1 - p_s) \dfrac{M_s - M_u}{M_s - 1}$
- Skewness: $\dfrac{(M_s - 2 m_s)(M_s - 2 M_u)\sqrt{M_s - 1}}{(M_s - 2)\sqrt{M_u m_s (M_s - m_s)(M_s - M_u)}}$

The home team then adds $x_H$ red h-marked balls to its match urn. Its match urn holds $M_u + x_H$ balls, of which
$m_u + x_H$ are red. The h-marked balls are added, not drawn, so they add exactly $x_H$ to the home team's red balls:
the mean becomes $M_u p_s + x_H$, and the variance and skewness stay as above.

The match urns stay the same for the whole match. Every ball drawn from a match urn during a round goes back before
the next round.

After the match the h-marked balls are taken out, and every other ball goes back into its skill pool. Each skill pool
then holds $M_s$ balls, $m_s$ of them red, as before the match.

## 4.3 Each round: shot or not

Each of the $n$ rounds starts with one draw from the tempo urn. A red ball means a shot; a white ball ends the round.
The probability of a shot in a round is $p_t = m_t / M_t$, the same in every round, so the number of shots $N$ in a
match is binomial:

$$
P(N = j) = \binom{n}{j}\, p_t^{\,j} (1 - p_t)^{n - j}
$$

- Mean: $E[N] = n p_t$
- Variance: $\operatorname{Var}(N) = n p_t (1 - p_t)$
- Skewness: $\dfrac{1 - 2p_t}{\sqrt{n p_t (1 - p_t)}}$

## 4.4 Who shoots

When there is a shot, each team draws $K_s$ balls from its match urn without replacement. The team that draws more
red balls attacks and shoots; the other team defends.

A tie is broken one ball at a time. If both teams draw the same number of red balls, each team draws one more ball
from what is left in its match urn, and this is repeated until one team draws red and the other white. That team
attacks. If a match urn runs out of balls, all drawn balls go back and the tie-break continues.

The shot is a big chance if the attacking team drew at least $b$ more red balls than the defending team; otherwise
it is an ordinary chance. A shot won in the tie-break is always an ordinary chance. All drawn balls then go back into
the match urns.

The probability that the home team attacks follows from the two draws. Let $k_{s,H}$ and $k_{s,A}$ be the red balls
the home and away team draw; each is hypergeometric in its own match urn. The probability $q$ that the home team
attacks, and the probabilities $\beta_H$ and $\beta_A$ that the shot is a home or an away big chance, are:

$$
q = P(k_{s,H} > k_{s,A}) + P(k_{s,H} = k_{s,A})\,P(\text{home wins the tie-break})
$$

$$
\beta_H = P(k_{s,H} - k_{s,A} \ge b), \qquad \beta_A = P(k_{s,A} - k_{s,H} \ge b)
$$

Each probability over the draws is a double sum, for example
$P(k_{s,H} > k_{s,A}) = \sum_{i > j} P(k_{s,H} = i)\,P(k_{s,A} = j)$. The probability of winning the tie-break is a
finite sum over the balls left in the two match urns.

The home share of shots is $S = N_H / N$, for matches with at least one shot. Given the match urns, every shot goes
to the home team with probability $q$, independently of $N$, so $N_H$ is binomial with $N$ trials:

- Mean: $E[S \mid q] = q$
- Variance: $\operatorname{Var}(S \mid q) = q(1 - q)\,E[1/N]$
- Third central moment: $\mu_3(S \mid q) = q(1 - q)(1 - 2q)\,E[1/N^2]$

Over matches between the same two teams, $q$ varies with the match urns. With $E[q]$, $\operatorname{Var}(q)$ and
$\mu_3(q)$ its moments over the draws of section 4.2:

- Mean: $E[S] = E[q]$
- Variance: $\operatorname{Var}(S) = E[1/N]\,E[q(1 - q)] + \operatorname{Var}(q)$
- Skewness: $\big(E[1/N^2]\,E[q(1 - q)(1 - 2q)] + 3\,E[1/N]\,\operatorname{Cov}(q,\, q(1 - q)) + \mu_3(q)\big)
  / \operatorname{Var}(S)^{3/2}$

## 4.5 The shot urn

The attacking team draws $K_a$ balls from its match urn and gets $k_a$ red balls. The defending team draws $K_d$
balls from its own match urn and gets $k_d$ red balls, then puts them back. Both draws are without replacement.

The defending team's red balls cancel the attacking team's red balls. The attacking team takes $c = \min(k_a, k_d)$
red balls out of its draw and puts the remaining $K_a - c$ balls, $k_a - c$ of them red, into the shot urn.

The x-marked set for the kind of shot is added to the shot urn: $X_o$ balls, $x_o$ of them red, for an ordinary
chance, and $X_b$ balls, $x_b$ of them red, for a big chance. The shot's xG is the red share of the shot urn:

$$
\text{xG} = g(k_a, k_d) = \frac{x + k_a - c}{X + K_a - c}
$$

Given the match urns and the kind of shot, the xG distribution is a finite sum. The balls from section 4.4 went
back, so $k_a$ and $k_d$ are hypergeometric in the attacking and defending team's full match urns, independent of
each other. With $P(i, j) = P(k_a = i)\,P(k_d = j)$:

- Distribution: $P(\text{xG} = v) = \sum_{g(i, j) = v} P(i, j)$
- Mean: $\mu = \sum_{i, j} P(i, j)\,g(i, j)$
- Variance: $\sigma^2 = \sum_{i, j} P(i, j)\,\big(g(i, j) - \mu\big)^2$
- Skewness: $\sum_{i, j} P(i, j)\,\big(g(i, j) - \mu\big)^3 / \sigma^3$

With the ordinary set these are $\mu_o$, $\sigma_o$ and the third central moment $\mu_{3,o}$; with the big-chance
set, $\mu_b$, $\sigma_b$ and $\mu_{3,b}$.

A team's shots are a mix of the two kinds. Given the match urns, a home shot is a big chance with probability
$f_b = \beta_H / q$, and an away shot with probability $f_b = \beta_A / (1 - q)$; in both cases $f_o = 1 - f_b$.
With $\bar\mu = f_o \mu_o + f_b \mu_b$, the xG of the team's shots has:

- Mean: $\bar\mu$
- Variance: $f_o \sigma_o^2 + f_b \sigma_b^2 + f_o f_b (\mu_b - \mu_o)^2$
- Third central moment: $\sum_{k \in \{o, b\}} f_k \big(\mu_{3,k} + 3\sigma_k^2(\mu_k - \bar\mu) + (\mu_k - \bar\mu)^3\big)$

Over matches between the same two teams, each pair of match urns counts in proportion to its probability and to how
many shots the team gets with it. For the home team:

$$
P(\text{xG} = v) = \frac{\sum_{U_H, U_A} P(U_H)\,P(U_A)\,\big[(q - \beta_H)\,P_o(v) + \beta_H\,P_b(v)\big]}
{\sum_{U_H, U_A} P(U_H)\,P(U_A)\,q}
$$

where $q$, $\beta_H$ and the ordinary and big-chance distributions $P_o$ and $P_b$ belong to each pair of match urns.
The moments follow from this distribution in the same way.

## 4.6 The goal

One ball is drawn from the shot urn, and a red ball is a goal. The x-marked balls are then taken out, and all of the
attacking team's drawn balls, the cancelled ones included, go back into its match urn. For each shot the model records the round, the
attacking team, the xG and whether it was a goal.

Given the xG values $\text{xG}_1, \dots, \text{xG}_N$ of a team's shots in a match, each shot is a goal with
probability equal to its xG, independently of the others. The team's goals $G$ then have:

- Mean: $E[G] = \sum_j \text{xG}_j$
- Variance: $\operatorname{Var}(G) = \sum_j \text{xG}_j (1 - \text{xG}_j)$
- Skewness: $\sum_j \text{xG}_j (1 - \text{xG}_j)(1 - 2\,\text{xG}_j) \,/\, \operatorname{Var}(G)^{3/2}$

Given only the match urns, every round gives the home team a goal with the same probability, since a round has at
most one shot and every ball goes back:

$$
\gamma_H = p_t\,\big[(q - \beta_H)\,\mu_o + \beta_H\,\mu_b\big]
$$

with $\mu_o$ and $\mu_b$ the mean xG of the home team's ordinary and big chances from section 4.5. For the away
team, with $\mu_o$ and $\mu_b$ its own mean xG:

$$
\gamma_A = p_t\,\big[(1 - q - \beta_A)\,\mu_o + \beta_A\,\mu_b\big]
$$

The home goals $G_H$ are binomial, and the away goals $G_A$ the same with $\gamma_A$:

$$
P(G_H = j) = \binom{n}{j}\, \gamma_H^{\,j} (1 - \gamma_H)^{n - j}
$$

- Mean: $n \gamma_H$
- Variance: $n \gamma_H (1 - \gamma_H)$
- Skewness: $\dfrac{1 - 2\gamma_H}{\sqrt{n \gamma_H (1 - \gamma_H)}}$

Over matches between the same two teams, the goals are a mixture of these binomials over the match urns, weighted
by $P(U_H)\,P(U_A)$.

## 4.7 The result

The result follows from the goals of the two teams. Given the match urns, each round ends in a home goal with
probability $\gamma_H$, an away goal with probability $\gamma_A$, or neither, so the two goal counts are multinomial
over the $n$ rounds:

$$
P(G_H = i, G_A = j) = \frac{n!}{i!\,j!\,(n - i - j)!}\,\gamma_H^{\,i}\,\gamma_A^{\,j}\,(1 - \gamma_H - \gamma_A)^{n - i - j}
$$

The probability of a home win is the sum of this over $i > j$, of a draw over $i = j$, and of an away win over
$i < j$. Given the match urns, $\operatorname{Cov}(G_H, G_A) = -n \gamma_H \gamma_A$. Over matches between the same
two teams, the result probabilities are averaged over the match urns, weighted by $P(U_H)\,P(U_A)$.
