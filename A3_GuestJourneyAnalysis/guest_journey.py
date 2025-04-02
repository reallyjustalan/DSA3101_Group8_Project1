import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def plot_journey_network():
    # Mock data - replace with your actual transitions
    G = nx.DiGraph()
    transitions = {
        ('7','18'): 120,  # Carousel → Mickey's Fun Wheel
        ('12','16'): 85,  # Soarin' → Little Mermaid
        ('14','16'): 78   # Radiator Springs → Little Mermaid
    }
    
    for (source, target), weight in transitions.items():
        G.add_edge(source, target, weight=weight)

    fig, ax = plt.subplots(figsize=(10,6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx(
        G, pos, ax=ax,
        node_color='skyblue',
        node_size=800,
        width=[w/20 for w in transitions.values()],
        edge_color='gray',
        arrowsize=15
    )
    ax.set_title("Top Attraction Transitions (Thicker lines = more frequent)")
    st.pyplot(fig)

def plot_opportunity_zones():
    # Mock map - replace with your coordinates
    fig, ax = plt.subplots(figsize=(10,6))
    
    # Generate fake park layout
    np.random.seed(42)
    x = np.random.uniform(-118.46, -118.45, 20)
    y = np.random.uniform(34.12, 34.13, 20)
    
    # Plot "park"
    ax.scatter(x, y, c='blue', alpha=0.1, s=100, label='Other attractions')
    
    # Top locations (gold stars)
    ax.scatter(x[0], y[0], c='gold', s=300, marker='*', label='Top attraction')
    ax.scatter(x[5], y[5], c='gold', s=300, marker='*')
    
    # Opportunity zones (red)
    ax.scatter(x[2], y[2], c='red', s=150, label='Opportunity zone')
    ax.scatter(x[8], y[8], c='red', s=150)
    
    # Green circles
    circle1 = plt.Circle((x[0], y[0]), 0.001, color='green', fill=False, linestyle='--')
    circle2 = plt.Circle((x[5], y[5]), 0.001, color='green', fill=False, linestyle='--')
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    
    ax.set_title("Opportunity Zones Near Top Attractions")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.legend()
    st.pyplot(fig)

def insights():
    st.subheader("Key Findings")
    st.write("""
    1. **87.6% of photos** are taken far from top attractions
    2. Best opportunity zones:
       - Goofy's Sky School (near Incredicoaster)
       - Turtle Talk with Crush (underutilized show)
    3. Closed areas: A Bug's Land → Now Avengers Campus
    """)
