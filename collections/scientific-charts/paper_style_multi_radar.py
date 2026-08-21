"""Reproduce a paper-style 2 x 2 radar-chart comparison figure.

The values below were visually reconstructed from the supplied raster reference.
They are intended to reproduce the composition and styling, not to claim the
original benchmark measurements. Replace ``PANELS[*]["data"]`` with source
measurements when they are available.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.lines import Line2D


SERIES = {
    "FastV": {
        "label": "FastV (ECCV'24)",
        "color": "#C64F3C",
        "linewidth": 1.8,
        "linestyle": "-",
        "marker": None,
        "zorder": 4,
    },
    "SparseVLM": {
        "label": "SparseVLM (ICML'25)",
        "color": "#74869C",
        "linewidth": 1.7,
        "linestyle": "-",
        "marker": None,
        "zorder": 3,
    },
    "CDPruner": {
        "label": "CDPruner (NeurIPS'25)",
        "color": "#445A78",
        "linewidth": 1.8,
        "linestyle": "-",
        "marker": None,
        "zorder": 3,
    },
    "DivPrune": {
        "label": "DivPrune (CVPR'25)",
        "color": "#9AA7B2",
        "linewidth": 1.7,
        "linestyle": "-",
        "marker": None,
        "zorder": 2,
    },
    "VScan": {
        "label": "VScan (TMLR'26)",
        "color": "#5D9B79",
        "linewidth": 1.8,
        "linestyle": "-.",
        "marker": "*",
        "zorder": 5,
    },
    "STAR-Pro": {
        "label": "STAR-Pro (Ours)",
        "color": "#C98B28",
        "linewidth": 4.1,
        "linestyle": "-",
        "marker": "o",
        "zorder": 7,
    },
}


PANELS = [
    {
        "title": "LLaVA-NeXT-7B (↓ 88.9%)",
        "metrics": [
            "SEED",
            "GQA",
            "SQA",
            r"VQA$^{T}$",
            "POPE",
            "MME",
            r"MMB$^{E}$",
            r"MMB$^{C}$",
            "AI2D",
            "MMMU",
        ],
        "caption": "99.0% vs. 98.1%  (+0.9)",
        "data": {
            "FastV": [70, 70, 97, 71, 75, 70, 74, 71, 91, 94],
            "SparseVLM": [95, 92, 93, 96, 84, 90, 94, 96, 97, 93],
            "CDPruner": [96, 95, 96, 96, 96, 95, 97, 97, 96, 95],
            "DivPrune": [94, 93, 94, 97, 97, 87, 94, 95, 96, 94],
            "VScan": [94, 94, 95, 96, 97, 95, 97, 96, 95, 96],
            "STAR-Pro": [99, 97, 98, 98, 99, 99, 98, 99, 98, 95],
        },
    },
    {
        "title": "LLaVA-Video-7B (↓ 90.5%)",
        "metrics": [
            "MLVU",
            r"LVB$_{s}$",
            r"LVB$_{m}$",
            r"LVB$_{l}$",
            r"VMME$_{s}$",
            r"VMME$_{m}$",
            r"VMME$_{l}$",
        ],
        "caption": "92.7% vs. 89.9%  (+2.8)",
        "data": {
            "FastV": [82, 83, 78, 85, 82, 74, 84],
            "SparseVLM": [94, 91, 90, 90, 89, 90, 91],
            "CDPruner": [92, 92, 88, 89, 86, 88, 91],
            "DivPrune": [96, 94, 93, 93, 94, 92, 95],
            "VScan": [97, 96, 96, 94, 93, 94, 94],
            "STAR-Pro": [99, 98, 98, 98, 99, 99, 98],
        },
    },
    {
        "title": "Qwen3-VL-8B-Instruct (↓ 90.1%)",
        "metrics": [
            "AI2D",
            "POPE",
            "Hall",
            "MME",
            r"MMB$^{E}$",
            r"MMB$^{C}$",
            "MMStar",
            "SQA",
        ],
        "caption": "91.7% vs. 90.3%  (+1.4)",
        "data": {
            "FastV": [88, 70, 70, 70, 70, 70, 70, 88],
            "SparseVLM": [94, 92, 84, 86, 89, 85, 78, 90],
            "CDPruner": [94, 93, 84, 85, 88, 84, 79, 90],
            "DivPrune": [97, 95, 93, 94, 96, 95, 92, 96],
            "VScan": [95, 97, 97, 96, 98, 97, 95, 96],
            "STAR-Pro": [99, 99, 98, 99, 99, 99, 98, 99],
        },
    },
    {
        "title": "InternVL3-8B (↓ 90.0%)",
        "metrics": [
            "AI2D",
            "POPE",
            "Hall",
            "MME",
            r"MMB$^{E}$",
            r"MMB$^{C}$",
            "MMStar",
            "SQA",
        ],
        "caption": "92.2% vs. 87.7%  (+4.5)",
        "data": {
            "FastV": [88, 91, 95, 82, 88, 90, 90, 94],
            "SparseVLM": [95, 96, 95, 92, 92, 93, 94, 95],
            "CDPruner": [94, 95, 94, 91, 90, 93, 91, 94],
            "DivPrune": [97, 98, 97, 96, 96, 96, 95, 97],
            "VScan": [96, 98, 96, 97, 97, 97, 96, 98],
            "STAR-Pro": [99, 99, 99, 98, 99, 99, 99, 99],
        },
    },
]


def _closed(values: list[float]) -> np.ndarray:
    """Return a polygonal radar series with its first value repeated."""

    array = np.asarray(values, dtype=float)
    return np.concatenate([array, array[:1]])


def draw_panel(ax: plt.Axes, panel: dict[str, object]) -> None:
    """Draw one radar-chart panel."""

    metrics = panel["metrics"]
    count = len(metrics)
    angles = np.linspace(0, 2 * np.pi, count, endpoint=False)
    closed_angles = np.concatenate([angles, angles[:1]])

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_ylim(70, 100)
    ax.set_xticks(angles)
    ax.set_xticklabels(metrics, color="#3F4248", fontsize=10.6)
    ax.tick_params(axis="x", pad=2)
    ax.set_yticks([70, 80, 90])
    ax.set_yticklabels(["70", "80", "90"], color="#A6A9AD", fontsize=7.3)
    ax.set_rlabel_position(0)

    ax.set_facecolor("#FDFBF7")
    ax.grid(color="#C6CBD0", linewidth=0.9, alpha=0.82)
    ax.spines["polar"].set_color("#BFC6CD")
    ax.spines["polar"].set_linewidth(1.25)

    star_values = _closed(panel["data"]["STAR-Pro"])
    ax.fill(
        closed_angles,
        star_values,
        color="#E5C58E",
        alpha=0.27,
        zorder=1,
    )

    for key, style in SERIES.items():
        values = _closed(panel["data"][key])
        kwargs = {
            "color": style["color"],
            "linewidth": style["linewidth"],
            "linestyle": style["linestyle"],
            "zorder": style["zorder"],
            "solid_capstyle": "round",
            "solid_joinstyle": "round",
        }
        if style["marker"] is not None:
            kwargs.update(
                marker=style["marker"],
                markersize=4.8 if key == "STAR-Pro" else 4.2,
                markeredgewidth=0.8,
                markeredgecolor=style["color"],
                markerfacecolor="#F8EBD2" if key == "STAR-Pro" else style["color"],
            )
        ax.plot(closed_angles, values, **kwargs)

    ax.set_title(
        panel["title"],
        y=1.15,
        pad=0,
        color="#4A4A4A",
        fontsize=13.6,
        fontweight="normal",
    )
    ax.text(
        0.5,
        -0.15,
        panel["caption"],
        transform=ax.transAxes,
        ha="center",
        va="center",
        color="#9A6B26",
        fontsize=11.7,
        fontweight="bold",
    )


def make_figure() -> plt.Figure:
    """Create the full four-panel paper figure."""

    try:
        font_manager.findfont("Times New Roman", fallback_to_default=False)
        serif_font = "Times New Roman"
    except ValueError:
        serif_font = "DejaVu Serif"

    plt.rcParams.update(
        {
            "font.family": serif_font,
            "mathtext.fontset": "stix",
            "axes.unicode_minus": False,
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )

    figure, axes = plt.subplots(
        2,
        2,
        figsize=(8.35, 8.55),
        subplot_kw={"projection": "polar"},
    )
    figure.subplots_adjust(
        left=0.075,
        right=0.94,
        top=0.88,
        bottom=0.16,
        wspace=0.30,
        hspace=0.47,
    )

    for axis, panel in zip(axes.flat, PANELS):
        draw_panel(axis, panel)

    legend_order = ["FastV", "SparseVLM", "CDPruner", "DivPrune", "VScan", "STAR-Pro"]
    handles = []
    for key in legend_order:
        style = SERIES[key]
        handles.append(
            Line2D(
                [0],
                [0],
                color=style["color"],
                linewidth=style["linewidth"],
                linestyle=style["linestyle"],
                marker=style["marker"],
                markersize=5.2 if key == "STAR-Pro" else 4.2,
                markeredgewidth=0.8,
                markeredgecolor=style["color"],
                markerfacecolor="#F8EBD2" if key == "STAR-Pro" else style["color"],
                label=style["label"],
            )
        )

    legend = figure.legend(
        handles=handles,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.012),
        ncol=3,
        frameon=False,
        columnspacing=1.8,
        handlelength=2.2,
        handletextpad=0.75,
        fontsize=10.5,
    )
    legend.get_texts()[-1].set_fontweight("bold")
    legend.get_texts()[-1].set_color(SERIES["STAR-Pro"]["color"])

    return figure


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Directory for the PNG, SVG, and PDF outputs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    figure = make_figure()

    base = args.output_dir / "paper_style_multi_radar"
    figure.savefig(base.with_suffix(".png"), dpi=220)
    figure.savefig(base.with_suffix(".svg"))
    figure.savefig(base.with_suffix(".pdf"))
    plt.close(figure)

    print(f"Saved: {base.with_suffix('.png')}")
    print(f"Saved: {base.with_suffix('.svg')}")
    print(f"Saved: {base.with_suffix('.pdf')}")


if __name__ == "__main__":
    main()
