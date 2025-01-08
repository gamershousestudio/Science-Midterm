# Path library
import os

# Imports graphics proccessor
from canvas import Canvas

# Imports track data
from track import Track

# Neural network
from network import Network

dimensions = 5, 4, 2

# Initialization
car_image_path = [os.path.join("sprites", "cars", f"car{i}.png") for i in range(5)]
canvas = Canvas(Track(1), car_image_path)

# Neural networks
population_count = 100
networks = [Network(dimensions) for _ in range(population_count)]

# Simulation
simulation_round = 1
canvas.simulate_generation(networks, simulation_round)