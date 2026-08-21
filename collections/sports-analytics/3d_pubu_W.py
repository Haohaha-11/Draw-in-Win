import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as mcolors
import matplotlib.font_manager as fm
import os

# Load Times New Roman font
script_dir = os.path.dirname(os.path.abspath(__file__))
font_path = fm.findfont('DejaVu Serif')
times_font = fm.FontProperties(fname=font_path)

# Set style
plt.rcParams['font.family'] = times_font.get_name()
plt.rcParams['font.size'] = 10

# Load data
data_path = os.path.join(script_dir, 'wpc.csv')
df = pd.read_csv(data_path)

# Get unique policies (strategies) and rename them
policies = df['policy'].unique()

# Create policy name mapping
policy_mapping = {
    'Model(MPC)': 'Ours',
    'Baseline-Zero': 'Laissez-faire',
    'Baseline-MaxXL': 'Aggressive',
    'Baseline-Random': 'Random',
    'Baseline-Random2': 'Random2',
    'Baseline-Random3': 'Random3'
}

# Apply mapping to dataframe
df['policy_display'] = df['policy'].map(policy_mapping)
policies_display = [policy_mapping.get(p, p) for p in policies]

# Prepare data for W indicator
data_dict = {'Season': sorted(df['season'].unique())}
for i, policy in enumerate(policies):
    policy_data = df[df['policy'] == policy].sort_values('season')
    data_dict[policies_display[i]] = policy_data['W'].values

data = pd.DataFrame(data_dict)

# Use custom color scheme
custom_colors = ['#16058b', '#6200aa', '#9e169d', '#cc4a74', '#eb7852', '#fcb431']
colors = {}
for i, policy in enumerate(policies_display):
    hex_color = custom_colors[i]
    # Convert hex to RGB tuple (0-1 range)
    rgb = tuple(int(hex_color.lstrip('#')[j:j+2], 16)/255 for j in (0, 2, 4))
    colors[policy] = rgb

# Define text colors (black for all labels)
text_colors = {policy: (0, 0, 0) for policy in policies_display}

# Get x values (seasons)
x_values = data['Season'].values

# Create figure and 3D axis
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Initialize legend patches list
legend_patches = []

# Plot each policy
for i, policy in enumerate(reversed(list(policies_display))):
    color = colors[policy]
    z_values = data[policy].values
    x_valid = x_values
    z_valid = z_values

    # Get y position for this policy
    y_val = list(policies_display).index(policy)
    y_points = np.full_like(x_valid, y_val, dtype=float)

    # Draw line and scatter points
    ax.plot(x_valid, y_points, z_valid, color=color, alpha=1, linewidth=2)
    ax.scatter(x_valid, y_points, z_valid, color=color, marker='o', s=40)

    # Add data labels at each point (with adjusted spacing to avoid overlap)
    for j, (x, y, z) in enumerate(zip(x_valid, y_points, z_valid)):
        label = f'{z:.2f}'
        # Adjust vertical offset based on position to reduce overlap
        offset = 0.03 if j % 2 == 0 else 0.04
        text_color = text_colors[policy]
        ax.text(x, y, z + offset, label, ha='center', va='bottom',
                fontsize=11, fontproperties=times_font, color=text_color, fontweight='bold')

    # Create 3D polygon for waterfall effect
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
          framealpha=0.8,
          prop=times_font)

# Set y-axis ticks to show policy names
# Set y-axis ticks to show policy names
ax.set_yticks(range(len(policies_display)))
ax.set_yticklabels(policies_display, fontsize=7, fontproperties=times_font)

# Set axis limits with margin
margin = 0.1
x_min, x_max = min(x_values), max(x_values)
y_min, y_max = 0, len(policies_display) - 1
z_min = 0
z_max = data[list(policies_display)].values.max() * 1.15

ax.set_xlim(x_min - margin, x_max + margin)
ax.set_ylim(y_min - margin, y_max + margin)
ax.set_zlim(z_min, z_max)

# Set viewing angle
ax.view_init(elev=25, azim=-45)

# Adjust layout
plt.tight_layout()

# Save outputs
svg_path = os.path.join(script_dir, '3d_waterfall_W.svg')
png_path = os.path.join(script_dir, '3d_waterfall_W.png')

plt.savefig(svg_path, format='svg', dpi=300, bbox_inches='tight')
print(f"W indicator 3D Waterfall Chart saved as '{svg_path}'")

plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight')
print(f"Preview PNG also saved as '{png_path}'")

plt.show()
