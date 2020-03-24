import csv
import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt
import matplotlib as mpl
import math
from mpl_toolkits.mplot3d import Axes3D

def newton(t,Y,q,m,B,E):
    x0,y0,z0 = Y[0],Y[1],Y[2]
    u0,v0,w0 = Y[3],Y[4],Y[5]
    x1,y1,z1 = Y[6],Y[7],Y[8]
    u1,v1,w1 = Y[9],Y[10],Y[11]
    d = math.sqrt((x1-x0)**2+(y1-y0)**2+(z1-z0)**2)
    F = q/(d**2)
     
    alphaX0 = v0*B[2] - w0*B[1] + E[0] + (1/(d**2))*((x0-x1))/d
    alphaY0 = w0*B[0] - u0*B[2] + E[1] + (1/(d**2))*((y0-y1))/d
    alphaZ0 = u0*B[1] - v0*B[0] + E[2] + (1/(d**2))*((z0-z1))/d
    
    alphaX1 = v1*B[2] - w1*B[1] + E[0] + (1/(d**2))*((x1-x0))/d
    alphaY1 = w1*B[0] - u1*B[2] + E[1] + (1/(d**2))*((y1-y0))/d
    alphaZ1 = u1*B[1] - v1*B[0] + E[2] + (1/(d**2))*((z1-z0))/d
    
    x = np.array([u0,v0,w0,q/m * alphaX0,q/m * alphaY0,q/m *alphaZ0,u1,v1,w1,q/m * alphaX1,q/m * alphaY1,q/m *alphaZ1])
    return x

r = ode(newton).set_integrator('dopri5')

t0 = 0
x0 = np.array([1,0,1.5])
v0 = np.array([1,1,0])
x1 = np.array([1,0,-0.5])
v1 = np.array([1,-1,0])

B0 = np.array([2,0,0])
E0 = np.array([0,0,0])
initial_cond = np.concatenate((x0,v0,x1,v1))
m0 = 1.0
q0 = 1.0
r.set_initial_value(initial_cond,t0).set_f_params(q0,m0,B0,E0)

positions0 = []
positions1 = []
t1 = 150
dt = 0.05

maxX,maxY,maxZ = x0[0],x0[1],x0[2]
minX,minY,minZ = x0[0],x0[1],x0[2]

while r.successful() and r.t<t1:
    r.integrate(r.t+dt)
    positions0.append(r.y[:3])
    positions1.append(r.y[6:9])
    maxX,maxY,maxZ = max(maxX,r.y[0],r.y[6]),max(maxY,r.y[1],r.y[7]),max(maxZ,r.y[2],r.y[8])
    minX,minY,minZ = min(minX,r.y[0],r.y[6]),min(minY,r.y[1],r.y[7]),min(minZ,r.y[2],r.y[8])



print(len(positions0[0]))
with open("file_no_io_positions0.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow([0, 1, 2])
    writer.writerows(positions0)
    del writer

with open("file_no_io_positions1.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow([0, 1, 2])
    writer.writerows(positions1)
    del writer

"""
fig = plt.figure()
ax1 = fig.add_subplot(111,projection = '3d')
ax1.plot3D(positions0[:,0],positions0[:,1],positions0[:,2])
ax1.plot3D(positions1[:,0],positions1[:,1],positions1[:,2])
ax1.set_xlabel('x-axis',color='b')
ax1.set_ylabel('y-axis',color='b')
ax1.set_zlabel('z-axis',color='b')
mpl.pyplot.title('Brillouin Flow (Space Charge Effect Considered)', loc='center',color='purple')
plt.show()
"""