# 6. Prediction

This chapter shows how the skill distributions predict the next match. Inference (chapter 5) goes from matches to
skill; prediction goes from skill to the next match. Before a match, each team's skill is held as the distribution
$\pi_H$ or $\pi_A$, after the drift of section 5.7. From these the chapter predicts each team's number of shots, the
xG of a shot, and the result. The fit of chapter 7 scores the first two against real matches, and the result is
used to tune and test that fit and in chapter 9.

## 6.1 The match urns before the match

Every prediction mixes the equations of chapter 4 over the match urns the teams may draw. Before the match, the
probability that the home team's match urn holds $j$ red balls is

$$
\omega_H(j) = \sum_{s} \pi_H(s)\, P(m_u = j \mid m_s = s)
$$

with the hypergeometric probabilities of section 4.2, and $\omega_A(k)$ is the same for the away team. The two skill
distributions are independent (section 5.6), and so are the two draws into the match urns, so a pair of match urns
has the probability $\omega_H(j)\, \omega_A(k)$.

One pair is left out. When both match urns hold only red balls, who shoots is never decided (section 4.4), so the
pair is given probability zero, as in section 5.4, and the other pairs are scaled so that their probabilities add up
to one. Below, $\omega(j, k)$ is that scaled probability.

## 6.2 Shot counts

Given the match urns, each team's number of shots is binomial. Each round gives a home shot with probability $p_t q$
and an away shot with probability $p_t (1 - q)$, with $p_t$ of section 4.3 and $q$ of section 4.4, so before the
match

$$
P(N_H = c) = \sum_{j, k} \omega(j, k) \binom{n}{c} \big(p_t q\big)^c \big(1 - p_t q\big)^{n - c}
$$

with $q$ computed for the match urns $j$ and $k$, and $P(N_A = c)$ the same with $1 - q$. The two counts share the
$n$ rounds, so they are not independent: given the match urns, $N_H + N_A$ is the binomial $N$ of section 4.3.

## 6.3 The xG of a shot

The xG of a home shot is predicted from $\ell_H$ of section 5.2. Given that a shot is taken by the home team, each
pair of match urns is weighted by how likely it makes a home shot:

$$
P_H(v) = \frac{\sum_{j, k} \omega(j, k)\, \ell_H(v \mid j, k)}{\sum_{j, k} \omega(j, k)\, q(j, k)}
$$

and $P_A(v)$ is the same with $\ell_A$ and $1 - q$. Since $\ell_H(v \mid j, k)$ adds up to $q(j, k)$ over the
values $v$, $P_H$ adds up to one. It is the distribution of one home shot. The shots of one match share their match
urns, so their xG values are not independent of each other before the match.

## 6.4 The result

Given the match urns, every round is a draw with three outcomes: a home goal, an away goal, or neither. A round
holds at most one shot, and a shot is a goal with probability equal to its xG (section 4.6), so the probability of a
home goal in a round is the probability of a home shot times the mean xG of a home shot:

$$
\gamma_H(j, k) = p_t \sum_v v\, \ell_H(v \mid j, k), \qquad \gamma_A(j, k) = p_t \sum_v v\, \ell_A(v \mid j, k)
$$

The rounds are independent given the match urns, so the goals of the two teams are multinomial over the $n$ rounds:

$$
P(G_H = g,\, G_A = h \mid j, k) = \frac{n!}{g!\, h!\, (n - g - h)!}\, \gamma_H^{\,g}\, \gamma_A^{\,h}\,
(1 - \gamma_H - \gamma_A)^{n - g - h}
$$

The result before the match mixes this over the match urns:

$$
P(\text{home win}) = \sum_{j, k} \omega(j, k) \sum_{g > h} P(G_H = g,\, G_A = h \mid j, k)
$$

and the same with $g = h$ for a draw and $g < h$ for an away win. Section 4.7 gives the result once the xG of every
shot is known; this is the result before the match, when nothing about it is known but the skill distributions.

Given the match urns, the goals of the two teams are not independent here, unlike in section 4.7, since they share
the $n$ rounds.
