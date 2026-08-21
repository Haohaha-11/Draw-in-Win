import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as mcolors
import os

# Set style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10

# Load data
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, 'wpc.csv')
df = pd.read_csv(data_path)

# Get unique policies (strategies)
policies = df['policy'].unique()

# Prepare data for C indicator
data_dict = {'Season': sorted(df['season'].unique())}
for policy in policies:
    policy_data = df[df['policy'] == policy].sort_values('season')
    data_dict[policy] = policy_data['C'].values

data = pd.DataFrame(data_dict)

# Use plasma color scheme
plasma_colors = cm.plasma(np.linspace(0, 1, len(policies)))
colors = {policies[i]: tuple(plasma_colors[i]) for i in range(len(policies))}

# Get x values (seasons)
x_values = data['Season'].values

# Create figure and 3D axis
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Initialize legend patches list
legend_patches = []

# Get z range for proper scaling
z_min_data = data[list(policies)].values.min()
z_max_data = data[list(policies)].values.max()

# Plot each policy
for i, policy in enumerate(reversed(list(policies))):
    color = colors[policy]
    z_values = data[policy].values
    x_valid = x_values
    z_valid = z_values

    # Get y position for this policy
    y_val = list(policies).index(policy)
    y_points = np.full_like(x_valid, y_val, dtype=float)

    # Draw line and scatter points
    ax.plot(x_valid, y_points, z_valid, color=color, alpha=1, linewidth=2)
    ax.scatter(x_valid, y_points, z_valid, color=color, marker='o', s=40)

    # Add data labels at each point (with adjusted spacing to avoid overlap)
    for j, (x, y, z) in enumerate(zip(x_valid, y_points, z_valid)):
        label = f'{z:.2f}'
        # Adjust vertical offset based on position to reduce overlap
        offset = 0.1 if z >= 0 else -0.15
        ax.text(x, y, z + offset, label, ha='center', va='bottom' if z >= 0 else 'top',
                fontsize=9, fontweight='bold')

    # Create 3D polygon for waterfall effect (from z=0 baseline)
    verts = [list(zip(x_valid, y_points, z_valid)),
             list(zip(x_valid, y_points, np.zeros_like(z_valid)))]
    poly = Poly3DCollection([verts[0] + verts[1][::-1]], alpha=0.25)
    poly.set_color(color)
    ax.add_collection3d(poly)

    # Add to legend
    legend_patches.append(plt.Line2D([0], [0], color=color, lw=2, label=policy))

# Add legend
ax.legend(handles=legend_patches,
          loc='upper left',
          fontsize=8,
          frameon=True,
          shadow=False,
          fancybox=True,
          framealpha=0.8)

# Set axis labels and title
ax.set_xlabel('Season', fontsize=12)
ax.set_ylabel('Policy', fontsize=12)
ax.set_zlabel('C Score', fontsize=12)
ax.set_title('3D Waterfall Chart - C Indicator', fontdict={'size': 16, 'weight': 'bold'})

# Set y-axis ticks to show policy names
ax.set_yticks(range(len(policies)))
ax.set_yticklabels(policies, fontsize=7)

# Set axis limits with margin (handle negative values)
margin = 0.1
x_min, x_max = min(x_values), max(x_values)
y_min, y_max = 0, len(policies) - 1
z_min = z_min_data - abs(z_min_data) * 0.1 if z_min_data < 0 else 0
z_max = z_max_data * 1.1 if z_max_data > 0 else z_max_data * 0.9

ax.set_xlim(x_min - margin, x_max + margin)
ax.set_ylim(y_min - margin, y_max + margin)
ax.set_zlim(z_min, z_max)

# Add a horizontal plane at z=0 for reference
xx, yy = np.meshgrid([x_min - margin, x_max + margin],
                      [y_min - margin, y_max + margin])
zz = np.zeros_like(xx)
ax.plot_surface(xx, yy, zz, alpha=0.1, color='gray')

# Set viewing angle
ax.view_init(elev=25, azim=-45)

# Adjust layout
plt.tight_layout()

# Save outputs
svg_path = os.path.join(script_dir, '3d_waterfall_C.svg')
png_path = os.path.join(script_dir, '3d_waterfall_C.png')

plt.savefig(svg_path, format='svg', dpi=300, bbox_inches='tight')
print(f"C indicator 3D Waterfall Chart saved as '{svg_path}'")

plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight')
print(f"Preview PNG also saved as '{png_path}'")

plt.show()
