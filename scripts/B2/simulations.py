from objects import *
from optimisation import *
from heatmap import *

def start_simulation_run(Model, dataframe, num_rides):
    """Run an optimized short-duration simulation (71 steps) of theme park operations.
    
    Initializes a clean model instance, optimizes ride placement using genetic algorithms,
    and runs a simulation with periodic status updates and visualizations.

    Args:
        Model (ThemeParkGridModel): The base model instance to use as template.
        dataframe (pd.DataFrame): DataFrame containing ride attributes (Ranking, CAPACITY).
        num_rides (int): Number of rides to include in simulation (>2).

    Returns:
        str: Error message if input validation fails.
        None: Simulation completes successfully.
    """

    if num_rides < 3:
        return "Need a minimum of 3 rides to run the simulation"
    
    # Create a fresh copy of the model to avoid modifying the original
    if Model.restricted_bottom_left:
        Model2 = ThemeParkGridModel(width=Model.grid.width, 
                              height=Model.grid.height,
                              restricted_bottom_left=Model.restricted_bottom_left,
                              restricted_top_right=Model.restricted_top_right)
    else:
        Model2 = ThemeParkGridModel(width=Model.grid.width, 
                              height=Model.grid.height
                              )
        
    # Sort dataframe by Ranking to ensure lower numbers come first
    dataframe = dataframe.sort_values('Ranking').copy()
    possible_rides = []
    
    # Add rides dynamically from the sorted DataFrame
    for _, row in dataframe.iterrows():
        possible_rides.append({
            "name": str(row['Ranking']),
            "capacity": row['CAPACITY'],
            "service_time": random.randint(5, 10),
            "popularity_rank": row['Ranking']
        })

    # Optimize ride placement
    best_ride_positions = optimize_ride_placement(Model2, possible_rides, num_rides)
    
    # Verify selected rides
    selected_rides = [possible_rides[idx]['name'] for idx, _ in best_ride_positions]
    print(f"Selected rides by ranking: {selected_rides}")
    print("Best ride positions:", best_ride_positions)

    # Add the selected rides to the model
    for ride_idx, pos in best_ride_positions:
        row = dataframe.iloc[ride_idx]
        while True:        
            if not Model.is_restricted(*pos):
                cell_contents = Model.grid.get_cell_list_contents([pos])
                if not any(isinstance(agent, RideAgent) for agent in cell_contents):
                    break
            # Generate new position if current is invalid
            pos = generate_valid_position(Model)
        
        Model.add_ride(
            name=str(row['Ranking']),
            pos=pos,
            capacity=row['CAPACITY'],
            service_time=random.randint(5, 10),
            popularity_rank=row['Ranking']
        )

    # Run the simulation
    for step in range(71):
        Model.step()
        if step % 10 == 0:
            print(f'Step: {step}')
            fig = plot_combined_heatmap_and_rides_normalized(Model)
            number = Model.get_total_guests()
            print(f"total guests: {number}")
    return
    # return model  # Return the model with the optimized configuration
def full_simulation_run(Model, dataframe,num_rides):
    """Run an optimized full-day simulation (180 steps) of theme park operations.
    
    Initializes a clean model instance, optimizes ride placement using genetic algorithms,
    and runs an extended simulation with periodic status updates and visualizations.

    Args:
        Model (ThemeParkGridModel): The base model instance to use as template.
        dataframe (pd.DataFrame): DataFrame containing ride attributes (Ranking, CAPACITY).
        num_rides (int): Number of rides to include in simulation (>2).

    Returns:
        str: Error message if input validation fails.
        None: Simulation completes successfully..

    Note:
        This is identical to start_simulation_run() except for the longer duration (180 steps).
        Both functions maintain identical parameter signatures and behavior patterns.
    """

    if num_rides < 3:
        return "Need a minimum of 3 rides to run the simulation"
    
    # Create a fresh copy of the model to avoid modifying the original
    if Model.restricted_bottom_left:
        Model2 = ThemeParkGridModel(width=Model.grid.width, 
                              height=Model.grid.height,
                              restricted_bottom_left=Model.restricted_bottom_left,
                              restricted_top_right=Model.restricted_top_right)
    else:
        Model2 = ThemeParkGridModel(width=Model.grid.width, 
                              height=Model.grid.height
                              )
        
    # Sort dataframe by Ranking to ensure lower numbers come first
    dataframe = dataframe.sort_values('Ranking').copy()
    possible_rides = []
    
    # Add rides dynamically from the sorted DataFrame
    for _, row in dataframe.iterrows():
        possible_rides.append({
            "name": str(row['Ranking']),
            "capacity": row['CAPACITY'],
            "service_time": random.randint(5, 10),
            "popularity_rank": row['Ranking']
        })

    # Optimize ride placement
    best_ride_positions = optimize_ride_placement(Model2, possible_rides, num_rides)
    
    # Verify selected rides
    selected_rides = [possible_rides[idx]['name'] for idx, _ in best_ride_positions]
    print(f"Selected rides by ranking: {selected_rides}")
    print("Best ride positions:", best_ride_positions)

    # Add the selected rides to the model
    for ride_idx, pos in best_ride_positions:
        row = dataframe.iloc[ride_idx]
        while True:        
            if not Model.is_restricted(*pos):
                cell_contents = Model.grid.get_cell_list_contents([pos])
                if not any(isinstance(agent, RideAgent) for agent in cell_contents):
                    break
            # Generate new position if current is invalid
            pos = generate_valid_position(Model)
        
        Model.add_ride(
            name=str(row['Ranking']),
            pos=pos,
            capacity=row['CAPACITY'],
            service_time=random.randint(5, 10),
            popularity_rank=row['Ranking']
        )

    # Run the simulation
    for step in range(180):
        Model.step()
        if step % 10 == 0:
            print(f'Step: {step}')
            fig = plot_combined_heatmap_and_rides_normalized(Model)
            number = Model.get_total_guests()
            print(f"total guests: {number}")
    return

