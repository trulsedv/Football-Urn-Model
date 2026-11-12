# 4. Model mechanics

This chapter defines the model: how a match is played with urns and balls, and how the mean, variance and skewness
of each step follow from the step before. The rules stated here are the rules of the model, and anything that plays
or computes the model follows them. The sections follow one match from start to finish.

## 4.1 Containers and symbols

The model uses four kinds of urn and two kinds of marked ball, and every ball is red or white. A marked red ball
counts as red. Marked balls are added for a purpose and taken out again afterwards.

| Container | What it holds | Lifetime |
| --- | --- | --- |
| Skill pool | One per team; its red balls are the team's skill | Changes only between matches |
| Match urn | One per team, drawn from the skill pool; the home team's also holds h-marked balls | One match |
| Tempo urn | One, shared by both teams | Fixed |
| Shot urn | The shooting team's remaining chance balls and a set of x-marked balls | One shot |

All symbols are in one table, with the starting values used in the examples. The starting values are not fitted.

| Symbol | Meaning | Starting value |
| --- | --- | --- |
| $M_s$, $m_s$ | Balls and red balls in a skill pool | 100; $m_s$ from 10 to 25 by team |
| $M_u$, $m_u$ | Balls drawn from the skill pool into a match urn, and red balls among them | 20; $m_u$ is drawn |
| $m_h$ | Red h-marked balls added to the home team's match urn | 1 |
| $M_t$, $m_t$ | Balls and red balls in the tempo urn; $p = m_t / M_t$ | 4 and 1 ($p = 0.25$) |
| $n$ | Rounds per match | 100 |
| $T$ | Shots in a match | drawn |
| $k_w$ | Balls each team grabs to decide who shoots | 3 |
| $b$ | Big-chance margin: red balls by which the shooter must win the grab | 2 |
| $q$ | Probability that the home team wins a shot | follows from the match urns |
| $\beta_h$, $\beta_a$ | Probability that a shot is a home, away big chance | follow from the match urns |
| $k_c$, $R_1$ | Chance balls drawn by the shooting team, and red balls among them | 5; $R_1$ is drawn |
| $k_d$, $R_2$ | Balls drawn by the defending team, and red balls among them | 1; $R_2$ is drawn |
| $c$ | Red chance balls cancelled by the defender, $c = \min(R_1, R_2)$ | drawn |
| $M_{xo}$, $m_{xo}$ | x-marked balls and red x-marked balls for an ordinary chance | 21 and 1 |
| $M_{xb}$, $m_{xb}$ | x-marked balls and red x-marked balls for a big chance | 20 and 8 |
| $M_x$, $m_x$ | Whichever x-marked set the shot uses | – |

The two match urns are written $U_h$ and $U_a$ where it matters which is meant. The home team's match urn holds
$M_u + m_h$ balls, $m_u + m_h$ of them red; the away team's holds $M_u$ balls, $m_u$ of them red.

## 4.2 Before the match: skill pool and match urn

Skill change is the first step of a match, and it is not random. Whoever runs the model may change the number of red
balls in each team's skill pool between matches.

Each team then fills its match urn by drawing $M_u$ balls from its skill pool without replacement. The number of red
balls $m_u$ in the match urn is hypergeometric:

$$
P(m_u = j) = \frac{\binom{m_s}{j}\binom{M_s - m_s}{M_u - j}}{\binom{M_s}{M_u}}
$$

The moments of $m_u$ follow from the skill pool alone. With $p_s = m_s / M_s$:

- Mean: $E[m_u] = M_u p_s$
- Variance: $\operatorname{Var}(m_u) = M_u p_s (1 - p_s) \dfrac{M_s - M_u}{M_s - 1}$
- Skewness: $\dfrac{(M_s - 2 m_s)(M_s - 2 M_u)\sqrt{M_s - 1}}{(M_s - 2)\sqrt{M_u m_s (M_s - m_s)(M_s - M_u)}}$

The variance is zero when $M_s = M_u$, since the whole pool then goes into the urn, and rises towards
$M_u p_s (1 - p_s)$ as $M_s$ grows. The skewness is zero for a pool that is half red, and positive when red is the
minority colour (with $M_u < M_s / 2$).

The home team adds $m_h$ red h-marked balls to its match urn. During the match an h-marked ball is an ordinary red
ball. The h-marked balls shift the home team's red count by $m_h$, so its variance and skewness are those above.

The match urns do not change during the match. Every ball drawn from a match urn in a round goes back before the
next round, so every round is played against the same two match urns.

After the match the h-marked balls are removed and every other ball goes back into the skill pool. The skill pool is
then exactly as it was before the match: $M_s$ balls, $m_s$ red.

## 4.3 Each round: shot or not

Each of the $n$ rounds starts with one draw from the tempo urn, and red means a shot. White ends the round with
nothing happening. The tempo urn does not depend on the match urns.

The number of shots $T$ in a match is binomial, $T \sim \text{Bin}(n, p)$, since the tempo urn is the same in every
round:

- Mean: $E[T] = np$
- Variance: $\operatorname{Var}(T) = np(1 - p)$
- Skewness: $\dfrac{1 - 2p}{\sqrt{np(1 - p)}}$

The variance is always below the mean. With the starting values, $E[T] = 25$ shots, the standard deviation is
$\sqrt{18.75} \approx 4.33$ and the skewness is $0.12$.

## 4.4 Who shoots

When there is a shot, each team grabs $k_w$ balls from its match urn, and the team with more red balls shoots. A tie
is broken one ball at a time. Each team draws one more ball from the balls left after its grab, and this repeats
until one team draws red and the other white; that team shoots. If a team's urn runs empty, all balls go back and
the tie-break continues from full urns.

If both urns hold only one colour, drawing can never break a tie. A fair draw then decides: one ball from an urn of
one red and one white ball, with each colour standing for one team. This rule is provisional.

The margin of the grab decides whether the shot is a big chance. If the shooting team had at least $b$ more red
balls in its grab, the shot is a big chance; otherwise it is ordinary. A team that wins in the tie-break never has a
big chance. All balls from the grab and the tie-break go back into the match urns.

The probability that the home team shoots follows from the two grabs. Let $X_h$ and $X_a$ be the red balls in the
home and away grabs; each is hypergeometric in its own match urn. With $t$ the probability that the home team wins
the tie-break, a finite calculation on the balls left in the two urns:

$$
q = P(X_h > X_a) + P(X_h = X_a)\,t, \qquad \beta_h = P(X_h - X_a \ge b), \qquad \beta_a = P(X_a - X_h \ge b)
$$

Each probability over the grabs is a double sum, for example $P(X_h > X_a) = \sum_{i > j} P(X_h = i)\,P(X_a = j)$.
A home shot is a big chance with probability $\beta_h / q$, and an away shot with probability $\beta_a / (1 - q)$.

The table shows how $k_w$ and the two red shares set the shooting team's probability, for match urns of 20 balls
and no home advantage:

| A red share | B red share | $k_w = 1$ | $k_w = 3$ | $k_w = 5$ | $k_w = 10$ |
| --- | --- | --- | --- | --- | --- |
| 0.55 | 0.45 | 0.60 | 0.64 | 0.67 | 0.77 |
| 0.60 | 0.40 | 0.70 | 0.76 | 0.81 | 0.93 |
| 0.30 | 0.20 | 0.64 | 0.67 | 0.71 | 0.82 |
| 0.15 | 0.10 | 0.62 | 0.64 | 0.66 | 0.76 |

The home share of shots $S$ is the home shots divided by $T$, for matches with at least one shot. Given the match
urns, every shot goes to the home team with the same probability $q$, independently of $T$, so the home shots are
$\text{Bin}(T, q)$:

- Mean: $E[S \mid q] = q$
- Variance: $\operatorname{Var}(S \mid q) = q(1 - q)\,E[1/T]$
- Third central moment: $\mu_3(S \mid q) = q(1 - q)(1 - 2q)\,E[1/T^2]$

Over matches between the same two teams, $q$ varies with the match urns of section 4.2. With $E[q]$,
$\operatorname{Var}(q)$ and $\mu_3(q)$ its moments over the two hypergeometric draws:

- Mean: $E[S] = E[q]$
- Variance: $\operatorname{Var}(S) = E[1/T]\,E[q(1 - q)] + \operatorname{Var}(q)$
- Skewness: $\big(E[1/T^2]\,E[q(1 - q)(1 - 2q)] + 3\,E[1/T]\,\operatorname{Cov}(q,\, q(1 - q)) + \mu_3(q)\big)
  / \operatorname{Var}(S)^{3/2}$

The first term of the variance is the noise from the limited number of shots, and the second is how much $q$ varies
between matches.

## 4.5 Chance quality: the shot urn

The shooting team draws $k_c$ chance balls from its match urn and gets $R_1$ red balls; the defending team draws
$k_d$ balls from its own match urn and gets $R_2$ red balls. Both draws are without replacement within the urn, and
the defender puts its balls back straight away.

The defender's red balls cancel the shooter's red balls. The shooter removes $c = \min(R_1, R_2)$ red balls, so a
good defence can take away part or all of a good attack, but never more than the attacker drew. The remaining
$k_c - c$ balls, of which $R_1 - c$ are red, go into the shot urn.

The x-marked set for the kind of shot decided in section 4.4 is added to the shot urn: $M_{xo}$ balls, $m_{xo}$ red,
for an ordinary chance, and $M_{xb}$ balls, $m_{xb}$ red, for a big chance. The shot's xG is the red share of the
shot urn:

$$
\text{xG} = g(R_1, R_2) = \frac{m_x + R_1 - c}{M_x + k_c - c}
$$

The starting values give each kind of shot a small set of possible values. With $k_c = 5$ and $k_d = 1$, an
ordinary shot can take 11 values, from $1/26 \approx 0.04$ to $6/26 \approx 0.23$, and a big chance 11 values, from
$8/25 = 0.32$ to $13/25 = 0.52$.

Given the match urns and the kind of shot, the xG distribution is a finite sum. The balls from the grab went back,
so $R_1$ and $R_2$ are fresh hypergeometric draws from the shooter's and the defender's match urns, independent of
each other and of the grab. Writing $P(r_1, r_2) = P(R_1 = r_1)\,P(R_2 = r_2)$:

- Distribution: $P(\text{xG} = v) = \sum_{g(r_1, r_2) = v} P(r_1, r_2)$
- Mean: $\mu_x = \sum_{r_1, r_2} P(r_1, r_2)\,g(r_1, r_2)$
- Variance: $\sigma_x^2 = \sum_{r_1, r_2} P(r_1, r_2)\,\big(g(r_1, r_2) - \mu_x\big)^2$
- Skewness: $\sum_{r_1, r_2} P(r_1, r_2)\,\big(g(r_1, r_2) - \mu_x\big)^3 / \sigma_x^3$

The ordinary set gives the moments $\mu_o$, $\sigma_o$ and third central moment $\mu_{3,o}$; the big-chance set gives
$\mu_b$, $\sigma_b$ and $\mu_{3,b}$.

A team's shots mix the two kinds. Given the match urns, a home shot is ordinary with weight $w_o = (q - \beta_h)/q$
and a big chance with weight $w_b = \beta_h / q$; for the away team, $w_b = \beta_a / (1 - q)$ and $w_o = 1 - w_b$.
With $\mu = w_o \mu_o + w_b \mu_b$:

- Mean: $\mu$
- Variance: $w_o \sigma_o^2 + w_b \sigma_b^2 + w_o w_b (\mu_b - \mu_o)^2$
- Third central moment: $\sum_{k \in \{o, b\}} w_k \big(\mu_{3,k} + 3\sigma_k^2(\mu_k - \mu) + (\mu_k - \mu)^3\big)$

Over matches between the same two teams, each pair of match urns contributes in proportion to its probability and
to how many shots the team gets with it. For the home team:

$$
P(\text{xG} = v) = \frac{\sum_{U_h, U_a} P(U_h)\,P(U_a)\,\big[(q - \beta_h)\,P_o(v) + \beta_h\,P_b(v)\big]}
{\sum_{U_h, U_a} P(U_h)\,P(U_a)\,q}
$$

where $q$, $\beta_h$ and the ordinary and big-chance distributions $P_o$ and $P_b$ belong to each pair of match urns.
The moments follow from this distribution as above.

## 4.6 The goal

One ball is drawn from the shot urn, and red, marked or not, is a goal. The x-marked balls are then taken out, and
the chance balls go back to the match urn they came from. For each shot the model records the round, the shooting
team, the xG and whether it was a goal.

Given the xG values $x_1, \dots, x_k$ of a team's shots in a match, its goals $G$ are a sum of independent draws,
one per shot, each a goal with probability $x_j$:

- Mean: $E[G] = \sum_j x_j$
- Variance: $\operatorname{Var}(G) = \sum_j x_j (1 - x_j)$
- Skewness: $\sum_j x_j (1 - x_j)(1 - 2x_j) \,/\, \operatorname{Var}(G)^{3/2}$

Given only the match urns, each round gives the home team a goal with one fixed probability. A round has at most one
shot, and since every ball goes back, every round is played the same way:

$$
\gamma_h = p\,\big[(q - \beta_h)\,\mu_o + \beta_h\,\mu_b\big]
$$

with $\mu_o$ and $\mu_b$ the home team's ordinary and big-chance mean xG from section 4.5. The away team's
$\gamma_a$ is the same with $1 - q$, $\beta_a$ and the away team's mean xG. The home goals are then
$\text{Bin}(n, \gamma_h)$:

- Mean: $n \gamma_h$
- Variance: $n \gamma_h (1 - \gamma_h)$
- Skewness: $\dfrac{1 - 2\gamma_h}{\sqrt{n \gamma_h (1 - \gamma_h)}}$

Over matches between the same two teams, the goals are a mixture of these binomials over the match urns, weighted
by $P(U_h)\,P(U_a)$.

## 4.7 The result

The result follows from the goals of the two teams. Given the match urns, each round ends in a home goal with
probability $\gamma_h$, an away goal with probability $\gamma_a$, or neither. The two goal counts are therefore
multinomial over the $n$ rounds:

$$
P(G_h = i, G_a = j) = \frac{n!}{i!\,j!\,(n - i - j)!}\,\gamma_h^{\,i}\,\gamma_a^{\,j}\,(1 - \gamma_h - \gamma_a)^{n - i - j}
$$

The probability of a home win is the sum of this over $i > j$, of a draw over $i = j$, and of an away win over
$i < j$. Given the match urns the two goal counts are slightly negatively correlated,
$\operatorname{Cov}(G_h, G_a) = -n \gamma_h \gamma_a$, because a round cannot give both teams a goal. Over matches
between the same two teams, the result probabilities are averaged over the match urns, weighted by
$P(U_h)\,P(U_a)$.
