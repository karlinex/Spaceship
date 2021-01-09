import numpy as np

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (10, 10)
plt.ion()

class MovableObject(object):
    def __init__(self):
        super().__init__()
        self.__angle = np.random.random() * np.pi
        self.attribute_name = 'Noname'

        self.geometry = []
        self.R = np.identity(3)


    def set_angle(self, angle):
        self.__angle = angle
        theta = np.radians(self.__angle)
        self.R = np.array([[np.cos(theta), -np.sin(theta), 0],
                           [np.sin(theta), np.cos(theta),  0],
                           [0,              0,             1]])


    def get_angle(self):
        return self.__angle

    def draw(self):
        x_values = []
        y_values = []

        for vec in self.geometry:
            vec3d = np.dot(vec, np.array([[1, 0],
                                          [0, 1],
                                          [0, 0]])) + np.array([0, 0, 1])
            vec3d = np.dot(self.R, vec3d)
            vec = np.dot(vec3d, np.array([[1, 0, 0],
                                          [0, 1, 0]]))
            x_values.append(vec[0])
            y_values.append(vec[1])

        plt.plot(x_values, y_values)

class Asteroid(MovableObject):
    def __init__(self):
        super().__init__()
        self.attribute_name = 'Asteroid'

    def draw(self):
        print('draw asteroid')

class Player(MovableObject):
    def __init__(self):
        super().__init__()
        self.attribute_name = 'Player'

        self.geometry = np.array ([
            [-1, 0],
            [1, 0],
            [0, 1],
            [-1, 0]
        ])

    # def draw(self):
    #     plt.plot(self.geometry[:, 0], self.geometry[:, 1])


playerA = Player()
playerA.set_angle(0)

actors = [Asteroid()]
for _ in range(10):
    actors.append(Asteroid())

#actors += [Player()] #concat 2 lists
actors.append(playerA)

is_running = True
def press(event):
    global is_running, player
    print('press', event.key)
    if event.key == 'escape':
        is_running = False
    elif event.key == 'right':
        playerA.set_angle(playerA.get_angle() - 5)
    elif event.key == 'left':
        playerA.set_angle(playerA.get_angle() + 5)

fig, _ = plt.subplots()
fig.canvas.mpl_connect('key_press_event', press)

while is_running:
    plt.clf()

    plt.xlim(-10, 10)
    plt.ylim(-10, 10)

    for actor in actors:  # polymorphism
        actor.draw()

        plt.title(f"angle: {playerA.get_angle()}")

    plt.draw()
    plt.pause(0.01)