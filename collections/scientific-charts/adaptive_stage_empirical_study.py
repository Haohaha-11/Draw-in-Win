"""Reproduce the paper-style adaptive-stage empirical study figure.

The reference image does not provide its numerical source data.  The values in
this script are therefore deterministic, visually inferred approximations.
Replace the checkpoint arrays and cluster-node coordinates with the original
measurements if they become available.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator, FuncFormatter, MultipleLocator


GOLD = "#E5A416"
GOLD_LIGHT = "#F3C65B"
GREEN = "#38A762"
BLUE = "#3E83C7"
PURPLE = "#8D70C6"
RED = "#DE5149"
GRID = "#D9D9D9"


def paper_style() -> None:
    """Apply a restrained serif style similar to the supplied paper figure."""
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif", "STIXGeneral"],
            "mathtext.fontset": "stix",
            "font.size": 11,
            "axes.labelsize": 13,
            "axes.linewidth": 1.15,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.major.size": 4,
            "ytick.major.size": 4,
            "xtick.minor.size": 2.5,
            "ytick.minor.size": 2.5,
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
        }
    )


def interpolate_curve(k_dense: np.ndarray, checkpoints: dict[int, float]) -> np.ndarray:
    """Linearly interpolate hand-read checkpoints on an ascending K grid."""
    x = np.array(sorted(checkpoints), dtype=float)
    y = np.array([checkpoints[int(value)] for value in x], dtype=float)
    return np.interp(k_dense, x, y)


def sample_triangle(
    rng: np.random.Generator,
    vertices: np.ndarray,
    count: int,
    jitter: tuple[float, float],
) -> np.ndarray:
    """Draw a diffuse point cloud from a triangle using barycentric weights."""
    weights = rng.dirichlet(np.ones(3), size=count)
    points = weights @ vertices
    points += rng.normal(scale=np.asarray(jitter), size=(count, 2))
    return points


def draw_cluster(
    ax: plt.Axes,
    rng: np.random.Generator,
    *,
    nodes: np.ndarray,
    triangle: np.ndarray,
    color: str,
    fill_color: str,
    count: int,
    jitter: tuple[float, float],
    path_order: list[int],
) -> None:
    """Draw a translucent search region, samples, and numbered search path."""
    cloud = sample_triangle(rng, triangle, count, jitter)
    ax.fill(
        triangle[:, 0],
        triangle[:, 1],
        color=fill_color,
        alpha=0.13,
        linewidth=0,
        zorder=1,
    )
    ax.scatter(
        cloud[:, 0],
        cloud[:, 1],
        s=8,
        c=color,
        alpha=0.18,
        edgecolors="none",
        zorder=2,
    )

    ordered = nodes[path_order]
    ax.plot(
        ordered[:, 0],
        ordered[:, 1],
        color=color,
        linewidth=1.9,
        alpha=0.88,
        zorder=3,
    )
    ax.scatter(
        nodes[:, 0],
        nodes[:, 1],
        s=66,
        facecolor="white",
        edgecolor=color,
        linewidth=2.0,
        zorder=4,
    )
    for index, (x, y) in enumerate(nodes):
        ax.text(
            x,
            y,
            str(index),
            color=color,
            ha="center",
            va="center",
            fontsize=7.5,
            fontweight="bold",
            zorder=5,
        )


def add_gain_annotation(
    ax: plt.Axes,
    *,
    k: float,
    lower: float,
    upper: float,
    label: str,
    text_dx: float,
    text_dy: float = 0.0,
) -> None:
    """Add the red double-headed gain indicator used in the reference."""
    ax.annotate(
        "",
        xy=(k, upper),
        xytext=(k, lower),
        arrowprops={
            "arrowstyle": "<|-|>",
            "color": RED,
            "lw": 1.8,
            "mutation_scale": 9,
            "shrinkA": 0,
            "shrinkB": 0,
        },
        zorder=8,
    )
    ax.text(
        k + text_dx,
        (upper + lower) / 2 + text_dy,
        label,
        color=RED,
        fontsize=12,
        fontweight="bold",
        ha="left",
        va="center",
        zorder=9,
    )


def create_figure() -> plt.Figure:
    paper_style()
    rng = np.random.default_rng(42)

    fig, ax = plt.subplots(figsize=(8.45, 5.15), dpi=180)
    fig.subplots_adjust(left=0.105, right=0.985, top=0.965, bottom=0.205)

    # Visually inferred checkpoint values (percentage points).
    k_dense = np.linspace(5, 128, 500)
    star = interpolate_curve(
        k_dense,
        {5: 74, 8: 78, 16: 83.5, 24: 86.2, 32: 88.3, 48: 90.4,
         64: 92.0, 80: 93.5, 96: 94.5, 112: 95.2, 128: 95.0},
    )
    cdpruner = interpolate_curve(
        k_dense,
        {5: 43, 8: 50, 16: 62, 24: 71, 32: 78, 48: 84.7,
         64: 88.0, 80: 91.0, 96: 92.6, 112: 93.6, 128: 94.0},
    )
    divprune = interpolate_curve(
        k_dense,
        {5: 32, 8: 42, 16: 57, 24: 65, 32: 72, 48: 81.0,
         64: 85.0, 80: 89.0, 96: 91.0, 112: 92.2, 128: 93.0},
    )

    # Confidence-like bands are widened as fewer visual tokens remain.
    scarcity = (128 - k_dense) / 123
    cd_band = 0.8 + 2.3 * scarcity**1.7
    div_band = 0.7 + 1.9 * scarcity**1.5
    star_band = 0.35 + 0.55 * scarcity
    ax.fill_between(k_dense, star - star_band, star + star_band,
                    color=GOLD_LIGHT, alpha=0.12, linewidth=0, zorder=0)
    ax.fill_between(k_dense, cdpruner - cd_band, cdpruner + cd_band,
                    color=GREEN, alpha=0.13, linewidth=0, zorder=0)
    ax.fill_between(k_dense, divprune - div_band, divprune + div_band,
                    color=BLUE, alpha=0.13, linewidth=0, zorder=0)

    marker_every = 16
    ax.plot(k_dense, star, color=GOLD, lw=2.7, ls="-.", marker="o",
            markersize=2.4, markevery=marker_every, zorder=7)
    ax.plot(k_dense, cdpruner, color=GREEN, lw=1.8, ls=(0, (7, 3)), marker="s",
            markersize=2.1, markevery=marker_every, zorder=6)
    ax.plot(k_dense, divprune, color=BLUE, lw=1.8, ls="-", marker="^",
            markersize=2.1, markevery=marker_every, zorder=6)

    # Three lower search trajectories and their surrounding candidate clouds.
    gold_nodes = np.array(
        [[122.5, 75.5], [104.5, 68.3], [100.0, 71.7], [96.8, 62.7],
         [94.1, 50.6], [87.0, 80.2], [96.5, 79.4]]
    )
    draw_cluster(
        ax,
        rng,
        nodes=gold_nodes,
        triangle=np.array([[122.5, 75.5], [94.1, 50.6], [87.0, 80.2]]),
        color=GOLD,
        fill_color=GOLD_LIGHT,
        count=400,
        jitter=(2.8, 1.9),
        path_order=[0, 1, 2, 3, 4, 6, 5],
    )

    green_nodes = np.array(
        [[66.0, 63.2], [60.8, 62.0], [59.3, 57.8], [54.7, 47.6],
         [49.0, 71.5], [51.8, 70.1], [57.6, 67.3]]
    )
    draw_cluster(
        ax,
        rng,
        nodes=green_nodes,
        triangle=np.array([[68.0, 63.0], [54.5, 47.6], [48.5, 72.0]]),
        color=GREEN,
        fill_color=GREEN,
        count=360,
        jitter=(2.4, 1.8),
        path_order=[0, 1, 2, 3, 6, 5, 4],
    )

    blue_nodes = np.array(
        [[35.8, 51.7], [32.7, 51.6], [29.0, 53.0], [26.4, 50.8],
         [22.4, 58.2], [20.3, 60.0], [27.4, 56.0]]
    )
    draw_cluster(
        ax,
        rng,
        nodes=blue_nodes,
        triangle=np.array([[39.0, 57.0], [26.0, 46.0], [19.5, 61.0]]),
        color=BLUE,
        fill_color=BLUE,
        count=330,
        jitter=(2.1, 1.6),
        path_order=[0, 1, 2, 3, 6, 4, 5],
    )

    # PCA wedge and direction arrow in the lower-left corner.
    pca_triangle = np.array([[128.0, 43.5], [117.0, 47.5], [118.0, 35.7]])
    ax.fill(pca_triangle[:, 0], pca_triangle[:, 1], color=PURPLE,
            alpha=0.20, linewidth=0, zorder=1)
    ax.annotate(
        "",
        xy=(118.5, 40.0),
        xytext=(118.5, 35.5),
        arrowprops={"arrowstyle": "-|>", "color": PURPLE, "lw": 1.5},
        zorder=4,
    )
    ax.annotate(
        "",
        xy=(124.5, 35.5),
        xytext=(118.5, 35.5),
        arrowprops={"arrowstyle": "-|>", "color": PURPLE, "lw": 1.5},
        zorder=4,
    )
    ax.text(123.8, 42.1, "PCA", color=PURPLE, fontsize=10,
            ha="left", va="center", fontweight="bold")

    # Direct method labels mirror the source figure's lower annotations.
    ax.scatter([113.0], [43.8], s=120, color=GOLD, edgecolor="white",
               linewidth=0.8, zorder=7)
    ax.text(110.8, 43.9, "STAR-Pro", color=GOLD, fontsize=17,
            fontweight="bold", ha="left", va="center", zorder=7)
    ax.scatter([75.0], [40.8], s=62, color=GREEN, marker="s", zorder=7)
    ax.text(72.5, 40.9, "CDPruner", color=GREEN, fontsize=12.5,
            fontweight="bold", ha="left", va="center", zorder=7)
    ax.scatter([40.0], [37.7], s=58, color=BLUE, marker="^", zorder=7)
    ax.text(37.5, 37.8, "DivPrune", color=BLUE, fontsize=11.5,
            fontweight="bold", ha="left", va="center", zorder=7)

    # Performance gaps read from the callouts in the supplied raster.
    add_gain_annotation(ax, k=127.7, lower=93.0, upper=95.0,
                        label="+2%", text_dx=-1.4, text_dy=1.2)
    add_gain_annotation(ax, k=96.0, lower=92.5, upper=94.5,
                        label="+2%", text_dx=-1.0, text_dy=1.1)
    add_gain_annotation(ax, k=64.0, lower=88.0, upper=92.0,
                        label="+4%", text_dx=-2.0, text_dy=1.1)
    add_gain_annotation(ax, k=32.0, lower=78.0, upper=88.0,
                        label="+10%", text_dx=-1.6)
    add_gain_annotation(ax, k=5.25, lower=43.0, upper=74.0,
                        label="+31%", text_dx=12.0)

    ax.set_xlim(128, 5)
    ax.set_ylim(33, 101)
    ax.set_xticks([128, 96, 64, 32, 5])
    ax.set_xlabel(r"Selected visual tokens  $K$")
    ax.set_ylabel("Visual Feature Retention Ratio")
    ax.yaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    ax.xaxis.set_minor_locator(AutoMinorLocator(4))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.0f}%"))
    ax.grid(which="major", color=GRID, linewidth=0.65, alpha=0.60)
    ax.grid(which="minor", axis="x", color=GRID, linewidth=0.40, alpha=0.22)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color("#303030")
        spine.set_linewidth(1.15)

    fig.text(
        0.5,
        0.055,
        "(a) Empirical Study on Adaptive Stage",
        ha="center",
        va="center",
        fontsize=14.5,
        fontweight="bold",
        family="serif",
    )
    return fig


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Directory for PNG, SVG, and PDF outputs.",
    )
    parser.add_argument("--dpi", type=int, default=300, help="PNG output DPI.")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    fig = create_figure()
    stem = "adaptive_stage_empirical_study"
    fig.savefig(args.output_dir / f"{stem}.png", dpi=args.dpi)
    fig.savefig(args.output_dir / f"{stem}.svg")
    fig.savefig(args.output_dir / f"{stem}.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
