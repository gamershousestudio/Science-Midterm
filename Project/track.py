# Path library
import os

# Graphics library
from pyglet import image
import itertools

class Track:
    def __init__(self):
        # Track info
        self.track_image = image.load(os.path.join("sprites", "assets-parkinglot", "parkinglot.png"))
        pitch = self.track_image.width * len("RGBA")
        pixels = self.track_image.get_data("RGBA", pitch)
        map = [1 if b == (75, 75, 75, 255) else 0 for b in itertools.batched(pixels, 4)] # determines what is and is not the road
        self.map_matrix = map_matrix = [map[n:n + self.track_image.width] for n in range(0, self.track_image.width * self.track_image.height, self.track_image.width)] # matrix based on the bianary map istrack(1 = true, 0 = false)

        # Test
        print(self.map_matrix[270])