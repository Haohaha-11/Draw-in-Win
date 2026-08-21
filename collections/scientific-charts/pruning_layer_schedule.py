"""Reproduce the pruning-layer schedule surface and projected contours.

The original score grid was not supplied.  This script uses a deterministic
analytic surface whose range and visual landmarks follow the raster reference.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FormatStrFormatter
from mpl_toolkits.mplot3d import proj3d


GOLD = "#E5A940"
DARK_GOLD = "#B8771F"
FLOOR = 66.86


def paper_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif", "STIXGeneral"],
            "mathtext.fontset": "stix",
            "font.size": 11,
            "axes.titleweight": "bold",
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )


def score_surface(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Construct a smooth plateau with local ridges similar to the reference."""
    plateau = 67.18 + 0.83 / (1.0 + np.exp(-(x - 7.6) * 1.55))
    broad_rise = 0.26 * np.exp(-((x - 11.8) ** 2 / 11.0 + (y - 20.5) ** 2 / 12.0))
    target_peak = 0.20 * np.exp(-((x - 12.0) ** 2 / 1.7 + (y - 20.0) ** 2 / 2.8))
    far_ridge = 0.16 * np.exp(-((x - 9.0) ** 2 / 3.0 + (y - 25.5) ** 2 / 3.8))
    trough = -0.22 * np.exp(-((x - 8.2) ** 2 / 1.6 + (y - 22.5) ** 2 / 2.0))
    undulation = 0.075 * np.sin(1.55 * (x - 6.0)) * np.cos(0.78 * (y - 18.0))
    z = plateau + broad_rise + target_peak + far_ridge + trough + undulation
    return np.clip(z, 66.92, 68.62)


def create_figure() -> plt.Figure:
    paper_style()
    x = np.linspace(6, 15, 70)
    y = np.linspace(18, 27, 70)
    xx, yy = np.meshgrid(x, y)
    zz = score_surface(xx, yy)
    cmap = LinearSegmentedColormap.from_list(
        "paper_gold",
        ["#FFFDF8", "#F8E5B9", "#EDBC5E", "#D9962F"],
    )

    fig = plt.figure(figsize=(9.4, 7.1), dpi=180)
    ax = fig.add_subplot(111, projection="3d")
    fig.subplots_adjust(left=0.01, right=0.86, top=0.93, bottom=0.06)

    surface = ax.plot_surface(
        xx,
        yy,
        zz,
        cmap=cmap,
        vmin=66.9,
        vmax=68.65,
        rstride=1,
        cstride=1,
        linewidth=0.16,
        edgecolor=(1.0, 0.94, 0.80, 0.45),
        antialiased=True,
        alpha=0.94,
    )
    surface.set_rasterized(True)
    ax.contour(
        xx,
        yy,
        zz,
        zdir="z",
        offset=FLOOR,
        levels=np.linspace(67.0, 68.6, 9),
        colors=[DARK_GOLD],
        linewidths=0.8,
        alpha=0.65,
    )

    star_x, star_y = 12.0, 20.0
    star_z = float(score_surface(np.array(star_x), np.array(star_y)))
    marker_z = star_z + 0.075
    ax.plot([star_x, star_x], [star_y, star_y], [FLOOR, marker_z],
            color=DARK_GOLD, ls="--", lw=1.5, alpha=0.9, zorder=8)
    ax.scatter([star_x], [star_y], [marker_z], marker="*", s=330,
               facecolor="white", edgecolor=DARK_GOLD, linewidth=2.2,
               depthshade=False, zorder=10)
    ax.text(star_x + 0.35, star_y + 0.35, marker_z + 0.16,
            "STAR-Pro\n(12, 20)", fontsize=12, fontweight="bold",
            ha="center", va="bottom", color="#3D3A36", zorder=12)

    ax.set_xlim(6, 15)
    ax.set_ylim(18, 27)
    ax.set_zlim(FLOOR, 68.65)
    ax.set_xticks(np.arange(6, 16, 1))
    ax.set_yticks(np.arange(18, 28, 2))
    ax.set_zticks([67.0, 67.4, 67.8, 68.2, 68.6])
    ax.zaxis.set_major_formatter(FormatStrFormatter("%.1f"))
    ax.set_xlabel(r"First pruning depth  $\ell_1$", labelpad=13)
    ax.set_ylabel(r"Second pruning depth  $\ell_2$", labelpad=13)
    ax.set_zlabel("Score", labelpad=8)
    ax.set_title("(c) Pruning Layer Schedule", fontsize=14.5, pad=8, loc="left")
    ax.view_init(elev=27, azim=-132)
    ax.set_box_aspect((1.1, 1.0, 0.68))

    # A 2D overlay keeps the highlighted star visible above mplot3d's surface
    # depth sorting while retaining the exact projected 3D coordinate.
    projected_x, projected_y, _ = proj3d.proj_transform(
        star_x, star_y, marker_z, ax.get_proj()
    )
    star_overlay = ax.annotate(
        "★",
        xy=(projected_x, projected_y),
        xycoords="data",
        ha="center",
        va="center",
        fontsize=24,
        fontfamily="DejaVu Sans",
        color="white",
        zorder=30,
    )
    star_overlay.set_path_effects(
        [path_effects.withStroke(linewidth=2.5, foreground=DARK_GOLD)]
    )

    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((1, 1, 1, 0))
        axis.pane.set_edgecolor("#CDD4DC")
        axis._axinfo["grid"]["color"] = (0.79, 0.83, 0.87, 0.70)
        axis._axinfo["grid"]["linewidth"] = 0.65
    ax.tick_params(colors="#4E565F", labelsize=9, pad=1)

    cbar = fig.colorbar(surface, ax=ax, fraction=0.035, pad=0.055, shrink=0.62)
    cbar.set_ticks([67.0, 67.4, 67.8, 68.2, 68.6])
    cbar.ax.tick_params(labelsize=9, colors="#4E565F")
    cbar.outline.set_edgecolor("#747A82")
    cbar.set_label("Score", rotation=270, labelpad=14)
    return fig


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parent)
    parser.add_argument("--dpi", type=int, default=300)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    fig = create_figure()
    stem = "pruning_layer_schedule"
    fig.savefig(args.output_dir / f"{stem}.png", dpi=args.dpi)
    fig.savefig(args.output_dir / f"{stem}.svg")
    fig.savefig(args.output_dir / f"{stem}.pdf")
    plt.close(fig)


if __name__ == "__main__":
    main()
