# Appendix A. Computation

This appendix shows how the likelihood of chapter 5 and the predictions of chapter 6 are computed. It adds nothing to
the maths: every quantity here is defined in chapters 4 to 6, and the appendix only shows how they are computed
exactly and cheaply.

## A.1 The lookup table

Everything the inference needs from chapter 4 fits in one table, computed once per set of parameters. The table has
one cell for each pair of match urns $j$ and $k$, from 0 to $M_u$ red balls each, so $(M_u + 1)^2$ cells. Each cell
holds $\ell_H(u \mid j, k)$ and $\ell_A(u \mid j, k)$ of section 5.2 for every value $u$ in the list of section 5.5.
Each kind of shot gives at most one value for each pair of the attacker's red balls $k_a$ and the cancelled balls
$c \le \min(k_a, K_d)$, so the list is short whatever the parameters.

The cell where both match urns hold only red balls, $j = k = M_u$, is given a likelihood of zero (section 5.4).

A second table holds the hypergeometric probabilities of section 4.2, $W_{s j} = P(m_u = j \mid m_s = s)$, with one
row for each possible skill pool and one column for each possible match urn.

The tables depend on the parameters and not on the teams. They are recomputed whenever the parameters change, as
they do during the fit of chapters 6 and 7.

## A.2 One match

A match is computed by lookups, products and two matrix products. For each shot, its two neighbours in the list and
their weights (section 5.5) are found once, and the same weights are used in every cell. For each cell, the shots'
factors are multiplied, which gives the matrix $\Lambda$ with $\Lambda_{j k} = L(D \mid j, k)$. The double sum of
section 5.4 is then, for every pair of skill pools at once,

$$
L = W\, \Lambda\, W^\mathsf{T}, \qquad L_{s_H s_A} = L(D \mid m_{s,H} = s_H,\, m_{s,A} = s_A)
$$

The products of many small factors are taken as sums of logarithms. Before the matrix product, $\Lambda$ is scaled
so that its largest entry is one; the scale cancels when the distribution after the match is normalised (section
5.6).

## A.3 The predictions

The predictions of chapter 6 use the same tables. The weights of section 6.1 are the vectors
$\omega_H = \pi_H^\mathsf{T} W$ and $\omega_A = \pi_A^\mathsf{T} W$, and every prediction has the form

$$
\frac{\omega_H\, Q\, \omega_A^\mathsf{T}}{\omega_H\, I'\, \omega_A^\mathsf{T}}
$$

where $Q$ holds one number for each pair of match urns and $I'$ is a matrix of ones. Both are zero in the all-red
cell. The denominator is then the total weight of the pairs that count, so the quotient is the mixture over the scaled
weights $\omega(j, k)$ of section 6.1. For a shot count, $Q$ holds the binomial
probabilities of section 6.2; for the xG of a shot, $\ell_H(v \mid j, k)$ in the numerator and $q(j, k)$ in the
denominator in place of $I'$ (section 6.3); for a result, its probability given the match urns (section 6.4). These
entries depend only on the parameters, so they are tabulated with the lookup table and reused for every match.
