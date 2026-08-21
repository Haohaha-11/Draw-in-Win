"""Reproduce the paper-style progressive-stage empirical study figure.

The reference raster contains no source table.  The five sequences below are
deterministic visual estimates of the plotted values, while the dark curve is
computed from them as their layer-wise arithmetic mean.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator, FuncFormatter, MultipleLocator


COLORS = {
    "d1": "#E8AA28",
    "d2": "#56A970",
    "d3": "#5DB7B2",
    "d4": "#78A9DD",
    "d5": "#9172C7",
    "mean": "#244D78",
}


def paper_style() -> None:
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


def source_sequences() -> tuple[np.ndarray, list[np.ndarray]]:
    """Return decoder layers and five visually inferred continuity sequences."""
    layers = np.arange(32)
    d1 = np.array([
        43, 55, 69, 76, 73, 72, 73, 71.5, 69.5, 67, 67.3, 68.5, 69.5,
        69.0, 68.0, 67.8, 67.6, 67.4, 66.8, 66.2, 67.5, 65.8, 63.0, 61.5,
        50.0, 52.0, 55.0, 51.0, 67.0, 66.4, 65.2, 57.0,
    ])
    d2 = np.array([
        38, 57, 49, 59, 62, 63, 62.5, 65, 66, 62, 64, 62, 66, 63, 67, 65,
        64, 63, 63, 63, 61, 63, 62, 57, 63, 53, 61, 53, 63, 57, 68, 54,
    ])
    d3 = np.array([
        36, 48, 53, 54, 55, 56, 57, 58, 59, 60, 61, 61, 62, 64, 63, 65,
        63, 62, 61, 61, 61, 62, 51, 59, 53, 50, 61, 49, 57, 60, 68, 55,
    ])
    d4 = np.array([
        33, 45, 45, 46, 43, 51, 51, 51, 51, 54, 57, 57, 56, 58, 58.5, 59,
        58.5, 58, 60, 56, 60, 58, 55, 50, 53, 52, 56, 43, 53, 48, 56, 52,
    ])
    d5 = np.array([
        25, 41, 47, 44, 49, 38, 46, 48, 51, 51, 53, 54, 54, 55, 54, 56,
        55, 56, 55, 56, 53, 59, 45, 55, 54, 50, 53, 38, 48, 57, 51, 41,
    ])
    return layers, [d1, d2, d3, d4, d5]


def create_figure() -> plt.Figure:
    paper_style()
    layers, series = source_sequences()
    mean_over_d = np.mean(np.vstack(series), axis=0)

    fig, ax = plt.subplots(figsize=(8.45, 5.15), dpi=180)
    fig.subplots_adjust(left=0.105, right=0.985, top=0.965, bottom=0.205)

    labels = [r"$d=1$", r"$d=2$", r"$d=3$", r"$d=4$", r"$d=5$"]
    colors = [COLORS[f"d{index}"] for index in range(1, 6)]
    markers = ["o", "s", "D", "^", "v"]
    handles = []
    for values, label, color, marker in zip(series, labels, colors, markers):
        line, = ax.plot(
            layers,
            values,
            color=color,
            lw=1.55,
            alpha=0.72,
            marker=marker,
            markersize=3.0,
            markeredgewidth=0,
            label=label,
            zorder=3,
        )
        handles.append(line)

    mean_line, = ax.plot(
        layers,
        mean_over_d,
        color=COLORS["mean"],
        lw=3.0,
        label=r"mean over $d$",
        zorder=5,
    )
    handles.append(mean_line)

    ax.set_xlim(-0.6, 31.6)
    ax.set_ylim(20, 81)
    ax.set_xticks(np.arange(0, 32, 4))
    ax.set_xlabel(r"Decoder layer  $\ell$")
    ax.set_ylabel("Selection Continuity")
    ax.yaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.0f}%"))
    ax.grid(which="major", color="#D9D9D9", linewidth=0.65, alpha=0.58)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color("#303030")
        spine.set_linewidth(1.15)

    # Matplotlib fills columns first at ncol=3; this order reproduces the
    # reference's two-row layout: d=1,d=3,d=5 / d=2,d=4,mean over d.
    legend = ax.legend(
        handles=handles,
        labels=labels + [r"mean over $d$"],
        loc="lower center",
        bbox_to_anchor=(0.61, 0.035),
        ncol=3,
        frameon=False,
        fontsize=14,
        handlelength=2.6,
        columnspacing=1.6,
        handletextpad=0.6,
        borderaxespad=0,
    )
    for text_item in legend.get_texts():
        text_item.set_fontfamily("serif")

    fig.text(
        0.5,
        0.055,
        "(b) Empirical Study on Progressive Stage",
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
    stem = "progressive_stage_empirical_study"
    fig.savefig(args.output_dir / f"{stem}.png", dpi=args.dpi)
    fig.savefig(args.output_dir / f"{stem}.svg")
    fig.savefig(args.output_dir / f"{stem}.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
