from objects import *
import matplotlib.pyplot as plt
import numpy as np

# Function to plot heatmap and rides
def plot_combined_heatmap_and_rides_normalized(model):
    '''Create a grid to track guest positions using a heatmap. Given the size, the value is normalised. Output a fig of the heatmap'''
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create heatmap grid
    heatmap = np.zeros((model.grid.width, model.grid.height))
    
    # Count guest positions
    for agent in model.schedule.agents:
        if isinstance(agent, GuestAgent):
            x, y = agent.pos
            heatmap[x][y] += 1

    # Normalize
    if np.max(heatmap) > 0:
        heatmap = heatmap / np.max(heatmap)

    # Plot heatmap ON OUR AXIS
    im = ax.imshow(heatmap.T, cmap='hot', interpolation='nearest', origin='lower')
    fig.colorbar(im, ax=ax, label="Normalized Guest Activity")

    # Plot rides
    for ride in model.rides:
        x, y = ride.pos
        ax.scatter(x, y, color='blue', s=200, edgecolor='white', label='Ride')
        ax.text(x, y + 0.3, ride.name, fontsize=12, ha='center', color='white')

    # Plot restricted area
    if model.restricted_area:
        for (x, y) in model.restricted_area:
            ax.fill([x-0.5, x+0.5, x+0.5, x-0.5], 
                   [y-0.5, y-0.5, y+0.5, y+0.5], 
                   color='blue', alpha=0.3)

    # Configure axes
    ax.set_xticks(range(model.grid.width))
    ax.set_yticks(range(model.grid.height))
    ax.grid(color='black', linestyle='--', linewidth=0.5, alpha=0.5)
    ax.set_title("Theme Park Heatmap with Rides", fontsize=16)
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    fig.show()
    # Remove plt.show() - we want to save, not display
    return fig