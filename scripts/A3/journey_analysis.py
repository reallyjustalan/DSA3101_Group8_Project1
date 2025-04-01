import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from collections import defaultdict
from scipy.spatial import KDTree
import plotly.express as px
import plotly.graph_objects as go

def load_data(poi_path, visits_path):
    """Load and preprocess the dataset"""
    # Load POI and visits data
    poi = pd.read_csv(poi_path, delimiter=";")
    seq = pd.read_csv(visits_path, delimiter=";")
    
    # Basic preprocessing
    seq = seq.dropna()
    seq['takenUnix'] = pd.to_datetime(seq['takenUnix'], unit='s')
    seq.rename(columns={'takenUnix': 'dateTaken'}, inplace=True)
    seq['poiID'] = seq['poiID'].astype(int)
    
    # Merge photos_df with poi_df on 'poiID'
    df = seq.merge(poi[['poiID', 'poiName', 'lat', 'long']], on='poiID', how='left')
    
    return poi, seq, df

def plot_poi_map(poi):
    """Create interactive scatter plot of POI locations"""
    fig = px.scatter(
        poi,
        x="long",
        y="lat",
        hover_name="poiName",
        hover_data={
            "poiID": True,
            "rideDuration": True,
            "theme": True,
            "long": True,
            "lat": True
        },
        color="theme",
        text="poiID",
        title="<b>Disney California Adventure Park Attractions</b>",
        labels={
            "long": "Longitude",
            "lat": "Latitude",
            "theme": "Theme"
        },
        width=1000,
        height=700,
    )
    
    # Customize hover tooltip
    fig.update_traces(
        marker=dict(size=10, line=dict(width=1, color="DarkSlateGrey")),
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "POI ID: %{customdata[0]}<br>"
            "Duration: %{customdata[1]} min<br>"
            "Theme: %{customdata[2]}<br>"
            "<extra></extra>"
        ),
        textposition="top center",
        textfont=dict(color="black", size=10, family="Arial"),
    )
    
    # Improve layout
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        title_font=dict(size=20),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial",
            font_color="black"
        ),
        legend_title_text="<b>Theme</b>",
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02,
            font=dict(color="black")
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="lightgray",
            title_font=dict(size=14),
            tickfont=dict(color="black")
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="lightgray",
            title_font=dict(size=14),
            tickfont=dict(color="black")
        ),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    # Add a small buffer to axis limits
    fig.update_xaxes(range=[poi["long"].min() - 0.002, poi["long"].max() + 0.002])
    fig.update_yaxes(range=[poi["lat"].min() - 0.001, poi["lat"].max() + 0.001])
    
    return fig

def analyze_journey_patterns(df, poi):
    """Analyze guest journey patterns and extract top patterns"""
    # Create poi name mapping
    poi_name_map = dict(zip(poi['poiID'].astype(str), poi['poiName']))
    
    # Enforce poiID as string
    df['poiID'] = df['poiID'].astype(str)
    
    # Group journeys with validation
    journey_patterns = defaultdict(int)
    skipped_single_attraction = 0
    skipped_all_repeats = 0
    
    for (visitor, seq_id), group in df.sort_values('dateTaken').groupby(['nsid', 'seqID']):
        poi_sequence = group['poiID'].tolist()
        
        # Skip single-attraction visits
        if len(poi_sequence) < 2:
            skipped_single_attraction += 1
            continue
        
        # Check for at least one unique transition (A→B)
        has_unique_transition = any(poi_sequence[i] != poi_sequence[i+1]
                                   for i in range(len(poi_sequence)-1))
        
        if has_unique_transition:
            journey_str = ' → '.join(poi_sequence)
            journey_patterns[journey_str] += 1
        else:
            skipped_all_repeats += 1
    
    # Get top patterns
    top_patterns = sorted(journey_patterns.items(), key=lambda x: -x[1])[:10]
    
    # Format with POI names
    formatted_patterns = []
    for pattern, count in top_patterns:
        named_pattern = ' → '.join(poi_name_map.get(pid, pid) for pid in pattern.split(' → '))
        formatted_patterns.append((named_pattern, count))
    
    return journey_patterns, formatted_patterns

def create_flow_network(journey_patterns, poi_name_map, top_n=50):
    """Create a network graph of visitor flows between attractions"""
    # Extract all POIs from journey patterns
    all_pois = set()
    for journey in journey_patterns.keys():
        pois = journey.split(' → ')
        all_pois.update(pois)
    
    # Calculate edge weights
    edge_weights = defaultdict(int)
    for journey, count in journey_patterns.items():
        pois = journey.split(' → ')
        for i in range(len(pois)-1):
            if pois[i] != pois[i+1]:  # Only unique transitions
                edge = (pois[i], pois[i+1])
                edge_weights[edge] += count
    
    # Get top N edges by weight
    sorted_edges = sorted(edge_weights.items(), key=lambda x: -x[1])[:top_n]
    filtered_edges = dict(sorted_edges)
    
    # Create graph with only filtered edges
    G = nx.DiGraph()
    for poi_id in all_pois:
        if poi_name_map:
            G.add_node(poi_id, label=poi_name_map.get(poi_id, poi_id))
        else:
            G.add_node(poi_id)
    
    for (src, tgt), weight in filtered_edges.items():
        G.add_edge(src, tgt, weight=weight)
    
    # Remove isolated nodes
    G.remove_nodes_from(list(nx.isolates(G)))
    
    return G, filtered_edges

def plot_flow_network(G, filtered_edges):
    """Plot the visitor flow network"""
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G,
                          k=5,
                          iterations=200,
                          scale=5,
                          seed=42)
    
    # Draw nodes
    node_colors = ['red' if node == '14' else 'skyblue' for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=800, node_color=node_colors)
    
    # Draw edges with width proportional to weight
    if filtered_edges:
        max_weight = max(filtered_edges.values())
        edge_widths = [3 * (G[u][v]['weight']/max_weight) for u, v in G.edges()]
        nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color='gray', arrowsize=20)
        
        # Draw edge weight labels
        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    # Draw labels
    node_labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10)
    
    plt.title("Top Visitor Flows", fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    
    return plt.gcf()

def analyze_opportunity_zones(df):
    """Analyze opportunity zones near top attractions"""
    # Identify top locations (top 20% most photographed POIs)
    top_locations = df['poiID'].value_counts().nlargest(
        int(0.2 * len(df['poiID'].unique()))
    ).index
    
    # Get their coordinates
    top_locations_df = df[df['poiID'].isin(top_locations)][['lat', 'long']].drop_duplicates()
    top_coords = list(zip(top_locations_df['lat'], top_locations_df['long']))
    
    # Build a KDTree for fast spatial queries
    top_locations_tree = KDTree(top_locations_df[['lat', 'long']].values)
    
    # Check distances for all photos
    df_coords = df[['lat', 'long']].values
    distances, _ = top_locations_tree.query(df_coords, distance_upper_bound=0.0009)  # ~100m in degrees
    
    # Assign flags
    df['is_top_location'] = df['poiID'].isin(top_locations)
    df['near_top_location'] = (distances != np.inf) & (~df['is_top_location'])
    
    # Calculate actual percentages
    photo_counts = df.groupby('near_top_location')['id'].count()
    photo_percentage = (photo_counts / photo_counts.sum()) * 100
    far_percentage = photo_percentage.get(False, 0)  # % of photos >100m from top locations
    
    # Prepare for visualization
    plot_df = df.copy()
    plot_df['category'] = np.where(
        plot_df['near_top_location'],
        'Near top location (<100m)',
        'Far from top location (>100m)'
    )
    
    # Calculate photo density
    coord_density = plot_df.groupby(['lat', 'long']).size().reset_index(name='density')
    plot_df = plot_df.merge(coord_density, on=['lat', 'long'])
    
    return plot_df, top_coords, far_percentage

def plot_opportunity_zones(plot_df, top_coords, far_percentage):
    """Plot opportunity zones near top attractions"""
    plt.figure(figsize=(12, 8))
    plt.title(
        'Opportunity Zones Near Top Attractions\n'
        'Bubble size = Density at location',
        pad=20
    )
    
    # A. Far from top locations
    far_df = plot_df[
        (plot_df['category'] == 'Far from top location (>100m)') &
        (~plot_df['is_top_location'])
    ]
    plt.scatter(
        x=far_df['long'],
        y=far_df['lat'],
        s=10 + 100 * (far_df['density'] / far_df['density'].max()),
        c='blue',
        alpha=0.6,
        label=f'Photos >100m from top locations ({far_percentage:.1f}%)'
    )
    
    # B. Near top locations (but not at them)
    near_df = plot_df[plot_df['category'] == 'Near top location (<100m)']
    plt.scatter(
        x=near_df['long'],
        y=near_df['lat'],
        s=10 + 100 * (near_df['density'] / near_df['density'].max()),
        c='red',
        alpha=0.6,
        label='Photos ≤100m from top locations'
    )
    
    # C. Highlight top locations (gold stars)
    for i, (lat, lon) in enumerate(top_coords):
        plt.scatter(
            lon, lat,
            c='gold',
            s=200,
            marker='*',
            edgecolors='black',
            label='Top Attractions' if i == 0 else None
        )
        plt.gca().add_patch(plt.Circle(
            (lon, lat),
            0.001,
            color='green',
            fill=False,
            linestyle='--',
            linewidth=2,
            label='Opportunity Zone (100m radius)' if i == 0 else None
        ))
    
    # Add legend and labels
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Insight annotation with dynamic percentage
    plt.annotate(
        f"Insight: {far_percentage:.1f}% of photos are taken >100m from top attractions.\n"
        "Green circles highlight underutilized areas near popular spots.",
        xy=(0.5, -0.15),
        xycoords='axes fraction',
        ha='center',
        fontsize=10,
        bbox=dict(boxstyle="round", alpha=0.1, color="gray")
    )
    
    return plt.gcf()

def get_business_insights():
    """Return key business insights"""
    insights = {
        "popular_pairings": [
            "Radiator Springs Racers is a major traffic driver, frequently paired with Disney Junior and The Bakery Tour",
            "Disney Junior is a strong family attraction, often leading to The Bakery Tour and The Little Mermaid Ride",
            "The Bakery Tour is a high-traffic secondary attraction, commonly followed by King Triton's Carousel"
        ],
        "guest_flow_trends": [
            "Families with young children dominate paths connecting Disney Junior, Carousel, and Little Mermaid",
            "Food & Ride Combos: Bakery Tour acts as a 'resting spot' between rides",
            "RSR is a crowd puller, with guests pairing high-thrill rides with low-intensity shows or food experiences"
        ],
        "recommendations": [
            "Extend RSR FastPass/Genie+ Slots to reduce congestion",
            "Deploy Mobile Food Carts near Disney Junior exit",
            "Bundle experiences with 'Family Fun Pack' tickets",
            "Increase F&B revenue with upsell opportunities around Bakery Tour",
            "Align Disney Junior showtimes with RSR ride exits for smoother transitions"
        ],
        "opportunity_zones": [
            "It's Tough to be a Bug (3D Show, Family, Indoor)",
            "Goofy's Sky School (Roller Coaster)",
            "Jumpin Jellyfish (Ride)",
            "Turtle Talk with Crush (Family, Show, Indoor)",
            "The Bakery Tour (Show, Family, Indoor)"
        ]
    }
    return insights
