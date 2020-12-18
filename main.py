import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (10, 10)
plt.ion()

class Character:
    def __init__(self):
        super().__init__()
        self.geometry = []
        self.__angle = 0
        self.generate_geometry()

    def set_angle(self, angle):
        self.__angle = angle

    #TODO implement getter for angle
    def get_angle(self):
        return self.__angle

    def generate_geometry(self):
        pass

    def draw(self):
        x_data = []
        y_data = []
        for vec2 in self.geometry:
            x_data.append(vec2[0])
            y_data.append(vec2[1])
        plt.plot(x_data, y_data)

class Player(Character):
    def __init__(self):
        super().__init__()

    def generate_geometry(self):
        # TODO implement geometry to resemble space ship, centered around [0,0] coordinates
        self.geometry = np.array([
            [0, 1],
            [-0.4, -0.5],
            [-0.8, -1],
            [0.8, -1],
            [0.4, -0.5],
            [0, 1]

        ])

characters = []
player = Player()
characters.append(player)

is_running = True

def on_press(event):
    global is_running
    if event.key == 'escape':
        is_running = False
    if event.key == 'left':
        player.set_angle(player.get_angle() - 5)
    if event.key == 'right':
        player.set_angle(player.get_angle() + 5)

fig, _ = plt.subplots()
fig.canvas.mpl_connect('key_press_event', on_press)

dt = 1e-2
while is_running:
    plt.clf()
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)

    for each in characters:
        each.draw()
        #TODO display angle in plot title
        plt.title(f"angle: {each.get_angle()}")

    plt.draw()
    plt.pause(dt)