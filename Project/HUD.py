# Graphics library
from pyglet.text import Label
from pyglet.shapes import Circle

# Network display
class NeuronSprite:
    def __init__(self, x, y, batch):
        self.node_border = Circle(x, y, 22, color = (0, 0, 0, 255), batch=batch)
        self.node_fill = Circle(x, y, 20, color = (255, 255, 255, 255), batch=batch)
        self.node_value = Labek(x = x, y = y, color = (255, 255, 255, 255), font_size = 12, anchor_x = "center", anchor_y = "center", batch=batch)

# Text for information like round number and current population
class Hud:
    def __init__(self, simulation_round, batch):
        self.round_label = Label(f"Round: {simulation_round}", x = 30, y = 520, color = (255, 255, 255), batch=batch)
        self.population_label = Label(x = 130, y = 520, color = (255, 255, 255), batch=batch)

    # Updates population
    def update(self, alive, population):
        self.population_label.text = f"Population: {alive}/{population}"