import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LinearRegression
import matplotlib.font_manager as fm
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']
plt.rcParams['axes.unicode_minus'] = False

# Generate sample data for three brands
np.random.seed(42)

# Pret data
pret_x = np.random.uniform(0.5, 3.5, 50)
pret_y = 2.3 * pret_x + np.random.normal(0, 0.4, 50) + 8.5

# Starbucks data
starbucks_x = np.random.uniform(0.8, 4.0, 50)
starbucks_y = 2.1 * starbucks_x + np.random.normal(0, 0.35, 50) + 8.8

# Costa data
costa_x = np.random.uniform(0.6, 3.8, 50)
costa_y = 1.9 * costa_x + np.random.normal(0, 0.45, 50) + 9.0

# Create figure with 1x3 subplots
fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=True)
fig.patch.set_facecolor('white')

# Brand configurations
brands = [
    {
        'name': 'Pret',
        'x': pret_x,
        'y': pret_y,
        'color': '#800000',  # Deep Maroon
        'fill_color': '#FFB6C1',  # Soft rose
        'ax': axes[0]
    },
    {
        'name': 'Starbucks',
        'x': starbucks_x,
        'y': starbucks_y,
        'color': '#1a5d38',  # Forest Green
        'fill_color': '#90EE90',  # Soft sage green
        'ax': axes[1]
    },
    {
        'name': 'Costa',
        'x': costa_x,
        'y': costa_y,
        'color': '#7b3f4d',  # Muted Burgundy
        'fill_color': '#D8BFD8',  # Soft lavender-gray
        'ax': axes[2]
    }
]

# Process each brand
for brand in brands:
    ax = brand['ax']
    x = brand['x']
    y = brand['y']

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    r_squared = r_value ** 2

    # Generate regression line
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = slope * x_line + intercept

    # Calculate confidence interval
    predict = slope * x + intercept
    residuals = y - predict
    std_residuals = np.std(residuals)

    # 95% confidence interval
    ci = 1.96 * std_residuals
    y_upper = slope * x_line + intercept + ci
    y_lower = slope * x_line + intercept - ci

    # Plot scatter points
    ax.scatter(x, y, c=brand['color'], s=30, alpha=0.7, edgecolors='none', zorder=3)

    # Plot regression line
    ax.plot(x_line, y_line, color=brand['color'], linewidth=2.5, zorder=4)

    # Plot confidence interval
    ax.fill_between(x_line, y_lower, y_upper, color=brand['fill_color'],
                     alpha=0.18, zorder=2)

    # Grid styling
    ax.grid(True, which='major', color='gray', alpha=0.2, linewidth=0.5, zorder=1)
    ax.grid(True, which='minor', color='gray', alpha=0.1, linewidth=0.3, zorder=1)
    ax.minorticks_on()

    # Set background
    ax.set_facecolor('white')

    # Labels
    ax.set_xlabel('log(Brand outlets per km²)', fontsize=11, fontweight='normal')
    if brand['name'] == 'Pret':
        ax.set_ylabel('log(Workplace earnings)', fontsize=11, fontweight='normal')

    # Annotation in top-left corner
    annotation_text = f"{brand['name']}\nSlope: {slope:.3f}\n$R^2$: {r_squared:.3f}"
    ax.text(0.05, 0.95, annotation_text,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='none'),
            fontweight='bold' if brand['name'] in annotation_text.split('\n')[0] else 'normal')

    # Spine styling
    for spine in ax.spines.values():
        spine.set_edgecolor('gray')
        spine.set_linewidth(0.8)

# Adjust layout
plt.tight_layout()

# Save as SVG in the same directory as the script
script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, 'xianxingnihe.svg')
plt.savefig(output_path, format='svg', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')

print(f"Figure saved to: {output_path}")
plt.show()
