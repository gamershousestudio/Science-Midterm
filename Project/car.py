# Graphics library
from pyglet.sprite import Sprite

# Python library
import math

class Car:
    # Caps car speed
    max_speed = 6.0

    # Physics stuff
    deceleration_rate = 0.2 # Deceleration when off track
    friction = 0.05  # Friction while driving on track
    drift_factor = 0.1  # Drift intensity (higher means more drift)



    def __init__(self, network, image, batch):
        self.network = network
        # Sprite setup
        image.anchor_x = 25
        image.anchor_y = 25
        self.body = Sprite(image, batch=batch)
        self.is_running = True
        
        # Puts sprite on screen
        self.body.x, self.body.y = 480, 260
        self.speed = 0.0
        self.rotation = 0.0

    # Updates speed
    def update(self, delta_time):
        render_speed = delta_time * 60 # change in time

        if self.is_running:
            # Friction
            self.speed -= self.friction

            # Gives the neural network / 'brain' control over the car
            acceleration, steer_position = self.network.feed_forward()
            
            if acceleration > 0:
                self.speed += 0.1

            # Prevents negative speed
            if self.speed < 0:
                self.speed = 0.0

            # Limits speed
            if self.speed > 6:
                self.speed = 6.0

            # Apply drifting based on steering position and speed
            if abs(steer_position) > 0.3 and self.speed > 4.0:  # Only apply drift at high speed and strong steering
                drift = steer_position * self.speed * self.drift_factor
                self.rotation -= drift
                self.speed -= self.drift_factor  # Reduce speed slightly due to drift

            # Regular rotation (without drift) is still influenced by the steer position
            self.rotation -= steer_position * self.speed * render_speed

            # Rotation
            self.rotation -= steer_position * self.speed * render_speed
            self.body.rotation = -self.rotation

            # Updates position
            self.body.x += self.speed * render_speed * math.cos(math.radians(self.rotation)) # uses cosine to calculate x position to make the car go forward
            self.body.y += self.speed * render_speed * math.sin(math.radians(self.rotation)) # similer thing but for the y value
    
        # deceases car speed if the engine is off
        else:
            # If the car is off the track, apply deceleration gradually
            self.speed -= self.deceleration_rate  # Apply deceleration
            if self.speed < 0:  # Don't let speed go negative
                self.speed = 0

            # Gradual rotation stopping
            self.rotation *= 0.98  # Slowly reduce the rotation angle
            self.body.rotation = -self.rotation

            # If the car has stopped, don't update position anymore
            self.body.x += self.speed * render_speed * math.cos(math.radians(self.rotation))
            self.body.y += self.speed * render_speed * math.sin(math.radians(self.rotation))