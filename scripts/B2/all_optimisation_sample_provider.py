import os
from pathlib import Path
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
from optimisation import *
from objects import *
from cleaning import *
from heatmap import *
from simulations import *


# Set up base directory structure
downloads_path = str(Path.home() / "Downloads")
simulations_dir = os.path.join(downloads_path, 'simulations')
os.makedirs(simulations_dir, exist_ok=True)

# Define the three different model configurations
MODEL_CONFIGS = {
    'model1': {  # Small park with central restricted area
        'width': 9,
        'height': 9,
        'restricted_bottom_left': (2, 2),
        'restricted_top_right': (6, 6)
        },
    'model2': {  # Medium park with no restricted areas
        'width': 9,
        'height': 9,
        'restricted_bottom_left': None,
        'restricted_top_right': None
    },
    'model3': {  # Large park with multiple restricted zones
        'width': 15,
        'height': 15,
        'restricted_bottom_left': (1,2),
        'restricted_top_right': (3,6)
    }
}

# Load your data

def plot_and_save_solution(best_individual, model, possible_rides, sample_num, save_path):
    plt.figure(figsize=(10, 8))
    
    # Create and normalize heatmap
    heatmap = np.zeros((model.grid.width, model.grid.height))
    for agent in model.schedule.agents:
        if isinstance(agent, GuestAgent):
            x, y = agent.pos
            if 0 <= x < model.grid.width and 0 <= y < model.grid.height:
                heatmap[x][y] += 1
    if np.max(heatmap) > 0:
        heatmap = heatmap / np.max(heatmap)
    
    # Plot heatmap and rides
    plt.imshow(heatmap.T, cmap='hot', interpolation='nearest', origin='lower')
    
    
    for ride_idx, pos in best_individual:
        ride = possible_rides[ride_idx]
        x, y = pos
        plt.scatter(x, y, color='blue', s=200, edgecolor='white')
        plt.text(x, y + 0.3, str(ride['popularity_rank']), 
                ha='center', color='white', fontsize=12)
    
    # Handle different restricted area formats
    if hasattr(model, 'restricted_area'):
        if isinstance(model.restricted_bottom_left, list):  # Multiple zones
            for bl, tr in zip(model.restricted_bottom_left, model.restricted_top_right):
                plt.fill([bl[0]-0.5, tr[0]+0.5, tr[0]+0.5, bl[0]-0.5],
                        [bl[1]-0.5, bl[1]-0.5, tr[1]+0.5, tr[1]+0.5],
                        color='blue', alpha=0.3)
        elif model.restricted_bottom_left:  # Single zone
            bl, tr = model.restricted_bottom_left, model.restricted_top_right
            plt.fill([bl[0]-0.5, tr[0]+0.5, tr[0]+0.5, bl[0]-0.5],
                    [bl[1]-0.5, bl[1]-0.5, tr[1]+0.5, tr[1]+0.5],
                    color='blue', alpha=0.3)
    
    plt.title(f"Model: {model.name}\nRides: {len(best_individual)} | Sample: {sample_num}")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig(save_path, bbox_inches='tight', dpi=150)
    plt.close()

# Run simulations for all models and ride counts
def run_all_simulations(MODEL_CONFIGS, ranking, simulations_dir):
    for model_name, config in MODEL_CONFIGS.items():
        model_dir = os.path.join(simulations_dir, model_name)
        os.makedirs(model_dir, exist_ok=True)
        
        print(f"\nRunning simulations for {model_name}...")
        print(f"Configuration: {config}")
        
        for num_rides in range(3, 14):  # From 3 to 14 rides
            rides_dir = os.path.join(model_dir, f'number_rides_{num_rides}')
            os.makedirs(rides_dir, exist_ok=True)
            
            print(f"  Optimizing {num_rides} rides...")
            
            for sample_num in range(10):  # 10 samples per configuration
                # Initialize model with current configuration
                if isinstance(config['restricted_bottom_left'], list):
                    # Handle multiple restricted areas
                    park = ThemeParkGridModel(
                        width=config['width'],
                        height=config['height'],
                        restricted_bottom_left=config['restricted_bottom_left'],
                        restricted_top_right=config['restricted_top_right']
                    )
                else:
                    # Handle single or no restricted area
                    park = ThemeParkGridModel(
                        width=config['width'],
                        height=config['height'],
                        restricted_bottom_left=config['restricted_bottom_left'],
                        restricted_top_right=config['restricted_top_right']
                    )
                park.name = model_name  # Store model name for plotting
                
                # Prepare top N rides
                top_rides = ranking.sort_values('Ranking').head(num_rides)
                possible_rides = [{
                    "name": str(row['Ranking']),
                    "capacity": row['CAPACITY'],
                    "service_time": random.randint(5, 10),
                    "popularity_rank": row['Ranking']
                } for _, row in top_rides.iterrows()]
                
                # Optimize and save results
                best_ride_positions = optimize_ride_placement(park, possible_rides, num_rides)
                save_path = os.path.join(rides_dir, f'sample_{sample_num}.png')
                plot_and_save_solution(best_ride_positions, park, possible_rides, sample_num, save_path)

