from mesa import Agent
import random
from prey_predator.random_walk import RandomWalker


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # Initialize energy of the sheep as if is has eaten 3 patch of grass
        self.energy = 3 * self.model.sheep_gain_from_food

    def eat_grass(self):
        """
        If there is grass on the patch and the sheep is not at 100% energy, it eats the patch.
        """
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        # Because grass patches where initialized first they are always in the first position of the list
        grass_patch = cellmates[0]
        if grass_patch.fully_grown == 1:
            #Patch gets eaten
            grass_patch.patch_is_eaten()
            #Sheep gets energy
            self.energy += self.model.sheep_gain_from_food

    def reproduce(self):
        """
        The sheep reproduces with probability sheep_reproduce
        """
        will_reproduce = random.choices([0, 1], [1 - self.model.sheep_reproduce, self.model.sheep_reproduce])[0]
        if will_reproduce:
            # Add new sheep
            self.model.new_sheep(self.pos)

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        # Move
        self.random_move()
        self.energy -= self.model.sheep_loss_from_movement
        self.energy = max(0, self.energy)
        # If energy is too low, you die
        if self.energy == 0:
            self.model.remove(self)
            return

        # Eat grass
        self.eat_grass()

        # Reproduce
        self.reproduce()
        


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # Initialize energy of the wolf as if is has eaten 3 patch of grass
        self.energy = 3 * self.model.wolf_gain_from_food

    def eat_sheep(self):
        """
        If there is grass on the patch and the wolf is not at 100% energy, it eats the patch.
        """
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        sheep = [obj for obj in cellmates if isinstance(obj, Sheep)]
        if len(sheep) > 0:
            # Choose a random sheep to eat on your grid space
            sheep_to_eat = self.random.choice(sheep)
            self.model.remove(sheep_to_eat)
            # Gain energy
            self.energy += self.model.wolf_gain_from_food

    def reproduce(self):
        """
        The wolf reproduces with probability wolf_reproduce
        """
        will_reproduce = random.choices([0, 1], [1 - self.model.wolf_reproduce, self.model.wolf_reproduce])[0]
        if will_reproduce:
            # Add new wolf
            self.model.new_wolf(self.pos)

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        # Move
        self.random_move()
        self.energy -= self.model.wolf_loss_from_movement
        self.energy = max(0, self.energy)
        # If energy is too low, you die
        if self.energy == 0:
            self.model.remove(self)
            return

        # Eat grass
        self.eat_sheep()

        # Reproduce
        self.reproduce()


class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, fully_grown, countdown, model):
        """
        Creates a new patch of grass

        Args:
            fully_grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.pos = pos
        self.countdown = countdown

    def patch_is_eaten(self):
        self.fully_grown = 0
        self.countdown = self.model.grass_regrowth_time

    def step(self):
        if self.fully_grown == 0:
            if self.countdown > 0:
                self.countdown -= 1
            else :
                self.fully_grown = 1