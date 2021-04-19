"""Dummy challenge for Kitt Demo"""
import numpy as np

def circle_area(radius):
    """Returns the area of the circle of given radius"""
    return np.pi * radius ** 2 if radius >= 0 else 0
