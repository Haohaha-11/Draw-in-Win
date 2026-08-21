"""
Multi-dimensional Polar Bubble Chart for Time-Series Geographic Data Visualization

This chart type is ideal for displaying:
1. Multiple categories (e.g., provinces, regions, forest types) around the circle
2. Time-series data (e.g., 2000, 2010, 2020) as concentric rings
3. Primary metric (e.g., Grain Yield) as radial distance
4. Secondary metric (e.g., Planting Area) as bubble size

Key Features:
- Clear visualization of temporal trends across multiple categories
- Intuitive comparison between different time periods
- Bubble size provides additional quantitative dimension
- Smooth curves reveal patterns and outliers
- Publication-ready aesthetic for academic papers

Use Cases:
- Agricultural data: Crop yield and planting area by province over time
- Environmental data: Forest coverage and biodiversity by region
- Economic data: GDP and population by country across decades
- Climate data: Temperature and precipitation by latitude bands
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
from scipy.interpolate import make_interp_spline
from scipy.ndimage import gaussian_filter1d
import matplotlib.patches as mpatches
import os

# Set global font to serif (Times New Roman style)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 2

# Define regions (30 Chinese province abbreviations)
regions = [
    'NX', 'BJ', 'TJ', 'HE', 'SX', 'NM', 'LN', 'JL', 'HL',
    'SH', 'JS', 'ZJ', 'AH', 'FJ', 'JX', 'SD', 'HA', 'HB',
    'HN', 'GD', 'GX', 'HI', 'CQ', 'SC', 'GZ', 'YN', 'XZ',
    'SN', 'GS', 'QH', 'XJ'
]

n_regions = len(regions)
angles = np.linspace(0, 2 * np.pi, n_regions, endpoint=False)

# Generate simulated data - Each year's data distributed around fixed radii
# This simulates real-world geographic data with natural variation
np.random.seed(42)

# DESIGN PRINCIPLE:
# - Each time period (year) has a base radius corresponding to grid circles
# - Data points vary around this base to show regional differences
# - Variation amplitude creates organic, realistic patterns

# Year 2000: Data points around radius ~2000 (earliest time period)
base_radius_2000 = 2000
variation_2000 = np.random.uniform(-400, 400, n_regions)  # Regional variation
grain_yield_2000_raw = base_radius_2000 + variation_2000
# Smooth to create realistic geographic patterns (neighboring regions similar)
grain_yield_2000 = gaussian_filter1d(grain_yield_2000_raw, sigma=3, mode='wrap')
grain_yield_2000 = np.clip(grain_yield_2000, 1600, 2400)
# Secondary metric (bubble size): varies independently
planting_area_2000 = np.random.uniform(2000, 3500, n_regions)

# Year 2010: Data points around radius ~4000 (middle time period)
base_radius_2010 = 4000
variation_2010 = np.random.uniform(-500, 500, n_regions)
grain_yield_2010_raw = base_radius_2010 + variation_2010
grain_yield_2010 = gaussian_filter1d(grain_yield_2010_raw, sigma=3, mode='wrap')
grain_yield_2010 = np.clip(grain_yield_2010, 3500, 4500)
planting_area_2010 = np.random.uniform(3500, 5000, n_regions)

# Year 2020: Data points around radius ~6000 (latest time period)
base_radius_2020 = 6000
variation_2020 = np.random.uniform(-600, 600, n_regions)
grain_yield_2020_raw = base_radius_2020 + variation_2020
grain_yield_2020 = gaussian_filter1d(grain_yield_2020_raw, sigma=3, mode='wrap')
grain_yield_2020 = np.clip(grain_yield_2020, 5400, 6600)
planting_area_2020 = np.random.uniform(5000, 7000, n_regions)

# Create smooth curves using spline interpolation for organic "flower petal" shape
def smooth_polar_curve(angles, radii, smoothness=300):
    """
    Create smooth interpolated curve for polar plot
    Returns smoothed angles and radii
    """
    # Close the loop by appending first point (ensure exact match for periodic)
    angles_extended = np.concatenate([angles, [angles[0]]])
    radii_extended = np.concatenate([radii, [radii[0]]])

    # Create parameter for interpolation
    t = np.linspace(0, 1, len(angles_extended))
    t_smooth = np.linspace(0, 1, smoothness)

    # Use cubic spline interpolation without periodic constraint
    # Instead, manually ensure closure
    spline = make_interp_spline(t, radii_extended, k=3)
    radii_smooth = spline(t_smooth)

    # Corresponding smooth angles
    angles_smooth = np.linspace(0, 2 * np.pi, smoothness, endpoint=True)

    return angles_smooth, radii_smooth

# Generate smooth curves for all three years
angles_smooth_2000, yield_smooth_2000 = smooth_polar_curve(angles, grain_yield_2000)
angles_smooth_2010, yield_smooth_2010 = smooth_polar_curve(angles, grain_yield_2010)
angles_smooth_2020, yield_smooth_2020 = smooth_polar_curve(angles, grain_yield_2020)

# Create figure with polar projection
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='polar')

# Color scheme: Progressive blue gradient representing time progression
# Lighter colors for earlier years, darker for recent years
color_2000 = '#A8D8EA'  # Light cyan blue (Past)
color_2010 = '#5DADE2'  # Medium blue (Transition)
color_2020 = '#2E86AB'  # Deep blue (Present)

# Plot smooth filled areas and contour lines for each year
# Visual hierarchy: All layers visible through transparency

# Layer 1: 2000 (Inner ring - earliest data)
ax.fill(angles_smooth_2000, yield_smooth_2000,
       color=color_2000, alpha=0.35, linewidth=0, zorder=1,
       label='2000 (filled area)')
ax.plot(angles_smooth_2000, yield_smooth_2000,
       color=color_2000, linewidth=2.5, alpha=0.85, zorder=4,
       label='2000 (outline)')

# Layer 2: 2010 (Middle ring - intermediate data)
ax.fill(angles_smooth_2010, yield_smooth_2010,
       color=color_2010, alpha=0.35, linewidth=0, zorder=2)
ax.plot(angles_smooth_2010, yield_smooth_2010,
       color=color_2010, linewidth=2.5, alpha=0.85, zorder=5)

# Layer 3: 2020 (Outer ring - latest data)
ax.fill(angles_smooth_2020, yield_smooth_2020,
       color=color_2020, alpha=0.35, linewidth=0, zorder=3)
ax.plot(angles_smooth_2020, yield_smooth_2020,
       color=color_2020, linewidth=2.5, alpha=0.85, zorder=6)

# Normalize bubble sizes for planting area (secondary metric visualization)
def normalize_size(area, min_size=50, max_size=300):
    """
    Normalize area values to bubble sizes for visual clarity
    Larger bubbles = higher secondary metric value
    """
    area_min, area_max = area.min(), area.max()
    normalized = (area - area_min) / (area_max - area_min)
    return normalized * (max_size - min_size) + min_size

# Plot scatter points for ALL THREE YEARS at their respective positions
# KEY INSIGHT: Bubble size adds a 4th dimension to the visualization

# 2000: Bubbles on inner ring (smallest overall, representing early development)
scatter_2000 = ax.scatter(angles, grain_yield_2000,
                         s=normalize_size(planting_area_2000, min_size=60, max_size=250),
                         c=color_2000, alpha=0.8, edgecolors='white',
                         linewidths=1.5, zorder=7)

# 2010: Bubbles on middle ring (medium size, showing growth)
scatter_2010 = ax.scatter(angles, grain_yield_2010,
                         s=normalize_size(planting_area_2010, min_size=70, max_size=280),
                         c=color_2010, alpha=0.8, edgecolors='white',
                         linewidths=1.5, zorder=8)

# 2020: Bubbles on outer ring (largest, indicating recent expansion)
scatter_2020 = ax.scatter(angles, grain_yield_2020,
                         s=normalize_size(planting_area_2020, min_size=80, max_size=320),
                         c=color_2020, alpha=0.8, edgecolors='white',
                         linewidths=1.5, zorder=9)

# Configure radial axis (R-axis) with donut hole
# Grid circles at 2000, 4000, 6000 (the base radii for each year)
ax.set_rorigin(-800)  # Create hollow center
ax.set_ylim(0, 7000)
ax.set_yticks([2000, 4000, 6000])
ax.set_yticklabels(['2000', '4000', '6000'], fontsize=9, color='#666666')

# Configure angular axis (theta-axis) - region labels OUTSIDE the circle
ax.set_xticks(angles)
ax.set_xticklabels(regions, fontsize=9, color='#333333')
ax.tick_params(axis='x', pad=15)  # Push labels outward

# Grid styling - Light grey circular grid lines
ax.grid(True, linestyle='-', linewidth=0.8, color='#CCCCCC', alpha=0.5, zorder=0)
ax.spines['polar'].set_linewidth(2.5)
ax.spines['polar'].set_color('black')  # Black outer circle

# Ensure radial grid lines are visible at 2000, 4000, 6000
ax.set_rgrids([2000, 4000, 6000], angle=90, fontsize=9, color='#666666')

# Add center text in the donut hole - clearly label the primary metric
ax.text(0, 0, 'Grain Yield\n(10k tons)',
       ha='center', va='center', fontsize=13,
       fontweight='bold', color='#333333',
       transform=ax.transData,
       bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                edgecolor='none', alpha=0.8))

# Create custom legends (RIGHT SIDE) - matching target image style
# Legend 1: Planting Area (bubble size) - FILLED CIRCLES
legend_elements_area = [
    Line2D([0], [0], marker='o', color='w',
          markerfacecolor='#5DADE2', markeredgecolor='white',
          markersize=14, markeredgewidth=1.5, label='6000'),
    Line2D([0], [0], marker='o', color='w',
          markerfacecolor='#5DADE2', markeredgecolor='white',
          markersize=11, markeredgewidth=1.5, label='4000'),
    Line2D([0], [0], marker='o', color='w',
          markerfacecolor='#5DADE2', markeredgecolor='white',
          markersize=8, markeredgewidth=1.5, label='2000'),
]

legend1 = ax.legend(handles=legend_elements_area,
                   loc='upper right', bbox_to_anchor=(1.22, 1.05),
                   frameon=True, fancybox=False, shadow=False,
                   title='Planting Area (Kha)', title_fontsize=10, fontsize=9,
                   edgecolor='#CCCCCC', framealpha=1.0, facecolor='white')

# Legend 2: Year colors - COLORED SQUARES
legend_elements_year = [
    mpatches.Patch(color=color_2020, label='2020'),
    mpatches.Patch(color=color_2010, label='2010'),
    mpatches.Patch(color=color_2000, label='2000'),
]

legend2 = ax.legend(handles=legend_elements_year,
                   loc='upper right', bbox_to_anchor=(1.22, 0.75),
                   frameon=True, fancybox=False, shadow=False,
                   title='Year', title_fontsize=10, fontsize=9,
                   edgecolor='#CCCCCC', framealpha=1.0, facecolor='white')

# Add first legend back (matplotlib removes previous legend by default)
ax.add_artist(legend1)

# Set background - light grey like target image
fig.patch.set_facecolor('#F5F5F5')
ax.set_facecolor('white')

# Adjust layout
plt.tight_layout()

# Save as SVG (vector format)
script_dir = os.path.dirname(os.path.abspath(__file__))
svg_path = os.path.join(script_dir, 'grain_polar_bubble.svg')
png_path = os.path.join(script_dir, 'grain_polar_bubble.png')

plt.savefig(svg_path, format='svg', dpi=300, bbox_inches='tight',
           facecolor='white', edgecolor='none')
print(f"[OK] Polar bubble chart saved as '{svg_path}'")

plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight',
           facecolor='white', edgecolor='none')
print(f"[OK] Preview PNG saved as '{png_path}'")

plt.show()


# Save outputs
plt.savefig(svg_path, format='svg', dpi=300, bbox_inches='tight',
           facecolor='white', edgecolor='none')
print(f"[OK] Polar bubble chart saved as '{svg_path}'")

plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight',
           facecolor='white', edgecolor='none')
print(f"[OK] Preview PNG saved as '{png_path}'")

print("\n" + "="*60)
print("CHART INTERPRETATION GUIDE:")
print("="*60)
print("• Angular Position: Different categories (provinces/regions)")
print("• Radial Distance: Primary metric value (Grain Yield)")
print("• Concentric Rings: Time periods (2000, 2010, 2020)")
print("• Bubble Size: Secondary metric (Planting Area)")
print("• Color Gradient: Time progression (light→dark = past→present)")
print("\nKEY INSIGHTS:")
print("• Compare same category across time: Follow radial line outward")
print("• Compare categories in same period: Follow circular ring")
print("• Identify outliers: Look for unusually large/small bubbles")
print("• Spot trends: Observe if outer rings are consistently higher")
print("="*60)

plt.show()
