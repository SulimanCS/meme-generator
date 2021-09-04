"""Represent models quotes."""
from PIL import Image, ImageFont, ImageDraw
import random
import os


def make_dir(target):
    """Create a target directory.

    :param directory: The dir that should be created if it does not exist
    """
    dir = os.path.join(os.getcwd(), target)
    if not os.path.isdir(dir):
        os.mkdir(dir)


class MemeEngine:
    """A meme engine that generates a memem with an image and a quote."""

    def __init__(self, output_dir):
        """Create a new `MemeEngine`.

        :param output_dir: The dir of where the generated meme should be stored
        """
        self.output_dir = output_dir
