"""Represent meme engine."""
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

    def draw(self, image, text, author, show_image=False):
        """Draw on image.

        :param image: The image that will be drawn on
        :param text: The text that will be drawn on the image
        :param author: The author that will be drawn on the image
        :param show_image: A switch to show the image if needed
        """
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 30)
        color = (0, 0, 0)
        width, height = image.size
        # taking 30% of width and height to hopefully avoid
        # the text running out of image border
        random_location_width = random.randint(0, (width * 0.3))
        random_location_height = random.randint(0, (height * 0.3))
        random_location = (random_location_width, random_location_height)
        draw.text(random_location, f"{text}\n  - {author}", color, font=font)
        if show_image:
            image.show()

    def make_meme(self, img_path, text, author, width=500) -> str:
        """Generate image path.

        :param img_path: The path of the image that will be drawn on
        :param text: The text that will be drawn on the image
        :param author: The author that will be drawn on the image
        :param width:  Maximum width of the image

        :return: Generated image path.
        """
        image = Image.open(img_path)
        maxsize = (width,) * 2
        # image.thumbnail resized image up to max width, height while
        # maintaining original aspect ratio
        image.thumbnail(maxsize, Image.ANTIALIAS)
        self.draw(image, text, author)
        make_dir(self.output_dir)
        filename = os.path.basename(img_path)
        new_path = f"{self.output_dir}/{filename}"
        file_type = filename.split(".")[-1].upper()
        if file_type == "JPG":
            file_type = "JPEG"
        image.save(new_path, file_type)
        return new_path
