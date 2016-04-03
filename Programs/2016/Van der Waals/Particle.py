import random, math, time


def d_vector(p1, p2):
    u = []
    for i in range(len(p1)):
        u.append(p2[i] - p1[i])
    return u


def norm(v):
    u = 0
    for i in range(len(v)):
        u += v[i] ** 2
    return math.sqrt(u)


class Particle:
    def __init__(self, position, velocity, mass):
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.acceleration = []
        for i in range(len(velocity)):
            self.acceleration.append(0)

    def move(self, dt):
        self.position += dt * self.velocity
        self.velocity += dt * self.acceleration

    def collide_check(self, container):
        for i in range(len(container.dimensions)):
            if self.position[i] <= 0:
                self.velocity[i] *= -1
                self.position[i] = 0
            if self.position[i] >= container.dimensions[i]:
                self.velocity[i] *= -1
                self.position[i] = container.dimensions[i]

    def interact(self, container, A, B, a, b):
        for i in range(container.num_particles):
            if container.particles[i] is not self:
                particle = container.particles[i]
                r_vector = d_vector(self.position, particle.position)
                r = norm(r_vector)
                for j in range(container.n):
                    try:
                        self.acceleration[j] += particle.mass * r_vector[j] * (
                        A / math.pow(r, (a + 1)) - B / math.pow(r, (b + 1)))
                    except ZeroDivisionError:
                        self.acceleration[j] += particle.mass * r_vector[j] * (
                        A / (math.pow(r, (a + 1) + 0.001)) - B / (math.pow(r, (b + 1)) + 0.001))


class Container:
    def __init__(self, dimensions, num_particles):
        self.dimensions = dimensions
        self.particles = []
        self.n = len(self.dimensions)
        self.num_particles = num_particles

    def generate_particles(self, mass_interval, velocity_interval):
        for i in range(self.num_particles):
            m = random.uniform(mass_interval[0], mass_interval[1])
            pi = []
            vi = []
            for j in range(self.n):
                vi.append(random.uniform(velocity_interval[0], velocity_interval[1]))
                pi.append(random.uniform(0, self.dimensions[j]))
            particle = Particle(pi, vi, m)
            self.particles.append(particle)


Container = Container((10, 10, 10, 10, 10, 10), 2)
Container.generate_particles((0, 10), (4, 9))
print("mass: {0}".format(Container.particles[1].mass))
print("velocity: {0}".format(Container.particles[1].velocity))
print("position: {0}".format(Container.particles[1].position))
print("acceleration: {0}".format(Container.particles[1].acceleration))
print(" ")

tic = time.clock()
Container.particles[1].interact(Container, 1, 1, 2, 12)
toc = time.clock()

print("new acceleration: {0}".format(Container.particles[1].acceleration))
print("time: {0}".format(toc - tic))

print("position: {0}".format(Container.particles[0].position))
