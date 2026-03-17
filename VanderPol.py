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
        def dx_dt(x, y):
            return x - (1/3)*x**3 - y
        
        def dy_dt(x, y):
            return (1/params.mu) * x

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


'''
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
'''

# Section 1.2 Convergence of the midpoint method
# I am going to define the parameters for the time stepping scheme
mu = 10
a = 0
b = 0
x0 = 2
y0 = 0
dt = 0.0000001
endTime = 0.7
params = ModelParams(0, mu, 0, 0)
print("Checkpoint 2")
# Setting the initial arrays
Error = []
dtA = []

# This finds all of the values for the given paraemters up to endTime = 10
eulerPositionsRef, midpointPositionsRef = VanderPolModel(x0, y0, dt, endTime, params)

# These are defining my reference values
xRef = midpointPositionsRef[-1, 0] 
yRef = midpointPositionsRef[-1, 1]

print("before loop") 
e1, m1 = VanderPolModel(x0, y0, 0.0001, endTime, params)
x1 = m1[-1][0]
y1 = m1[-1][1]
err1 = float(((xRef -x1)**2 + (yRef -y1)**2)**0.5)
e2, m2 = VanderPolModel(x0, y0, 0.001, endTime, params)
x2 = m2[-1][0]
y2 = m2[-1][1]
err2 = float(((xRef -x2)**2 + (yRef -y2)**2)**0.5)
e3, m3 = VanderPolModel(x0, y0, 0.01, endTime, params)
x3 = m3[-1][0]
y3 = m3[-1][0]
err3 = float(((xRef -x3)**2 + (yRef -y3)**2)**0.5)
e4, m4 = VanderPolModel(x0, y0, 0.1, endTime, params)
x4 = m4[-1][0]
y4 = m4[-1][1]
err4 = float(((xRef -x4)**2 + (yRef -y4)**2)**0.5)

'''
error = np.array[err1, err2, err3, err4]
h = np.array[0.0001, 0.001, 0.01, 0.1]

plt.loglog(error, h)
plt.show()

for j in range (10): 
    dt2 = 0.000001 + 0.005*j
    eulerPositionsTemp, midpointPositionsTemp = VanderPolModel(x0, y0, dt2, endTime, params)
    xTempSol = midpointPositionsTemp[-1][0]
    yTempSol = midpointPositionsTemp[-1][1]
    tempError = ((xRef - xTempSol)**2 + (yRef - yTempSol)**2)**0.5
    Error.append(tempError) 
    dtA.append(dt2) 

if __name__ == "__main__":
    axs.plot(np.log10(Error), np.log10(dtA))
    if not os.path.exists("VanderPol"):
        os.makedirs("VanderPol")
    fig.savefig("VanderPol/error_midpoint3.png", dpi=300)
'''

print("I'm finished")


x0 = 0.01
y0 = 0.01
h = 0.001
T = 40
muValues = [0.1 , 4, 100]


def VanderPolModel2(x0, y0, T, h, mu):
    # change vales of params = ModelParams(I, mu, a, b)
    params = ModelParams(0, mu, 0, 0)
    eulerPositions, midpointPositions = VanderPolModel(x0, y0, h, T, params) 

    #define ts, xs, ys
    
    #define time array
    t = np.linspace(0, T, len(midpointPositions))

    # define x(t) and y(t) from midpoint method
    x = midpointPositions[:, 0]
    y = midpointPositions[:, 1]

    return t, x, y
   
#define t, x, y
t, x, y = VanderPolModel2(x0, y0, T, h, mu)


#plot x and y against t 
for mu in muValues:
    T = 0
    if mu == 0.1:
        T=25
    if mu == 4:
        T=50
    if mu == 100:
        T=1000
    t, x, y = VanderPolModel2(x0, y0, T, h, mu)
    plt.figure()
    plt.plot(t,x, label=f"x(t), μ={mu}")       #add labels for each mu value
    plt.plot(t,y, linestyle='--', label=f"y(t), μ={mu}")
    plt.xlabel("t")
    plt.ylabel("solutions")            
    plt.title(f"Variation of x(t) and y(t) against time for μ={mu}")     
    plt.grid(True)                                  #add grid lines          
plt.legend()                            
plt.show()

#plot the phase plane of x against y
for mu in muValues:
    t, x, y = VanderPolModel2(x0, y0, T, h, mu)
    plt.figure()
    plt.plot(x,y, label=f"μ={mu}")
    plt.xlabel("x(t)")
    plt.ylabel("y(t)")
    plt.title(f"Phase plane of trajectories with μ={mu} and nullclines")       #better title?
    plt.grid(True)
    
    #plot y nullcline at x=0
    plt.axvline(x=0, color="red", linestyle='--', label="y-nullcline")
    
    # x-nullcline: y = x - x^3/3
    xGrid = np.linspace(-2.5, 2.5, 400)  
    yNullcline = xGrid - (1/3)*xGrid**3
    plt.plot(xGrid, yNullcline, color="purple", linestyle="--", label="x-nullcline")

plt.legend()
plt.show()

print("working")

#streamplot when mu = 4
def stream_plot(x_range=(-0.5, 0.5, 0.1), y_range=(-0.5, 0.5, 0.1)):
    x = np.arange(*x_range)# * turns tuple into individual function arguments
    y = np.arange(*y_range)
    
    # Create meshgrid
    X, Y = np.meshgrid(x, y)
    
    # Vector field
    xdot = X - (1/3)*X**3 - Y
    ydot = (1/4) * X

    #Plotting
    plt.figure()
    plt.streamplot(X,Y,xdot,ydot)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Solution trajectories illustrated using streamplot when μ=4',
         loc='left')
    plt.axis('equal')
    plt.grid(True)
    plt.show()
    return None

stream_plot(x_range=(-0.5, 0.5, 0.1), y_range=(-0.5, 0.5, 0.1))
plt.show()

#streamplot when mu = 0.1
def stream_plot(x_range=(-0.5, 0.5, 0.1), y_range=(-0.5, 0.5, 0.1)):
    x = np.arange(*x_range)# * turns tuple into individual function arguments
    y = np.arange(*y_range)
    
    # Create meshgrid
    X, Y = np.meshgrid(x, y)
    
    # Vector field
    xdot = X - (1/3)*X**3 - Y
    ydot = (1/0.1) * X

    #Plotting
    plt.figure()
    plt.streamplot(X,Y,xdot,ydot)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Solution trajectories illustrated using streamplot when μ=0.1',
         loc='left')
    plt.axis('equal')
    plt.grid(True)
    plt.show()
    return None

stream_plot(x_range=(-0.5, 0.5, 0.1), y_range=(-0.5, 0.5, 0.1))
plt.show()


#streamplot when mu = 100
def stream_plot(x_range=(-0.5, 0.5, 0.1), y_range=(-0.5, 0.5, 0.1)):
    x = np.arange(*x_range)# * turns tuple into individual function arguments
    y = np.arange(*y_range)
    
    # Create meshgrid
    X, Y = np.meshgrid(x, y)
    
    # Vector field
    xdot = X - (1/3)*X**3 - Y
    ydot = (1/100) * X

    #Plotting
    plt.figure()
    plt.streamplot(X,Y,xdot,ydot)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Solution trajectories illustrated using streamplot when μ=100',
         loc='left')
    plt.axis('equal')
    plt.grid(True)
    plt.show()
    return None

stream_plot(x_range=(-0.5, 0.5, 0.1), y_range=(-0.5, 0.5, 0.1))
plt.show()
