# Appendix A. Computation

This appendix shows how the likelihood of chapter 5 is computed. It adds nothing to the maths: every quantity here
is defined in chapters 4 and 5, and the appendix only says how to compute them exactly and cheaply.

## A.1 The lookup table

Everything the inference needs from chapter 4 fits in one table, computed once per set of parameters. The table has
one cell for each pair of match urns $j$ and $k$, from 0 to $M_u$ red balls each, so $(M_u + 1)^2$ cells. Each cell
holds $\ell_H(u \mid j, k)$ and $\ell_A(u \mid j, k)$ of section 5.2 for every value $u$ in the list of section 5.5.
With $K_d = 1$, each kind of shot gives at most $2K_a + 1$ values, so the list has at most $2(2K_a + 1)$ entries.

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

## A.3 Cost

The size of the skill pool costs little. The table is indexed by the match urns, so a larger skill pool only adds
rows to $W$, and the update of section 5.6 works on $(M_s + 1)^2$ pairs of skill pools. A larger match urn costs
more, since the number of cells grows with the square of $M_u + 1$. A larger list of xG values, for a finer xG, adds
entries to every cell. All of it is computed once per set of parameters.
