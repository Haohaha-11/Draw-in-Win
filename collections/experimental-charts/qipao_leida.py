import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from matplotlib.patches import Circle
import matplotlib.font_manager as fm

# Set up Chinese provinces in clockwise order
provinces = ['BJ', 'TJ', 'HE', 'SX', 'IM', 'LN', 'JL', 'HL', 'SH', 'JS',
             'ZJ', 'AH', 'FJ', 'JX', 'SD', 'HA', 'HB', 'HN', 'GD', 'GX',
             'HI', 'CQ', 'SC', 'GZ', 'YN', 'XZ', 'SN', 'GS', 'QH', 'NX', 'XJ']

n_provinces = len(provinces)

# Generate realistic grain yield data (10k tons)
np.random.seed(42)
year_2000 = np.random.uniform(2000, 5000, n_provinces)
year_2010 = year_2000 + np.random.uniform(500, 1500, n_provinces)
year_2020 = year_2010 + np.random.uniform(500, 1500, n_provinces)

# Ensure values are within reasonable range
year_2020 = np.clip(year_2020, 1000, 7000)
year_2010 = np.clip(year_2010, 1000, 6500)

# Set up angles for polar plot
angles = np.linspace(0, 2 * np.pi, n_provinces, endpoint=False)

# Create figure
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='polar')

# Configure polar plot
ax.set_theta_zero_location('N')  # Start from top
ax.set_theta_direction(-1)  # Clockwise

# Set radial limits with inner hole
inner_radius = 1000
outer_radius = 7000
ax.set_ylim(0, outer_radius)

# Remove default grid
ax.grid(False)
ax.set_yticks([])

# Draw custom concentric circles (grid lines)
grid_values = [2000, 4000, 6000]
for grid_val in grid_values:
    # Make the outermost circle thicker
    if grid_val == 6000:
        linewidth = 2.5
        alpha = 0.8
    else:
        linewidth = 0.8
        alpha = 0.5

    circle = Circle((0, 0), grid_val, transform=ax.transData._b,
                   fill=False, edgecolor='gray', linewidth=linewidth,
                   linestyle='--', alpha=alpha, zorder=1)
    ax.add_patch(circle)

# Add radial grid lines from center to each province
for angle in angles:
    ax.plot([angle, angle], [inner_radius, outer_radius],
           color='lightgray', linewidth=0.6, linestyle='-',
           alpha=0.4, zorder=1)

# Add background bubbles at grid intersections
bubble_color = '#6B8CAE'  # Slate blue
for angle in angles:
    for grid_val in grid_values:
        # Vary bubble size based on grid value
        size = 50 + (grid_val / 6000) * 100
        ax.scatter(angle, grid_val, s=size, c=bubble_color,
                  alpha=0.3, zorder=2, edgecolors='none')

# Function to smooth polar data with spline interpolation
def smooth_polar_data(angles, values, n_points=300):
    # Close the loop
    angles_closed = np.concatenate([angles, [angles[0]]])
    values_closed = np.concatenate([values, [values[0]]])

    # Create parameter for interpolation
    t = np.linspace(0, 1, len(angles_closed))
    t_smooth = np.linspace(0, 1, n_points)

    # Spline interpolation
    spl = make_interp_spline(t, values_closed, k=3)
    values_smooth = spl(t_smooth)

    # Corresponding angles
    angles_smooth = np.linspace(0, 2 * np.pi, n_points)

    return angles_smooth, values_smooth

# Plot data for each year with smooth curves
years_data = [
    (year_2000, 'Year 2000', '#7FCDCD', 0.4),  # Light cyan
    (year_2010, 'Year 2010', '#4A90E2', 0.5),  # Sky blue
    (year_2020, 'Year 2020', '#1E3A8A', 0.6),  # Deep ocean blue
]

for data, label, color, alpha in years_data:
    angles_smooth, values_smooth = smooth_polar_data(angles, data)
    ax.fill(angles_smooth, values_smooth, color=color, alpha=alpha,
           label=label, zorder=3)
    ax.plot(angles_smooth, values_smooth, color=color, linewidth=1.5,
           alpha=0.8, zorder=4)

# Add white circle in center (donut hole)
center_circle = Circle((0, 0), inner_radius, transform=ax.transData._b,
                       facecolor='white', edgecolor='none', zorder=10)
ax.add_patch(center_circle)

# Add center text
ax.text(0, 0, 'Grain Yield\n(10k tons)',
       ha='center', va='center', fontsize=16,
       fontfamily='serif', weight='bold', zorder=11)

# Add province labels
ax.set_xticks(angles)
ax.set_xticklabels(provinces, fontsize=10, weight='bold')

# Rotate labels to be readable
for label, angle in zip(ax.get_xticklabels(), angles):
    angle_deg = np.degrees(angle)
    if angle_deg > 90 and angle_deg < 270:
        label.set_rotation(angle_deg + 180)
        label.set_ha('right')
    else:
        label.set_rotation(angle_deg)
        label.set_ha('left')

# Remove spines
ax.spines['polar'].set_visible(False)

# Create custom legend
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

legend_elements = []

# Add year legend items
for data, label, color, alpha in reversed(years_data):
    legend_elements.append(Rectangle((0, 0), 1, 1, fc=color,
                                    alpha=alpha, label=label))

# Add planting area (bubble size) legend
for grid_val in grid_values:
    size = 50 + (grid_val / 6000) * 100
    legend_elements.append(Line2D([0], [0], marker='o', color='w',
                                 markerfacecolor=bubble_color,
                                 markersize=np.sqrt(size)/3,
                                 alpha=0.3, label=f'Grid: {grid_val}'))

ax.legend(handles=legend_elements, loc='upper left',
         bbox_to_anchor=(1.15, 1.0), frameon=True,
         fontsize=10, title='Legend')

# Adjust layout
plt.tight_layout()

# Save as SVG (in the same directory as the script)
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, 'grain_yield_chart.svg')
plt.savefig(output_path, format='svg', bbox_inches='tight', dpi=300)

print(f"Chart saved as {output_path}")
plt.show()
