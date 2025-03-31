import os, json, io
from PIL import Image
import tempfile
import hashlib
import base64

def execute(question: str, parameter, file_bytes = None):
    if file_bytes is None:
        return " No file provided"
    
    file = io.BytesIO(file_bytes)
    scrambled_image = Image.open(file)  # Ensure this is the correct path to your image

    # Define constants
    piece_size = 100  # Each piece is 100x100 pixels (500/5)
    grid_size = 5     # 5x5 grid

    # Create a blank image for the reconstructed result
    reconstructed_image = Image.new("RGB", (500, 500))

    # Mapping of scrambled positions to original positions
    mapping = [
        (2, 1, 0, 0), (1, 1, 0, 1), (4, 1, 0, 2), (0, 3, 0, 3), (0, 1, 0, 4),
        (1, 4, 1, 0), (2, 0, 1, 1), (2, 4, 1, 2), (4, 2, 1, 3), (2, 2, 1, 4),
        (0, 0, 2, 0), (3, 2, 2, 1), (4, 3, 2, 2), (3, 0, 2, 3), (3, 4, 2, 4),
        (1, 0, 3, 0), (2, 3, 3, 1), (3, 3, 3, 2), (4, 4, 3, 3), (0, 2, 3, 4),
        (3, 1, 4, 0), (1, 2, 4, 1), (1, 3, 4, 2), (0, 4, 4, 3), (4, 0, 4, 4)
    ]

    # Rearrange pieces based on mapping
    for original_row, original_col, scrambled_row, scrambled_col in mapping:
        # Calculate coordinates of the scrambled piece
        scrambled_x = scrambled_col * piece_size
        scrambled_y = scrambled_row * piece_size

        # Extract the scrambled piece
        piece = scrambled_image.crop((scrambled_x,
                                    scrambled_y,
                                    scrambled_x + piece_size,
                                    scrambled_y + piece_size))

        # Calculate coordinates for the original position
        original_x = original_col * piece_size
        original_y = original_row * piece_size

        # Paste the piece into its original position in the reconstructed image
        reconstructed_image.paste(piece,
                                (original_x,
                                    original_y))

    buffered = io.BytesIO()
    reconstructed_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # Create Base64 URI
    image_uri = f"data:{parameter["content_type"]};base64,{img_str}"
    return image_uri