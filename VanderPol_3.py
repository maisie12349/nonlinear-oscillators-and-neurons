import numpy as np 
import matplotlib.pyplot as plt
import os
from helpers import *
from VanderPol import * 

# Defining the parameters
mu = 10
params = ModelParams(0, mu, 0, 0)

eulerPositionsExplore, midpointPositionsExplore = VanderPolModel(x0, y0, endTime / numSteps, numSteps, params)
xValuesExplore = midpointPositionsExplore[:, 0]
yValuesExplore = midpointPositionsExplore[:, 1]

if __name__ == "__main__":
    # Define the parameters for the FitzHugh-Nagumo model
    IValues = np.linspace(0, 2, 3)
    muValues = np.linspace(0.1, 60, 5)
    a = 0
    b = 0
    x0 = 2
    y0 = 0
    dt = 0.1
    endTime = 100
    xAxisValues = np.linspace(-2, 2, 100)

    fig, axs = plt.subplots()
    # Run the FitzHugh-Nagumo model for each value of I
    for I in IValues:
        # Create the parameters for the FitzHugh-Nagumo model
        params = ModelParams(I, mu, a, b)
        # Run the FitzHugh-Nagumo model for the current value of I
        positionValues = VanderPolModel(
            x0, y0, dt, endTime, params
        )
        # Plot the position values on a graph
        xValues = positionValues[:, 0]
        yValues = positionValues[:, 1]
        axs.plot(xValues, yValues)
        xNullcline = xNullclineWithParams(I)
        xNullclineValues = xNullcline(xAxisValues)
        axs.plot(xAxisValues, xNullclineValues, linestyle = "--", color = "red", label = f"x Nullcline I = {I}")

    yNullcline = yNullclineWithParams(a, b)
    yNullclineValues = yNullcline(xAxisValues)
    axs.plot(xAxisValues, yNullclineValues, linestyle = "--", color = "blue", label = f"y Nullcline")
    axs.legend()
    axs.set_title("FitzHugh-Nagumo Model Phase Portrait")
    axs.set_xlabel("X")
    axs.set_ylabel("Y")
    # Save the figure
    # Check if the directory exists, if not create it
    if not os.path.exists("FitzHughNagumo"):
        os.makedirs("FitzHughNagumo")

    fig.savefig("FitzHughNagumo/fitzHughNagumo.png", dpi=3