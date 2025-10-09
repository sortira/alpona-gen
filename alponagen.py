"""
AlponaGen v1.1
---------------------
Fractal based mathematical generation of alpona/mandala style images.
This version uses a modular design, separating the generation engine
from the pattern drawing functions.

Author: Aritro Shome
Date: 2025-10-09
"""

import os
import random
from PIL import Image, ImageDraw
from datetime import datetime
import colorlog
import uuid

# Local module imports
from utils import ensure_dir
import layer_styles

# Configure colorlog
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s[%(levelname)s] %(message)s',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
))
logger = colorlog.getLogger('ArtGenerator')
logger.addHandler(handler)
logger.setLevel('INFO')

# ----------------------------------------------------------------------
# Art Generator Class
# ----------------------------------------------------------------------

class ArtGenerator:
    """
    Modular generative art engine. 
    
    Available styles: `alpona`

    Usage:
        gen = ArtGenerator(width=1024, height=1024, output_dir="output")
        gen.generate("alpona")
    """

    def __init__(self, width=1024, height=1024, output_dir="output"):
        self.width = width
        self.height = height
        self.output_dir = output_dir
        ensure_dir(output_dir)
        self.styles = {}
        self._register_builtin_styles()
        logger.info("ArtGenerator initialized.")

    # ------------------------------------------------------------------
    # Style Registration System
    # ------------------------------------------------------------------

    def register_style(self, name):
        """Decorator for registering new art generation methods."""
        def decorator(func):
            self.styles[name] = func
            logger.info(f"Style registered: {name}")
            return func
        return decorator

    def _register_builtin_styles(self):
        """Register all internal style methods."""
        for name in dir(self):
            if name.startswith("style_"):
                func = getattr(self, name)
                self.styles[name.replace("style_", "")] = func
                logger.info(f"Builtin style registered: {name.replace('style_', '')}")

    # ------------------------------------------------------------------
    # Main Generation Entry Point
    # ------------------------------------------------------------------

    def generate(self, style_name=None, id = str(uuid.uuid1())):
        """
        Generate one art image and save to output directory.
        """
        if not style_name or style_name not in self.styles:
            logger.info("No style specified. Choosing a random style.")
            style_name = random.choice(list(self.styles.keys()))
        
        logger.critical(f"Generating image with id = {id}")
        logger.info(f"Generating style: {style_name}")

        img = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 255))
        draw = ImageDraw.Draw(img, "RGBA")

        self.styles[style_name](draw)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = os.path.join(self.output_dir, f"image_{id}.png")
        img.save(filename, "PNG")
        logger.info(f"Image saved: {filename}")

    # ------------------------------------------------------------------
    # Style Implementations
    # ------------------------------------------------------------------

    def style_alpona(self, draw):
        """
        Generate an intricate Alpona/Rangoli-inspired circular design.
        The algorithm prioritizes 'filled' layers, ensures symmetrical patterns,
        and makes outlined layers more prominent with thicker lines.
        """
        center = (self.width // 2, self.height // 2)
        n_layers = random.randint(15, 25)
        base_radius = min(self.width, self.height) // 2.2
        
        # Environment dictionary to pass common parameters to pattern functions
        environment = {
            "center": center,
            "white": (245, 245, 240),
            "clay": (110, 60, 40)
        }

        draw.rectangle([0, 0, self.width, self.height], fill=environment["clay"])

        # Categorize styles from the patterns module
        filled_styles = [
            layer_styles.draw_triangles_filled, layer_styles.draw_circles_filled, layer_styles.draw_spiral, 
            # layer_styles.draw_dots, 
            layer_styles.draw_petals_filled, layer_styles.draw_checkerboard
        ]
        outlined_styles = [
            layer_styles.draw_triangles_outlined, layer_styles.draw_circles_outlined, 
            layer_styles.draw_tesselation, layer_styles.draw_petals_outlined, layer_styles.draw_radial_lines, 
            # layer_styles.draw_wave, 
            # layer_styles.draw_crosshatch, 
            layer_styles.draw_concentric_rings
        ]
        
        # ------------------------------------------------------------------
        # Draw concentric layers with logic that prioritizes filling
        # ------------------------------------------------------------------

        last_layer_was_filled = False # want the first layer to be filled, hence driving the motivation
        last_layer_style = None

        for i in range(n_layers):
            inner_r = base_radius * (i / n_layers)
            outer_r = base_radius * ((i + 1) / n_layers)

            if i == 0:
                style = random.choice([layer_styles.draw_spiral, 
                                       # layer_styles.draw_dots, 
                                       layer_styles.draw_circles_filled])
                last_layer_was_filled = True
            else:
                available_styles = (
                    filled_styles if last_layer_was_filled else outlined_styles
                )
                available_styles = [s for s in available_styles if s != last_layer_style]

                if last_layer_was_filled:
                    if random.random() < 0.7:
                        style = random.choice(available_styles)
                        last_layer_was_filled = True
                    else:
                        style = random.choice(available_styles)
                        last_layer_was_filled = False
                else:
                    if random.random() < 0.85:
                        style = random.choice(available_styles)
                        last_layer_was_filled = True
                    else:
                        style = random.choice(available_styles)
                        last_layer_was_filled = False

            last_layer_style = style

            logger.info(f"Layer {i + 1}/{n_layers}: Using style {style.__name__}")

            # Call the selected style function from the patterns module
            style(draw=draw, environment=environment, inner_r=inner_r, outer_r=outer_r)

            # Draw the boundary circle for the layer
            draw.ellipse(
                (center[0] - outer_r, center[1] - outer_r, center[0] + outer_r, center[1] + outer_r),
                outline=environment["white"] + (180,), width=random.randint(1, 3)
            )