# Graphics library
from pyglet.sprite import Sprite
from pyglet.window import key

# Python library
import math

class Car:
    # Caps car speed
    max_speed = 6.0

    def __init__(self, image, batch):
        # Sprite setup
        image.anchor_x = 25
        image.anchor_y = 25
        self.body = Sprite(image, batch=batch)
        
        # Puts sprite on screen
        self.body.x, self.body.y = 480, 260
        self.speed = 0.0
        self.rotation = 0.0

    # Updates speed
    def update(self, delta_time, keyboard):
        render_speed = delta_time * 60 # change in time

        acceleration = 0.0

        # Friction
        self.speed -= .05

        # Turning
        steer_position = 0.0

        # Keyboard control
        if keyboard[key.UP]:
            acceleration = 1

        if keyboard[key.LEFT]:
            steer_position = -1.0
        
        if keyboard[key.RIGHT]:
            steer_position = 1.0
        
        if acceleration > 0:
            self.speed += 0.1

        # Prevents negative speed
        if self.speed < 0:
            self.speed = 0.0

        # Limits speed
        if self.speed > 6:
            self.speed = 6.0

        # Rotation
        self.rotation -= steer_position * self.speed * render_speed
        self.body.rotation = -self.rotation

        # Updates position
        self.body.x += self.speed * render_speed * math.cos(math.radians(self.rotation)) # uses cosine to calculate x position to make the car go forward
        self.body.y += self.speed * render_speed * math.sin(math.radians(self.rotation)) # similer thing but for the y value