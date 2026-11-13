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

The subscripts $H$ and $A$ mark the home and away team, for example $m_{u,H}$ and $m_{u,A}$ for the red balls each
team draws into its match urn. The lowercase subscripts $a$ and $d$ mark the attacking and the defending team,
whichever side each is on.

A running example follows one match through sections 4.2 to 4.5 and ends in section 4.8. The home team has
$m_{s,H} = 18$ red balls in its skill pool and the away team $m_{s,A} = 12$, and every other symbol has its starting
value. The example asks for the probability that the home team gets a big chance with $\text{xG} = 0.40$ in the
first round.

## 4.2 Before the match: skill pool and match urn

Skill change is the first step of a match, and it is not random. Whoever runs the model may change the number of red
balls in each team's skill pool between matches.

Each team then fills its match urn by drawing $M_u$ balls from its skill pool without replacement. The number of red
balls $m_u$ in the match urn is hypergeometric. With $p_s = m_s / M_s$:

$$
P(m_u = j) = \frac{\binom{m_s}{j}\binom{M_s - m_s}{M_u - j}}{\binom{M_s}{M_u}}
$$

- Mean: $E[m_u] = M_u p_s$
- Variance: $\mathrm{Var}(m_u) = M_u p_s (1 - p_s) \dfrac{M_s - M_u}{M_s - 1}$
- Skewness: $\dfrac{(M_s - 2 m_s)(M_s - 2 M_u)\sqrt{M_s - 1}}{(M_s - 2)\sqrt{M_u m_s (M_s - m_s)(M_s - M_u)}}$

The home team then adds $x_H$ red h-marked balls to its match urn. Its match urn holds $M_u + x_H$ balls, of which
$m_{u,H} + x_H$ are red; the away team's holds $M_u$ balls, of which $m_{u,A}$ are red. The h-marked balls are added, not drawn, so they add exactly $x_H$ to the home team's red balls:
the mean becomes $M_u p_s + x_H$, and the variance and skewness stay as above.

The match urns stay the same for the whole match. Every ball drawn from a match urn during a round goes back before
the next round.

After the match the h-marked balls are taken out, and every other ball goes back into its skill pool. Each skill pool
then holds $M_s$ balls, $m_s$ of them red, as before the match.

**Example.** The home team draws $m_{u,H} = 4$ red balls with probability 0.2383, and the away team draws
$m_{u,A} = 2$ with probability 0.2978. With the h-marked ball, the home team's match urn then holds 5 red balls out
of 21, and the away team's 2 out of 20. Sections 4.3 to 4.5 follow these two match urns.

## 4.3 Each round: shot or not

Each of the $n$ rounds starts with one draw from the tempo urn. A red ball means a shot; a white ball ends the round.
The probability of a shot in a round is $p_t = m_t / M_t$, the same in every round, so the number of shots $N$ in a
match is binomial:

$$
P(N = j) = \binom{n}{j}\, p_t^{\,j} (1 - p_t)^{n - j}
$$

- Mean: $E[N] = n p_t$
- Variance: $\mathrm{Var}(N) = n p_t (1 - p_t)$
- Skewness: $\dfrac{1 - 2p_t}{\sqrt{n p_t (1 - p_t)}}$

**Example.** The first round has a shot with probability $p_t = 1/4 = 0.25$.

## 4.4 Who shoots

When there is a shot, each team draws $K_s$ balls from its match urn without replacement. The team that draws more
red balls attacks and shoots; the other team defends.

A tie is broken one ball at a time. If both teams draw the same number of red balls, each team draws one more ball
from what is left in its match urn, and this is repeated until one team draws red and the other white. That team
attacks. If a match urn runs out of balls, all drawn balls go back and the tie-break continues.

The shot is a big chance if the attacking team drew at least $b$ more red balls than the defending team; otherwise
it is an ordinary chance. A shot won in the tie-break is always an ordinary chance. All drawn balls then go back into
the match urns.

The two draws are hypergeometric in the two match urns. With $k_{s,H}$ and $k_{s,A}$ the red balls the home and
away team draw:

$$
P(k_{s,H} = i) = \frac{\binom{m_{u,H} + x_H}{i}\binom{M_u - m_{u,H}}{K_s - i}}{\binom{M_u + x_H}{K_s}}, \qquad
P(k_{s,A} = j) = \frac{\binom{m_{u,A}}{j}\binom{M_u - m_{u,A}}{K_s - j}}{\binom{M_u}{K_s}}
$$

The tie-break is a recursion on the balls left in the two match urns. With $r_H$ red balls among $\ell_H$ left in the
home team's match urn and $r_A$ among $\ell_A$ in the away team's, the probability $t$ that the home team wins the
tie-break is

$$
t(r_H, \ell_H, r_A, \ell_A) = \frac{r_H}{\ell_H}\Big(1 - \frac{r_A}{\ell_A}\Big)
+ \frac{r_H}{\ell_H}\,\frac{r_A}{\ell_A}\; t(r_H - 1, \ell_H - 1, r_A - 1, \ell_A - 1)
+ \Big(1 - \frac{r_H}{\ell_H}\Big)\Big(1 - \frac{r_A}{\ell_A}\Big)\; t(r_H, \ell_H - 1, r_A, \ell_A - 1)
$$

When $\ell_H$ or $\ell_A$ reaches zero, all balls go back, and $t$ takes its value from the full match urns,
$t^* = t(m_{u,H} + x_H,\ M_u + x_H,\ m_{u,A},\ M_u)$. Every path then ends either in a winner or in $t^*$, so $t^*$
is the solution of one linear equation. A tie at $i$ red balls each starts the tie-break from
$t_i = t(m_{u,H} + x_H - i,\ M_u + x_H - K_s,\ m_{u,A} - i,\ M_u - K_s)$.

The probability $q$ that the home team attacks, and the probabilities $\beta_H$ and $\beta_A$ that the shot is a home
or an away big chance, are then

$$
q = \sum_{i > j} P(k_{s,H} = i)\,P(k_{s,A} = j) + \sum_i P(k_{s,H} = i)\,P(k_{s,A} = i)\,t_i
$$

$$
\beta_H = \sum_{i - j \ge b} P(k_{s,H} = i)\,P(k_{s,A} = j), \qquad
\beta_A = \sum_{j - i \ge b} P(k_{s,H} = i)\,P(k_{s,A} = j)
$$

Each shot is therefore, independently of the others, a home ordinary chance with probability $q - \beta_H$, a home
big chance with probability $\beta_H$, an away ordinary chance with probability $1 - q - \beta_A$, or an away big
chance with probability $\beta_A$.

Given the $N$ shots of section 4.3, the home team's shots $N_H$ are binomial, and the home share of shots is
$S = N_H / N$:

$$
P(N_H = j) = \binom{N}{j}\, q^{\,j} (1 - q)^{N - j}
$$

- Mean: $E[S] = q$
- Variance: $\mathrm{Var}(S) = q(1 - q) / N$
- Skewness: $\dfrac{1 - 2q}{\sqrt{N q (1 - q)}}$

**Example.** With 5 red balls out of 21, the home team draws $k_{s,H} = 0, 1, 2, 3$ red balls with probabilities
0.4211, 0.4511, 0.1203 and 0.0075; with 2 out of 20, the away team draws $k_{s,A} = 0, 1, 2$ with probabilities
0.7158, 0.2684 and 0.0158. A home big chance needs $k_{s,H} - k_{s,A} \ge 2$, which happens for $(2, 0)$, $(3, 0)$
and $(3, 1)$ with probabilities 0.0861, 0.0054 and 0.0020. So $\beta_H = 0.0935$. A big chance is never won in the
tie-break, so the tie-break is not needed here.

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

The two draws are hypergeometric in the two match urns. Let the attacking team's match urn hold $M_{u,a}$ balls,
$m_{u,a}$ of them red, and the defending team's $M_{u,d}$ balls, $m_{u,d}$ of them red; for the home team these are
$M_u + x_H$ and $m_{u,H} + x_H$, and for the away team $M_u$ and $m_{u,A}$. The balls from section 4.4 went back,
so both draws are from full match urns:

$$
P(k_a = i) = \frac{\binom{m_{u,a}}{i}\binom{M_{u,a} - m_{u,a}}{K_a - i}}{\binom{M_{u,a}}{K_a}}, \qquad
P(k_d = j) = \frac{\binom{m_{u,d}}{j}\binom{M_{u,d} - m_{u,d}}{K_d - j}}{\binom{M_{u,d}}{K_d}}
$$

Given the kind of shot, the xG distribution is a finite sum over the two draws. With
$P(i, j) = P(k_a = i)\,P(k_d = j)$ and $x$, $X$ the x-marked set for that kind of shot:

- Distribution: $P(\text{xG} = v) = \sum_{g(i, j) = v} P(i, j)$
- Mean: $\mu = \sum_{i, j} P(i, j)\,g(i, j)$
- Variance: $\sigma^2 = \sum_{i, j} P(i, j)\,\big(g(i, j) - \mu\big)^2$
- Skewness: $\sum_{i, j} P(i, j)\,\big(g(i, j) - \mu\big)^3 / \sigma^3$

**Example.** For a home big chance the shot urn gets $X_b = 20$ x-marked balls, $x_b = 8$ of them red. The xG is
$10/25 = 0.40$ only when the home team draws $k_a = 2$ red balls and the away team $k_d = 0$, so that nothing is
cancelled. The home team gets 2 red balls among its $K_a = 5$ with probability 0.2752, and the away team draws a
white ball with probability $18/20 = 0.9$. So $P(\text{xG} = 0.40) = 0.2752 \times 0.9 = 0.2477$.

## 4.6 The goal

One ball is drawn from the shot urn, and a red ball is a goal. The x-marked balls are then taken out, and all of the
attacking team's drawn balls, the cancelled ones included, go back into its match urn. For each shot the model
records the round, the attacking team, the xG and whether it was a goal.

Given the shot's xG, the goal is a single draw that succeeds with probability xG:

- Mean: $\text{xG}$
- Variance: $\text{xG}\,(1 - \text{xG})$
- Skewness: $\dfrac{1 - 2\,\text{xG}}{\sqrt{\text{xG}\,(1 - \text{xG})}}$

A team's goals in a match add up these draws, one for each of its shots. With $\text{xG}_1, \dots, \text{xG}_{N_H}$
the xG values of the home team's shots, its goals $G_H$ have the distribution given by the coefficients of $z^g$ in a
product with one factor per shot:

$$
\sum_g P(G_H = g)\, z^g = \prod_{j=1}^{N_H} \big(1 - \text{xG}_j + \text{xG}_j\, z\big)
$$

- Mean: $E[G_H] = \sum_j \text{xG}_j$
- Variance: $\mathrm{Var}(G_H) = \sum_j \text{xG}_j (1 - \text{xG}_j)$
- Skewness: $\sum_j \text{xG}_j (1 - \text{xG}_j)(1 - 2\,\text{xG}_j) \,/\, \mathrm{Var}(G_H)^{3/2}$

The away team's goals $G_A$ are the same over its $N_A$ shots.

## 4.7 The result

The result follows from the goals of the two teams. Given the xG values of both teams' shots, every shot's goal
draw is separate, so $G_H$ and $G_A$ are independent:

$$
P(\text{home win}) = \sum_{i > j} P(G_H = i)\,P(G_A = j), \qquad
P(\text{draw}) = \sum_i P(G_H = i)\,P(G_A = i), \qquad
P(\text{away win}) = \sum_{i < j} P(G_H = i)\,P(G_A = j)
$$

## 4.8 The running example

The running example ends with the probability that the home team gets a big chance with $\text{xG} = 0.40$ in the
first round. Given the two match urns of the example, it is the product of the three steps:

$$
p_t\,\beta_H\,P(\text{xG} = 0.40) = 0.25 \times 0.0935 \times 0.2477 = 0.00579
$$

From the skill pools alone, the same product is taken for every pair of match urns and weighted by the probabilities
of section 4.2:

$$
P = \sum_{j, k} P(m_{u,H} = j)\,P(m_{u,A} = k)\; p_t\,\beta_H(j, k)\,P_b(\text{xG} = 0.40 \mid j, k) = 0.00544
$$

Here $\beta_H(j, k)$ and $P_b(\text{xG} = 0.40 \mid j, k)$ are the results of sections 4.4 and 4.5 for match urns
with $j$ and $k$ red balls drawn.
