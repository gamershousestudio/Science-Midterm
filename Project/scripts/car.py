# Graphics library
from pyglet.sprite import Sprite

class Car:
    def __init__(self, image, batch):
        # Sprite setup
        image.anchor_x = 25
        image.anchor_y = 25
        self.body = Sprite(image, batch=batch)
        
        # Puts sprite on screen
        self.body.x, self.body.y = 480, 260