import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
# Import the helpers module
from helpers import *


def fitzHughNagumoModel(
    x0: float, y0: float, dt: float, endTime: float, params: ModelParams
) -> tuple[np.array[float, float], np.array[float]]:
    positionValues = [np.array([x0, y0])]
    numSteps = int(endTime / dt)
    timeValues = [0]

    for _ in range(numSteps):
        # Gets the dx/dt and dy/dt functions with the parameters so we can time step the model
        # The euler method requires a dx_dt and dy_dt function with two parameters (x, y)
        # So by using dx_dtWithParams and dy_dtWithParams, we can pass the parameters (I, mu, a, b) to the functions
        dx_dt = dx_dtWithParams(params.I)
        dy_dt = dy_dtWithParams(params.mu, params.a, params.b)
        prevPosition = positionValues[-1]
        prevTime = timeValues[-1]
        # Run the euler method with the current position and the parameters
        eulerX, eulerY = euler_step_2d(
            prevPosition[0], prevPosition[1], dt, dx_dt, dy_dt
        )
        time = prevTime + dt
        positionValues.append(np.array([eulerX, eulerY]))
        timeValues.append(time)

    # Return the position values as a numpy array
    return np.array(positionValues), np.array(timeValues)


# Main function
if __name__ == "__main__":
    setFont()
    # Define the parameters for the FitzHugh-Nagumo model
    IValues = [0.2, 1.0, 1.8]
    mu = 10
    a = 0.8
    b = 0.7
    x0 = 2
    y0 = 0
    dt = 0.1
    endTime = 100
    xLimits = (-3, 4)
    yLimits = (-2, 3.5)
    xAxisValues = np.linspace(xLimits[0], xLimits[1], 100)

    colors = {
        0: ["#62A1A4", "#568C8F"],
        1: ["#F2AD00", "#FFA244"],
        2: ["#AD84FF", "#843EB9"],
    }

    # Clean the generated directory
    if os.path.exists("FitzHughNagumo/Generated"):
        shutil.rmtree("FitzHughNagumo/Generated")
    os.makedirs("FitzHughNagumo/Generated/PhasePortrait")
    os.makedirs("FitzHughNagumo/Generated/TimeSeries")

    # Run the FitzHugh-Nagumo model for each value of I
    for index, I in enumerate(IValues):
        """
        Phase portrait plot
        """
        fig, axs = plt.subplots()

        # Create the parameters for the FitzHugh-Nagumo model
        params = ModelParams(I, mu, a, b)
        # Run the FitzHugh-Nagumo model for the current value of I
        eulerPositionValues, timeValues = fitzHughNagumoModel(
            x0, y0, dt, endTime, params
        )
        # Plot the position values on a graph
        eulerXValues = eulerPositionValues[:, 0]
        eulerYValues = eulerPositionValues[:, 1]

        axs.plot(
            eulerXValues,
            eulerYValues,
            color=colors[index][1],
            label=f"Trajectory",
            zorder=10,
        )

        xNullcline = xNullclineWithParams(I)
        xNullclineValues = xNullcline(xAxisValues)
        axs.plot(
            xAxisValues,
            xNullclineValues,
            linestyle="--",
            color=colors[index][0],
            label=f"dx/dt = 0",
            alpha=0.7,
            zorder=5,
        )

        yNullcline = yNullclineWithParams(a, b)
        yNullclineValues = yNullcline(xAxisValues)
        axs.plot(
            xAxisValues,
            yNullclineValues,
            linestyle="--",
            color="#717171",
            label=f"dy/dt = 0",
            alpha=0.7,
            zorder=5,
        )

        axs.legend(loc="upper right")

        axs.set_xlim(xLimits)
        axs.set_ylim(yLimits)
        axs.set_xlabel("x(t)")
        axs.set_ylabel("y(t)")
        axs.grid(True, color="gray", alpha=0.2)
        axs.set_aspect("equal")
        axs.set_xticks(np.arange(xLimits[0], xLimits[1] + 0.01, 1))
        axs.set_yticks(np.arange(yLimits[0], yLimits[1] + 0.01, 1))
        axs.set_title(f"I = {I:.2f} FitzHugh-Nagumo Model Phase Portrait")

        fig.savefig(
            f"FitzHughNagumo/Generated/PhasePortrait/fitzHughNagumo_I={I:.2f}.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.close()

    xLimits = (0, 70)
    yLimits = (-4, 4)
    endTime = xLimits[1]
    xAxisValues = np.linspace(xLimits[0], xLimits[1], 100)

    for index, I in enumerate(IValues):
        """
        Time series plot
        """
        fig, axs = plt.subplots()

        # Create the parameters for the FitzHugh-Nagumo model
        params = ModelParams(I, mu, a, b)
        # Run the FitzHugh-Nagumo model for the current value of I
        eulerPositionValues, timeValues = fitzHughNagumoModel(
            x0, y0, dt, endTime, params
        )
        # Plot the position values on a graph
        eulerXValues = eulerPositionValues[:, 0]
        eulerYValues = eulerPositionValues[:, 1]

        axs.plot(timeValues, eulerXValues, color="#FCBA56", label=f"Trajectory")
        axs.plot(timeValues, eulerYValues, color="#51C0E8", label="y(t)")
        axs.legend(loc="upper right")
        axs.set_xlim(xLimits)
        axs.set_ylim(yLimits)
        axs.set_xlabel("x(t)")
        axs.set_ylabel("y(t)")
        axs.grid(True, color="gray", alpha=0.2)
        axs.set_xticks(np.arange(xLimits[0], xLimits[1] + 0.01, 10))
        axs.set_yticks(np.arange(yLimits[0], yLimits[1] + 0.01, 2))
        axs.set_title(f"I = {I:.2f} FitzHugh-Nagumo Model Time Series")

        fig.savefig(
            f"FitzHughNagumo/Generated/TimeSeries/fitzHughNagumo_I={I:.2f}_timeSeries.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.close()
