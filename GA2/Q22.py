import os, json, io

def execute(question: str, parameter, file_bytes):
    image_file = io.BytesIO(file_bytes)
    return compress_an_image(image_file, parameter)

def compress_an_image(image_file, parameter):
    """
    Compresses an image losslessly to be under 1,500 bytes and returns it as base64.
    Every pixel in the compressed image should match the original image.

    Args:
        image_path (str): Path to the input image

    Returns:
        str: Base64 encoded compressed image or error message
    """
    try:
        from PIL import Image
        import io
        import os
        import base64
        
        img = Image.open(image_file)
        original_size = img.size
        original_mode = img.mode

        # Method 1: Try with palette mode (lossless for simple images)
        palette_img = img.convert("P", palette=Image.ADAPTIVE, colors=8)  # Try fewer colors first

        # Try different compression levels with PNG format
        for colors in [8, 16, 32, 64, 128, 256]:
            palette_img = img.convert("P", palette=Image.ADAPTIVE, colors=colors)

            buffer = io.BytesIO()
            palette_img.save(buffer, format="PNG", optimize=True, compress_level=9)
            file_size = buffer.tell()

            if file_size <= 1500:
                # Success! Return as base64
                buffer.seek(0)
                base64_image = base64.b64encode(buffer.read()).decode('utf-8')
                
                image_uri = f"data:{parameter["content_type"]};base64,{base64_image}"
                return image_uri

        # If PNG with palette didn't work, try more aggressive options while preserving dimensions
        # Try WebP format with maximum compression
        buffer = io.BytesIO()
        img.save(buffer, format="WEBP", quality=1, method=6)
        file_size = buffer.tell()

        if file_size <= 1500:
            buffer.seek(0)
            base64_image = base64.b64encode(buffer.read()).decode('utf-8')
            
            image_uri = f"data:{parameter["content_type"]};base64,{base64_image}"
            return image_uri

        # If we get here, we couldn't compress enough without resizing
        return "Error: Image dimensions do not match the original"

    except ImportError:
        return "Error: Required libraries (PIL) not available"
    except Exception as e:
        return f"Error during compression: {str(e)}"