# 4. Model mechanics

This chapter sets out the urn chain exactly: every container, every draw and what each draw decides. The rules
are the ones in the [README](../../README.md) ("How to play") and in [design.md](../design.md); where this chapter and those two
differ, they are right and this chapter is wrong. The chapter follows one match from start to finish, then shows
why the whole match can be computed rather than simulated, and closes with the tension between the resolution and
the variance of the draws.

## 4.1 Containers and symbols

The model uses five kinds of container, and each holds only red and white balls. The skill pool is the team's
skill, the match urn is its form on the day, the tempo urn decides whether a round has a shot, and the shot urn
holds one chance. Marked balls are a fixed supply added to the shot urn; a marked red ball counts as red.

| Container | Balls | Red balls | What it stands for |
| --- | --- | --- | --- |
| Skill pool, one per team | M\_s | m\_s | Underlying skill |
| Match urn, one per team per match | M\_u (home: M\_u + m\_h) | drawn from the skill pool (home: + m\_h) | Match-day form |
| Tempo urn, shared | M\_t | m\_t | Whether a round has a shot |
| Shot urn, one per shot | what the shooter keeps plus the marked balls | the shooter's surviving red plus marked red | The quality of one chance (its xG) |

The draw sizes are the rest of the notation. Each team grabs k\_w balls to decide who shoots; the shooting team
draws k\_c chance balls and the defending team k\_d balls; a match has n rounds. The big-chance margin is the
number of red balls by which the shooter must win the grab for the shot to be a big chance.

The parameter values used as examples in this chapter are starting values, not decided ones. They are taken from
`model_settings()` in `src/football_urn_model/simulate.py`: M\_s = 100, M\_u = 20, m\_h = 1, n = 100, M\_t = 4,
m\_t = 1, k\_w = 3, k\_c = 5, k\_d = 1, a big-chance margin of 2, ordinary marked balls 1 red and 20 white, and
big-chance marked balls 8 red and 12 white.

The chain maps onto the three layers of randomness from chapter 2. Skill change between matches acts on the skill
pool. Match-day form is the draw from the skill pool into the match urn. Chance within the game is everything that
happens in the rounds: the tempo urn sets how often there is a shot, the match urns decide who creates it, the
attack-versus-defence draw sets how good it is, and the shot urn decides whether it goes in.

## 4.2 Before the match: skill pool and match urn

Skill change is the first step of a match, and it is not random. Whoever runs the model may change the number of red
balls in each team's skill pool between matches. In simulation this is an input; in inference it is what the model
estimates (chapter 6).

The match urn is filled by drawing M\_u balls from the skill pool without replacement. This draw is match-day form:
a team with m\_s red balls in its pool may get more or fewer than its average share on the day. The number of red
balls j in the match urn is hypergeometric:

$$
P(m_u = j) = \frac{\binom{m_s}{j}\binom{M_s - m_s}{M_u - j}}{\binom{M_s}{M_u}}
$$

with mean M\_u · m\_s / M\_s. Writing p\_s = m\_s / M\_s, the red share of the match urn has variance

$$
\operatorname{Var}\!\left(\frac{m_u}{M_u}\right) = \frac{p_s(1 - p_s)}{M_u} \cdot \frac{M_s - M_u}{M_s - 1}.
$$

The second factor is what M\_s controls. When M\_s equals M\_u the whole pool goes into the urn and there is no form
at all; as M\_s grows, the draw approaches drawing with replacement and form is as large as M\_u allows.

Home advantage is m\_h extra red balls in the home team's match urn. The home match urn then holds M\_u + m\_h
balls, of which m\_u + m\_h are red. The extra balls are ordinary red balls once in the urn; they do not need marking,
because the match urns are emptied and refilled for every match.

The match urns do not change during the match. Every ball drawn from a match urn in a round goes back before the
next round. Form is therefore set once, at kick-off, and every round of the match is played against the same two
match urns.

## 4.3 Each round: shot or not

Each of the n rounds starts with one draw from the tempo urn, and red means a shot. White ends the round with
nothing happening. The tempo urn is shared by the two teams and does not depend on their skill; this is the
"neutral urn" of the design discussion.

The tempo urn is independent of skill because the data showed no dependence. Total shots per match were the one
observable whose mean did not move with the skill proxy (chapter 5). The model reproduces that by letting tempo be
set by neither team.

The total number of shots in a match is binomial. With p = m\_t / M\_t, the mean is μ = n · p and the variance is
n · p · (1 − p) = μ − μ²/n. With the starting values, μ = 100 · 1/4 = 25 shots and the variance is 18.75. The
variance is always below the mean, which is a limit that section 4.8 returns to.

## 4.4 Who shoots

When there is a shot, each team grabs k\_w balls from its match urn, and the team with more red balls shoots. The
grab is without replacement, so each team's count of red balls is hypergeometric in its own match urn. A larger
k\_w gives the better team a bigger share of the shots, and more so when M\_u is small, since a grab of k\_w then
reveals more of the urn. Design.md has a table of shot shares for a range of k\_w.

A tie is broken one ball at a time. Each team draws one more ball from the balls left after its grab, and this
repeats until one team draws red and the other white; that team shoots. If a team's urn runs empty, all balls go
back and the tie-break continues from full urns. If both urns hold only one colour, a tie can never be broken; the
simulator then settles it with a fair draw, which is an open question rather than a rule.

The margin of the grab decides whether the shot is a big chance. If the shooting team won the grab by at least the
big-chance margin, the shot is a big chance; otherwise it is ordinary. A win in the tie-break has margin zero and is
never a big chance. All balls from the grab and the tie-break go back into the match urns.

This step is the "who creates" part of the game. It is the only place where the two teams' skills meet to decide
volume: the share of shots a team gets in a match is the probability that it wins this contest, and the type of
chance is decided by how clearly it wins.

## 4.5 Chance quality: the shot urn

The shot urn is built from an attack-versus-defence draw. The shooting team draws k\_c chance balls from its match
urn and gets R1 red balls; the defending team draws k\_d balls from its own match urn and gets R2 red balls. Both
draws are without replacement within the urn.

The defender's red balls cancel the shooter's red balls. The shooter removes c = min(R1, R2) red balls, so a good
defence can take away part or all of a good attack, but never more than the attacker drew. The remaining k\_c − c
balls, of which R1 − c are red, go into the shot urn.

The marked balls set the base level of the chance. Ordinary shots and big chances have their own numbers of marked
red and marked white balls, and the set for the kind of shot decided in section 4.4 is added to the shot urn. With
r\_x and w\_x the marked red and white balls for that kind of shot, the shot's xG is the red share of the shot urn:

$$
\text{xG} = \frac{r_x + R_1 - c}{r_x + w_x + k_c - c}.
$$

The starting values show how the two kinds of chance differ. With k\_c = 5 and k\_d = 1, an ordinary shot
(1 marked red, 20 marked white) can take 11 values, from 1/26 ≈ 0.04 to 6/26 ≈ 0.23. A big chance (8 marked red,
12 marked white) can also take 11 values, from 0.32 to 13/25 = 0.52. The marked balls place the two ranges far
apart; the chance balls and the defender spread each kind of shot within its range.

This step is the "how good is the chance" part of the game. The attacker's match urn raises the xG of its shots,
the defender's match urn lowers it, and both act through the same red share that decided who shoots.

## 4.6 The goal

One ball is drawn from the shot urn, and red, marked or not, is a goal. The probability of a goal is therefore the
red share of the shot urn, so a shot's xG in the model is exactly the probability that it goes in. Finishing is
pure chance given the xG; no team converts better than its xG says.

The round ends by clearing the shot urn. The marked balls go back to their supply, and the chance balls go back to
the match urns they came from, so the next round starts from the same match urns as this one.

What the model records for each shot is the round, the shooting team, its xG and whether it was a goal. These are
the quantities that real data also provides, which is what lets the model be compared with real seasons and used
for inference.

## 4.7 A match as independent rounds

Every round of a match is identical and independent, given the two match urns. The match urns are fixed for the
whole match, every drawn ball goes back, and no rule depends on the score or on earlier rounds. Teams in this model
do not play differently when they are ahead or behind.

One round therefore has a small, exact set of outcomes. Given the two match urns, the round produces nothing with
probability 1 − p, a home shot with probability p · w and an away shot with probability p · (1 − w), where w is the
probability that the home team wins the grab and tie-break. For each shot, the probability of each possible xG
value follows from enumerating the finite paths of section 4.5: every combination of R1 and R2 has a known
hypergeometric probability and ends in one shot urn with one red share.

A whole match then follows without simulation. The number of shots is binomial in n, each shot falls to the home
team with probability w, and each shot's xG is an independent draw from that team's xG distribution. The match-urn
draw is one more layer on top: compute the round for every possible pair of match urns and weight each pair by the
two hypergeometric probabilities of section 4.2.

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

The match urn shows the coupling and how M\_s loosens it. M\_u sets the resolution of form, since a match urn can
hold 0 to M\_u red balls. By the variance formula in section 4.2, a larger M\_u also reduces form, and a larger M\_s
then adds some back. M\_s can only raise form to the limit of drawing with replacement, p\_s(1 − p\_s)/M\_u, so finer
form comes at the cost of a lower ceiling on how much form there can be.

The shot urn has the same tension between chance balls and marked balls. More chance balls k\_c and more marked
balls give a finer grid of xG values. But the red share of k\_c balls drawn varies less as k\_c grows, and its weight
in the shot urn shrinks as marked balls are added. Raising all of them by the same factor makes the grid finer and
also narrows the spread of xG within each kind of shot. Keeping the spread while raising the resolution therefore
means moving k\_c, k\_d and the marked balls by different amounts; the concrete sizes are not yet chosen.

Some variances have a ceiling that no choice of ball counts can exceed. The total number of shots is binomial, so its
variance is always below its mean. The goal is a single-ball draw, as noisy as a draw can be given its xG. Form is
bounded by the with-replacement limit above. If real football turns out noisier than any of these, a further
mechanism is needed, for example making the ratio of a container itself random.

Resolution also has a computational cost. More balls mean more paths through each draw, and every path must be
enumerated for each cell of the inference table in chapter 6. The table is computed once, so the cost is paid once,
but it grows with every ball added.

This tension matters because the variance decides how confident the inference is. If the model's variance is lower
than real football's, the inference reads too much into each match and is overconfident; if it is higher, the
inference learns too slowly. Resolution and variance must therefore be tuned separately, with the variance matched
to the data first.
