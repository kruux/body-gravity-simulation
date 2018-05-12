# This script simulate bodies in a 3 dimensional system based on gravity.
# We use the leapfrog algorithm as it is symplectic.
# Created by Adam Rosén and Eric Andersson

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d as p3

G = 6.67259e-11     # m^3 kg^-1 s^-2


# Holds 3 dimensional coordinates.
# Doesn't have to be a point, can be a vector or whatever.
class Point:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def get_point_as_list(self):
        return [self.x, self.y, self.z]

    def print_point(self):
        print("x: %d\t\ty: %d\t\tz: %d" % (self.x, self.y, self.z))


# Class for all body object
class Body:
    def __init__(self, name, mass, position, velocity):
        self.name = name
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = Point()
        self.position_list = []

    def add_current_pos_to_list(self):
        pos = self.position
        self.position_list.append([pos.x, pos.y, pos.z])


# The who;e simulation runs through this class
class System:
    def __init__(self, start, stop, dt):
        self.bodies = []
        self.start = start
        self.stop = stop
        self.dt = dt
        self.t = start

    def add_body(self, body):
        if isinstance(body, Body):
            self.bodies.append(body)
            return 0
        else:
            print("Entry must be a body")
            return 1

    def get_bodies(self):
        return self.bodies

    def start_sim(self):
        # Calculate initial acceleration for all bodies
        self.__calculate_acc_for_all_bodies()

        # Update velocity from v_0 to v_1/2
        self.__update_vel_for_all_bodies(dt=self.dt/2)

        self.__add_pos_to_list_for_all_bodies()

        while(self.t <= self.stop):
            self.__update_pos_for_all_bodies()
            self.__calculate_acc_for_all_bodies()
            self.__update_vel_for_all_bodies(self.dt)

            self.__add_pos_to_list_for_all_bodies()

            self.t += self.dt
        return self.bodies

    def __calculate_acc_for_all_bodies(self):
        for body in self.bodies:
            body.acceleration = self.get_acc_for_body(body)

    def __update_vel_for_all_bodies(self, dt):
        for body in self.bodies:
            body.velocity.x += body.acceleration.x * dt
            body.velocity.y += body.acceleration.y * dt
            body.velocity.z += body.acceleration.z * dt

    def __update_pos_for_all_bodies(self):
        for body in self.bodies:
            body.position.x += body.velocity.x * self.dt
            body.position.y += body.velocity.y * self.dt
            body.position.z += body.velocity.z * self.dt

    def get_acc_for_body(self, body):
        acc = Point()

        # Sum up the acceleration that every other body impacts on this one.
        for other_body in self.bodies:
            # Don't calculate the acc of the body with itself
            if body.name != other_body.name:
                dx = body.position.x - other_body.position.x
                dy = body.position.y - other_body.position.y
                dz = body.position.z - other_body.position.z
                r = np.sqrt(dx*dx + dy*dy + dz*dz)

                if r**3 > 10e-10:
                    acc.x += -(G * other_body.mass * dx)/(r**3)
                    acc.y += -(G * other_body.mass * dy)/(r**3)
                    acc.z += -(G * other_body.mass * dz)/(r**3)

        return acc

    def __add_pos_to_list_for_all_bodies(self):
        for body in self.bodies:
            body.add_current_pos_to_list()


def main():
    seconds_per_year = 31556926
    start = 0                       # What time to start and stop the sim
    stop = 160 * seconds_per_year   # 100 years in seconds
    # Decrease h for a more precise result, increase for a faster result
    h = 36000                        # timestep of 36000 seconds

    # Initial values for all the bodies in the system
    sun_name = "Sun"
    sun_mass = 1.99e30
    sun_pos = Point(0, 0, 0)
    sun_vel = Point(0, 0, 0)
    sun = Body(sun_name, sun_mass, sun_pos, sun_vel)

    jup_name = "Jupiter"
    jup_mass = 1.90e27
    jup_pos = Point(0, 7.78e11, 0)
    jup_vel = Point(1.3e4, 0, 0)
    jupiter = Body(jup_name, jup_mass, jup_pos, jup_vel)

    earth_name = 'Earth'
    earth_mass = 5.97e24
    earth_pos = Point(0, 1.50e11, 0)
    earth_vel = Point(2.98e4, 0, 0)
    earth = Body(earth_name, earth_mass, earth_pos, earth_vel)

    venus_name = 'Venus'
    venus_mass = 4.87e24
    venus_pos = Point(0, 1.08e11, 0)
    venus_vel = Point(3.50e4, 0, 0)
    venus = Body(venus_name, venus_mass, venus_pos, venus_vel)

    neptune_name = 'Neptune'
    neptune_mass = 1.02e26
    neptune_pos = Point(0, 4.50e12, 0)
    neptune_vel = Point(5.43e3, 0, 0)
    neptune = Body(neptune_name, neptune_mass, neptune_pos, neptune_vel)

    system = System(start, stop, h)
    system.add_body(sun)
    system.add_body(jupiter)
    system.add_body(earth)
    system.add_body(venus)
    system.add_body(neptune)

    bodies = system.start_sim()

    fig = plt.figure()
    ax = p3.Axes3D(fig)
    ax.set_xlabel("Meters [m]")
    ax.set_ylabel("Meters [m]")
    ax.set_zlabel("Meters [m]")
    ax.set_facecolor('black')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.zaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='z', colors='white')
    ax.w_xaxis.set_pane_color((0, 0, 0, 1))
    ax.w_yaxis.set_pane_color((0, 0, 0, 1))
    ax.w_zaxis.set_pane_color((0, 0, 0, 1))

    # Plot all bodies from the simulation
    for body in bodies:
        coords = body.position_list
        x_pos = np.array([coords[i][0] for i in range(0, len(coords))])
        y_pos = np.array([coords[i][1] for i in range(0, len(coords))])
        z_pos = np.array([coords[i][2] for i in range(0, len(coords))])

        name = body.name.lower()

        if name == "sun":
            ax.scatter(x_pos, y_pos, z_pos, s=50, c="#FFEB65", label=body.name)

        elif name == "earth":
            ax.plot(x_pos, y_pos, z_pos, c="#336FFA", label=body.name)

        elif name == "jupiter":
            ax.plot(x_pos, y_pos, z_pos, c="#B99543", label=body.name)

        else:
            ax.plot(x_pos, y_pos, z_pos, label=body.name)

    ax.legend()
    plt.show()

    return 0


if __name__ == "__main__":
    main()
