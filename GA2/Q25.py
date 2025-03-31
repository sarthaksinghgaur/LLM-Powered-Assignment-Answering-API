import os, json
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import colorsys
import os

def execute(question: str, parameter, file_bytes):
    image_file = BytesIO(file_bytes)
    no_of_pixels = number_of_pixel(image_file)
    return no_of_pixels


def number_of_pixel(image_file):

    image = Image.open(image_file)
    # Convert to RGB mode to remove alpha (if present)
    image = image.convert("RGB")

    # Convert image to numpy array and normalize
    rgb = np.array(image) / 255.0

    # Apply colorsys.rgb_to_hls only on RGB values (avoid alpha channel)
    lightness = np.apply_along_axis(lambda x: colorsys.rgb_to_hls(*x[:3])[1], 2, rgb)

    # Count pixels with lightness > 0.667
    light_pixels = np.sum(lightness > 0.667)

    return int(light_pixels)