import base64
import re

from io import BytesIO

from PIL import Image, UnidentifiedImageError


def image_to_base64(image: str):
    """Utility function for converting a PIL image to base64."""
    
    format: str = None
    binary: str = None

    # Image format
    format = re.search("\.(.*?)'", str(image))

    if format is not None:
        format = format.group(1)
        # Convert image
        try:
            pic = Image.open(image)
            buffered = BytesIO()
            pic.save(buffered, format="PNG")

            # Clean up result string
            binary = str(base64.b64encode(buffered.getvalue()))
            binary = re.search("'(.*)'", binary).group(1)
        except UnidentifiedImageError:
            format = None
            binary = None

    return format, binary