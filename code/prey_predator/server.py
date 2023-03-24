from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}

    if type(agent) is Sheep:
        portrayal["Color"] = "white"
        portrayal["Layer"] = 3
        portrayal["r"] = 0.6

    elif type(agent) is Wolf:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.8

    elif type(agent) is GrassPatch:
        portrayal["Shape"] = "rect"
        portrayal["Layer"] = 1
        portrayal["w"] = 1
        portrayal["h"] = 1
        if agent.fully_grown == 1:
            portrayal["Color"] = "green"
        else:
            portrayal["Color"] = "burlywood"

    return portrayal
    
# Création des éléments à visualiser
canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element1 = ChartModule(
    [{"Label": "Wolves", "Color": "red"}, {"Label": "Sheep", "Color": "lightblue"}, {"Label": "Grown grass patchs", "Color": "green"}],
    data_collector_name='datacollector'
)
chart_element2 = ChartModule(
    [{"Label": "Wolves mean energy", "Color": "red"}, {"Label": "Sheep mean energy", "Color": "lightblue"}],
    data_collector_name='datacollector'
)

model_params = {
    'height': 20,
    'width': 20,
    'initial_sheep': 100,
    'initial_wolves': 50,
    'sheep_reproduce': 0.05,
    'wolf_reproduce': 0.025,
    'wolf_gain_from_food': 20,
    'grass': False,
    'grass_regrowth_time': 3,
    'sheep_gain_from_food': 4,
    'wolf_loss_from_movement': 4,
    'sheep_loss_from_movement': 2
    }

# Création des slider
initial_sheep_slider = UserSettableParameter('slider', 'Initial Sheep', value=model_params['initial_sheep'], min_value=1, max_value=500, step=1)
initial_wolves_slider = UserSettableParameter('slider', 'Initial Wolves', value=model_params['initial_wolves'], min_value=1, max_value=500, step=1)
sheep_reproduce_slider = UserSettableParameter('slider', 'Sheep Reproduce', value=model_params['sheep_reproduce'], min_value=0.0, max_value=1.0, step=0.01)
wolf_reproduce_slider = UserSettableParameter('slider', 'Wolf Reproduce', value=model_params['wolf_reproduce'], min_value=0.0, max_value=1.0, step=0.01)
wolf_gain_slider = UserSettableParameter('slider', 'Wolf Gain from Food', value=model_params['wolf_gain_from_food'], min_value=1, max_value=50, step=1)
grass_regrowth_slider = UserSettableParameter('slider', 'Grass Regrowth Time', value=model_params['grass_regrowth_time'], min_value=1, max_value=10, step=1)
sheep_gain_slider = UserSettableParameter('slider', 'Sheep Gain from Food', value=model_params['sheep_gain_from_food'], min_value=1, max_value=10, step=1)
wolf_loss_slider = UserSettableParameter('slider', 'Wolf Loss from Movement', value=model_params['wolf_loss_from_movement'], min_value=1, max_value=10, step=1)
sheep_loss_slider = UserSettableParameter('slider', 'Sheep Loss from Movement', value=model_params['sheep_loss_from_movement'], min_value=1, max_value=10, step=1)

model_params = {
    'height': 20,
    'width': 20,
    'initial_sheep': initial_sheep_slider,
    'initial_wolves': initial_wolves_slider,
    'sheep_reproduce': sheep_reproduce_slider,
    'wolf_reproduce': wolf_reproduce_slider,
    'wolf_gain_from_food': wolf_gain_slider,
    'grass': False,
    'grass_regrowth_time': grass_regrowth_slider,
    'sheep_gain_from_food': sheep_gain_slider,
    'wolf_loss_from_movement': wolf_loss_slider,
    'sheep_loss_from_movement': sheep_loss_slider
}

elements = [
    canvas_element, 
    chart_element1, 
    chart_element2
    ]

server = ModularServer(
    WolfSheep, elements, "Prey Predator Model", model_params
)
server.port = 8521