# Importing All The Relevant Packages
import sys
import numpy as np
from scipy.integrate import ode
import csv

# Initialising the Parameters
def newton(t, Y, q, m, B, E):
    """Computes the derivative of the state vector y according to the equation of motion:
    Y is the state vector (x, y, z, u, v, w) === (position, velocity).
    returns dY/dt.
    """
    x, y, z = Y[0], Y[1], Y[2]
    u, v, w = Y[3], Y[4], Y[5]
    alphaX = v * B[2] - w * B[1]
    alphaY = w * B[0] - u * B[2]
    alphaZ = u * B[1] - v * B[0]
    return np.array(
        [
            u,
            v,
            w,
            q / m * (alphaX + E[0]),
            q / m * (alphaY + E[1]),
            q / m * (alphaZ + E[2]),
        ]
    )


r = ode(newton).set_integrator("dopri5")

# Inputs From The User

t0 = 0

# print('Enter the coordinates of the initial position of the electron :')
coor_x = float(sys.argv[1])
coor_y = float(sys.argv[2])
coor_z = float(sys.argv[3])
x0 = np.array([int(coor_x), int(coor_y), int(coor_z)])

# print('Enter the initial velocity of the electron:')
vel_x = float(sys.argv[4])
vel_y = float(sys.argv[5])
vel_z = float(sys.argv[6])
v0 = np.array([int(vel_x), int(vel_y), int(vel_z)])

# print('Enter the magnitude of magnetic field in space:')
B_x = float(sys.argv[7])
B_y = float(sys.argv[8])
B_z = float(sys.argv[9])
B0 = np.array([int(B_x), int(B_y), int(B_z)])

# print('Enter the magnitude of electric field in space :')
E_x = float(sys.argv[10])
E_y = float(sys.argv[11])
E_z = float(sys.argv[12])
E0 = np.array([int(E_x), int(E_y), int(E_z)])

Q0 = float(sys.argv[13])

# Radius of the helical path formed
Radius = np.sqrt(v0.dot(v0) - (np.dot(B0, v0) / B0.dot(B0)) ** 2)
print("Radius: ", Radius)

initial_cond = np.concatenate((x0, v0))
r.set_initial_value(initial_cond, t0).set_f_params(int(Q0), 1.0, B0, E0)

positions = []
t1 = 50
dt = 0.05
while r.successful() and r.t < t1:
    r.integrate(r.t + dt)
    positions.append(r.y[:3])  # keeping only position, not velocity


with open("file_io_positions0.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([0, 1, 2])
    writer.writerows(positions)
    del writer
