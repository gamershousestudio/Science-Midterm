# VSC path library
import os

# Imports graphics proccessor
from canvas import Canvas

# Imports track data
from track import Track

track_image_path = os.path.join("sprites", "assets-parkinglot", "parkinglot.png")
car_image_path = [os.path.join("sprites", "assets-parkinglot", f"car{i}.png") for i in range(5)]
canvas = Canvas(Track(), car_image_path)

canvas.simulate_generation()