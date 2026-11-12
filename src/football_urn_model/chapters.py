"""The chapters of docs/design.md: real against simulated data per panel of skill proxy sum and difference."""

from collections import Counter
from functools import cache
from math import comb
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from football_urn_model.data import final_points, load_season
from football_urn_model.simulate import model_settings, simulate_season, starting_red_balls


def main() -> None:
    seasons = ["2023", "2024", "2025"]  # Understat season 2023 = 2023/24
    simulated_seasons = 100  # per real season; enough for the simulated statistics to match the theory
    output_dir = Path("output")

    settings = model_settings()
    real, simulated, fixtures = load_and_simulate(seasons, settings, simulated_seasons)
    ranges = add_terciles(real, simulated)
    names = ", ".join(f"{season}/{int(season) + 1 - 2000}" for season in seasons)
    simulation = f"real: {names}; simulated: {simulated_seasons} seasons per real season"

    output_dir.mkdir(exist_ok=True)
    # All match-level chapters share the same matches, so their counts are tabulated once.
    matches = panel_tables(real, simulated, {"observable": "total_shots", "theory": {}}, ranges, {"Matches": "count"})
    print(f"{simulation}\n\n{matches}")
    (output_dir / "matches_tables.md").write_text(matches)
    for chapter in chapter_settings(settings, fixtures):
        parameters = ", ".join(f"{symbol} = {settings[name]}" for symbol, name in chapter["parameters"])
        statistics = {"Mean": "mean", "Standard deviation": "std", "Skewness": "skew"}
        tables = panel_tables(real, simulated, chapter, ranges, statistics)
        print(f"{chapter['title']} ({parameters})\n\n{tables}")
        (output_dir / f"{chapter['name']}_tables.md").write_text(tables)
        figure = plot_grid(real, simulated, chapter, ranges, f"{simulation}, {parameters}")
        figure.write_html(output_dir / f"{chapter['name']}_grid.html")
        print(f"Wrote {output_dir}/{chapter['name']}_tables.md and {output_dir}/{chapter['name']}_grid.html\n")


def load_and_simulate(
    seasons: list[str],
    settings: dict[str, int],
    simulated_seasons: int,
) -> tuple[pd.DataFrame, pd.DataFrame, list[tuple[int, int]]]:
    """Load the real seasons, and simulate each season's fixture list with red balls from its final points.

    Returns:
        One row per real match and one per simulated match, with the final points of their own season as the skill
        proxy, and the red balls (home, away) of every real fixture.

    """
    rng = np.random.default_rng(1)
    real, simulated, fixtures = [], [], []
    for season in seasons:
        schedule, shots = load_season(season)
        shots = shots.merge(schedule[["game_id", "home_team_id"]], on="game_id")
        shots["is_home"] = shots["team_id"] == shots["home_team_id"]
        real.append(per_match(schedule, shots, final_points(schedule)))

        red_balls = starting_red_balls(final_points(schedule), settings)
        teams = schedule[["home_team", "away_team"]].to_numpy()
        fixtures.extend((red_balls[home], red_balls[away]) for home, away in teams)
        for _ in range(simulated_seasons):
            simulated_shots, matches = simulate_season(schedule, red_balls, settings, rng)
            simulated.append(per_match(matches, simulated_shots, final_points(matches)))
    return pd.concat(real, ignore_index=True), pd.concat(simulated, ignore_index=True), fixtures


def chapter_settings(settings: dict[str, int], fixtures: list[tuple[int, int]]) -> list[dict]:
    """Describe each chapter: its observable, how to plot it, the parameters behind it and its theory.

    Returns:
        One dict per chapter.

    """
    # The tempo urn makes the total shots binomial (see the Shot chapter of docs/design.md).
    p, rounds = settings["tempo_urn_red"] / settings["tempo_urn_size"], settings["rounds"]
    sd = np.sqrt(rounds * p * (1 - p))
    return [
        {
            "name": "shot",
            "title": "Total shots per match",
            "observable": "total_shots",
            "bin_width": None,  # discrete: one bar per value
            "decimals": 1,
            "parameters": [("n", "rounds"), ("m_t", "tempo_urn_red"), ("M_t", "tempo_urn_size")],
            "theory": {"Mean": rounds * p, "Standard deviation": sd, "Skewness": (1 - 2 * p) / sd},
        },
        {
            "name": "attack_defend",
            "title": "Home share of shots per match",
            "observable": "home_share",
            "bin_width": 0.1,
            "decimals": 2,
            "parameters": [
                ("k_w", "who_shoots_draws"),
                ("M_u", "match_urn_size"),
                ("m_h", "home_extra_red"),
                ("M_s", "skill_pool_size"),
                ("m_s from", "red_min"),
                ("to", "red_max"),
            ],
            "theory": home_share_theory(fixtures, settings),
        },
    ]


def home_share_theory(fixtures: list[tuple[int, int]], settings: dict[str, int]) -> dict[str, float]:
    """Compute the exact mean, sd and skewness of the home share of shots over the fixtures (Attack/defend chapter).

    Given the match urns, each shot is the home team's with probability q, and the number of shots T comes from the
    tempo urn independently. The share's moments follow from the spread of q over the matches and from E[1/T] and
    E[1/T^2] (matches without shots have no share).

    Returns:
        Mean, standard deviation and skewness.

    """
    rounds, p = settings["rounds"], settings["tempo_urn_red"] / settings["tempo_urn_size"]
    totals = np.arange(1, rounds + 1)
    total_weights = np.array([comb(rounds, t) * p**t * (1 - p) ** (rounds - t) for t in totals])
    total_weights /= total_weights.sum()
    inverse, inverse_squared = (total_weights / totals).sum(), (total_weights / totals**2).sum()

    q, weights = who_shoots_spread(fixtures, settings)
    mean = (weights * q).sum()
    variance_q, third_q = (weights * (q - mean) ** 2).sum(), (weights * (q - mean) ** 3).sum()
    binomial_variance = (weights * q * (1 - q)).sum()
    covariance = (weights * (q - mean) * (q * (1 - q) - binomial_variance)).sum()
    variance = inverse * binomial_variance + variance_q
    third = inverse_squared * (weights * q * (1 - q) * (1 - 2 * q)).sum() + 3 * inverse * covariance + third_q
    return {"Mean": mean, "Standard deviation": np.sqrt(variance), "Skewness": third / variance**1.5}


def who_shoots_spread(fixtures: list[tuple[int, int]], settings: dict[str, int]) -> tuple[np.ndarray, np.ndarray]:
    """Compute q for every pair of match urns, and how likely the fixtures' skill pools give those urns (phase 2).

    Returns:
        q and its weight, both indexed by (red balls drawn into the home urn, red balls in the away urn).

    """
    pool, urn, extra = settings["skill_pool_size"], settings["match_urn_size"], settings["home_extra_red"]
    q = np.array(
        [
            [
                who_shoots_probability((home + extra, urn + extra), (away, urn), settings["who_shoots_draws"])
                for away in range(urn + 1)
            ]
            for home in range(urn + 1)
        ],
    )
    weights = np.zeros_like(q)
    for (home_red_balls, away_red_balls), count in Counter(fixtures).items():
        home_urns, away_urns = hypergeometric(pool, home_red_balls, urn), hypergeometric(pool, away_red_balls, urn)
        weights += count * np.outer(home_urns, away_urns)
    return q, weights / weights.sum()


def who_shoots_probability(home_urn: tuple[int, int], away_urn: tuple[int, int], draws: int) -> float:
    """Compute the exact probability that the home team wins phase 4, for match urns given as (red, size).

    Returns:
        The probability that the home team shoots.

    """
    (home_red, home_size), (away_red, away_size) = home_urn, away_urn
    home_drawn = hypergeometric(home_size, home_red, draws)
    away_drawn = hypergeometric(away_size, away_red, draws)
    win = sum(home_drawn[x] * away_drawn[:x].sum() for x in range(draws + 1))
    if home_red in {0, home_size} and away_red in {0, away_size}:
        return win + 0.5 * (home_drawn * away_drawn).sum()  # a tie that can never be broken: a fair draw

    @cache
    def tie_break(home: tuple[int, int], away: tuple[int, int]) -> tuple[float, float]:
        """Follow the tie-break from these urns until a team wins or an urn runs empty.

        Returns:
            (a, b): the home team wins with probability a + b * (its win probability after all balls go back).

        """
        (red, size), (other_red, other_size) = home, away
        if size == 0 or other_size == 0:  # an urn ran empty, so all balls go back
            return 0.0, 1.0
        home_is_red, away_is_red = red / size, other_red / other_size
        result = np.array([home_is_red * (1 - away_is_red), 0.0])
        if red and other_red:  # both red: draw again
            both_red = tie_break((red - 1, size - 1), (other_red - 1, other_size - 1))
            result += home_is_red * away_is_red * np.array(both_red)
        if size - red and other_size - other_red:  # both white: draw again
            both_white = tie_break((red, size - 1), (other_red, other_size - 1))
            result += (1 - home_is_red) * (1 - away_is_red) * np.array(both_white)
        return float(result[0]), float(result[1])

    full_win, full_restart = tie_break(home_urn, away_urn)
    after_put_back = full_win / (1 - full_restart)
    tie = 0.0
    for x in range(draws + 1):
        start_win, start_restart = tie_break((home_red - x, home_size - draws), (away_red - x, away_size - draws))
        tie += home_drawn[x] * away_drawn[x] * (start_win + start_restart * after_put_back)
    return win + tie


def hypergeometric(size: int, red: int, draws: int) -> np.ndarray:
    """Probability of 0, 1, ..., draws red balls when drawing without replacement from an urn.

    Returns:
        One probability per number of red balls.

    """
    return np.array([comb(red, x) * comb(size - red, draws - x) / comb(size, draws) for x in range(draws + 1)])


def add_terciles(real: pd.DataFrame, simulated: pd.DataFrame) -> dict[tuple[str, str], str]:
    """Bin the matches into terciles of the real skill proxy; the simulated matches use the same edges.

    Returns:
        The range of the skill proxy in each tercile of the real matches, e.g. "[-65 to -8 pts]".

    """
    for proxy in ["difference", "sum"]:
        low, high = real[proxy].quantile([1 / 3, 2 / 3])
        for matches in [real, simulated]:
            matches[f"{proxy}_bin"] = pd.cut(
                matches[proxy],
                [-np.inf, low, high, np.inf],
                labels=["low", "mid", "high"],
            )
    return {
        (proxy, str(tercile)): f"[{values.min():.0f} to {values.max():.0f} pts]"
        for proxy in ["sum", "difference"]
        for tercile, values in real.groupby(f"{proxy}_bin", observed=True)[proxy]
    }


def per_match(matches: pd.DataFrame, shots: pd.DataFrame, points: pd.Series) -> pd.DataFrame:
    """Put the skill proxy and the observables side by side, one row per match.

    Returns:
        Skill proxy difference (home - away final points), skill proxy sum, total shots and the home share of shots.

    """
    home_points = points[matches["home_team"]].to_numpy()
    away_points = points[matches["away_team"]].to_numpy()
    # Matches without a shot have no rows in the shot data, so they get 0.
    counts = pd.crosstab(shots["game_id"], shots["is_home"]).reindex(matches["game_id"], fill_value=0)
    total_shots = counts[True] + counts[False]
    return pd.DataFrame(
        {
            "difference": home_points - away_points,
            "sum": home_points + away_points,
            "total_shots": total_shots.to_numpy(),
            "home_share": (counts[True] / total_shots).to_numpy(),
        },
    )


def panel_tables(
    real: pd.DataFrame,
    simulated: pd.DataFrame,
    chapter: dict,
    ranges: dict[tuple[str, str], str],
    statistics: dict[str, str],
) -> str:
    """Write statistics (title: pandas method) of each panel of the 3x3 grid as Markdown tables.

    Returns:
        One table per statistic, rows skill proxy sum (high first) and columns skill proxy difference, each cell
        "real / sim", each with all matches above it (and the theoretical value, where there is one).

    """
    observable, theory = chapter["observable"], chapter["theory"]
    terciles = ["low", "mid", "high"]
    header = "| Sum \\ difference | " + " | ".join(f"{t} {ranges['difference', t]}" for t in terciles) + " |"
    tables = []
    for title, statistic in statistics.items():
        number = "{:.0f}" if statistic == "count" else "{:.2f}"
        all_matches = [number.format(getattr(data[observable], statistic)()) for data in [real, simulated]]
        if title in theory:
            all_matches.append(f"{theory[title]:.2f}")
        names = " / ".join(["real", "sim", "theory"][: len(all_matches)])
        lines = [f"**{title}** (real / sim)", "", f"All matches ({names}): {' / '.join(all_matches)}", "", header]
        lines.append("| --- | --- | --- | --- |")
        for sum_tercile in reversed(terciles):
            cells = []
            for difference_tercile in terciles:
                values = [
                    data.loc[
                        (data["sum_bin"] == sum_tercile) & (data["difference_bin"] == difference_tercile),
                        observable,
                    ]
                    for data in [real, simulated]
                ]
                cells.append(" / ".join(number.format(getattr(value, statistic)()) for value in values))
            lines.append(f"| {sum_tercile} {ranges['sum', sum_tercile]} | " + " | ".join(cells) + " |")
        tables.append("\n".join(lines))
    return "\n\n".join(tables) + "\n"


def plot_grid(
    real: pd.DataFrame,
    simulated: pd.DataFrame,
    chapter: dict,
    ranges: dict[tuple[str, str], str],
    simulation: str,
) -> go.Figure:
    """Plot the distribution of an observable per tercile of skill proxy sum (rows) and difference (columns).

    Returns:
        A 3x3 grid; each panel has the real (bars) and the simulated (line) share of matches per value.

    """
    observable, bin_width, decimals = chapter["observable"], chapter["bin_width"], chapter["decimals"]
    terciles = ["low", "mid", "high"]
    few_matches = 20  # panels with fewer real matches are faded
    colours = {"real": "#2a78d6", "simulated": "#eb6834"}
    titles = []
    for sum_tercile in reversed(terciles):
        for difference_tercile in terciles:
            real_values = real.loc[
                (real["sum_bin"] == sum_tercile) & (real["difference_bin"] == difference_tercile),
                observable,
            ]
            simulated_values = simulated.loc[
                (simulated["sum_bin"] == sum_tercile) & (simulated["difference_bin"] == difference_tercile),
                observable,
            ]
            titles.append(
                f"sum {sum_tercile} {ranges['sum', sum_tercile]}<br>"
                f"difference {difference_tercile} {ranges['difference', difference_tercile]}<br>"
                f"matches: {len(real_values)} real, {len(simulated_values)} sim.<br>"
                f"mean (sd): {real_values.mean():.{decimals}f} ({real_values.std():.{decimals}f}) real, "
                f"{simulated_values.mean():.{decimals}f} ({simulated_values.std():.{decimals}f}) sim.",
            )

    figure = make_subplots(
        rows=3,
        cols=3,
        subplot_titles=titles,
        shared_xaxes=True,
        shared_yaxes=True,
        vertical_spacing=0.16,
    )
    for row, sum_tercile in enumerate(reversed(terciles), start=1):
        for col, difference_tercile in enumerate(terciles, start=1):
            for name, data in [("real", real), ("simulated", simulated)]:
                values = data.loc[
                    (data["sum_bin"] == sum_tercile) & (data["difference_bin"] == difference_tercile),
                    observable,
                ]
                is_faded = (
                    (real["sum_bin"] == sum_tercile) & (real["difference_bin"] == difference_tercile)
                ).sum() < few_matches
                if bin_width:  # a histogram of values from 0 to 1 (both included), plotted at the bin centres
                    bins = pd.cut(values, np.arange(0, 1 + bin_width / 2, bin_width), include_lowest=True)
                    values = bins.map(lambda interval: round(interval.mid, 3)).astype(float)
                shares = values.value_counts(normalize=True).sort_index()
                # Real data as bars; simulated data, with ten times the matches, as a line.
                trace = go.Bar if name == "real" else go.Scatter
                figure.add_trace(
                    trace(
                        x=shares.index,
                        y=shares.to_numpy(),
                        name=name,
                        marker_color=colours[name],
                        opacity=0.3 if is_faded else 1.0,
                        showlegend=row == 1 and col == 1,
                        hovertemplate=f"{name}: %{{x}}, share %{{y:.3f}}<extra></extra>",
                    ),
                    row=row,
                    col=col,
                )
    figure.update_layout(
        title=f"{chapter['title']}, by skill proxy sum (rows) and difference (columns)<br><sup>{simulation}</sup>",
        height=1200,
        margin={"t": 200},
    )
    figure.update_annotations(font_size=13)
    figure.update_xaxes(title_text=chapter["title"].lower(), row=3)
    figure.update_yaxes(title_text="share of matches", col=1)
    return figure
