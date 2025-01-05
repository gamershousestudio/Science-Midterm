# Graphics library
from pyglet.window import Window, key
from pyglet import image
from pyglet.graphics import Batch
from pyglet.sprite import Sprite
import pyglet

# Generic python libs
import time
import random

# Other scripts
from car import Car

# Display
class Canvas(Window):
    # defines fps(helps with computers like rasp. pies) -- limited to 60 fps
    frame_duration = 1 / 60

    # Creates the window
    def __init__(self, track, car_image_paths):
        super().__init__(vsync=True)

        # Allows for the window to be closed
        self.is_simulating = True

        # Window dimensions NOTE-- Change in the future to fit the rasp. pi screen
        self.width = 960
        self.height = 540

        # Rendering batches
        self.background_batch = Batch()
        self.track_image_sprite = Sprite(track.track_image, batch=self.background_batch)

        self.cars_batch = Batch()
        self.car_images = [image.load(c) for c in car_image_paths]

        # Track data
        self.track = track
    
    # Opens the window
    def simulate_generation(self, networks):
        # Creates cars
        self.car_sprites = []
        for network in networks:
            self.car_sprites.append(Car(network, random.choice(self.car_images), self.cars_batch))

        # Finds total population & current population
        self.population_total = len(self.car_sprites)
        self.population_alive = self.population_total

        # Gets current time 
        last_time = time.perf_counter()

        # Main simulation loop
        while self.is_simulating and self.population_alive > 0:
            elapsed_time = time.perf_counter() - last_time

            # Updates time & creates frames
            if elapsed_time > self.frame_duration:
                last_time = time.perf_counter()
                self.dispatch_events()
                self.update(elapsed_time)
                self.draw()

    # Updates simulation
    def update(self, delta_time):
        for car_sprite in self.car_sprites:
            car_sprite.update(delta_time)
    
            # Makes sure the car is still on the track, and if not disables the car
            if car_sprite.is_running:
                if not self.track.is_road(car_sprite.body.x, car_sprite.body.y):
                    car_sprite.is_running = False

        # Finds how many cars are still running
        running_cars = [c for c in self.car_sprites if c.is_running]
        self.population_alive = len(running_cars)

    # Passed changes to the gpu
    def draw(self):
        self.clear()
        self.background_batch.draw()
        self.cars_batch.draw()
        self.flip()

    # Termination
    def on_key_press(self, symbol, modifires):
        if symbol == key.ESCAPE:
            self.is_simulating = False
            print("Simulation Terminated.")