import numpy as np
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (10, 10)
plt.ion()


def get_matrix_rotation(theta):
    theta_rad = theta * np.pi / 180
    theta_cos = np.cos(theta_rad)
    theta_sin = np.sin(theta_rad)
    R = np.array(
        [
            [theta_cos, -theta_sin, 0],
            [theta_sin, theta_cos, 0],
            [0, 0, 1]
        ]
    )
    return R


def get_matrix_translation(t_x, t_y):
    T = np.array([
        [1, 0, t_x],
        [0, 1, t_y],
        [0, 0, 1]
    ])
    return T


def get_matrix_scale(s_x, s_y):
    T = np.array([
        [s_x, 0, 0],
        [0, s_y, 0],
        [0, 0, 1]
    ])
    return T


def get_vec3_from_vec2(vec2):
    I = np.array([
        [1, 0],
        [0, 1],
        [0, 0]
    ])

    vec3 = np.dot(I, vec2) + np.array([0, 0, 1])
    return vec3


def get_vec2_from_vec3(vec3):
    I = np.array([
        [1, 0, 0],
        [0, 1, 0]
    ])

    vec2 = np.dot(I, vec3)
    return vec2

class Character:
    def __init__(self):
        super().__init__()
        self.geometry = []

        self.angle = 0
        self.pos = np.array([0.0, 0.0])
        self.dir = np.array([0.0, 1.0])
        self.speed = 1e-1

        self.C = np.identity(3)  # Combined
        self.R = np.identity(3)  # Rotation
        self.T = np.identity(3)  # Translation

        self.x_data = []
        self.y_data = []

        self.generate_geometry()
        self.color = 'r'

    def generate_geometry(self):
        pass

    def draw(self):
        self.R = get_matrix_rotation(self.angle)

        dir3 = np.dot(self.R, np.array([0, 1, 0]))  # direction of original geometry
        # rotated by absolute angle
        self.dir = get_vec2_from_vec3(dir3)
        self.pos += self.dir * self.speed  # speed

        # TODO do not allow things to fly out of the space or spawn them in opposite side of the screen
        if self.pos[0] > 10.0 or self.pos[0] < -10.0 or self.pos[1] > 10.0 or self.pos[1] < -10.0:
            self.pos[0] = self.pos[0] * -1
            self.pos[1] = self.pos[1] * -1

        self.C = np.matmul(self.T_fix, self.S) if isinstance(self, Player) else np.identity(3)

        self.C = np.matmul(self.R, self.C)
        self.T = get_matrix_translation(t_x=self.pos[0], t_y=self.pos[1])
        self.C = np.matmul(self.T, self.C)

        self.x_data = []
        self.y_data = []
        for vec2 in self.geometry:
            vec3 = get_vec3_from_vec2(vec2)

            vec3 = np.dot(self.C, vec3)

            vec2 = get_vec2_from_vec3(vec3)

            self.x_data.append(vec2[0])
            self.y_data.append(vec2[1])

        plt.plot(self.x_data, self.y_data, color=self.color)


class Player(Character):
    def __init__(self):
        super().__init__()
        self.T_fix = get_matrix_translation(t_x=0, t_y=-0.5)
        self.S = get_matrix_scale(s_x=0.5, s_y=1.5)
        self.Score = 0


    def generate_geometry(self):
        self.geometry = np.array([
            [-1, 0],
            [0, 1],
            [1, 0],
            [-1, 0]
        ])


class Asteroid(Character):
    def __init__(self):
        super().__init__()

        self.pos = np.random.random((2,)) * 20.0 - 10.0  # (-10..10, -10..10)
        self.angle = np.random.random() * 360
        self.color = 'b'

    def generate_geometry(self):
        step_t = 2 * np.pi / 20
        radius = np.random.random() * 3 - 2

        list_geometry = []
        t = 0
        while t < np.pi * 2:
            # TODO to distort sphere change radius
            radius += np.random.random() * 0.1 - 0.05
            list_geometry.append(np.array([
                np.cos(t) * radius,
                np.sin(t) * radius]))
            t += step_t

        list_geometry.append(np.array(list_geometry[0]))
        self.geometry = np.array(list_geometry)

class Rocket(Character):
    def __init__(self, player):
        self.geometry = []

        self.angle = player.angle
        self.pos = np.array(player.pos)
        self.dir = np.array(player.dir)
        self.speed = 5e-1

        self.C = np.identity(3)  # Combined
        self.R = np.identity(3)  # Rotation
        self.T = np.identity(3)  # Translation

        self.generate_geometry()
        self.color = 'g'

    def generate_geometry(self):
        self.geometry = np.array([
            [-0.1, 0],
            [0, 0.1],
            [0.1, 0],
            [0.1, -0.1],
            [-0.1, -0.1],
            [-0.1, 0]
        ])


characters = []
player = Player()
characters.append(player)
for _ in range(10):
    characters.append(Asteroid())

is_running = True


def on_press(event):
    global is_running, player
    if event.key == 'escape':
        is_running = False
    elif event.key == 'left':
        player.angle += 5
    elif event.key == 'right':
        player.angle -= 5
    elif event.key == ' ':
        player.Score += 1
        characters.append(Rocket(player))
    # TODO shoot rockets


fig, _ = plt.subplots()
fig.canvas.mpl_connect('key_press_event', on_press)

dt = 1e-1
while is_running:
    plt.clf()
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)

    for each in characters:
        each.draw()
        # TODO display score
        if isinstance(each, Player):
            plt.title(f"score: {each.Score}")

    plt.draw()
    plt.pause(dt)
