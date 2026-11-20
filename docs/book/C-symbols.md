# Appendix C. Symbols

This appendix lists every symbol used in chapters 4 to 7 and appendices A and B, with the section where it is
defined. Summation indices such as $i$ and $r$ are left out, and so are symbols used only inside a single formula
whose text defines them there.

The symbols follow one pattern. $M$ and $m$ count the balls and the red balls an urn holds, $K$ and $k$ the balls
and the red balls a team draws, and $X$ and $x$ the marked balls and the red marked balls. The subscripts $H$ and $A$
mark the home and away team, and $a$ and $d$ the attacking and defending team.

## Model (chapter 4)

| Symbol | Meaning | Defined in |
| --- | --- | --- |
| $M_s$, $m_s$ | Balls and red balls in a skill pool; $m_s$ is the team's skill | 4.1 |
| $p_s$ | Red share of a skill pool, $m_s / M_s$ | 4.2 |
| $M_u$, $m_u$ | Balls drawn from the skill pool into a match urn, and red balls among them | 4.1, 4.2 |
| $M_{u,a}$, $m_{u,a}$, $M_{u,d}$, $m_{u,d}$ | Balls and red balls in the attacking and the defending team's match urn | 4.5 |
| $x_H$ | Red h-marked balls in the home team's match urn | 4.1, 4.2 |
| $M_t$, $m_t$ | Balls and red balls in the tempo urn | 4.1 |
| $p_t$ | Probability of a shot in a round, $m_t / M_t$ | 4.3 |
| $n$ | Rounds per match | 4.1 |
| $N$, $N_H$, $N_A$ | Shots in a match: total, home, away | 4.3, 4.4 |
| $K_s$, $k_s$ | Balls each team draws to decide who shoots, and red balls among them | 4.4 |
| $k_{s,H}$, $k_{s,A}$ | Red balls the home and the away team draw to decide who shoots | 4.4 |
| $P_\text{tie}$ | Probability that a who-shoots draw is a tie | 4.4 |
| $q$ | Probability that the home team takes a shot | 4.4 |
| $b$ | Big-chance margin | 4.4 |
| $\beta_H$, $\beta_A$ | Probability that a shot is a home or an away big chance | 4.4 |
| $S$ | Home share of shots, $N_H / N$ | 4.4 |
| $K_a$, $k_a$ | Balls drawn by the attacking team, and red balls among them | 4.5 |
| $K_d$, $k_d$ | Balls drawn by the defending team, and red balls among them | 4.5 |
| $c$ | Red balls cancelled, $\min(k_a, k_d)$ | 4.5 |
| $X_o$, $x_o$ | x-marked balls and red x-marked balls for an ordinary chance | 4.5 |
| $X_b$, $x_b$ | x-marked balls and red x-marked balls for a big chance | 4.5 |
| $X$, $x$ | Whichever x-marked set the shot uses | 4.5 |
| $g(k_a, k_d)$ | xG of a shot given the attack and defence draws | 4.5 |
| $P(i, j)$ | Probability of the attack and defence draws $k_a = i$, $k_d = j$ | 4.5 |
| $\mu$, $\sigma^2$ | Mean and variance of the xG of one kind of shot | 4.5 |
| $G_H$, $G_A$ | Goals of the home and the away team | 4.6 |
| $z$ | Variable of the generating function of the goals | 4.6 |

## Inference (chapter 5)

| Symbol | Meaning | Defined in |
| --- | --- | --- |
| $D$ | The observed match, its list of shots | 5.1 |
| $t_i$, $v_i$ | Team and xG of shot $i$ | 5.1 |
| $j$, $k$ | Red balls in the home and the away team's match urn | 5.2 |
| $P_H^o$, $P_H^b$, $P_A^o$, $P_A^b$ | Probability of an xG value for a home or away ordinary or big chance, given the match urns | 5.2 |
| $\ell_H(v \mid j, k)$, $\ell_A(v \mid j, k)$ | Probability that a shot is taken by the home or the away team and has xG $v$ | 5.2 |
| $L(D \mid j, k)$ | Likelihood of the match given the match urns | 5.3 |
| $L(D \mid m_{s,H}, m_{s,A})$ | Likelihood of the match given the skill pools | 5.4 |
| $u_1, \dots, u_V$ | The sorted list of xG values the urns can produce | 5.5 |
| $w$ | Weight of the lower neighbour when an observed xG is split | 5.5 |
| $\pi_H$, $\pi_A$ | Home and away team's skill distribution before the match | 5.6 |
| $\pi_H'$, $\pi_A'$ | The same after the match | 5.6 |
| $s$, $s_H$, $s_A$ | Red balls in a skill pool, as a value of the distribution | 5.6 |
| $T$ | Number of teams in a league | 5.6 |
| $G(s \mid s')$ | Drift: probability of moving from $s'$ to $s$ red balls between matches | 5.7 |
| $\sigma$ | Drift spread, as a share of the skill pool | 5.7 |

## Prediction (chapter 6)

| Symbol | Meaning | Defined in |
| --- | --- | --- |
| $\omega_H(j)$, $\omega_A(k)$ | Probability of a match urn before the match | 6.1 |
| $\omega(j, k)$ | Probability of a pair of match urns, with the all-red pair left out | 6.1 |
| $P_H(v)$, $P_A(v)$ | Predicted xG distribution of one home or away shot | 6.3 |
| $\gamma_H$, $\gamma_A$ | Probability of a home or an away goal in one round, given the match urns | 6.4 |
| $g$, $h$ | Goals of the home and the away team, as values | 6.4 |

## Fitting method (chapter 7)

| Symbol | Meaning | Defined in |
| --- | --- | --- |
| $B$ | Number of bins | 7.4 |
| $P_b$, $F_b$ | Predicted probability of bin $b$, and of bin $b$ or lower | 7.4 |
| $O_b$ | 1 if the observation is in bin $b$ or lower, else 0 | 7.4 |
| $o$ | Bin of the observation | 7.4 |
| $\mathrm{RPS}$ | Ranked probability score | 7.4 |
| $E_\text{match}$ | Error of one match | 7.5 |
| $\lambda$ | Weight of the xG scores against the shot-count scores; a hyperparameter | 7.5 |
| $\mu$ | Mean shot count, $n p_t$ | 7.7 |

## Computation (appendix A)

| Symbol | Meaning | Defined in |
| --- | --- | --- |
| $W$ | Hypergeometric probabilities, $W_{sj} = P(m_u = j \mid m_s = s)$ | A.1 |
| $\Lambda$ | Likelihood of the match for every pair of match urns, $\Lambda_{jk} = L(D \mid j, k)$ | A.2 |
| $L$ | Likelihood of the match for every pair of skill pools | A.2 |
| $Q$ | One number per pair of match urns, for a prediction | A.3 |
| $I'$ | Matrix of ones, zero in the all-red cell | A.3 |
