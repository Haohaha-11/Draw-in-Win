"""
Resilience Trajectory: Dynamic vs. Static Strategy (2024-2030)
High-end academic visualization showing SDG performance under shock conditions
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Rectangle
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

# Set Times New Roman font
font_path = fm.findfont('DejaVu Serif')
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
fm.fontManager.addfont(font_path)

# Data
YEARS = [2024, 2025, 2026, 2027, 2028, 2029, 2030]

# SDG 16
SDG16_DYN = [12.0658, 51.1295, 40.9036, 59.0391, 75.9765, 84.7019, 87.8929]
SDG16_STA = [12.0658, 49.1529, 39.3223, 46.6311, 50.5762, 52.9296, 54.5271]

# SDG 12
SDG12_DYN = [0.0000, 42.4455, 33.9564, 96.3120, 91.7764, 90.8365, 90.7141]
SDG12_STA = [0.0000, 52.1213, 41.6971, 56.8775, 63.6678, 66.7824, 68.3322]

# SDG 14
SDG14_DYN = [0.0000, 34.7515, 27.8012, 49.5141, 97.0237, 90.7239, 89.1199]
SDG14_STA = [0.0000, 43.6539, 34.9231, 42.9710, 47.1495, 49.6074, 51.2845]

# Color palette
COLOR_DYNAMIC_LINE = '#e89a94'  # Slightly darker shade of #fbb5ae for better visibility
COLOR_DYNAMIC_MARKER = '#fbb5ae'  # Original soft red/pink for markers
COLOR_STATIC = '#7db3cc'  # Muted blue based on #c0e5f5
COLOR_FILL = '#fcc3a4'  # Soft orange for resilience gap
COLOR_SHOCK = '#fbb5ae'  # Shock line color

# Create figure with 3 subplots
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
fig.patch.set_facecolor('white')

# Data for each subplot
sdg_data = [
    ('SDG 16', SDG16_DYN, SDG16_STA),
    ('SDG 12', SDG12_DYN, SDG12_STA),
    ('SDG 14', SDG14_DYN, SDG14_STA)
]

for idx, (ax, (title, dyn_data, sta_data)) in enumerate(zip(axes, sdg_data)):

    # Plot Static Strategy (dashed line)
    ax.plot(YEARS, sta_data,
            linestyle='--', linewidth=2.5,
            color=COLOR_STATIC,
            marker='s', markersize=6,
            markerfacecolor=COLOR_STATIC,
            markeredgecolor='white', markeredgewidth=1,
            label='Static Strategy', zorder=2)

    # Plot Dynamic Strategy (solid line)
    ax.plot(YEARS, dyn_data,
            linestyle='-', linewidth=3,
            color=COLOR_DYNAMIC_LINE,
            marker='o', markersize=8,
            markerfacecolor=COLOR_DYNAMIC_MARKER,
            markeredgecolor='white', markeredgewidth=1.5,
            label='Dynamic Strategy', zorder=3)

    # Fill area where Dynamic > Static (Resilience Gap)
    dyn_array = np.array(dyn_data)
    sta_array = np.array(sta_data)
    ax.fill_between(YEARS, sta_array, dyn_array,
                     where=(dyn_array > sta_array),
                     color=COLOR_FILL, alpha=0.3,
                     label='Resilience Gap', zorder=1)

    # Shock event vertical line at 2026
    ax.axvline(x=2026, color=COLOR_SHOCK, linestyle=':',
               linewidth=2, alpha=0.7, zorder=1)

    # Shock annotation (vertical text)
    ax.text(2026, ax.get_ylim()[1] * 0.95, 'Shock\n(2026)',
            ha='center', va='top', fontsize=10,
            color='black', fontweight='bold',
            fontproperties=font_prop, rotation=0)

    # Annotate final score difference at 2030
    final_diff = dyn_data[-1] - sta_data[-1]
    mid_y = (dyn_data[-1] + sta_data[-1]) / 2

    # Arrow pointing to the gap
    ax.annotate(f'+{final_diff:.1f}',
                xy=(2030, mid_y), xytext=(2030.3, mid_y),
                fontsize=11, fontweight='bold',
                color=COLOR_DYNAMIC_LINE,
                fontproperties=font_prop,
                ha='left', va='center',
                bbox=dict(boxstyle='round,pad=0.3',
                         facecolor='white',
                         edgecolor=COLOR_DYNAMIC_LINE,
                         linewidth=1.5),
                arrowprops=dict(arrowstyle='->',
                               color=COLOR_DYNAMIC_LINE,
                               lw=1.5))

    # Styling
    ax.set_title(title, fontsize=14, fontweight='bold',
                pad=15, fontproperties=font_prop)
    ax.set_xlabel('Year', fontsize=12, fontweight='bold',
                 fontproperties=font_prop)

    # Only show ylabel on first subplot
    if idx == 0:
        ax.set_ylabel('Performance Score', fontsize=12,
                     fontweight='bold', fontproperties=font_prop)

    # Set x-axis ticks
    ax.set_xticks(YEARS)
    ax.set_xticklabels(YEARS, fontsize=10, fontproperties=font_prop)

    # Y-axis ticks
    ax.tick_params(axis='both', labelsize=10, direction='out')

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Make left and bottom spines thicker
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)

    # Add very faint horizontal grid
    ax.grid(axis='y', alpha=0.15, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)

    # Set y-axis limits
    ax.set_ylim(-5, 105)

# Add overall title
fig.suptitle('Resilience Trajectory: Dynamic vs. Static Strategy (2024-2030)',
             fontsize=16, fontweight='bold', y=0.98,
             fontproperties=font_prop)

# Add legend (only once, on the first subplot)
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center',
          bbox_to_anchor=(0.5, -0.05),
          ncol=3, fontsize=11, frameon=True,
          fancybox=False, shadow=False, prop=font_prop)

# Adjust layout
plt.tight_layout(rect=[0, 0.02, 1, 0.96])

# Save figure
output_svg = SCRIPT_DIR / 'resilience_trajectory_plot.svg'
output_png = SCRIPT_DIR / 'resilience_trajectory_plot.png'

plt.savefig(output_svg, format='svg', dpi=300, bbox_inches='tight',
           facecolor='white', edgecolor='none')
plt.savefig(output_png, format='png', dpi=300, bbox_inches='tight',
           facecolor='white', edgecolor='none')

print("Resilience Trajectory Plot saved:")
print(f"  SVG: {output_svg}")
print(f"  PNG: {output_png}")

# Print statistics
print("\n=== Final Score Differences (2030) ===")
for title, dyn_data, sta_data in sdg_data:
    diff = dyn_data[-1] - sta_data[-1]
    improvement = (diff / sta_data[-1]) * 100
    print(f"{title}: Dynamic={dyn_data[-1]:.2f}, Static={sta_data[-1]:.2f}, "
          f"Difference=+{diff:.2f} (+{improvement:.1f}%)")

plt.show()
