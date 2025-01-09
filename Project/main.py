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
max_generation = 5
networks = [Network(dimensions) for _ in range(population_count)]

# Simulation
simulation_round = 1

while simulation_round <= max_generation and canvas.is_simulating:
    print(f"=== Round: {simulation_round} ===")
    canvas.simulate_generation(networks, simulation_round)
    simulation_round += 1

    if canvas.is_simulating:
        print(f"-- Average checkpoint reached: {sum(n.highest_checkpoint for n in networks) / len(networks)}.")