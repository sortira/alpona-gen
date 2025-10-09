"""
AlponaGen v1
---------------------
Fractal based mathematical generation of alpona/mandala style images

Author: Aritro Shome
Date: 2025-10-09
"""

import os
import random
import numpy as np

def ensure_dir(path: str):
    """Ensure the output directory exists."""
    if not os.path.exists(path):
        os.makedirs(path)

# def random_color(palette=None):
#     """Return a random color from a palette or RGB if none provided."""
#     if palette:
#         return random.choice(palette)
#     return tuple(np.random.randint(0, 256, 3))

def lerp(a, b, t):
    """Linear interpolation between a and b by factor t."""
    return a + (b - a) * t

def get_line_width(is_filled):
    """Returns a line width to draw the shapes of the current layer."""
    return random.randint(1, 2) if is_filled else random.randint(2, 4)