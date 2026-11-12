# 4. Model mechanics

This chapter sets out the urn chain exactly: every container, every draw and what each draw decides. The rules
are the ones in the [README](../../README.md#how-to-play) and in [design.md](../design.md); where this chapter and
those two differ, they are right and this chapter is wrong. The chapter follows one match from start to finish, then
shows why the whole match can be computed rather than simulated, and closes with the tension between the resolution
and the variance of the draws.

## 4.1 Containers and symbols

The model uses four kinds of urn and two kinds of marked ball, and every ball is red or white. The skill pool is the
team's skill, the match urn is its form on the day, the tempo urn decides whether a round has a shot, and the shot
urn holds one chance. Marked balls are extra balls added for a purpose and taken out again afterwards: h-marked balls
give the home team its advantage, and x-marked balls set the base level of a chance. A marked red ball counts as red.

| Container | Balls | Red balls | What it stands for |
| --- | --- | --- | --- |
| Skill pool, one per team | $M_s$ | $m_s$ | Underlying skill |
| Match urn, one per team per match | $M_u$ (home: $M_u + m_h$) | drawn from the skill pool (home: $+\,m_h$ h-marked) | Match-day form |
| Tempo urn, shared | $M_t$ | $m_t$ | Whether a round has a shot |
| Shot urn, one per shot | the shooter's surviving chance balls plus $M_x$ x-marked | the shooter's surviving red plus $m_x$ x-marked red | The quality of one chance (its xG) |

The draw sizes and the big-chance margin are the rest of the notation. Each team grabs $k_w$ balls to decide who
shoots; the shooting team draws $k_c$ chance balls and the defending team $k_d$ balls; a match has $n$ rounds. The
big-chance margin $b$ is the number of red balls by which the shooter must win the grab for the shot to be a big
chance. The x-marked balls come in two sets: $M_{xo}$ balls, $m_{xo}$ of them red, for an ordinary chance, and
$M_{xb}$ balls, $m_{xb}$ of them red, for a big chance. Where it does not matter which, $M_x$ and $m_x$ stand for the
set in use.

The parameter values used as examples in this chapter are starting values, not fitted ones. They are taken from
`model_settings()` in `src/football_urn_model/simulate.py`: $M_s = 100$, $M_u = 20$, $m_h = 1$, $n = 100$,
$M_t = 4$, $m_t = 1$, $k_w = 3$, $k_c = 5$, $k_d = 1$, $b = 2$, $M_{xo} = 21$ with $m_{xo} = 1$, and $M_{xb} = 20$
with $m_{xb} = 8$.

The chain maps onto the three layers of randomness from chapter 2. Skill change between matches acts on the skill
pool. Match-day form is the draw from the skill pool into the match urn. Chance within the game is everything that
happens in the rounds: the tempo urn sets how often there is a shot, the match urns decide who creates it, the
attack-versus-defence draw sets how good it is, and the shot urn decides whether it goes in.

## 4.2 Before the match: skill pool and match urn

Skill change is the first step of a match, and it is not random. Whoever runs the model may change the number of red
balls in each team's skill pool between matches. In simulation this is an input; in inference it is what the model
estimates (chapter 6).

The match urn is filled by drawing $M_u$ balls from the skill pool without replacement. This draw is match-day form:
a team with $m_s$ red balls in its pool may get more or fewer than its average share on the day. The number of red
balls $j$ in the match urn is hypergeometric:

$$
P(m_u = j) = \frac{\binom{m_s}{j}\binom{M_s - m_s}{M_u - j}}{\binom{M_s}{M_u}}
$$

with mean $M_u m_s / M_s$. Writing $p_s = m_s / M_s$, the red share of the match urn has variance

$$
\operatorname{Var}\!\left(\frac{m_u}{M_u}\right) = \frac{p_s(1 - p_s)}{M_u} \cdot \frac{M_s - M_u}{M_s - 1}.
$$

The second factor is what $M_s$ controls. When $M_s$ equals $M_u$ the whole pool goes into the urn and there is no
form at all; as $M_s$ grows, the draw approaches drawing with replacement and form is as large as $M_u$ allows.

Home advantage is $m_h$ extra red h-marked balls in the home team's match urn. The home match urn then holds
$M_u + m_h$ balls, of which $m_u + m_h$ are red. During the match an h-marked ball is an ordinary red ball: it can
win the grab, become a chance ball and score.

The h-marks exist so that the match can be undone cleanly. After the match the h-marked balls are removed and every
other ball goes back into the skill pool, which is then exactly as it was before the match: $M_s$ balls, $m_s$ red.
Without the marks, the home team's pool would gain red balls with every home match.

The match urns do not change during the match. Every ball drawn from a match urn in a round goes back before the
next round. Form is therefore set once, at kick-off, and every round of the match is played against the same two
match urns.

## 4.3 Each round: shot or not

Each of the $n$ rounds starts with one draw from the tempo urn, and red means a shot. White ends the round with
nothing happening. The tempo urn is shared by the two teams and does not depend on their skill; this is the
"neutral urn" of the design discussion.

The tempo urn is independent of skill because the data showed no dependence. Total shots per match were the one
observable whose mean did not move with the skill proxy (chapter 5). The model reproduces that by letting tempo be
set by neither team.

The total number of shots in a match is binomial. With $p = m_t / M_t$, the mean is $\mu = np$ and the variance is
$np(1 - p) = \mu - \mu^2/n$. With the starting values, $\mu = 100 \cdot 1/4 = 25$ shots and the standard deviation
is $\sqrt{18.75} \approx 4.33$. The variance is always below the mean, which is a limit that section 4.8 returns to.

## 4.4 Who shoots

When there is a shot, each team grabs $k_w$ balls from its match urn, and the team with more red balls shoots. The
grab is without replacement, so each team's count of red balls is hypergeometric in its own match urn. A larger
$k_w$ gives the better team a bigger share of the shots, and more so when $M_u$ is small, since a grab of $k_w$ then
reveals more of the urn. Design.md has a table of shot shares for a range of $k_w$.

A tie is broken one ball at a time. Each team draws one more ball from the balls left after its grab, and this
repeats until one team draws red and the other white; that team shoots. If a team's urn runs empty, all balls go
back and the tie-break continues from full urns. If both urns hold only one colour, a tie can never be broken; the
simulator then settles it with a fair draw, which is an open question rather than a rule.

The margin of the grab decides whether the shot is a big chance. If the shooting team had at least $b$ more red
balls in its grab, the shot is a big chance; otherwise it is ordinary. A team that wins in the tie-break never has a
big chance. All balls from the grab and the tie-break go back into the match urns.

This step is the "who creates" part of the game. It is the only place where the two teams' skills meet to decide
volume. Given the two match urns, every shot in the match goes to the home team with the same probability $q$, and
the type of chance is decided by how clearly the shooting team wins.

## 4.5 Chance quality: the shot urn

The shot urn is built from an attack-versus-defence draw. The shooting team draws $k_c$ chance balls from its match
urn and gets $R_1$ red balls; the defending team draws $k_d$ balls from its own match urn and gets $R_2$ red balls.
Both draws are without replacement within the urn, and the defender puts its balls back straight away.

The defender's red balls cancel the shooter's red balls. The shooter removes $c = \min(R_1, R_2)$ red balls, so a
good defence can take away part or all of a good attack, but never more than the attacker drew. The remaining
$k_c - c$ balls, of which $R_1 - c$ are red, go into the shot urn.

The x-marked balls set the base level of the chance. The set for the kind of shot decided in section 4.4 is added to
the shot urn: $M_{xo}$ and $m_{xo}$ for an ordinary chance, $M_{xb}$ and $m_{xb}$ for a big chance. The shot's xG
is the red share of the shot urn:

$$
\text{xG} = \frac{m_x + R_1 - c}{M_x + k_c - c}.
$$

The starting values show how the two kinds of chance differ. With $k_c = 5$ and $k_d = 1$, an ordinary shot
($M_{xo} = 21$, $m_{xo} = 1$) can take 11 values, from $1/26 \approx 0.04$ to $6/26 \approx 0.23$. A big chance
($M_{xb} = 20$, $m_{xb} = 8$) can also take 11 values, from $8/25 = 0.32$ to $13/25 = 0.52$. The x-marked balls
place the two ranges far apart; the chance balls and the defender spread each kind of shot within its range.

This step is the "how good is the chance" part of the game. The attacker's match urn raises the xG of its shots,
the defender's match urn lowers it, and both act through the same red share that decided who shoots.

## 4.6 The goal

One ball is drawn from the shot urn, and red, marked or not, is a goal. The probability of a goal is therefore the
red share of the shot urn, so a shot's xG in the model is exactly the probability that it goes in. Finishing is
pure chance given the xG; no team converts better than its xG says.

The round ends by clearing the shot urn. The x-marked balls are taken out, and the chance balls go back to the match
urn they came from, so the next round starts from the same match urns as this one.

What the model records for each shot is the round, the shooting team, its xG and whether it was a goal. These are
the quantities that real data also provides, which is what lets the model be compared with real seasons and used
for inference.

## 4.7 A match as independent rounds

Every round of a match is identical and independent, given the two match urns. The match urns are fixed for the
whole match, every drawn ball goes back, and no rule depends on the score or on earlier rounds. Teams in this model
do not play differently when they are ahead or behind.

One round therefore has a small, exact set of outcomes. Given the two match urns, the round produces nothing with
probability $1 - p$, a home shot with probability $pq$ and an away shot with probability $p(1 - q)$, where $q$ is
the probability that the home team wins the grab and tie-break. For each shot, the probability of each possible xG
value follows from enumerating the finite paths of section 4.5: every combination of $R_1$ and $R_2$ has a known
hypergeometric probability and ends in one shot urn with one red share.

A whole match then follows without simulation. The number of shots is binomial in $n$, each shot falls to the home
team with probability $q$, and each shot's xG is an independent draw from that team's xG distribution. The
match-urn draw is one more layer on top: compute the round for every possible pair of match urns and weight each
pair by the two hypergeometric probabilities of section 4.2.

This exactness is what the inference in chapter 6 relies on. For any pair of skill-pool counts, the probability of
an observed match can be calculated, not estimated from simulated matches. That calculation is the only thing the
inference ever runs.

## 4.8 Resolution against variance

Every draw in the chain has two properties that matter for fitting: its resolution and its variance. Resolution is
the set of values a draw can produce, such as the 11 possible xG values of an ordinary shot. Variance is how widely
those values spread from match to match or shot to shot. The data constrains the variance; the inference needs
resolution, because each observed xG is matched to the nearest value the urns can produce.

The two are set by different things. The number of balls in a container sets which ratios are possible. The number
of balls drawn sets how close the draw comes to the container's ratio: one ball is a coin flip with the largest
possible variance, and many balls drawn give a proportion that converges on the ratio. More balls drawn means less
variance.

The match urn shows the coupling and how $M_s$ loosens it. $M_u$ sets the resolution of form, since a match urn can
hold 0 to $M_u$ red balls. By the variance formula in section 4.2, a larger $M_u$ also reduces form, and a larger
$M_s$ then adds some back. $M_s$ can only raise form to the limit of drawing with replacement, $p_s(1 - p_s)/M_u$,
so finer form comes at the cost of a lower ceiling on how much form there can be.

The shot urn has the same tension between chance balls and x-marked balls. More chance balls $k_c$ and more x-marked
balls give a finer grid of xG values. But the red share of $k_c$ balls drawn varies less as $k_c$ grows, and its
weight in the shot urn shrinks as x-marked balls are added. Raising all of them by the same factor makes the grid
finer and also narrows the spread of xG within each kind of shot. Keeping the spread while raising the resolution
therefore means moving $k_c$, $k_d$ and the x-marked balls by different amounts; the concrete sizes are not yet
chosen.

Some variances have a ceiling that no choice of ball counts can exceed. The total number of shots is binomial, so its
variance is always below its mean. The goal is a single-ball draw, as noisy as a draw can be given its xG. Form is
bounded by the with-replacement limit above. Where real football is noisier than a ceiling, the urns as they stand
cannot follow it, and a further mechanism is needed, for example making the ratio of a container itself random.

Total shots per match already break their ceiling. Over the Premier League seasons 2023/24 to 2025/26, real total
shots have a mean of 26.1 and a standard deviation of 6.0, so their variance (about 36) is above their mean. No
binomial can do that, and the simulated standard deviation is 4.3, as the equation says. The excess is there within
each single season too, so it is not caused by pooling seasons. The tempo urn alone cannot match it; the comparison
is in the Shot chapter of [design.md](../design.md).

The home share of shots errs the other way. With the starting values, the model's home share varies more from match
to match than the real one: a standard deviation of 0.23 against 0.17. The limited number of shots accounts for the
same part of the spread in both, so the excess is in how much $q$ varies between matches. That spread comes from
form and from the gap in red balls between the teams, both set by parameters already in the model ($k_w$, $M_u$,
$M_s$ and the red balls), and these are starting values, not fitted ones. The two findings together show that variance has to be checked observable by
observable, since the model can be too quiet in one place and too noisy in another.

Resolution also has a computational cost. More balls mean more paths through each draw, and every path must be
enumerated for each cell of the inference table in chapter 6. The table is computed once, so the cost is paid once,
but it grows with every ball added.

This tension matters because the variance decides how confident the inference is. If the model's variance is lower
than real football's, the inference reads too much into each match and is overconfident; if it is higher, the
inference learns too slowly. Resolution and variance must therefore be tuned separately, with the variance matched
to the data first.
