import random
import simpy
import os
import numpy as np
import pandas as pd
import mesa
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
import random
import matplotlib.pyplot as plt

np.random.seed(50)

##start
# Guest Agent (Moves on Grid Toward a Ride)
class GuestAgent(Agent):
    """An agent representing a theme park guest who moves around and rides attractions.
    
    Attributes:
        unique_id (int): Unique identifier for the agent.
        destination (tuple): Current target position (x,y) the agent is moving toward.
        attraction (RideAgent): Current ride the agent is heading to or riding.
        arrival_time (int): Time when agent arrived at current position.
        ride_completion_time (int): Remaining time steps until ride completion.
        last_ride (RideAgent): Last ride the agent attempted or experienced.
        time_to_leave (int): Total time steps before agent decides to leave park.
        leaving (bool): Flag indicating if agent is exiting the park.
        failed_attempts (int): Count of unsuccessful ride attempts due to long queues.
        rides_completed (int): Count of successfully completed rides.
    """
    def __init__(self, unique_id, model):
        """Initialize a GuestAgent with default attributes.
        
        Args:
            unique_id (int): Unique identifier for the agent.
            model (ThemeParkGridModel): The model instance this agent belongs to.
        """
        super().__init__(model)
        self.unique_id = unique_id
        self.destination = None
        self.attraction = None
        self.arrival_time = 0
        self.ride_completion_time = 0
        self.last_ride = None
        self.time_to_leave = int(round(np.random.normal(loc = 360, scale = 90),2))
        self.leaving = False
        self.failed_attempts = 0  # Track failed ride attempts
        self.rides_completed = 0  # Track rides completed

    def step(self):
        """Execute one step of agent behavior including movement and ride decisions."""
        if self.leaving:
            if self.pos == self.model.start_pos:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
                self.model.guests_left += 1
                #print(f"Guest {self.unique_id} left the park")
            else:
                self.move_toward_destination(self.model.start_pos)
            return

        if self.ride_completion_time > 0:
            self.ride_completion_time -= 1
            if self.ride_completion_time == 0:
                #print(f"Guest {self.unique_id} finished riding {self.attraction.name}")
                self.rides_completed += 1  # Increment rides completed
                self.destination = None
            return

        if not self.destination:
            self.choose_ride()

        if self.destination:
            self.move_toward_destination(self.destination)

            if self.pos == self.destination:
                self.arrive_at_ride()

        self.time_to_leave -= 1
        if self.time_to_leave <= 0 and not self.leaving:
            self.leaving = True
            self.destination = self.model.start_pos
            #print(f"Guest {self.unique_id} decided to leave the park")

    def arrive_at_ride(self):
        """Handle guest arrival at a ride, deciding whether to join queue or leave."""
        if len(self.attraction.queue.queue) < self.attraction.capacity * 3:
            self.attraction.env.process(self.attraction.ride_experience(self))
            #print(f"Guest {self.unique_id} joined the queue at {self.attraction.name}")
            self.last_ride = self.attraction
        else:
            #print(f"Guest {self.unique_id} left {self.attraction.name} due to long queue")
            self.failed_attempts += 1  # Increment failed attempts
            self.destination = None

    def choose_ride(self):
        """Select a ride to visit based on popularity and queue length.
        
        Excludes the last ride visited to encourage variety. Uses weighted random
        selection where weights are inversely proportional to popularity rank.
        """
        if not self.model.rides:
            return

        # Exclude the last ride from the selection
        available_rides = [ride for ride in self.model.rides if ride != self.last_ride]

        if not available_rides:
            return  # No available rides

        # Weighted ride selection: 1/popularity_rank
        ride_weights = [1 / ride.popularity_rank for ride in available_rides]
        self.attraction = random.choices(available_rides, weights=ride_weights, k=1)[0]
        self.destination = self.attraction.pos
        #print(f"Guest {self.unique_id} chose {self.attraction.name} at {self.destination}")

    def move_toward_destination(self, destination):
        """Move agent one step closer to destination while avoiding restricted areas.
        
        Args:
            destination (tuple): Target (x,y) position to move toward.
        """
        x, y = self.pos
        dx, dy = destination

        # Calculate possible new positions
        possible_moves = []
        for new_x, new_y in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if not self.model.is_restricted(new_x, new_y) and not self.model.grid.out_of_bounds((new_x, new_y)):
                possible_moves.append((new_x, new_y))

        if possible_moves:
            # Choose the move that minimizes distance to the destination
            best_move = min(possible_moves, key=lambda pos: abs(pos[0] - dx) + abs(pos[1] - dy))
            self.model.grid.move_agent(self, best_move)
            #print(f"Guest {self.unique_id} moved from {self.pos} to {best_move}")


# Ride Agent (Fixed in Place)
class RideAgent(Agent):
    """An agent representing a theme park attraction with queue management.
    
    Attributes:
        unique_id (int): Unique identifier for the ride.
        name (str): Name of the ride.
        pos (tuple): Fixed (x,y) position on the grid.
        capacity (int): Maximum number of simultaneous riders.
        service_time (int): Time steps required for one ride cycle.
        popularity_rank (int): Relative popularity (lower = more popular).
        env (simpy.Environment): Discrete event simulation environment.
        queue (simpy.Resource): Queue management resource.
        queue_lengths (list): Historical record of queue lengths.
        wait_times (list): Historical record of guest wait times.
    """
    def __init__(self, unique_id, model, name, pos, capacity, service_time, popularity_rank):
        """Initialize a RideAgent with specified parameters.
        
        Args:
            unique_id (int): Unique identifier for the ride.
            model (ThemeParkGridModel): The containing model instance.
            name (str): Name of the ride.
            pos (tuple): Fixed (x,y) position on grid.
            capacity (int): Maximum simultaneous riders.
            service_time (int): Duration of one ride cycle in steps.
            popularity_rank (int): Popularity ranking (lower = more popular).
        """
        super().__init__(model)
        self.unique_id = unique_id
        self.name = name
        self.pos = pos
        self.capacity = capacity
        self.service_time = service_time  # Number of steps to complete one ride cycle
        self.popularity_rank = popularity_rank
        self.env = simpy.Environment()  # Simpy environment for queue management
        self.queue = simpy.Resource(self.env, capacity=capacity)
        self.queue_lengths = []  # Track queue lengths over time
        self.wait_times = []  # Track guest wait times

    def ride_experience(self, guest):
        """Simulate the complete ride experience including queuing and riding.
        
        Args:
            guest (GuestAgent): The guest experiencing the ride.
            
        Yields:
            simpy.events: Queue request and timeout events.
        """
        with self.queue.request() as request:
            queue_length = len(self.queue.queue)
            self.queue_lengths.append(queue_length)  # Track queue length

            yield request  # Wait for turn
            wait_time = self.env.now - guest.arrival_time
            self.wait_times.append(wait_time)

            yield self.env.timeout(self.service_time)  # Ride duration
            guest.ride_completion_time = self.service_time  # Set ride completion time
            #print(f"Guest {guest.unique_id} waited {wait_time:.2f} mins and started riding {self.name}")

# Theme Park Model (Grid-Based)
class ThemeParkGridModel(Model):
    """The main model representing a theme park with guests and rides.
    
    Attributes:
        grid (MultiGrid): The 2D grid representing park layout.
        schedule (RandomActivation): Agent activation scheduler.
        randomizer (random.Random): Random number generator.
        restricted_area (list): List of restricted (x,y) positions.
        start_pos (tuple): Park entrance/exit position.
        guests_entered (int): Total guests who entered the park.
        guests_left (int): Total guests who left the park.
        rides (list): List of RideAgent instances in the park.
        guest_inflow_type (pd.DataFrame): Optional guest arrival schedule.
    """
    def __init__(self, width, height, restricted_bottom_left=None, restricted_top_right=None, guest_inflow_type = None):
        """Initialize the theme park model with specified dimensions and parameters.
        
        Args:
            width (int): Grid width in cells.
            height (int): Grid height in cells.
            restricted_bottom_left (tuple): Bottom-left corner of restricted area.
            restricted_top_right (tuple): Top-right corner of restricted area.
            guest_inflow_type (pd.DataFrame): Optional guest arrival schedule.
        """
        super().__init__()  # Correctly initialize the Model
        self.grid = MultiGrid(width, height, True)  # Initialize grid first
        self.schedule = RandomActivation(self)
        self.randomizer = random  # Use built-in Python random
        if restricted_bottom_left is not None and restricted_top_right is not None:
            # Generate all coordinates in the rectangle defined by bottom-left and top-right
            self.restricted_bottom_left = restricted_bottom_left
            self.restricted_top_right = restricted_top_right
            x_min, y_min = restricted_bottom_left
            x_max, y_max = restricted_top_right
            self.restricted_area = [(x, y) for x in range(x_min, x_max + 1) for y in range(y_min, y_max + 1)]
        else:
            # Default restricted area (if not provided)
            self.restricted_bottom_left = None
            self.restricted_top_right = None
            self.restricted_area = None  # Restricted area in the center
        self.start_pos = (width // 2, 0)  # Bottom center for ingress/egress
        self.guests_entered = 0  # Track guests entering the park
        self.guests_left = 0  # Track guests leaving the park
        self.rides = []
        self.guest_inflow_type = guest_inflow_type
    
        for ride in self.rides:
            self.schedule.add(ride)
            self.grid.place_agent(ride, ride.pos)
        
    def add_ride(self, name, pos, capacity, service_time, popularity_rank):
        """Add a new ride to the theme park.
        
        Args:
            name (str): Name of the ride.
            pos (tuple): (x,y) position on grid.
            capacity (int): Maximum simultaneous riders.
            service_time (int): Ride duration in steps.
            popularity_rank (int): Popularity ranking (lower = more popular).
        """
        ride_id = len(self.rides) + 1  # Assign a unique ID
        new_ride = RideAgent(ride_id, self, name, pos, capacity, service_time, popularity_rank)
        self.rides.append(new_ride)
        self.schedule.add(new_ride)
        self.grid.place_agent(new_ride, pos)
        #print(f"Added new ride: {name} at {pos}")


    def is_restricted(self, x, y):
        """Check if a position is within the restricted area.
        
        Args:
            x (int): X-coordinate to check.
            y (int): Y-coordinate to check.
            
        Returns:
            bool: True if position is restricted, False otherwise.
        """
        if self.restricted_area is None:
            return False
        return (x, y) in self.restricted_area
    

    def step(self, guest_inflow_type=None):
        """Advance the model by one time step.
        
        Handles:
        - New guest arrivals (either scheduled or random)
        - Agent activations
        - Ride simulations
        - Statistics tracking
        """
        # Handle guest inflow
        if self.guest_inflow_type is not None:
            # Get guest count from dataset for current step
            try:
                current_step = self.schedule.steps  # Use Mesa's internal step counter
                new_guests_count = self.guest_inflow_type.iloc[current_step]['GuestCount']
            except (IndexError, KeyError):
                # Fallback if step exceeds dataset or column not found
                new_guests_count = int(round(np.random.normal(100, 25),2))
        else:
            # Default random inflow
            #if self.schedule.steps < 120:
            new_guests_count = int(round(np.random.normal(100, 25),2))
            # else:
            #    new_guests_count = 1
        
        # Add new guests
        for _ in range(new_guests_count):
            # Get next available unique_id
            existing_ids = [agent.unique_id for agent in self.schedule.agents]
            new_guest_id = max(existing_ids) + 1 if existing_ids else 0
            
            new_guest = GuestAgent(new_guest_id, self)
            self.schedule.add(new_guest)
            self.grid.place_agent(new_guest, self.start_pos)
            self.guests_entered += 1

        # Advance simulation - let Mesa handle the step counting
        self.schedule.step()
        
        # Advance each ride's environment
        for ride in self.rides:
            ride.env.run(until=ride.env.now + 1)

        # Reset counter for next step
        self.guests_left = 0
    
    def get_total_guests(self):
        """Get the total number of guests that have entered the park.
        
        Returns:
            int: Total count of guests entered.
        """
        return self.guests_entered
    
