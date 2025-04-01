def start_simulation_run(Model, dataframe, num_rides):
    if num_rides > 13:
        return "The model only supports less than 13 rides please input less than 13"
    if num_rides < 2:
        return "Need a minimum of 2 rides to run the simulation"
    
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
