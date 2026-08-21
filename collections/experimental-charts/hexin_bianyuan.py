"""
Core-Periphery Network Visualization (核心-边缘网络)
Radial hierarchical layout showing urban interaction network
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import networkx as nx
import numpy as np
import random

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Configure matplotlib for Chinese characters
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# Color palette (strictly following requirements)
COLORS = {
    'core': '#1f77b4',           # Deep Blue
    'secondary': '#b2df8a',      # Olive/Light Green
    'intermediate': '#a6cee3',   # Light Blue
    'periphery': '#006d2c',      # Dark Green
}

# Edge colors by connection type - Blue-Green alternating
EDGE_COLORS = {
    'core-secondary': '#1f77b4',      # Blue
    'core-intermediate': '#2ca02c',   # Green
    'secondary-intermediate': '#17becf',  # Cyan (Blue-Green)
    'secondary-periphery': '#1f77b4',     # Blue
    'intermediate-periphery': '#2ca02c',  # Green
    'periphery-periphery': '#7fcdbb'      # Light Blue-Green
}

# Node sizes
SIZES = {
    'core': 2000,
    'secondary': 800,
    'intermediate': 400,
    'periphery': 80  # Reduced size for periphery nodes
}

# 1. Create mock dataset with Chinese city names
cities = {
    'core': ['北京'],  # Beijing (Center)
    'secondary': ['上海', '广州', '深圳', '南京', '杭州', '成都', '武汉', '西安', '重庆', '天津'],  # Increased to 10 cities
    'intermediate': [
        '苏州', '郑州', '长沙', '沈阳', '青岛', '大连', '厦门', '宁波',
        '济南', '哈尔滨', '长春', '石家庄', '太原', '呼和浩特', '兰州', '银川',
        '西宁', '乌鲁木齐', '拉萨', '昆明', '贵阳', '南宁', '海口', '南昌'
    ],  # Increased to 24 cities
    'periphery': [
        '合肥', '福州', '温州', '无锡', '常州', '徐州', '扬州', '镇江',
        '泰州', '盐城', '淮安', '连云港', '宿迁', '嘉兴', '湖州', '绍兴',
        '金华', '衢州', '舟山', '台州', '丽水', '芜湖', '蚌埠', '淮南',
        '马鞍山', '淮北', '铜陵', '安庆', '黄山', '滁州', '阜阳', '宿州',
        '六安', '亳州', '池州', '宣城', '保定', '唐山', '秦皇岛', '邯郸',
        '邢台', '张家口', '承德', '沧州', '廊坊', '衡水', '包头', '鞍山',
        '抚顺', '本溪', '丹东', '锦州', '营口', '阜新', '辽阳', '盘锦',
        '铁岭', '朝阳', '葫芦岛', '吉林', '四平', '辽源', '通化', '白山',
        '松原', '白城', '延边', '齐齐哈尔', '鸡西', '鹤岗', '双鸭山', '大庆',
        '伊春', '佳木斯', '七台河', '牡丹江', '黑河', '绥化', '大兴安岭', '南通',
        '景德镇', '萍乡', '九江', '新余', '鹰潭', '赣州', '吉安', '宜春',
        '抚州', '上饶', '枣庄', '东营', '烟台', '潍坊', '济宁', '泰安',
        '威海', '日照', '临沂', '德州', '聊城', '滨州', '菏泽', '开封',
        '洛阳', '平顶山', '安阳', '鹤壁', '新乡', '焦作', '濮阳', '许昌',
        '漯河', '三门峡', '南阳', '商丘', '信阳', '周口', '驻马店', '黄石',
        '十堰', '宜昌', '襄阳', '鄂州', '荆门', '孝感', '荆州', '黄冈',
        '咸宁', '随州', '恩施', '仙桃', '潜江', '天门', '神农架', '株洲',
        '湘潭', '衡阳', '邵阳', '岳阳', '常德', '张家界', '益阳', '郴州',
        '永州', '怀化', '娄底', '湘西', '韶关', '珠海', '汕头', '佛山',
        '江门', '湛江', '茂名', '肇庆', '惠州', '梅州', '汕尾', '河源',
        '阳江', '清远', '东莞', '中山', '潮州', '揭阳', '云浮', '柳州',
        '桂林', '梧州', '北海', '防城港', '钦州', '贵港', '玉林', '百色',
        '贺州', '河池', '来宾', '崇左', '三亚', '三沙', '儋州', '五指山',
        '琼海', '文昌', '万宁', '东方', '定安', '屯昌', '澄迈', '临高',
        '白沙', '昌江', '乐东', '陵水', '保亭', '琼中', '自贡', '攀枝花',
        '泸州', '德阳', '绵阳', '广元', '遂宁', '内江', '乐山', '南充',
        '眉山', '宜宾', '广安', '达州', '雅安', '巴中', '资阳', '阿坝',
        '甘孜', '凉山', '六盘水', '遵义', '安顺', '毕节', '铜仁', '黔西南',
        '黔东南', '黔南', '曲靖', '玉溪', '保山', '昭通', '丽江', '普洱',
        '临沧', '楚雄', '红河', '文山', '西双版纳', '大理', '德宏', '怒江',
        '迪庆', '榆林', '延安', '汉中', '渭南', '咸阳', '宝鸡', '铜川',
        '商洛', '安康', '酒泉', '张掖', '武威', '天水', '嘉峪关', '金昌',
        '白银', '平凉', '庆阳', '定西', '陇南', '临夏', '甘南', '石嘴山',
        '吴忠', '固原', '中卫', '海东', '海北', '黄南', '海南', '果洛',
        '玉树', '海西', '克拉玛依', '吐鲁番', '哈密', '昌吉', '博尔塔拉', '巴音郭楞',
        '阿克苏', '克孜勒苏', '喀什', '和田', '伊犁', '塔城', '阿勒泰', '石河子',
        '阿拉尔', '图木舒克', '五家渠', '北屯', '铁门关', '双河', '可克达拉', '昆玉'
    ][:250]  # Increase to 250 periphery cities to fill the circle
}

# 2. Create network graph
G = nx.Graph()

# Add nodes with layer attribute
for layer, city_list in cities.items():
    for city in city_list:
        G.add_node(city, layer=layer)

# 3. Create connections with higher degree for core/secondary nodes
def add_connections(G, cities):
    """Add edges with preferential attachment to core/secondary nodes"""

    # Core connects to all secondary and some intermediate
    core = cities['core'][0]
    for city in cities['secondary']:
        G.add_edge(core, city, weight=random.uniform(0.7, 1.0))

    for city in random.sample(cities['intermediate'], k=8):
        G.add_edge(core, city, weight=random.uniform(0.5, 0.8))

    # Secondary connects to intermediate and some periphery
    for sec_city in cities['secondary']:
        # Connect to intermediate
        for city in random.sample(cities['intermediate'], k=random.randint(4, 7)):
            G.add_edge(sec_city, city, weight=random.uniform(0.5, 0.9))

        # Connect to periphery
        for city in random.sample(cities['periphery'], k=random.randint(5, 10)):
            G.add_edge(sec_city, city, weight=random.uniform(0.3, 0.6))

    # Intermediate connects to periphery
    for int_city in cities['intermediate']:
        for city in random.sample(cities['periphery'], k=random.randint(3, 6)):
            G.add_edge(int_city, city, weight=random.uniform(0.2, 0.5))

    # Some periphery-to-periphery connections
    for _ in range(30):
        city1, city2 = random.sample(cities['periphery'], k=2)
        if not G.has_edge(city1, city2):
            G.add_edge(city1, city2, weight=random.uniform(0.1, 0.3))

add_connections(G, cities)

# 4. Create radial layout
def radial_layout(G, cities):
    """Create concentric radial layout"""
    pos = {}

    # Core at center
    pos[cities['core'][0]] = (0, 0)

    # Secondary in inner ring
    n_sec = len(cities['secondary'])
    for i, city in enumerate(cities['secondary']):
        angle = 2 * np.pi * i / n_sec
        radius = 1.5
        pos[city] = (radius * np.cos(angle), radius * np.sin(angle))

    # Intermediate in middle ring
    n_int = len(cities['intermediate'])
    for i, city in enumerate(cities['intermediate']):
        angle = 2 * np.pi * i / n_int + np.pi / n_int  # Offset for visual balance
        radius = 3.0
        pos[city] = (radius * np.cos(angle), radius * np.sin(angle))

    # Periphery in outer ring (perfect circle)
    n_per = len(cities['periphery'])
    for i, city in enumerate(cities['periphery']):
        angle = 2 * np.pi * i / n_per
        radius = 5.0
        pos[city] = (radius * np.cos(angle), radius * np.sin(angle))

    return pos

pos = radial_layout(G, cities)

# 5. Create figure
fig, ax = plt.subplots(figsize=(16, 16), facecolor='white')
ax.set_aspect('equal')
ax.axis('off')

# 6. Draw edges with curved lines (Bezier style) - different colors and widths
def get_edge_color_and_width(node1, node2, weight):
    """Determine edge color based on node layers and width based on weight"""
    layer1 = G.nodes[node1]['layer']
    layer2 = G.nodes[node2]['layer']

    # Sort layers to get consistent color
    layers = tuple(sorted([layer1, layer2]))

    # Determine edge type
    if layers == ('core', 'secondary'):
        color = EDGE_COLORS['core-secondary']
    elif layers == ('core', 'intermediate'):
        color = EDGE_COLORS['core-intermediate']
    elif layers == ('intermediate', 'secondary'):
        color = EDGE_COLORS['secondary-intermediate']
    elif layers == ('periphery', 'secondary'):
        color = EDGE_COLORS['secondary-periphery']
    elif layers == ('intermediate', 'periphery'):
        color = EDGE_COLORS['intermediate-periphery']
    elif layers == ('periphery', 'periphery'):
        color = EDGE_COLORS['periphery-periphery']
    else:
        color = '#419b84'  # Default color

    # Width based on weight (0.1 to 2.0)
    width = 0.2 + weight * 2.5

    return color, width

for edge in G.edges(data=True):
    node1, node2, data = edge
    weight = data.get('weight', 0.5)

    x1, y1 = pos[node1]
    x2, y2 = pos[node2]

    # Get color and width based on layers and weight
    edge_color, edge_width = get_edge_color_and_width(node1, node2, weight)

    # Draw curved edge
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        connectionstyle=f"arc3,rad=0.2",
        arrowstyle='-',
        linewidth=edge_width,
        color=edge_color,
        alpha=0.25,
        zorder=1
    )
    ax.add_patch(arrow)

# 7. Draw nodes by layer
for layer in ['periphery', 'intermediate', 'secondary', 'core']:
    node_list = cities[layer]
    node_positions = [pos[node] for node in node_list]

    if node_positions:
        x_coords = [p[0] for p in node_positions]
        y_coords = [p[1] for p in node_positions]

        ax.scatter(x_coords, y_coords,
                  s=SIZES[layer],
                  c=COLORS[layer],
                  alpha=0.85,
                  edgecolors='white',
                  linewidths=2,
                  zorder=3,
                  label=f'{layer.capitalize()} Layer')

# 8. Add labels for core and secondary cities
# Core label
core_city = cities['core'][0]
ax.text(pos[core_city][0], pos[core_city][1], core_city,
       fontsize=14, fontweight='bold', ha='center', va='center',
       color='white', zorder=4)

# Secondary labels
for city in cities['secondary']:
    x, y = pos[city]
    # Position label outside the node
    offset = 0.3
    angle = np.arctan2(y, x)
    label_x = x + offset * np.cos(angle)
    label_y = y + offset * np.sin(angle)

    ax.text(label_x, label_y, city,
           fontsize=10, fontweight='bold', ha='center', va='center',
           bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                    edgecolor=COLORS['secondary'], alpha=0.8),
           zorder=4)

# 9. Add title
ax.text(0, 6.5, 'Core-Periphery Network Visualization',
       fontsize=20, fontweight='bold', ha='center',
       bbox=dict(boxstyle='round,pad=0.8', facecolor='white',
                edgecolor='gray', linewidth=2))

ax.text(0, 6.0, '核心-边缘网络可视化',
       fontsize=16, ha='center', color='gray')

# 10. Create legend with circular markers
from matplotlib.lines import Line2D

legend_elements = [
    Line2D([0], [0], marker='o', color='w',
           markerfacecolor=COLORS['core'], markersize=15,
           markeredgecolor='white', markeredgewidth=2,
           label='Core Layer (核心层)', linestyle='None'),
    Line2D([0], [0], marker='o', color='w',
           markerfacecolor=COLORS['secondary'], markersize=12,
           markeredgecolor='white', markeredgewidth=2,
           label='Secondary Core (次核心层)', linestyle='None'),
    Line2D([0], [0], marker='o', color='w',
           markerfacecolor=COLORS['intermediate'], markersize=10,
           markeredgecolor='white', markeredgewidth=2,
           label='Intermediate Layer (中间层)', linestyle='None'),
    Line2D([0], [0], marker='o', color='w',
           markerfacecolor=COLORS['periphery'], markersize=8,
           markeredgecolor='white', markeredgewidth=2,
           label='Periphery Layer (边缘层)', linestyle='None')
]

legend = ax.legend(handles=legend_elements,
                  loc='lower center',
                  bbox_to_anchor=(0.5, -0.05),
                  ncol=4,
                  fontsize=11,
                  frameon=True,
                  fancybox=False,
                  shadow=False)
legend.get_frame().set_linewidth(1.5)
legend.get_frame().set_edgecolor('gray')

# 11. Set axis limits
ax.set_xlim(-6.5, 6.5)
ax.set_ylim(-6.5, 7.0)

# 12. Save as high-quality SVG
output_svg = 'New_Draw_XYL/core_periphery_network.svg'
output_png = 'New_Draw_XYL/core_periphery_network.png'

plt.savefig(output_svg, format='svg', dpi=300, bbox_inches='tight',
           facecolor='white', edgecolor='none')
plt.savefig(output_png, format='png', dpi=300, bbox_inches='tight',
           facecolor='white', edgecolor='none')

print("Core-Periphery Network Visualization created successfully!")
print(f"  SVG: {output_svg}")
print(f"  PNG: {output_png}")

# Print network statistics
print(f"\n=== Network Statistics ===")
print(f"Total nodes: {G.number_of_nodes()}")
print(f"Total edges: {G.number_of_edges()}")
print(f"Core layer: {len(cities['core'])} nodes")
print(f"Secondary layer: {len(cities['secondary'])} nodes")
print(f"Intermediate layer: {len(cities['intermediate'])} nodes")
print(f"Periphery layer: {len(cities['periphery'])} nodes")

# Calculate degree for core and secondary
core_degree = G.degree(cities['core'][0])
avg_secondary_degree = np.mean([G.degree(city) for city in cities['secondary']])
avg_periphery_degree = np.mean([G.degree(city) for city in cities['periphery']])

print(f"\nAverage degree:")
print(f"  Core: {core_degree}")
print(f"  Secondary: {avg_secondary_degree:.1f}")
print(f"  Periphery: {avg_periphery_degree:.1f}")

plt.show()
