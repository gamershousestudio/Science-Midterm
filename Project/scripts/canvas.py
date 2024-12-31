# Graphics library
from pyglet.window import Window, key
from pyglet import image
from pyglet.graphics import Batch
from pyglet.sprite import Sprite

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
    def __init__(self, track_image_path, car_image_paths):
        super().__init__()

        # Allows for the window to be closed
        self.is_simulating = True

        # Window dimensions NOTE-- Change in the future to fit the rasp. pi screen
        self.width = 960
        self.height = 540

        # Rendering batches
        self.background_batch = Batch()
        self.track_image_sprite = Sprite(image.load(track_image_path), batch=self.background_batch)

        self.cars_batch = Batch()
        self.car_images = [image.load(c) for c in car_image_paths]

        # Keyboard
        self.keyboard = key.KeyStateHandler()
        self.push_handlers(self.keyboard)
    
    # Opens the window
    def simulate_generation(self):
        self.car_sprites = []
        self.car_sprites.append(Car(random.choice(self.car_images), self.cars_batch))

        # Gets current time 
        last_time = time.perf_counter()

        # Main simulation loop
        while self.is_simulating:
            elapsed_time = time.perf_counter() - last_time

            # Updates time & creates frames
            if elapsed_time > self.frame_duration:
                last_time = time.perf_counter()
                self.dispatch_events()
                self.update(elapsed_time)
                self.draw()

    # Passed changes to the gpu
    def update(self, delta_time):
        for car_sprite in self.car_sprites:
            car_sprite.update(self, delta_time, self.keyboard)
    
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