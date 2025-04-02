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
simulations_dir = os.path.join(downloads_path, 'heatmaps')
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
        'restricted_bottom_left': (1, 2),
        'restricted_top_right': (3, 6)
    }
}

def start_simulation_run(model, dataframe, num_rides, model_name, output_dir):
    """Run a single simulation with optimized ride placement and save periodic heatmap visualizations.
    
    Args:
        model (ThemeParkGridModel): The base theme park model to use
        dataframe (pd.DataFrame): DataFrame containing ride information (Ranking, CAPACITY)
        num_rides (int): Number of rides to include in simulation (minimum 3)
        model_name (str): Name/identifier for this model configuration
        output_dir (str): Directory path to save heatmap images
        
    The function:
    1. Creates a clean model copy
    2. Selects top N rides by ranking
    3. Optimizes ride placement using genetic algorithm
    4. Runs simulation for 70 steps
    5. Saves heatmap images every 10 steps
    """
    
    if num_rides < 3:
        print("Need a minimum of 3 rides to run the simulation")
        return
    
    if model.restricted_bottom_left:
        model2 = ThemeParkGridModel(width=model.grid.width, 
                              height=model.grid.height,
                              restricted_bottom_left=model.restricted_bottom_left,
                              restricted_top_right=model.restricted_top_right)
    else:
        model2 = ThemeParkGridModel(width=model.grid.width, 
                              height=model.grid.height
                              )
    # Create model directory structure
    model_dir = os.path.join(output_dir, model_name)
    rides_dir = os.path.join(model_dir, f'num_rides_{num_rides}')
    os.makedirs(rides_dir, exist_ok=True)
    
    # Sort dataframe by Ranking
    dataframe = dataframe.sort_values('Ranking').copy()
    possible_rides = []
    
    # Prepare rides
    for _, row in dataframe.head(num_rides).iterrows():
        possible_rides.append({
            "name": str(row['Ranking']),
            "capacity": row['CAPACITY'],
            "service_time": random.randint(5, 10),
            "popularity_rank": row['Ranking']
        })

    # Optimize ride placement
    best_ride_positions = optimize_ride_placement(model2, possible_rides, num_rides)
    print(best_ride_positions)
    # Add rides to the model
    for i, position in enumerate(best_ride_positions):
        ride_idx = position[0]  # Get the ride index
        pos = position[1]  # Get the position (x, y)
        #print(pos)
        # Get the corresponding row from the DataFrame
        row = dataframe.iloc[ride_idx]
        while True:        
            # Check if the position is not in the restricted area and not occupied by another ride
            if not model.is_restricted(*pos):  # Ensure the position is not in the restricted area
                # Check if the position is not occupied by another ride
                cell_contents = model.grid.get_cell_list_contents([pos])
                if not any(isinstance(agent, RideAgent) for agent in cell_contents):
                    break  # Valid position found
        #print(f"here {i}")
        model.add_ride(
            name=row['Ranking'],  # Use the correct column name
            pos=position[1],
            capacity=row['CAPACITY'],
            service_time=random.randint(5, 10),
            popularity_rank=row['Ranking']
        )

    # Run the simulation and save heatmaps at intervals
    for step in range(71):
        model.step()
        if step % 10 == 0:  # Save at 0,10,20,...,70
            # Create and save heatmap
            print(f"number of steps: {step}")
            fig = plot_combined_heatmap_and_rides_normalized(model)  # Assuming this does the plotting
            fig.savefig(os.path.join(rides_dir, f'heatmap_step_{step}.png'), 
                    bbox_inches='tight', 
                    dpi=150)
            plt.close(fig)


def run_all_simulations_heatmap(MODEL_CONFIGS,dataframe, simulations_dir):
    """Execute multiple simulation scenarios across different park configurations and ride counts.
    
    Args:
        MODEL_CONFIGS (dict): Dictionary defining different park layouts and restrictions
        dataframe (pd.DataFrame): DataFrame containing ride information (Ranking, CAPACITY)
        simulations_dir (str): Base directory to save all simulation results
        
    The function:
    1. Iterates through all model configurations
    2. For each model, tests 3-13 ride configurations
    3. Runs each configuration through start_simulation_run()
    4. Organizes output in directory structure by model/num_rides
    """
    for model_name, config in MODEL_CONFIGS.items():
        print(f"\nRunning simulations for {model_name}...")
        
        # Run simulations for 3-13 rides
        for num_rides in range(3, 14):
            # Initialize model
            model = ThemeParkGridModel(
                width=config['width'],
                height=config['height'],
                restricted_bottom_left=config['restricted_bottom_left'],
                restricted_top_right=config['restricted_top_right']
            )
            
            print(f"  Running {num_rides} rides configuration...")
            start_simulation_run(
                model=model,
                dataframe=dataframe,
                num_rides=num_rides,
                model_name=model_name,
                output_dir=simulations_dir
            )

# # Example usage:
# if __name__ == "__main__":
#     # Load your ride data
#     #tivoli_attr_ranking = pd.read_csv('tivoli_attr_ranking.csv')  # Replace with your data
    
#     # Run all simulations
#     run_all_simulations(tivoli_attr_ranking)
    
#     print(f"\nAll simulations completed! Results saved in: {simulations_dir}")