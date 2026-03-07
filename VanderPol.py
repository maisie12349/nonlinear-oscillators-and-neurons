import numpy as np 
import matplotlib.pyplot as plt
import os
from helpers import *

def VanderPolModel(
    x0: float, y0: float, dt: float, numSteps: int, params: ModelParams
) -> tuple[np.array, np.array]:
    eulerPositionValues = [np.array([x0, y0])]
    midpointPositionValues = [np.array([x0, y0])]
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
    # Return the two lists of position values as numpy arrays
    return np.array(eulerPositionValues), np.array(midpointPositionValues)

# Main function
# This code here checks if the file is being run directly and not imported as a module
if __name__ == "__main__":
    """
    Section 1.1 Time-Stepping
    """
    # Define the parameters for the Van der Pol model
    mu = 10
    a = 0
    b = 0
    I = 0
    x0 = 2
    y0 = 0
    endTime = 30
    numSteps = 10000

    # Create the parameters for the Van der Pol model
    params = ModelParams(I, mu, a, b)

    # Run the Van der Pol model
    eulerPositions, midpointPositions = VanderPolModel(
        x0, y0, endTime / numSteps, numSteps, params
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

    fig.savefig("VanderPol/vanderpol_comparison.png", dpi=300)
    plt.close()

    """
    Section 1.2 Convergence of the midpoint method
    """
    fig, axs = plt.subplots()

    mu = 10
    a = 0
    b = 0
    x0 = 2
    y0 = 0
    numSteps = 100000
    endTime = 10
    params = ModelParams(0, mu, 0, 0)
    # Setting the initial arrays

    # This finds all of the values for the given paraemters up to endTime = 10
    eulerPositionsRef, midpointPositionsRef = VanderPolModel(x0, y0, endTime / numSteps, numSteps, params)

    # These are defining my reference values
    referenceFinalPosition = midpointPositionsRef[-1]

    # Generates the values from 10^2 to 10^4
    numStepsValues = np.logspace(2, 4, 10, dtype=int)

    # Define lists for the plot
    dtValues = endTime / numStepsValues
    errors = []
    for numSteps in numStepsValues:
        eulerPositions, midpointPositions = VanderPolModel(x0, y0, endTime / numSteps, numSteps, params)
        finalPosition = midpointPositions[-1]
        err = np.linalg.norm(referenceFinalPosition - finalPosition)
        errors.append(err)

    axs.loglog(dtValues, errors)
    axs.set_xlabel("h (time step)")
    axs.set_ylabel("Error")
    axs.set_title("Log-Log Plot of Error vs h")

    # Save the figure
    # Check if the directory exists, if not create it
    if not os.path.exists("VanderPol"):
        os.makedirs("VanderPol")

    fig.savefig("VanderPol/vanderpol_convergence.png", dpi=300)
    plt.close()
