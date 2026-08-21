"""
Polar Coverage Chart - Multi-Configuration Comparison Visualization

This chart visualizes coverage performance across multiple categories (provinces/regions)
for different configuration types.

Chart Components:
1. Radial Axes: Each ray represents a category (e.g., province)
2. Radial Distance: Represents coverage value (0.0 to 1.0)
3. Filled Areas: Show overall coverage pattern for each configuration
4. Bubbles: Individual data points with size representing coverage intensity
5. Colors: Distinguish different configuration types

Use Cases:
- Network coverage comparison across regions
- Service deployment analysis by configuration
- Resource allocation visualization
- Performance benchmarking across categories
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.interpolate import make_interp_spline
from scipy.ndimage import gaussian_filter1d
import matplotlib.patches as mpatches
import os

# Set global font style
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.5

# Define categories (Chinese provinces)
provinces = [
    'ZJ', 'BJ', 'TJ', 'HE', 'SX', 'NM', 'LN', 'JL', 'HL',
    'SH', 'JS', 'AH', 'FJ', 'JX', 'SD', 'HA', 'HB',
    'HN', 'GD', 'GX', 'HI', 'CQ', 'SC', 'GZ', 'YN', 'XZ',
    'SN', 'GS', 'QH', 'NX', 'XJ'
]

n_categories = len(provinces)
angles = np.linspace(0, 2 * np.pi, n_categories, endpoint=False)

# Generate simulated data for three configurations
np.random.seed(42)

# Configuration L1 (Green) - Lower coverage, more variation
coverage_L1 = np.random.uniform(0.2, 0.6, n_categories)
coverage_L1 = gaussian_filter1d(coverage_L1, sigma=2, mode='wrap')
coverage_values_L1 = np.random.uniform(0.15, 0.55, n_categories)  # Bubble sizes

# Configuration L2 (Purple) - Medium coverage
coverage_L2 = np.random.uniform(0.4, 0.8, n_categories)
coverage_L2 = gaussian_filter1d(coverage_L2, sigma=2, mode='wrap')
coverage_values_L2 = np.random.uniform(0.35, 0.75, n_categories)

# Configuration L3 (Blue) - Higher coverage
coverage_L3 = np.random.uniform(0.5, 0.95, n_categories)
coverage_L3 = gaussian_filter1d(coverage_L3, sigma=2, mode='wrap')
coverage_values_L3 = np.random.uniform(0.45, 0.90, n_categories)

# Create smooth curves for filled areas
def smooth_polar_curve(angles, radii, smoothness=200):
    """Create smooth interpolated curve for polar plot"""
    angles_extended = np.concatenate([angles, [angles[0]]])
    radii_extended = np.concatenate([radii, [radii[0]]])

    t = np.linspace(0, 1, len(angles_extended))
    t_smooth = np.linspace(0, 1, smoothness)

    spline = make_interp_spline(t, radii_extended, k=3)
    radii_smooth = spline(t_smooth)
    angles_smooth = np.linspace(0, 2 * np.pi, smoothness, endpoint=True)

    return angles_smooth, radii_smooth

# Generate smooth curves
angles_smooth_L1, coverage_smooth_L1 = smooth_polar_curve(angles, coverage_L1)
angles_smooth_L2, coverage_smooth_L2 = smooth_polar_curve(angles, coverage_L2)
angles_smooth_L3, coverage_smooth_L3 = smooth_polar_curve(angles, coverage_L3)

# Create figure
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='polar')

# Set viewing angle
ax.set_theta_offset(np.pi / 2)  # Start from top
ax.set_theta_direction(-1)  # Clockwise

# Color scheme for configurations
color_L1 = '#7CB342'  # Green
color_L2 = '#AB47BC'  # Purple
color_L3 = '#42A5F5'  # Blue

# Plot filled areas (radar shapes) for each configuration
# Layer 1: L1 (Green - lowest coverage)
ax.fill(angles_smooth_L1, coverage_smooth_L1,
       color=color_L1, alpha=0.25, linewidth=0, zorder=1)
ax.plot(angles_smooth_L1, coverage_smooth_L1,
       color=color_L1, linewidth=2.5, alpha=0.8, zorder=4)

# Layer 2: L2 (Purple - medium coverage)
ax.fill(angles_smooth_L2, coverage_smooth_L2,
       color=color_L2, alpha=0.25, linewidth=0, zorder=2)
ax.plot(angles_smooth_L2, coverage_smooth_L2,
       color=color_L2, linewidth=2.5, alpha=0.8, zorder=5)

# Layer 3: L3 (Blue - highest coverage)
ax.fill(angles_smooth_L3, coverage_smooth_L3,
       color=color_L3, alpha=0.25, linewidth=0, zorder=3)
ax.plot(angles_smooth_L3, coverage_smooth_L3,
       color=color_L3, linewidth=2.5, alpha=0.8, zorder=6)

# Normalize bubble sizes based on coverage values
def normalize_bubble_size(values, min_size=80, max_size=400):
    """Map coverage values (0-1) to bubble sizes"""
    # Values are already 0-1, so just scale
    return values * (max_size - min_size) + min_size

# Plot bubbles for each configuration at their respective positions
# Bubbles show individual data points with size = coverage value

# L1 bubbles (Green)
bubble_sizes_L1 = normalize_bubble_size(coverage_values_L1)
scatter_L1 = ax.scatter(angles, coverage_L1,
                       s=bubble_sizes_L1,
                       c=color_L1, alpha=0.7, edgecolors='white',
                       linewidths=2, zorder=7)

# L2 bubbles (Purple)
bubble_sizes_L2 = normalize_bubble_size(coverage_values_L2)
scatter_L2 = ax.scatter(angles, coverage_L2,
                       s=bubble_sizes_L2,
                       c=color_L2, alpha=0.7, edgecolors='white',
                       linewidths=2, zorder=8)

# L3 bubbles (Blue)
bubble_sizes_L3 = normalize_bubble_size(coverage_values_L3)
scatter_L3 = ax.scatter(angles, coverage_L3,
                       s=bubble_sizes_L3,
                       c=color_L3, alpha=0.7, edgecolors='white',
                       linewidths=2, zorder=9)

# Configure radial axis (0.0 to 1.0 scale)
ax.set_ylim(0, 1.0)
ax.set_yticks([0.33, 0.67, 1.0])
ax.set_yticklabels(['0.33', '0.67', '1.00'], fontsize=9, color='#666666')

# Configure angular axis (province labels)
ax.set_xticks(angles)
ax.set_xticklabels(provinces, fontsize=9, color='#333333')
ax.tick_params(axis='x', pad=10)

# Grid styling
ax.grid(True, linestyle='-', linewidth=0.8, color='#CCCCCC', alpha=0.5, zorder=0)
ax.spines['polar'].set_linewidth(2.0)
ax.spines['polar'].set_color('#333333')

# Set background
fig.patch.set_facecolor('#F8F8F8')
ax.set_facecolor('white')

# Add center text
ax.text(0, 0, 'Coverage\nAnalysis',
       ha='center', va='center', fontsize=14,
       fontweight='bold', color='#333333',
       transform=ax.transData,
       bbox=dict(boxstyle='round,pad=0.6', facecolor='white',
                edgecolor='#CCCCCC', linewidth=1.5, alpha=0.95))

# Create custom legends
# Legend 1: Configuration types (colored patches)
legend_elements_config = [
    mpatches.Patch(facecolor=color_L3, edgecolor='none', alpha=0.7, label='L3'),
    mpatches.Patch(facecolor=color_L2, edgecolor='none', alpha=0.7, label='L2'),
    mpatches.Patch(facecolor=color_L1, edgecolor='none', alpha=0.7, label='L1'),
]

legend1 = ax.legend(handles=legend_elements_config,
                   loc='upper right', bbox_to_anchor=(1.20, 1.05),
                   frameon=True, fancybox=False, shadow=False,
                   title='Configuration', title_fontsize=11, fontsize=10,
                   edgecolor='#999999', framealpha=1.0, facecolor='white')

# Legend 2: Coverage value (bubble size)
legend_elements_coverage = [
    Line2D([0], [0], marker='o', color='w',
          markerfacecolor='#888888', markeredgecolor='white',
          markersize=16, markeredgewidth=2, label='0.8'),
    Line2D([0], [0], marker='o', color='w',
          markerfacecolor='#888888', markeredgecolor='white',
          markersize=12, markeredgewidth=2, label='0.5'),
    Line2D([0], [0], marker='o', color='w',
          markerfacecolor='#888888', markeredgecolor='white',
          markersize=8, markeredgewidth=2, label='0.2'),
]

legend2 = ax.legend(handles=legend_elements_coverage,
                   loc='upper right', bbox_to_anchor=(1.20, 0.75),
                   frameon=True, fancybox=False, shadow=False,
                   title='Coverage Value', title_fontsize=11, fontsize=10,
                   edgecolor='#999999', framealpha=1.0, facecolor='white')

# Add first legend back
ax.add_artist(legend1)

# Adjust layout
plt.tight_layout()

# Save outputs
script_dir = os.path.dirname(os.path.abspath(__file__))
svg_path = os.path.join(script_dir, 'polar_coverage_chart.svg')
png_path = os.path.join(script_dir, 'polar_coverage_chart.png')

plt.savefig(svg_path, format='svg', dpi=300, bbox_inches='tight',
           facecolor='#F8F8F8', edgecolor='none')
print(f"[OK] Polar coverage chart saved as '{svg_path}'")

plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight',
           facecolor='#F8F8F8', edgecolor='none')
print(f"[OK] Preview PNG saved as '{png_path}'")

print("\n" + "="*70)
print("CHART INTERPRETATION GUIDE:")
print("="*70)
print("\n[1] COORDINATE SYSTEM (Polar/Radial)")
print("    • Each ray = One category (province)")
print("    • Radial distance = Coverage value (0.0 to 1.0)")
print("    • Outer ring = Higher coverage")
print("\n[2] BUBBLES (Scatter Points)")
print("    • Size = Coverage value (larger = higher coverage)")
print("    • Color = Configuration type (L1=Green, L2=Purple, L3=Blue)")
print("    • Position = Specific coverage for that province & configuration")
print("\n[3] FILLED AREAS (Radar Shapes)")
print("    • Color regions show overall coverage pattern per configuration")
print("    • Larger area = Better overall coverage")
print("    • Shape reveals which provinces have strong/weak coverage")
print("\n[4] HOW TO READ:")
print("    ► To check a specific province:")
print("      - Find the ray for that province")
print("      - Look at bubble size & color on that ray")
print("      - Example: ZJ (Zhejiang) has large blue bubble → L3 has high coverage")
print("\n    ► To compare configurations:")
print("      - Compare the extent of colored areas")
print("      - L3 (blue) extends furthest → best overall coverage")
print("      - L1 (green) smaller area → lower coverage")
print("\n    ► To find outliers:")
print("      - Look for unusually large/small bubbles")
print("      - Check if certain provinces lag behind in all configurations")
print("="*70)

plt.show()
