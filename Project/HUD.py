# Graphics library
from pyglet.text import Label

# Text for information like round number and current population
class Hud:
    def __init__(self, simulation_round, batch):
        self.round_label = Label(f"Round: {simulation_round}", x = 30, y = 520, color = (255, 255, 255), batch=batch)
        self.population_label = Label(x = 130, y = 520, color = (255, 255, 255), batch=batch)

    # Updates population
    def update(self, alive, population):
        self.population_label.text = f"Population: {alive}/{population}"