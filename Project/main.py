# Path library
import os

# Imports graphics proccessor
from canvas import Canvas

# Imports track data
from track import Track

# Neural network
from network import FirstNetwork

# Initialization
track_image_path = os.path.join("sprites", "assets-parkinglot", "parkinglot.png")
car_image_path = [os.path.join("sprites", "assets-parkinglot", f"car{i}.png") for i in range(5)]
canvas = Canvas(Track(), car_image_path)

# Neural networks
population_count = 3
networks = [FirstNetwork() for _ in range(population_count)]

canvas.simulate_generation(networks)