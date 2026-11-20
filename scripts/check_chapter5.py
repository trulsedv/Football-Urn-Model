"""Check chapter 5's per-shot probabilities against the simulator, with the parameters in model_settings().

Section 5.2 gives, for match urns with j and k red balls, the probability that a shot is taken by each team and has
each xG value. This script computes those probabilities from the book's equations and compares them with shots
played by the simulator's own who_shoots and build_shot_urn. It also checks that the matrix form of appendix A equals
the double sum of section 5.4. Rerun it whenever the parameters change:

    uv run python scripts/check_chapter5.py
"""

from collections import Counter
from collections.abc import Generator
from fractions import Fraction
from math import comb

import numpy as np

from football_urn_model.simulate import build_shot_urn, model_settings, who_shoots

SHOTS_PER_CELL = 200_000
CELLS = [(4, 2), (1, 6)]  # match urns (j, k) to compare against the simulator
LIMIT = 4.0  # largest deviation, in standard errors, accepted for any outcome
TOLERANCE = 1e-12


def hypergeometric(red: int, total: int, draws: int) -> list[float]:
    """Return the probability of drawing 0 to `draws` red balls, without replacement.

    Returns:
        One probability for each number of red balls drawn.

    """
    return [comb(red, i) * comb(total - red, draws - i) / comb(total, draws) for i in range(draws + 1)]


def xg_distribution(attack: tuple[int, int], defence: tuple[int, int], marked: tuple[int, int], s: dict) -> Counter:
    """Return the xG distribution of one kind of shot (section 4.5), for urns given as (red, size).

    Returns:
        xG value to probability.

    """
    marked_red, marked_size = marked
    out: Counter = Counter()
    for k_a, p_a in enumerate(hypergeometric(*attack, s["chance_draws"])):
        for k_d, p_d in enumerate(hypergeometric(*defence, s["defender_draws"])):
            c = min(k_a, k_d)
            out[Fraction(marked_red + k_a - c, marked_size + s["chance_draws"] - c)] += p_a * p_d
    return out


def per_shot(j: int, k: int, s: dict) -> Counter:
    """Return the probability of each team and xG for one shot given the match urns: l_H and l_A of section 5.2.

    Returns:
        (team, xG value) to probability; empty when who shoots can never be decided.

    """
    home, away = (j + s["home_extra_red"], s["match_urn_size"] + s["home_extra_red"]), (k, s["match_urn_size"])
    draws, margin = s["who_shoots_draws"], s["big_chance_margin"]
    p_home, p_away = hypergeometric(*home, draws), hypergeometric(*away, draws)
    pairs = [(a, b, p_home[a] * p_away[b]) for a in range(draws + 1) for b in range(draws + 1)]
    tie = sum(p for a, b, p in pairs if a == b)
    if tie > 1 - TOLERANCE:
        return Counter()  # both match urns all red: the redraw never ends, likelihood zero (section 5.4)
    q = sum(p for a, b, p in pairs if a > b) / (1 - tie)
    beta_h = sum(p for a, b, p in pairs if a - b >= margin) / (1 - tie)
    beta_a = sum(p for a, b, p in pairs if b - a >= margin) / (1 - tie)
    ordinary = (s["marked_red"], s["marked_red"] + s["marked_white"])
    big = (s["big_chance_marked_red"], s["big_chance_marked_red"] + s["big_chance_marked_white"])
    out: Counter = Counter()
    for team, att, dfn, total, share in (("H", home, away, q, beta_h), ("A", away, home, 1 - q, beta_a)):
        for v, p in xg_distribution(att, dfn, ordinary, s).items():
            out[team, v] += (total - share) * p
        for v, p in xg_distribution(att, dfn, big, s).items():
            out[team, v] += share * p
    return out


def finish(steps: Generator) -> object:
    """Run one of the simulator's step generators to its end.

    Returns:
        The generator's return value.

    """
    try:
        while True:
            next(steps)
    except StopIteration as stop:
        return stop.value


def simulated_shot(j: int, k: int, s: dict, rng: np.random.Generator) -> tuple[str, Fraction]:
    """Play one shot with the simulator's own functions.

    Returns:
        The team that shot, "H" or "A", and the shot's xG.

    """
    urns = {True: (j + s["home_extra_red"], s["match_urn_size"] + s["home_extra_red"]), False: (k, s["match_urn_size"])}
    is_home, margin = finish(who_shoots(urns[True], urns[False], s["who_shoots_draws"], rng))
    is_big = margin >= s["big_chance_margin"]
    red, size = finish(build_shot_urn(urns, s, rng, is_home=is_home, is_big_chance=is_big))
    return ("H" if is_home else "A"), Fraction(red, size)


def require(message: str, *, ok: bool) -> None:
    """Stop the check when a condition fails.

    Raises:
        RuntimeError: If `ok` is false.

    """
    if not ok:
        raise RuntimeError(message)


def compare_with_simulator(s: dict) -> None:
    """Compare l_H and l_A of section 5.2 with shots played by the simulator, for each pair of match urns in CELLS."""
    rng = np.random.default_rng(11)
    for j, k in CELLS:
        exact = per_shot(j, k, s)
        require("l_H and l_A must sum to 1 over all values", ok=abs(sum(exact.values()) - 1) < TOLERANCE)
        sim = Counter(simulated_shot(j, k, s, rng) for _ in range(SHOTS_PER_CELL))
        require("the simulator produced a value the equations do not allow", ok=set(sim) <= set(exact))
        n = SHOTS_PER_CELL
        worst = max(abs(sim[key] / n - p) / np.sqrt(p * (1 - p) / n) for key, p in exact.items() if p > 0)
        print(f"match urns {j}, {k}: {len(exact)} outcomes, worst deviation {worst:.2f} standard errors")
        require("equations and simulator disagree", ok=worst < LIMIT)


def check_matrix_form(s: dict) -> None:
    """Check that W Lambda W^T (appendix A) equals the double sum of section 5.4, for a match of three shots."""
    size = s["match_urn_size"]
    table = {(j, k): per_shot(j, k, s) for j in range(size + 1) for k in range(size + 1)}
    values = sorted({key for cell in table.values() for key in cell})
    shots = [values[0], values[len(values) // 2], values[-1]]
    lam = np.array([[np.prod([table[j, k][x] for x in shots]) for k in range(size + 1)] for j in range(size + 1)])
    w = np.array([hypergeometric(m, s["skill_pool_size"], size) for m in range(s["skill_pool_size"] + 1)])
    matrix = w @ lam @ w.T
    home, away = s["red_max"], s["red_min"]
    double_sum = sum(w[home, j] * w[away, k] * lam[j, k] for j in range(size + 1) for k in range(size + 1))
    require("matrix form and double sum disagree", ok=bool(np.isclose(matrix[home, away], double_sum)))
    print(f"matrix form equals the double sum of section 5.4 ({matrix[home, away]:.6g} for skill pools {home}, {away})")


def main() -> None:
    """Run both checks with the parameters in model_settings()."""
    settings = model_settings()
    compare_with_simulator(settings)
    check_matrix_form(settings)


if __name__ == "__main__":
    main()
