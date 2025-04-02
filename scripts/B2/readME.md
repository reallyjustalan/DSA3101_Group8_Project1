# Theme Park Simulation System

A comprehensive agent-based modeling system for simulating and optimizing theme park layouts using genetic algorithms.

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Core Components](#core-components)
   - [objects.py](#objectspy)
   - [optimisation.py](#optimisationpy)
   - [simulations.py](#simulationspy)
   - [heatmap.py](#heatmappy)
4. [Installation & Usage](#installation--usage)
5. [Dependencies](#dependencies)

## System Overview

This system simulates visitor behavior in theme parks using agent-based modeling combined with genetic algorithms for optimal ride placement.

### Key Features

-  **Configurable park layouts** with customizable dimensions and restricted zones
-  **Queue Theory** utilisation of queue theory in support of optimisation of park layouts
-  **Intelligent guest agents** with realistic decision-making and movement patterns
-  **Genetic algorithm optimization** Reinforment learning for strategic ride placement
-  **Heatmap visualization** to analyze visitor traffic patterns
-  **Multi-scenario analysis** for comparative studies of different park designs

## Architecture

The system follows a modular architecture with clear separation of concerns:
```{markdown}
+--------------+
| objects.py   |
| - Base Models|
+--------------+
|
v
+----------------------+     +----------------------------+
| optimisation.py      |     | simulation.py             |
| - GA Implementation  |---->| - Simulation Execution    |
+----------------------+     +----------------------------+
|                                |
v                                v
+---------------------------+   +------------------------------------------+
| heatmap.py               |    | all_heatmaps_simulated.py                |
| - Visualization Engine   |-->| - start_simulation_run()                 |
+---------------------------+   | - run_all_simulations_heatmap()         |
|                               +------------------------------------------+
|                                                |
v                                                |
+------------------------------------------+     |
| all_optimisation_sample_provider.py     |      |
| - run_all_simulations()                 |<-----+
| - plot_and_save_solution()              |
+------------------------------------------+
|
v
+------------------------------------------+
| example.py                               |
| - System Integration & Examples          |
+------------------------------------------+
```

## Core Components

### objects.py

Contains the foundational simulation entities:

```python
class ThemeParkGridModel:
    """
    Manages the park grid and simulation state
    - width, height: Park dimensions
    - restricted_area: Non-walkable zones
    - add_ride(): Places new attractions
    - step(): Advances simulation
    """

class GuestAgent:
    """
    Simulates park visitors
    - choose_ride(): Selection logic (weighted by popularity)
    - move_toward_destination(): Pathfinding
    - arrive_at_ride(): Queue handling
    """

class RideAgent:
    """
    Manages attraction operations
    - capacity: Max simultaneous riders
    - service_time: Ride duration
    - queue: SimPy queue management
    """
```

### optimisation.py

Implements genetic algorithm optimization for ride placement:

| Step | Description |
|------|-------------|
| 1 | Initialize Population |
| 2 | Evaluate Fitness (Guest satisfaction, Ride utilization, Spatial distribution) |
| 3 | Select Parents (Tournament selection) |
| 4 | Apply Operators (Crossover: 80%, Mutation: 20%) |
| 5 | Repeat for 10 Generations |

```python
def fitness_function(individual):
    """
    Evaluates solution quality using:
    - Failed ride attempts (minimize)
    - Rides per guest (maximize)
    - Density penalties
    """

def optimize_ride_placement():
    """
    Coordinates GA process:
    - Population size: 8
    - Generations: 10
    - Returns best (ride, position) pairs
    """
```

### simulations.py

Handles execution of simulation scenarios:

```python
def start_simulation_run():
    """
    Executes single scenario:
    - Model initialization
    - Ride optimization
    - Simulation execution
    - Data collection
    """

def run_all_simulations_heatmap():
    """
    Runs all configured scenarios:
    - Iterates park layouts
    - Tests 3-13 ride counts
    - Organizes output directories
    """
```

### heatmap.py

Generates visual representations of simulation results:

- Guest density heatmaps (normalized)
- Ride locations (marked with popularity rank)
- Restricted area overlays
- Timestep annotations

### Inclusion of addition python scripts
used to create batch job simulations in preparation for the streamlit page.

## Data Source

Data was sourced from Kaggle: "Disneyland Visitors Data (100+ Rides)" authored by AyushTankha.
link: https://www.kaggle.com/datasets/ayushtankha/hackathon
Within this workspace, we will api call the kaggle dataset, ensuring that the data used within our model is up to date. 

## Dependencies

- **Core Libraries**:
  - Python 3.8+
  - Mesa (Agent-based modeling)
  - SimPy (Process-based simulation)
  - DEAP (Evolutionary algorithms)
  
- **Data Processing**:
  - Pandas
  - NumPy
  
- **Visualization**:
  - Matplotlib
