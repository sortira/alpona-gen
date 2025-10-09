"""
AlponaGen v1.1
---------------------
Fractal based mathematical generation of alpona/mandala style images.
This version uses a modular design, separating the generation engine
from the pattern drawing functions.

Author: Aritro Shome
Date: 2025-10-09
"""

import math
import random
import numpy as np

from utils import lerp

def _get_line_width(is_filled):
    """Determines line width: thicker for outlined, thinner for filled."""
    return random.randint(1, 2) if is_filled else random.randint(2, 4)

# --- Triangles ---
def draw_triangles_base(draw, environment, inner_r, outer_r, is_filled):
    """
    Draws a series of triangles arranged in a circular pattern.

    Parameters:
    - draw: The drawing context from PIL.
    - center: Tuple (x, y) representing the center of the circular pattern.
    - inner_r: Radius of the inner circle where triangle bases are anchored.
    - outer_r: Radius of the outer circle where triangle tips are anchored.
    - is_filled: Boolean indicating whether triangles are filled or outlined.
    - white: Base color for the triangles.

    Mathematical Explanation:
    - Each triangle is defined by three points:
      - Two points on the inner circle, calculated using polar coordinates:
        (x, y) = (center_x + inner_r * cos(angle), center_y + inner_r * sin(angle))
      - One point on the outer circle, calculated similarly but using the midpoint angle.
    """
    
    n_triangles = random.randint(16, 30)
    line_width = _get_line_width(is_filled)
    center = environment["center"]
    white = environment["white"]
    for i in range(n_triangles):
        angle1 = 2 * math.pi * i / n_triangles
        angle2 = 2 * math.pi * (i + 1) / n_triangles
        mid_angle = (angle1 + angle2) / 2
        
        # Define the three main points of the triangle
        p1 = (center[0] + inner_r * math.cos(angle1), center[1] + inner_r * math.sin(angle1))
        p2 = (center[0] + inner_r * math.cos(angle2), center[1] + inner_r * math.sin(angle2))
        p3 = (center[0] + outer_r * math.cos(mid_angle), center[1] + outer_r * math.sin(mid_angle))
        
        if is_filled:
            # For a filled shape, we approximate the curved base with many small line segments
            arc_points = []
            num_arc_segments = 10  # More segments = smoother curve
            
            # Generate points along the arc from p2's angle to p1's angle
            for step in range(num_arc_segments + 1):
                t = step / num_arc_segments
                current_angle = lerp(angle2, angle1, t)
                arc_x = center[0] + inner_r * math.cos(current_angle)
                arc_y = center[1] + inner_r * math.sin(current_angle)
                arc_points.append((arc_x, arc_y))

            # The final polygon combines the outer point with the points on the arc
            polygon_points = [p3] + arc_points
            
            draw.polygon(polygon_points, fill=white + (200,), outline=white + (220,) if line_width > 1 else None, width=line_width)
        else:
            # For an outlined shape, we simply draw the two sides, leaving the base open to the circle
            draw.line([p1, p3], fill=white + (200,), width=line_width)
            draw.line([p2, p3], fill=white + (200,), width=line_width)

def draw_triangles_filled(draw, environment, inner_r, outer_r): draw_triangles_base(draw, environment, inner_r, outer_r, True)
def draw_triangles_outlined(draw, environment, inner_r, outer_r): draw_triangles_base(draw, environment, inner_r, outer_r, False)

# --- Circles ---
def draw_circles_base(draw, environment, inner_r, outer_r, is_filled):
    """
    Draws a series of circles arranged in a circular pattern.

    Parameters:
    - draw: The drawing context from PIL.
    - center: Tuple (x, y) representing the center of the circular pattern.
    - inner_r: Radius of the inner circle where circles are placed.
    - outer_r: Radius of the outer circle where circles are placed.
    - is_filled: Boolean indicating whether circles are filled or outlined.
    - white: Base color for the circles.

    Mathematical Explanation:
    - Each circle is defined by:
      - A center point calculated using polar coordinates:
        (x, y) = (center_x + r_placement * cos(theta), center_y + r_placement * sin(theta))
      - A radius derived from the spacing between circles.
    """
    n_circles = random.randint(10, 20)
    line_width = random.randint(1, 2) if is_filled else random.randint(2, 4)
    r_placement = lerp(inner_r, outer_r, random.uniform(0.3, 0.7))
    radius = min((outer_r - inner_r) / random.uniform(2.5, 4.0), (2 * math.pi * r_placement / n_circles) / random.uniform(2.5, 4.0))

    for i in range(n_circles):
        theta = 2 * math.pi * i / n_circles
        x = environment["center"][0] + r_placement * math.cos(theta)
        y = environment["center"][1] + r_placement * math.sin(theta)
        
        if is_filled:
            draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=environment["white"] + (180,), outline=environment["white"] + (200,) if line_width > 1 else None, width=line_width)
        else:
            draw.ellipse([x - radius, y - radius, x + radius, y + radius], outline=environment["white"] + (180,), width=line_width)

def draw_circles_filled(draw, environment, inner_r, outer_r): draw_circles_base(draw, environment, inner_r, outer_r, True)
def draw_circles_outlined(draw, environment, inner_r, outer_r): draw_circles_base(draw, environment, inner_r, outer_r, False)

# --- Petals ---
def draw_petals_base(draw, environment, inner_r, outer_r, is_filled):
    """
    Draws a series of petal-like shapes arranged in a circular pattern.

    Parameters:
    - draw: The drawing context from PIL.
    - center: Tuple (x, y) representing the center of the circular pattern.
    - inner_r: Radius of the inner circle where petal bases are anchored.
    - outer_r: Radius of the outer circle where petal tips are anchored.
    - is_filled: Boolean indicating whether petals are filled or outlined.
    - white: Base color for the petals.

    Mathematical Explanation:
    - Each petal is defined by three points:
      - One point on the inner circle.
      - Two points on the outer circle, offset by ±π/n_petals.
    """
    n_petals = random.randint(10, 20)
    line_width = random.randint(1, 2) if is_filled else random.randint(2, 4)
    for i in range(n_petals):
        angle = 2 * math.pi * i / n_petals
        p1 = (environment["center"][0] + inner_r * math.cos(angle), environment["center"][1] + inner_r * math.sin(angle))
        p2 = (environment["center"][0] + outer_r * math.cos(angle + math.pi / n_petals),
              environment["center"][1] + outer_r * math.sin(angle + math.pi / n_petals))
        p3 = (environment["center"][0] + outer_r * math.cos(angle - math.pi / n_petals),
              environment["center"][1] + outer_r * math.sin(angle - math.pi / n_petals))
        if is_filled:
            draw.polygon([p1, p2, p3], fill=environment["white"] + (180,), outline=environment["white"] + (200,) if line_width > 1 else None, width=line_width)
        else:
            draw.polygon([p1, p2, p3], outline=environment["white"] + (180,), width=line_width)

def draw_petals_filled(draw, environment, inner_r, outer_r): draw_petals_base(draw, environment, inner_r, outer_r, True)
def draw_petals_outlined(draw, environment, inner_r, outer_r): draw_petals_base(draw, environment, inner_r, outer_r, False)

# --- Other Patterns ---
def draw_spiral(draw, environment, inner_r, outer_r):
    """
    Draws a spiral pattern between two radii.

    Parameters:
    - draw: The drawing context from PIL.
    - inner_r: Radius of the inner circle where the spiral starts.
    - outer_r: Radius of the outer circle where the spiral ends.
    - environment: 

    Mathematical Explanation:
    - The spiral is defined by polar coordinates:
      (x, y) = (center_x + r * cos(t), center_y + r * sin(t))
      where r interpolates linearly between inner_r and outer_r as t increases.
    """
    points = []
    turns = random.randint(4, 7)
    line_width = random.randint(1, 2)
    for t in np.linspace(0, 2 * math.pi * turns, 300):
        r = lerp(inner_r, outer_r, t / (2 * math.pi * turns))
        points.append((environment["center"][0] + r * math.cos(t), environment["center"][1] + r * math.sin(t)))
    draw.line(points, fill=environment["white"] + (180,), width=line_width)

# def draw_dots(draw, inner_r, outer_r, environment):
#     """
#     Draws a series of dots arranged in concentric rings.

#     Parameters:
#     - draw: The drawing context from PIL.
#     - inner_r: Radius of the inner circle where dots start.
#     - outer_r: Radius of the outer circle where dots end.
#     - environment: 

#     Mathematical Explanation:
#     - Each ring is defined by:
#       - A radius interpolated between inner_r and outer_r.
#       - Dots placed evenly around the ring using polar coordinates.
#     """
#     n_dots_total = random.randint(80, 150)
#     num_rings = random.randint(2, 4)
#     line_width = random.randint(1, 2)
#     for ring in range(num_rings):
#         r = lerp(inner_r, outer_r, (ring + 1) / (num_rings + 1))
#         n_dots_ring = n_dots_total // num_rings
#         for i in range(n_dots_ring):
#             offset = (math.pi / n_dots_ring) if ring % 2 != 0 else 0
#             theta = (2 * math.pi * i / n_dots_ring) + offset
#             x = environment["center"][0] + r * math.cos(theta)
#             y = environment["center"][1] + r * math.sin(theta)
#             size = random.randint(1, 3)
#             draw.ellipse([x - size, y - size, x + size, y + size], fill=environment["white"] + (200,), outline=environment["white"] + (220,) if line_width > 1 else None, width=line_width)

def draw_radial_lines(draw, environment, inner_r, outer_r):
    n_lines = random.randint(20, 40)
    line_width = _get_line_width(False)
    center = environment["center"]
    white = environment["white"]
    for i in range(n_lines):
        angle = 2 * math.pi * i / n_lines + random.uniform(-0.05, 0.05)
        p1 = (center[0] + inner_r * math.cos(angle), center[1] + inner_r * math.sin(angle))
        p2 = (center[0] + outer_r * math.cos(angle), center[1] + outer_r * math.sin(angle))
        draw.line((p1, p2), fill=white + (180,), width=line_width)

def draw_wave(draw, environment, inner_r, outer_r):
    points = []
    segments = random.randint(50, 80)
    freq = random.choice([5, 7, 9, 11])
    line_width = _get_line_width(False)
    center = environment["center"]
    white = environment["white"]
    for i in range(segments + 1):
        theta = 2 * math.pi * i / segments
        r_offset = (outer_r - inner_r) * (0.5 + 0.5 * math.sin(freq * theta + random.uniform(0, math.pi)))
        r = inner_r + r_offset
        points.append((center[0] + r * math.cos(theta), center[1] + r * math.sin(theta)))
    draw.line(points, fill=white + (180,), width=line_width)

def draw_tesselation(draw, environment, inner_r, outer_r):
    n = random.randint(20, 40)
    line_width = _get_line_width(False)
    center = environment["center"]
    white = environment["white"]
    for i in range(n):
        angle1 = 2 * math.pi * i / n
        angle2 = 2 * math.pi * (i + 1) / n
        p = [(center[0] + inner_r * math.cos(angle1), center[1] + inner_r * math.sin(angle1)),
             (center[0] + inner_r * math.cos(angle2), center[1] + inner_r * math.sin(angle2)),
             (center[0] + outer_r * math.cos((angle1+angle2)/2), center[1] + outer_r * math.sin((angle1+angle2)/2))]
        draw.polygon(p, outline=white + (180,), fill=None, width=line_width)

def draw_crosshatch(draw, environment, inner_r, outer_r):
    line_width = _get_line_width(False)
    center = environment["center"]
    white = environment["white"]
    for direction in [-1, 1]:
        points = []
        turns = random.randint(6, 10)
        for t in np.linspace(0, 2*math.pi*turns, 200):
            r = lerp(inner_r, outer_r, t/(2*math.pi*turns))
            angle_offset = 0.15 * math.sin(t * 0.7)
            points.append((center[0] + r*math.cos(t*direction + angle_offset), center[1] + r*math.sin(t*direction + angle_offset)))
        draw.line(points, fill=white + (150,), width=line_width)

def draw_concentric_rings(draw, environment, inner_r, outer_r):
    num_rings = random.randint(4, 8)
    line_width = _get_line_width(False)
    center = environment["center"]
    white = environment["white"]
    for i in range(num_rings):
        current_r = lerp(inner_r, outer_r, (i + 0.5) / num_rings)
        bbox = [center[0] - current_r, center[1] - current_r, center[0] + current_r, center[1] + current_r]
        draw.ellipse(bbox, outline=white+(180,), width=line_width)

def draw_checkerboard(draw, environment, inner_r, outer_r):
    n_angular = random.randint(32, 64)
    n_radial = random.randint(3, 6)
    center = environment["center"]
    white = environment["white"]
    for j in range(n_radial):
        r1 = lerp(inner_r, outer_r, j / n_radial)
        r2 = lerp(inner_r, outer_r, (j + 1) / n_radial)
        for i in range(n_angular):
            if (i + j) % 2 == 0:
                continue
            angle1 = 2 * math.pi * i / n_angular
            angle2 = 2 * math.pi * (i + 1) / n_angular
            p1 = (center[0] + r1 * math.cos(angle1), center[1] + r1 * math.sin(angle1))
            p2 = (center[0] + r1 * math.cos(angle2), center[1] + r1 * math.sin(angle2))
            p3 = (center[0] + r2 * math.cos(angle2), center[1] + r2 * math.sin(angle2))
            p4 = (center[0] + r2 * math.cos(angle1), center[1] + r2 * math.sin(angle1))
            draw.polygon([p1, p2, p3, p4], fill=white + (180,))

# ----------------------------------------------------------------------
# NEW LAYER STYLES (Added on 2025-10-09)
# ----------------------------------------------------------------------

# --- 1. Sunburst ---
def draw_sunburst_base(draw, environment, inner_r, outer_r, is_filled):
    """
    Draws a series of long, sharp triangular rays, creating a sunburst effect.

    Mathematical Explanation:
    - Each ray is a thin isosceles triangle defined by three points:
      - One point on the inner circle (the base center).
      - Two points on the outer circle, very close to each other to form a sharp tip.
      This is an inverse of the `draw_triangles` pattern for a different aesthetic.
    """
    n_rays = random.randint(24, 48)
    line_width = _get_line_width(is_filled)
    center = environment["center"]
    white = environment["white"]
    for i in range(n_rays):
        angle = 2 * math.pi * i / n_rays
        # Small angle offset for the two outer points
        angle_offset = (math.pi / n_rays) * 0.2
        
        p1 = (center[0] + inner_r * math.cos(angle), center[1] + inner_r * math.sin(angle))
        p2 = (center[0] + outer_r * math.cos(angle - angle_offset), center[1] + outer_r * math.sin(angle - angle_offset))
        p3 = (center[0] + outer_r * math.cos(angle + angle_offset), center[1] + outer_r * math.sin(angle + angle_offset))
        
        if is_filled:
            draw.polygon([p1, p2, p3], fill=white + (200,))
        else:
            draw.polygon([p1, p2, p3], outline=white + (200,), width=line_width)

def draw_sunburst_filled(draw, environment, inner_r, outer_r): draw_sunburst_base(draw, environment, inner_r, outer_r, True)
def draw_sunburst_outlined(draw, environment, inner_r, outer_r): draw_sunburst_base(draw, environment, inner_r, outer_r, False)


# --- 2. Lotus Petals (Rounded) ---
def draw_lotus_petals_base(draw, environment, inner_r, outer_r, is_filled):
    """
    Draws soft, rounded petals resembling a lotus flower.

    Mathematical Explanation:
    - The curve of each petal is approximated by a polygon with many vertices.
    - The path follows a sinusoidal curve from a base point on the inner radius
      out to a maximum width at the midpoint radius, and back to the tip at the outer radius.
    - Two symmetrical curves are generated to form one complete petal.
    """
    n_petals = random.randint(8, 16)
    line_width = _get_line_width(is_filled)
    center = environment["center"]
    white = environment["white"]
    petal_width_factor = (math.pi / n_petals) * 0.8  # Max angular width of a petal

    for i in range(n_petals):
        base_angle = 2 * math.pi * i / n_petals
        
        # Build one half of the petal
        points_half = []
        for t in np.linspace(0, 1, 15): # 15 segments for a smooth curve
            r = lerp(inner_r, outer_r, t)
            # Use sin(t*pi) to make the petal bulge in the middle
            angle_offset = petal_width_factor * math.sin(t * math.pi)
            points_half.append((
                center[0] + r * math.cos(base_angle + angle_offset),
                center[1] + r * math.sin(base_angle + angle_offset)
            ))
        
        # Mirror the half to create the full petal
        points_full = points_half + points_half[-2::-1]
        
        if is_filled:
            draw.polygon(points_full, fill=white + (180,))
        else:
            draw.line(points_full, fill=white + (180,), width=line_width, joint="curve")

def draw_lotus_petals_filled(draw, environment, inner_r, outer_r): draw_lotus_petals_base(draw, environment, inner_r, outer_r, True)
def draw_lotus_petals_outlined(draw, environment, inner_r, outer_r): draw_lotus_petals_base(draw, environment, inner_r, outer_r, False)


# --- 4. Braid ---
def draw_braid(draw, environment, inner_r, outer_r):
    """
    Draws two phase-shifted waves that cross over each other to form a braid.

    Mathematical Explanation:
    - Two separate sinusoidal waves are drawn.
    - Their radii oscillate between `inner_r` and `outer_r` based on their angle `theta`.
    - One wave is given a phase offset of `pi` relative to the other,
      causing them to intersect at the midpoint radius.
    """
    segments = 150
    freq = random.randint(16, 24)
    line_width = _get_line_width(False)
    center = environment["center"]
    white = environment["white"]
    mid_r = (inner_r + outer_r) / 2
    amplitude = (outer_r - inner_r) / 2

    for phase in [0, math.pi]: # Two waves, 180 degrees out of phase
        points = []
        for i in range(segments + 1):
            theta = 2 * math.pi * i / segments
            r = mid_r + amplitude * math.sin(theta * freq + phase)
            points.append((
                center[0] + r * math.cos(theta),
                center[1] + r * math.sin(theta)
            ))
        draw.line(points, fill=white + (180,), width=line_width, joint="curve")

# --- 10. Sprouts ---
def draw_sprouts(draw, environment, inner_r, outer_r):
    """
    Draws a series of 'sprouts', each with a main stem and two branching leaves.

    Mathematical Explanation:
    - A main stem is drawn as a radial line from `inner_r` to `outer_r`.
    - From the midpoint of the stem, two smaller lines (leaves) branch off
      at a fixed angle (e.g., +/- 45 degrees) relative to the stem.
    """
    n_sprouts = random.randint(10, 20)
    line_width = _get_line_width(False)
    center = environment["center"]
    white = environment["white"]
    branch_angle = math.pi / 4 # 45 degrees

    for i in range(n_sprouts):
        angle = 2 * math.pi * i / n_sprouts
        
        # Main stem
        p_start = (center[0] + inner_r * math.cos(angle), center[1] + inner_r * math.sin(angle))
        p_end = (center[0] + outer_r * math.cos(angle), center[1] + outer_r * math.sin(angle))
        draw.line([p_start, p_end], fill=white+(180,), width=line_width)
        
        # Branches
        mid_r = (inner_r + outer_r) / 2
        branch_length = (outer_r - inner_r) * 0.3
        p_mid = (center[0] + mid_r * math.cos(angle), center[1] + mid_r * math.sin(angle))
        
        # Branch 1
        p_branch1 = (p_mid[0] + branch_length * math.cos(angle + branch_angle),
                     p_mid[1] + branch_length * math.sin(angle + branch_angle))
        draw.line([p_mid, p_branch1], fill=white+(180,), width=line_width)
        
        # Branch 2
        p_branch2 = (p_mid[0] + branch_length * math.cos(angle - branch_angle),
                     p_mid[1] + branch_length * math.sin(angle - branch_angle))
        draw.line([p_mid, p_branch2], fill=white+(180,), width=line_width)