"""
AlponaGen v1.1
---------------------
Fractal based mathematical generation of alpona/mandala style images.
This version uses a modular design, separating the generation engine
from the pattern drawing functions.

Author: Aritro Shome
Date: 2025-10-09
"""

from alponagen import ArtGenerator
import colorlog
import argparse

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
logger = colorlog.getLogger('AlponaGen')
logger.addHandler(handler)
logger.setLevel('INFO')

if __name__ == "__main__":
    argparser = argparse.ArgumentParser("AlponaGen")
    argparser.add_argument("-w", "--width", type=int, default=1024, help="Width of the generated image.")
    argparser.add_argument("-ht", "--height", type=int, default=1024, help="Height of the generated image.")
    argparser.add_argument("-out", "--output", type=str, default="output", help="Output directory for generated images.")
    argparser.add_argument("-v", "--version", action="version", version="AlponaGen v1.1", help="Show program version.")
    argparser.add_argument("-count", "-c", type=int, default=10, help="Number of images to generate. Defaults to 10.")
    args = argparser.parse_args()

    logger.info(f"Width: {args.width}")
    logger.info(f"Height: {args.height}")
    logger.info(f"Output Directory: {args.output}")

    gen = ArtGenerator(width=args.width, height=args.height, output_dir=args.output)
    for index in range(10):
        logger.info("Generating alpona...")
        gen.generate("alpona", id=index)
    logger.info(f"\n[+] Generation complete. Check the '{args.output}' directory.")