# Path library
import os
import json

# Graphics library
from pyglet import image
from itertools import zip_longest

class Track:
    def __init__(self, index):
        # Track info
        self.track_image = image.load(os.path.join("sprites", "tracks", f"track{index}.png"))
        self.overlay_image = image.load(os.path.join("sprites", "overlay", f"track{index}-overlay.png"))

        # Loads track info
        with open(os.path.join("info", f"track{index}.json"), "r") as file:
            data = json.load(file)
        self.checkpoints = data["checkpoints"]
        
        # The 'pitch' is the width of the image multiplied by the length of "RGBA" to get the row's byte width
        pitch = self.track_image.width * len("RGBA")
        
        # Get pixel data for the track image
        pixels = self.track_image.get_data("RGBA", pitch)

        # Determines what is and is not the road. It checks if each pixel is the color (75, 75, 75, 255).
        # If the pixel matches the color, it will be marked as 1 (true), otherwise 0 (false).
        map = [
            1 if (r, g, b, a) == (75, 75, 75, 255) else 0
            for r, g, b, a in zip_longest(*[iter(pixels)] * 4)
        ]
        
        # The map_matrix will hold the binary values (1 for road, 0 for non-road).
        self.map_matrix = [
            map[n:n + self.track_image.width]
            for n in range(0, self.track_image.width * self.track_image.height, self.track_image.width)
        ]

    # Determines if the car is on the road or not
    def is_road(self, x, y):
        if x < 0 or x > 960 or y < 0 or y > 540: # Matches with window dimensions
            return False
        return self.map_matrix[int(y)][int(x)] == 1
