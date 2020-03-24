# Importing All The Relevant Packages
import sys
import numpy as np
from scipy.integrate import ode

# Initialising the Parameters
def newton(t,Y,q,m,B,E):
    """Computes the derivative of the state vector y according to the equation of motion:
    Y is the state vector (x, y, z, u, v, w) === (position, velocity).
    returns dY/dt.
    """
    x,y,z = Y[0],Y[1],Y[2]
    u,v,w = Y[3],Y[4],Y[5]
    alphaX = v*B[2] - w*B[1]
    alphaY = w*B[0] - u*B[2]
    alphaZ = u*B[1] - v*B[0]
    return np.array([u,v,w,q/m * (alphaX + E[0]),q/m * (alphaY+E[1]),q/m * (alphaZ+E[2])])

r = ode(newton).set_integrator('dopri5')

# Inputs From The User

t0 = 0

print('Enter the coordinates of the initial position of the electron :')
coor_x = sys.argv[1]#input('Enter the x co-ordinate: ')
coor_y = sys.argv[2]#input('Enter the y co-ordinate: ')
coor_z = sys.argv[3]#input('Enter the z co-ordinate: ')
x0 = np.array([int(coor_x),int(coor_y),int(coor_z)])

print('Enter the initial velocity of the electron:')
vel_x = sys.argv[4]#input('Enter the velocity in x direction: ')
vel_y = sys.argv[5]#input('Enter the velocity in y direction: ')
vel_z = sys.argv[6]#input('Enter the velocity in z direction: ')
v0 = np.array([int(vel_x),int(vel_y),int(vel_z)])

print('Enter the magnitude of magnetic field in space:')
B_x = sys.argv[7]#input('Enter the magnitude of magnetic field in x direction: ')
B_y = sys.argv[8]#input('Enter the magnitude of magnetic field in y direction: ')
B_z = sys.argv[9]#input('Enter the magnitude of magnetic field in z direction: ')
B0 = np.array([int(B_x),int(B_y),int(B_z)])

print('Enter the magnitude of electric field in space :')
E_x = sys.argv[10]#input('Enter the magnitude of electric field in x direction: ')
E_y = sys.argv[11]#input('Enter the magnitude of electric field in y direction: ')
E_z = sys.argv[12]#input('Enter the magnitude of electric field in z direction: ')
E0 = np.array([int(E_x),int(E_y),int(E_z)])

Q0 = sys.argv[13]#input('Enter the magnitude of charge: ')

#Radius of the helical path formed
Radius = np.sqrt(v0.dot(v0) - (np.dot(B0,v0)/B0.dot(B0))**2)
print('Radius: ',Radius)

initial_cond = np.concatenate((x0,v0))
r.set_initial_value(initial_cond,t0).set_f_params(int(Q0),1.0,B0,E0)

positions = []
t1 = 50
dt = 0.05
while r.successful() and r.t < t1:
    r.integrate(r.t+dt)
    positions.append(r.y[:3]) # keeping only position, not velocity


with open("file_io_positions0.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow([0, 1, 2])
    writer.writerows(positions)
    del writer
# positions = np.array(positions)

# # Intergrating The Results
# import matplotlib.pyplot as plt

# import matplotlib as mpl
# from mpl_toolkits.mplot3d import Axes3D
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot3D(positions[:, 0], positions[:, 1], positions[:, 2])
# plt.xlabel('x-axis')
# plt.ylabel('y-axis')
# ax.set_zlabel('z-axis')
# mpl.pyplot.title('Flow of Electron', loc='left')
# plt.show()
