from deap import base, creator, tools, algorithms
import random
import numpy as np
import math
import matplotlib.pyplot as plt
import warnings
from objects import *

warnings.filterwarnings("ignore", category=UserWarning)

# Define the fitness function
def fitness_function(individual, model, possible_rides):
    """Calculate the fitness score for a ride placement configuration.
    
    Evaluates the quality of a ride layout based on guest satisfaction, ride utilization,
    and spatial distribution. Applies penalties for poor configurations.
    
    Args:
        individual (list): List of tuples representing (ride_index, position) pairs.
        model (ThemeParkGridModel): The simulation model containing park layout and agents.
        possible_rides (list): List of available ride configurations.
        
    Returns:
        tuple: Single-element tuple containing the computed fitness score.
    """
    # Reset the model for this individual
    reset_model(model, possible_rides, individual)

    total_failed_attempts = 0
    total_rides_per_guest = 0
    grid_density = np.zeros((model.grid.width, model.grid.height))
    restricted_penalty = 0  # Penalty for rides in restricted areas
    popular_ride_penalty = 0  # Penalty for popular rides placed too close
    total_guests = 0
    # Extract ride positions and selected rides from the individual
    ride_positions = [pos for _, pos in individual]
    selected_rides = [possible_rides[ride_idx] for ride_idx, _ in individual]

    # Check if any ride is in a restricted area
    for pos in ride_positions:
        if model.is_restricted(*pos):  # Check if position is restricted
            restricted_penalty -= 1000  # Apply a large penalty

    # Calculate distance between popular rides
    popular_ride_positions = []
    for i, pos in enumerate(ride_positions):
        ride = selected_rides[i]
        if ride['popularity_rank'] <= 3:  # Define popular rides as those with rank <= 2
            popular_ride_positions.append(pos)

    # Calculate pairwise distances between popular rides
    for i in range(len(popular_ride_positions)):
        for j in range(i + 1, len(popular_ride_positions)):
            x1, y1 = popular_ride_positions[i]
            x2, y2 = popular_ride_positions[j]
            distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)  # Euclidean distance
            if distance < 3:  # Threshold for spacing (adjust as needed)
                popular_ride_penalty -= (3 - distance) * 100  # Penalize based on closeness
    
    # Add a fixed number of guests for this evaluation
    num_guests = 100
    for i in range(num_guests):
        guest = GuestAgent(i, model)
        model.schedule.add(guest)
        model.grid.place_agent(guest, model.start_pos)

    # Initialize variables for fitness calculation

    # Simulate guest behavior for this ride configuration
    for step in range(26):  # Simulate 26 steps by right 50
        model.step()  # Advance the entire simulation by one step

        # Track guest positions at the 25th step
        if step == 25:
            for guest in model.schedule.agents:
                if isinstance(guest, GuestAgent):
                    x, y = guest.pos
                    if 0 <= x < model.grid.width and 0 <= y < model.grid.height:
                        grid_density[x][y] += 1

    # Track failed ride attempts and rides completed
    for guest in model.schedule.agents:
        if isinstance(guest, GuestAgent):
            total_failed_attempts += guest.failed_attempts
            total_rides_per_guest += guest.rides_completed
            total_guests += 1

    # Calculate density score (average density at the 25th step)
    density_score = np.sum(grid_density) / (model.grid.width * model.grid.height)

    # Combine objectives into a single fitness score
    satisfaction_score = -total_failed_attempts  # Minimize failed attempts
    rides_score = total_rides_per_guest  # Maximize rides per guest
    fitness = satisfaction_score + rides_score - density_score * 2 + restricted_penalty + popular_ride_penalty

    # Debug: Print intermediate results
    print(f"Failed attempts: {total_failed_attempts}, Rides per guest: {total_rides_per_guest}, total_guests: {total_guests}")
    print(f"Density score: {density_score}, Popularity Penalty: {popular_ride_penalty}, restricted_penalty: {restricted_penalty}")
    print(f"Fitness: {fitness}")

    # Remove guests after evaluation
    for guest in list(model.schedule.agents):
        if isinstance(guest, GuestAgent):
            model.schedule.remove(guest)
            model.grid.remove_agent(guest)

    return (fitness,)

# Function to generate a valid position (not in restricted area and not occupied by another ride)
def generate_valid_position(model):
    """Generate a random valid position within the park grid.
    
    Args:
        model (ThemeParkGridModel): The simulation model containing grid dimensions.
        
    Returns:
        tuple: Valid (x,y) position not in restricted areas.
    """

    while True:
        pos = (random.randint(0, model.grid.width - 1), random.randint(0, model.grid.height - 1))
        if not model.is_restricted(*pos):  # Ensure position is not restricted
            return pos

# Function to ensure uniqueness of ride indices in an individual
def ensure_unique_rides(individual, possible_rides):
    """Ensure no duplicate ride indices exist in an individual's configuration.
    
    Args:
        individual (list): Current ride configuration to validate.
        possible_rides (list): Available ride configurations for replacement.
        
    Returns:
        list: Individual with duplicate rides replaced by unique alternatives.
    """
    ride_indices = [ride_idx for ride_idx, _ in individual]
    unique_ride_indices = list(set(ride_indices))  # Remove duplicates
    if len(unique_ride_indices) < len(ride_indices):
        # If duplicates exist, replace them with unique ride indices
        available_rides = set(range(len(possible_rides))) - set(unique_ride_indices)
        for i in range(len(ride_indices)):
            if ride_indices[i] in unique_ride_indices:
                unique_ride_indices.remove(ride_indices[i])
            else:
                # Replace duplicate with a unique ride index
                ride_indices[i] = available_rides.pop()
        # Update the individual with unique ride indices
        individual = [(ride_indices[i], pos) for i, (_, pos) in enumerate(individual)]
    return individual

# Function to ensure uniqueness of positions in an individual
def ensure_unique_positions(individual, model):
    """Ensure all ride positions in an individual are unique and valid.
    
    Args:
        individual (list): Current ride configuration to validate.
        model (ThemeParkGridModel): Simulation model for position validation.
        
    Returns:
        list: Individual with duplicate positions replaced by unique alternatives.
    """
    positions = [pos for _, pos in individual]
    unique_positions = list(set(positions))  # Remove duplicates
    if len(unique_positions) < len(positions):
        # If duplicates exist, replace them with unique positions
        for i in range(len(positions)):
            if positions[i] in unique_positions:
                unique_positions.remove(positions[i])
            else:
                # Replace duplicate with a unique position
                positions[i] = generate_valid_position(model)
        # Update the individual with unique positions
        individual = [(ride_idx, positions[i]) for i, (ride_idx, _) in enumerate(individual)]
    return individual

# Function to repair the best individual
def repair_individual(individual, possible_rides, model):
    """Apply all necessary repairs to ensure a valid ride configuration.
    
    Combines uniqueness checks for both rides and positions.
    
    Args:
        individual (list): Current ride configuration to repair.
        possible_rides (list): Available ride configurations.
        model (ThemeParkGridModel): Simulation model for validation.
        
    Returns:
        list: Fully repaired individual configuration.
    """
    individual = ensure_unique_rides(individual, possible_rides)
    individual = ensure_unique_positions(individual, model)
    return individual

# Function to reset the model for each individual
def reset_model(model, possible_rides, individual):
    """Reset the simulation model with a new ride configuration.
    
    Clears existing rides and initializes with the specified individual's layout.
    
    Args:
        model (ThemeParkGridModel): Simulation model to reset.
        possible_rides (list): Available ride configurations.
        individual (list): New ride configuration to apply.
    """
    # Clear existing rides
    for agent in list(model.schedule.agents):
        if isinstance(agent, RideAgent):
            model.schedule.remove(agent)
            model.grid.remove_agent(agent)

    # Add rides from the current individual
    for ride_idx, pos in individual:
        ride = possible_rides[ride_idx]
        model.add_ride(
            name=ride['name'],
            pos=pos,
            capacity=ride['capacity'],
            service_time=ride['service_time'],
            popularity_rank=ride['popularity_rank']
        )

# Function to plot the current best solution
def plot_best_solution(best_individual, model, possible_rides, generation):
    """Visualize the current best ride configuration and guest distribution.
    
    Generates a heatmap showing guest activity and ride placements.
    
    Args:
        best_individual (list): Optimal ride configuration to visualize.
        model (ThemeParkGridModel): Simulation model containing layout data.
        possible_rides (list): Ride configurations for labeling.
        generation (int): Current generation number for title.
        
    Returns:
        matplotlib.figure.Figure: The generated visualization figure.
    """
    plt.close('all')  # Properly close any existing figures
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create and normalize heatmap
    heatmap = np.zeros((model.grid.width, model.grid.height))
    for agent in model.schedule.agents:
        if isinstance(agent, GuestAgent):
            x, y = agent.pos
            heatmap[x][y] += 1
    if np.max(heatmap) > 0:
        heatmap = heatmap / np.max(heatmap)

    # Plot heatmap with colorbar
    im = ax.imshow(heatmap.T, cmap='hot', interpolation='nearest', origin='lower')
    plt.colorbar(im, ax=ax, label="Normalized Guest Activity")

    # Plot rides with popularity numbers
    sorted_rides = sorted(best_individual, key=lambda x: possible_rides[x[0]]['popularity_rank'])
    for i, (ride_idx, pos) in enumerate(sorted_rides):
        x, y = pos
        ax.scatter(x, y, color='blue', s=200, edgecolor='white')
        ax.text(x, y + 0.3, str(i+1), fontsize=12, ha='center', color='white')

    # Plot restricted area if it exists
    if hasattr(model, 'restricted_area') and model.restricted_area:
        for (x, y) in model.restricted_area:
            ax.fill([x-0.5, x+0.5, x+0.5, x-0.5],
                   [y-0.5, y-0.5, y+0.5, y+0.5],
                   color='blue', alpha=0.3)

    # Configure axes and labels
    ax.set_xticks(range(model.grid.width))
    ax.set_yticks(range(model.grid.height))
    ax.grid(color='black', linestyle='--', linewidth=0.5, alpha=0.5)
    ax.set_title(f"Generation {generation}: Theme Park Heatmap with Rides", fontsize=16)
    ax.set_xlabel("X Coordinate")
    ax.set_yticks(range(model.grid.height))
    ax.set_ylabel("Y Coordinate")
    
    plt.tight_layout()  # Prevent label clipping
    return fig

# Function to set up and run the Genetic Algorithm
def optimize_ride_placement(model, possible_rides, num_rides):
    """Execute genetic algorithm optimization for ride placement.
    
    Implements a complete evolutionary optimization process including:
    - Population initialization
    - Fitness evaluation
    - Selection and reproduction
    - Iterative improvement
    
    Args:
        model (ThemeParkGridModel): Simulation model to optimize within.
        possible_rides (list): Available ride configurations.
        num_rides (int): Number of rides to place in the park.
        
    Returns:
        list: Optimized ride configuration as (ride_index, position) tuples.
    """

    '''Optimisation of ride placement through the use of Genetic Algorithm, a reinforcing algorithm. Here the output is ((a,(x,y)),(b,(x,y)), ...) with a and b being the rank and x,y being the position'''
    # Set up DEAP for Genetic Algorithm
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    # Define an attribute for a ride-position pair
    toolbox.register("attr_ride_pos", lambda: (random.randint(0, len(possible_rides) - 1), generate_valid_position(model)))
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_ride_pos, n=num_rides)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def evaluate(individual):
        '''takes in an individual and apply it to the modle and the number of possible rides'''
        return fitness_function(individual, model, possible_rides)

    # Define custom mutation function to handle tuples and avoid restricted areas
    def mutate_individual(individual, indpb, model):
        '''Function that ensures that within each generation of iteration, the position evolves, allowing it to optimise and self learn.'''
        for i in range(len(individual)):
            if random.random() < indpb:
                # Mutate the ride index or position
                if random.random() < 0.5:  # Mutate ride index
                    individual[i] = (random.randint(0, len(possible_rides) - 1), individual[i][1])
                else:  # Mutate position
                    individual[i] = (individual[i][0], generate_valid_position(model))
        # Ensure uniqueness of ride indices and positions after mutation
        individual = ensure_unique_rides(individual, possible_rides)
        individual = ensure_unique_positions(individual, model)
        return individual,

    # Define custom crossover function to ensure unique positions
    def cxTwoPointUnique(ind1, ind2, model):
        """Perform a two-point crossover while ensuring unique positions.Ensures uniqueness between positions"""
        # Perform the standard two-point crossover
        tools.cxTwoPoint(ind1, ind2)
        # Ensure uniqueness of positions in both individuals
        ind1[:] = ensure_unique_positions(ind1, model)
        ind2[:] = ensure_unique_positions(ind2, model)
        return ind1, ind2

    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", cxTwoPointUnique, model=model)
    toolbox.register("mutate", mutate_individual, indpb=0.1, model=model)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # Initialize population
    population = toolbox.population(n=8)
    # Ensure uniqueness of ride indices and positions in the initial population
    for ind in population:
        ind[:] = ensure_unique_rides(ind, possible_rides)
        ind[:] = ensure_unique_positions(ind, model)

    # Run the GA in a loop
    ngen = 10  # Number of generations
    for generation in range(ngen):
        print(f"Generation {generation}")

        # Select the next generation
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < 0.5:  # Crossover probability
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
                child1[:] = ensure_unique_rides(child1, possible_rides)
                child1[:] = ensure_unique_positions(child1, model)
                child2[:] = ensure_unique_rides(child2, possible_rides)
                child2[:] = ensure_unique_positions(child2, model)

        for mutant in offspring:
            if random.random() < 0.2:  # Mutation probability
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the new individuals
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Replace the population with the new generation
        population[:] = offspring

    # Get the best solution
    best_individual = tools.selBest(population, k=1)[0]
    # Repair the best individual to ensure no duplicates
    best_individual = repair_individual(best_individual, possible_rides, model)
    fig = plot_best_solution(best_individual, model, possible_rides, generation)
    fig.show()
    #print("Best ride positions (after repair):", best_individual)
    return best_individual
    