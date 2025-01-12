# Graphics library
from pyglet.text import Label
from pyglet.shapes import Circle

# Network display
class NeuronSprite:
    def __init__(self, x, y, batch):
        self.node_border = Circle(x, y, 22, color = (0, 0, 0, 255), batch=batch)
        self.node_fill = Circle(x, y, 20, color = (255, 255, 255, 255), batch=batch)
        self.node_value = Label(x = x, y = y, color = (255, 255, 255, 255), font_size = 12, anchor_x = "center", anchor_y = "center", batch=batch)

    # Changes neuron color
    def update(self, value):
        self.node_value.text = f"{value:.2f}"

        if value > 0:
            self.node_fill.color  = 0, int(value * 200), 0, 255
        elif value < 0:
            self.node_fill.color = int(value * 200), 0, 0, 255
        else:
                self.node_value.color = 0, 0, 0, 127

# Text for information like round number and current population
class Hud:
    def __init__(self, simulation_round, dimensions, batch):
        # Labels
        self.round_label = Label(f"Round: {simulation_round}", x = 30, y = 520, color = (255, 255, 255), batch=batch)
        self.population_label = Label(x = 130, y = 520, color = (255, 255, 255), batch=batch)

        # Network display
        self.neurons = []

        x = 40

        if dimensions != False:
            for neuron_count in dimensions:
                total_height = neuron_count * 50 - 10

                y = 540 - (540 - total_height) / 2

                # Creates each neuron
                for _ in range(neuron_count):
                    self.neurons.append(NeuronSprite(x, y, batch))
                    y -= 50
                x += 50



    # Updates population & network display
    def update(self, network, alive, population):
        self.population_label.text = f"Population: {alive}/{population}"

        if network != False:
            index = 0
            for input in network.inputs:
                self.neurons[index].update(input)
                index += 1
            
            for layer in network.layers:
                for value in layer.outputs:
                    self.neurons[index].update(value)
                    index += 1