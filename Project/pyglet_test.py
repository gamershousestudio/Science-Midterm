import pyglet
from pyglet import shapes

# Create window with V-Sync disabled
config = pyglet.gl.Config(double_buffer=True)
window = pyglet.window.Window(config=config)

batch = pyglet.graphics.Batch()
point1 = shapes.Circle(100, 100, 10, color=(50, 50, 255), batch=batch)
point2 = shapes.Circle(200, 200, 10, color=(255, 50, 50), batch=batch)

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()
