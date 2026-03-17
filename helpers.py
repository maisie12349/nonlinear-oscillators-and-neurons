from typing import Callable

def euler_step_2d(
    prevX: float,
    prevY: float,
    dt: float,
    dx_dt: Callable[[float, float], float],
    dy_dt: Callable[[float, float], float],
) -> tuple[float, float]:
    """
    Euler time stepping method for solving 2D ODEs.
    """
    newX = prevX + dt * dx_dt(prevX, prevY)
    newY = prevY + dt * dy_dt(prevX, prevY)
    return newX, newY

def midpoint_step_2d(
    prevX: float,
    prevY: float,
    dt: float,
    dx_dt: Callable[[float, float], float],
    dy_dt: Callable[[float, float], float],
) -> tuple[float, float]:
    """
    Midpoint method for solving 2D ODEs.
    """
    midX = prevX + dt / 2 * dx_dt(prevX, prevY)
    midY = prevY + dt / 2 * dy_dt(prevX, prevY)
    newX = prevX + dt * dx_dt(midX, midY)
    newY = prevY + dt * dy_dt(midX, midY)
    return newX, newY

def dx_dtWithParams(I: float = 0) -> Callable[[float, float], float]:
    """
    Returns a dx/dt function with the given parameters
    """
    # Create a function that returns the dx/dt function with the given parameters
    def dx_dt(x, y):
        return _dx_dt(x, y, I)
    return dx_dt

def dy_dtWithParams(
    mu: float, a: float = 0, b: float = 0
) -> Callable[[float, float], float]:
    """
    Returns a dy/dt function with the given parameters
    """
    # Creates a function that returns the dy/dt function with the given parameters
    def dy_dt(x, y):
        return _dy_dt(x, y, mu, a, b)
    return dy_dt

def _dx_dt(x: float, y: float, I: float) -> float:
    return x - 1 / 3 * x**3 - y + I

def _dy_dt(x: float, y: float, mu: float, a: float, b: float) -> float:
    return 1 / mu * (x - a * y + b)

def xNullclineWithParams(I: float) -> Callable[[float], float]:
    """
    Returns a function that calculates the x nullcline
    """
    def xNullcline(x: float) -> float:
        return x - 1 / 3 * x**3 + I
    return xNullcline

def yNullclineWithParams(a: float, b: float) -> Callable[[float], float]:
    """
    Returns a function that calculates the y nullcline
    """
    def yNullcline(x: float) -> float:
        return (x + b) / a
    return yNullcline

class ModelParams:
    def __init__(self, I: float, mu: float, a: float, b: float):
        self.I = I
        self.mu = mu
        self.a = a
        self.b = b

def setFont():
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    import matplotlib
    import os

    _font_path = os.path.join(
        matplotlib.get_data_path(), "fonts", "ttf", "STIXGeneral.ttf"
    )
    fm.fontManager.addfont(_font_path)
    _prop = fm.FontProperties(fname=_font_path)
    plt.rcParams["font.family"] = _prop.get_name()