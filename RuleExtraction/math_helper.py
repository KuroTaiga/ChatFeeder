# math_helper.py

import math
from typing import Tuple

def calculate_angle(a: Tuple[float, float], b: Tuple[float, float], c: Tuple[float, float]) -> float:
    """
    Calculates the angle formed at point b by the line segments ba and bc.

    Args:
        a (Tuple[float, float]): Coordinates of point a (x, y).
        b (Tuple[float, float]): Coordinates of point b (x, y).
        c (Tuple[float, float]): Coordinates of point c (x, y).

    Returns:
        float: The angle in degrees between the lines ba and bc at point b.
    """
    # Calculate the angle using the arctangent of the determinant and dot product
    ab = (a[0] - b[0], a[1] - b[1])
    cb = (c[0] - b[0], c[1] - b[1])
    dot_product = ab[0] * cb[0] + ab[1] * cb[1]
    determinant = ab[0] * cb[1] - ab[1] * cb[0]
    angle = math.degrees(math.atan2(determinant, dot_product))
    angle = angle + 360 if angle < 0 else angle
    return angle

def calculate_distance(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """
    Calculates the Euclidean distance between two points.

    Args:
        a (Tuple[float, float]): Coordinates of point a (x, y).
        b (Tuple[float, float]): Coordinates of point b (x, y).

    Returns:
        float: The distance between points a and b.
    """
    return math.hypot(a[0] - b[0], a[1] - b[1])
