"""
Prey-Predator Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import random

from prey_predator.agents import Sheep, Wolf, GrassPatch
from prey_predator.schedule import RandomActivationByBreed


class WolfSheep(Model):
    """
    Wolf-Sheep Predation Model
    """

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(
            self, 
            height, 
            width, 
            initial_sheep, 
            initial_wolves, 
            sheep_reproduce, 
            wolf_reproduce, 
            wolf_gain_from_food, 
            grass, 
            grass_regrowth_time, 
            sheep_gain_from_food,
            wolf_loss_from_movement,
            sheep_loss_from_movement
            ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
            wolf_loss_from_movement: Energy wolf lose by moving.
            sheep_loss_from_movement: Energy sheep lose by moving.
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food
        # New parameters we added
        self.wolf_loss_from_movement = wolf_loss_from_movement # Variable to model wolf fatigue because of movement
        self.sheep_loss_from_movement = sheep_loss_from_movement  # Variable to model sheep fatigue because of movement
        self.current_unique_id = 0  # To make sure all agents (alive and dead) will have a different unique_id

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)

        # Datacollector
        """
        Three functions
        """
        def wolves_mean_energy(m):
            wolves = [wolf.energy for sheep in m.schedule.agents if (isinstance(wolf, Wolf))]
            if len(wolves) == 0:
                return 0
            else:
                return sum(wolves) / len(wolves)
            
        def sheep_mean_energy(m):
            sheeps = [sheep.energy for sheep in m.schedule.agents if (isinstance(sheep, Sheep))]
            if len(sheeps) == 0:
                return 0
            else:
                return sum(sheeps) / len(sheeps)
        
        def nb_grown_grass_patchs(m):
            grown_grass_patchs = [grass for grass in m.schedule.agents if (isinstance(grass, GrassPatch) and grass.fully_grown)]
            return len(grown_grass_patchs)

    
        self.datacollector = DataCollector(
            {
                "Wolves": lambda m: m.schedule.get_breed_count(Wolf),
                "Wolves mean energy": wolves_mean_energy,
                "Sheep": lambda m: m.schedule.get_breed_count(Sheep),
                "Sheep mean energy": sheep_mean_energy,
                "Grown grass patchs": nb_grown_grass_patchs,
            }
        )

        # Create grass patches
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                # Define position
                pos = (x, y)
                # Iniziatize fully_grown randomly
                fully_grown = random.randint(0, 1)
                # Initialize countdown to 0 if fully_grown, randomly between 1 and grass_regrowth_time otherwise
                countdown = random.randint(1, grass_regrowth_time) * (1 - fully_grown)
                # Initialize grass patch
                grass_patch = GrassPatch(self.current_unique_id, pos, fully_grown, countdown, self)
                self.schedule.add(grass_patch)
                # Place this initial grass_patch in its position
                self.grid.place_agent(grass_patch, (x, y))
                # Increment unique_id by 1
                self.current_unique_id += 1

        # Create sheep:
        for i in range(self.initial_sheep):
            # Initialiaze the agent
            sheep = Sheep(self.current_unique_id, self)
            self.schedule.add(sheep)
            # Randomly choose an initial position
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            # Add the agent to his grid cell
            self.grid.place_agent(sheep, (x, y))
            # Increment unique_id by 1
            self.current_unique_id += 1

        # Create wolves
        for i in range(self.initial_wolves):
            wolf = Wolf(self.current_unique_id, self)
            self.schedule.add(wolf)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            # Add the agent to his grid cell
            self.grid.place_agent(wolf, (x, y))
            # Increment unique_id by 1
            self.current_unique_id += 1
    
    def new_sheep(self, pos):
        """
        This method is called by a sheep that 'wants' to reproduce.
        A new 'baby' sheep is then created from the model.
        """
        # Initialiaze the agent
        sheep = Sheep(self.current_unique_id, self)
        self.schedule.add(sheep)
        # Add the agent to his grid cell
        self.grid.place_agent(sheep, pos)
        # Increment unique_id by 1
        self.current_unique_id += 1
    
    def new_wolf(self, pos):
        """
        This method is called by a wolf that 'wants' to reproduce.
        A new 'baby' wolf is then created from the model.
        """
        # Initialiaze the agent
        wolf = Wolf(self.current_unique_id, self)
        self.schedule.add(wolf)
        # Add the agent to his grid cell
        self.grid.place_agent(wolf, pos)
        # Increment unique_id by 1
        self.current_unique_id += 1

    def remove(self, agent):
        """
        This method is called (by the agent) whenever an agent is eaten or dies from fatigue.
        """
        self.grid.remove_agent(agent)
        self.schedule.remove(agent)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def run_model(self, step_count=200):
        for i in range(step_count):
            self.step()