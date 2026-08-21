import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as mcolors

# Set style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10

# Generate synthetic wavy data for 7 groups over 10 time points
np.random.seed(42)
time_points = 10
n_groups = 7

# Create drawing order (group names)
drawing_order = [f'Group{i+1}' for i in range(n_groups)]

# Create synthetic data
data_dict = {'Count': list(range(time_points))}
for i in range(n_groups):
    base = 20 + i * 5
    wave = base + 10 * np.sin(np.arange(time_points) * 0.8 + i * 0.5) + np.random.randn(time_points) * 2
    data_dict[drawing_order[i]] = wave

data = pd.DataFrame(data_dict)

# Use plasma color scheme
plasma_colors = cm.plasma(np.linspace(0, 1, len(drawing_order)))
colors = {drawing_order[i]: tuple(plasma_colors[i]) for i in range(len(drawing_order))}

# Get x values
x_values = data['Count'].values

# Create figure and 3D axis
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Initialize legend patches list
legend_patches = []

# Plot each group
for i, y_label in enumerate(reversed(drawing_order)):
    color = colors[y_label]
    z_values = data[y_label].values
    x_valid = x_values
    z_valid = z_values

    # Get y position for this group
    y_val = drawing_order.index(y_label)
    y_points = np.full_like(x_valid, y_val)

    # Draw line and scatter points
    ax.plot(x_valid, y_points, z_valid, color=color, alpha=1, linewidth=1.5)
    ax.scatter(x_valid, y_points, z_valid, color=color, marker='o', s=20)

    # Add data labels at every other point
    for x, y, z in zip(x_valid, y_points, z_valid):
        if int(x) % 2 == 1:
            label = f'{z:.1f}' if isinstance(z, float) else str(z)
            ax.text(x, y, z + 0.5, label, ha='center', va='bottom', fontsize=8)

    # Create 3D polygon for waterfall effect
    verts = [list(zip(x_valid, y_points, z_valid)),
             list(zip(x_valid, y_points, np.zeros_like(z_valid)))]
    poly = Poly3DCollection([verts[0] + verts[1][::-1]], alpha=0.25)
    poly.set_color(color)
    ax.add_collection3d(poly)

    # Add to legend
    legend_patches.append(plt.Line2D([0], [0], color=color, lw=2, label=y_label))

# Add legend
ax.legend(handles=legend_patches,
          loc='upper right',
          fontsize=10,
          frameon=True,
          shadow=False,
          fancybox=True,
          framealpha=0.8)

# Set axis labels and title
ax.set_xlabel('Count')
ax.set_ylabel('Groups')
ax.set_zlabel('Values')
ax.set_title('3D Waterfall Chart of Groups', fontdict={'size': 20})

# Set y-axis ticks to show group names
ax.set_yticks(range(len(drawing_order)))
ax.set_yticklabels(drawing_order)

# Set axis limits with margin
margin = 0.1
x_min, x_max = min(x_values), max(x_values)
y_min, y_max = 0, len(drawing_order) - 1
z_min, z_max = 0, data[drawing_order].values.max() * 1.1

ax.set_xlim(x_min - margin, x_max + margin)
ax.set_ylim(y_min - margin, y_max + margin)
ax.set_zlim(z_min, z_max)

# Set viewing angle
ax.view_init(elev=30, azim=-35)

# Adjust layout
plt.tight_layout()

# Save as SVG (in the same directory as the script)
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
svg_path = os.path.join(script_dir, 'output.svg')
png_path = os.path.join(script_dir, 'output.png')

plt.savefig(svg_path, format='svg', dpi=300, bbox_inches='tight')
print(f"3D Waterfall Chart saved as '{svg_path}'")

# Also save as PNG for preview
plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight')
print(f"Preview PNG also saved as '{png_path}'")

plt.show()
