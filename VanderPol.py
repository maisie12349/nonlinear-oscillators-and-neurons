import numpy as np 
import matplotlib.pyplot as plt
import os
from helpers import *

def VanderPolModel(
    x0: float, y0: float, dt: float, endTime: float, params: ModelParams
) -> tuple[float, float]:
    eulerPositionValues = [np.array([x0, y0])]
    midpointPositionValues = [np.array([x0, y0])]
    numSteps = int(endTime / dt)
    print("VC1")
    for _ in range(numSteps):
        # Gets the dx/dt and dy/dt functions with the parameters so we can time step the model
        # The euler method requires a dx_dt and dy_dt function with two parameters (x, y)
        # So by using dx_dtWithParams and dy_dtWithParams, we can pass the parameters (I, mu, a, b) to the functions
        dx_dt = dx_dtWithParams(params.I)
        dy_dt = dy_dtWithParams(params.mu, params.a, params.b)

        prevEulerPosition = eulerPositionValues[-1]
        prevMidpointPosition = midpointPositionValues[-1]

        # Run the euler method with the previously calculated position and the parameters
        eulerX, eulerY = euler_step_2d(prevEulerPosition[0], prevEulerPosition[1], dt, dx_dt, dy_dt)
        midpointX, midpointY = midpoint_step_2d(prevMidpointPosition[0], prevMidpointPosition[1], dt, dx_dt, dy_dt)
        
        eulerPositionValues.append(np.array([eulerX, eulerY]))
        midpointPositionValues.append(np.array([midpointX,midpointY]))
    print("VC2")
    # Return the two lists of position values as numpy arrays
    return np.array(eulerPositionValues), np.array(midpointPositionValues)


# Main function
# This code here checks if the file is being run directly and not imported as a module
if __name__ == "__main__":
    # Define the parameters for the Van der Pol model
    mu = 10
    a = 0
    b = 0
    I = 0
    x0 = 2
    y0 = 0
    dt = 0.1
    endTime = 30

    # Create the parameters for the Van der Pol model
    params = ModelParams(I, mu, a, b)

    # Run the Van der Pol model
    eulerPositions, midpointPositions = VanderPolModel(
        x0, y0, dt, endTime, params
    )

    # Plot the positions on a graph
    eulerXValues = eulerPositions[:, 0]
    eulerYValues = eulerPositions[:, 1]
    midpointXValues = midpointPositions[:, 0] 
    midpointYValues = midpointPositions[:, 1]

    fig, axs = plt.subplots()

    axs.plot(eulerXValues, eulerYValues, color = "darkblue", label = "Euler")
    axs.plot(midpointXValues, midpointYValues, linestyle = "--", color = "red", label = "Midpoint")

    axs.set_title("Van der Pol: Euler & Midpoint")
    axs.set_xlabel("X")
    axs.set_ylabel("Y")
    axs.legend()
    # Save the figure
    # Check if the directory exists, if not create it
    if not os.path.exists("VanderPol"):
        os.makedirs("VanderPol")

    fig.savefig("VanderPol/vanderpol.png", dpi=300)
print("Checkpoint1")

print(midpointXValues)
print(midpointYValues)

'''
# Section 1.2 Convergence of the midpoint method
# I am going to define the parameters for the time stepping scheme
mu = 10
a = 0
b = 0
x0 = 2
y0 = 0
dt = 0.000001
endTime = 1
params = ModelParams(0, mu, 0, 0)
print("Checkpoint 2")
# Setting the initial arrays
Error = []
dtA = []

# This finds all of the values for the given paraemters up to endTime = 10
RefArray, yRefArray = VanderPolModel(x0, y0, dt, endTime, params) 

# These are defining my reference value
xRefSol = RefArray[-1][0]
yRefSol = RefArray[-1][1]
print("before loop") 


for j in range (4): 
    dt = dt*10 
    TempArray = VanderPolModel(x0, y0, dt, endTime, params)
    xTempSol = TempArray[-1][0]
    yTempSol = TempArray[-1][1]
    tempError = ((xRefSol - xTempSol)**0.5 + (yRefSol - yTempSol)**2)**0.5
    Error.append(tempError) 
    dtA.append(dt) 

if __name__ == "__main__":
    axs.plot(np.log(Error), np.log(dtA))
    if not os.path.exists("VanderPol"):
        os.makedirs("VanderPol")
    fig.savefig("VanderPol/error_midpoint.png", dpi=300)

print(np.log(Error), np.log(dtA))
    
'''