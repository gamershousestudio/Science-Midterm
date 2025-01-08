# Graphics library
from pyglet.sprite import Sprite
from pyglet.shapes import Line

# Python library
import math

# Sensors for the car
class Sensor:
    max_length_pixels = 200 # view distance

    def __init__(self, angle, batch):
        # __init__ variables
        self.angle = angle # angle from car
        self.beam = Line(0, 0, 0, 0, width = 2, color = (255, 255, 255, 50), batch=batch) # actual sensor

class Car:
    # Probes a sensor
    def probe_sensor(self, sensor):
        probe_length = 0

        sensor.beam.x = self.body.x
        sensor.beam.y = self.body.y

        x2 = sensor.beam.x
        y2 = sensor.beam.y

        # Checks if there is road in front of the sensor
        while probe_length < sensor.max_length_pixels and self.track.is_road(x2, y2):
            probe_length += 2 # higher number = optimal cpu usage
            x2 = self.body.x + probe_length * math.cos(math.radians(self.rotation + sensor.angle))
            y2 = self.body.y + probe_length * math.sin(math.radians(self.rotation + sensor.angle))
        
        # Line cordinates are updates
        sensor.beam.x2 = x2
        sensor.beam.y2 = y2

        return probe_length

    # Caps car speed
    max_speed = 6.0

    # Physics stuff
    deceleration_rate = 0.2 # Deceleration when off track
    friction = 0.05  # Friction while driving on track
    drift_factor = 0.4  # Drift intensity (higher means more drift)



    def __init__(self, network, track, image, batch):
        # __init__
        self.network = network
        self.track = track

        # Sprite setup
        image.anchor_x = 25
        image.anchor_y = 25
        self.body = Sprite(image, batch=batch)
        self.is_running = True
        self.last_checkpoint_passed = 0
        
        # Puts sprite on screen
        self.body.x, self.body.y = track.checkpoints[0]
        self.speed = 0.0
        self.rotation = 0.0

        # Sensors
        self.sensors = [Sensor(i, batch) for i in range(-70, 71, 35)]

    # Updates speed
    def update(self, delta_time):
        render_speed = delta_time * 60  # change in time

        if self.is_running:
            # Calculates output from the sensors(0 meaning no road & 1 meaning road)
            measurements = [self.probe_sensor(sensor) / sensor.max_length_pixels for sensor in self.sensors]

            # Friction
            self.speed -= self.friction

            # Gives the neural network / 'brain' control over the car
            acceleration, steer_position = self.network.feed_forward(measurements)
            
            if acceleration > 0:
                self.speed += 0.1

            # Prevents negative speed
            if self.speed <= 0:
                self.shut_off()

            # Limits speed
            if self.speed > 100:
                self.speed = 100

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
            self.body.x += self.speed * render_speed * math.cos(math.radians(self.rotation))  # uses cosine to calculate x position to make the car go forward
            self.body.y += self.speed * render_speed * math.sin(math.radians(self.rotation))  # similar thing but for the y value

        # Decreases car speed if the engine is off
        else:
            # If the car is off the track, apply deceleration gradually
            self.speed -= self.deceleration_rate  # Apply deceleration
            if self.speed < 0:  # Don't let speed go negative
                self.speed = 0

            # Stop rotation from reducing if the car is off
            self.body.rotation = -self.rotation

            # If the car has stopped, don't update position anymore
            self.body.x += self.speed * render_speed * math.cos(math.radians(self.rotation))
            self.body.y += self.speed * render_speed * math.sin(math.radians(self.rotation))

        
    # Runs every time a car hits a new checkpoint
    def hit_checkpoint(self, id):
        if id - self.last_checkpoint_passed == 1:
            self.last_checkpoint_passed = id

        # Checks if a car is going in the wrong direction or finished the track
        elif id < self.last_checkpoint_passed:
            self.shut_off()
    
    def shut_off(self):
        self.sensors = None
        self.is_running = False