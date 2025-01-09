# Graphics library
from pyglet.window import Window, key
from pyglet import image
from pyglet.graphics import Batch
from pyglet.sprite import Sprite
from pyglet.shapes import Circle
from pyglet.text import Label

# Generic python libs
import time
import random
import math

# Other scripts
from car import Car
from HUD import Hud
from fitness import Fitness

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

        self.overlay_batch = Batch()
        self.track_overlay_sprite = Sprite(track.overlay_image, batch=self.overlay_batch)

        self.cars_batch = Batch()
        self.car_images = [image.load(c) for c in car_image_paths]

        # Checkpoints
        self.checkpoint_sprites = []
        for i, checkpoint in enumerate(track.checkpoints):
            self.checkpoint_sprites.append((Circle(checkpoint[0], checkpoint[1], 15, color = (255, 255, 255, 25), batch=self.background_batch), Label(str(i), x = checkpoint[0], y = checkpoint[1], anchor_x = "center", anchor_y = "center", color = (0, 0, 0, 100), batch = self.background_batch)))

        # Track data
        self.track = track
    
    # Opens the window
    def simulate_generation(self, networks, simulation_round):
        # Generates UI
        self.hud = Hud(simulation_round, self.overlay_batch)

        # Creates cars
        self.car_sprites = []
        for network in networks:
            self.car_sprites.append(Car(network, self.track, random.choice(self.car_images), self.cars_batch))

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
        
        # Calls fitness function 
        Fitness.calculate_cost(self.car_sprites)

        

    # Updates simulation
    def update(self, delta_time):
        for car_sprite in self.car_sprites:
            car_sprite.update(delta_time)
    
            # Makes sure the car is still on the track, and if not disables the car
            if car_sprite.is_running:
                if not self.track.is_road(car_sprite.body.x, car_sprite.body.y):
                    car_sprite.shut_off()
                
                # Checks how many checkpoints each car has reached
                self.check_checkpoints(car_sprite, self.track.checkpoints)

        # Finds how many cars are still running
        running_cars = [c for c in self.car_sprites if c.is_running]
        self.population_alive = len(running_cars)

        # Updates HUD
        if self.population_alive > 0:
            self.hud.update(self.population_alive, self.population_total)

    # Passed changes to the gpu
    def draw(self):
        self.clear()
        self.background_batch.draw()
        self.overlay_batch.draw()
        self.cars_batch.draw()
        self.flip()

    # Termination
    def on_key_press(self, symbol, modifires):
        if symbol == key.ESCAPE:
            self.is_simulating = False
            print("Simulation Terminated.")
    
    # Figures out how many checkpoints each car passed
    def check_checkpoints(self, car_sprite, checkpoints):
        for i, checkpoint in enumerate(checkpoints):
            length = math.sqrt((checkpoint[0] - car_sprite.body.x) ** 2 + (checkpoint[1] - car_sprite.body.y) ** 2)
            if length < 40:
                car_sprite.hit_checkpoint(i)