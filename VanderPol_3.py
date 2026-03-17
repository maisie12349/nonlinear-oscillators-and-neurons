import numpy as np 
import matplotlib.pyplot as plt
import os
from helpers import *
from VanderPol import * 

# Parameters of the system 
mu = 2

# Create a grod in the phase plane 
x_vals = np.linspace(-2.5,2.5,25)
y_vals = np.linspace(-2.5,2.5,25)
X, Y = np.meshgrid(x_vals, y_vals) 

# Vector field components 
F = X - (1/3)*X**3 - Y 
G = X/mu 

# Normalise vectors to show direction only 
magnitude = np.sqrt(F**2 + G**2) 
F_hat = F / magnitude
G_hat = G / magnitude

# Nullclines 
def x_nullclineVP(x):
    y = x - (1/3)*x**3
    return y 

def y_nullclineVP(x):
    x = 0
    return 0 

yXNullcline = np.array(x_nullclineVP(x_vals))
x_vals_yN = np.linspace(0,0,25)

plt.figure(figsize =(7, 7))
# Plot the vector field 
plt.plot(x_vals, yXNullcline, label = "x-nullcline")
plt.plot(x_vals_yN, y_vals, label = "y-nullcline")
plt.quiver(X, Y, F_hat, G_hat, color = "gray")
plt.legend()
plt.title("Phase plane mu = 2, with nullclines")
plt.xlabel("x values")
plt.ylabel("y values")
plt.show()
# plot x(t) against time and y(t) against time
