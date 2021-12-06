import base64
import re

from io import BytesIO

from PIL import Image


def image_to_base64(image: str):
    """Utility function for converting a PIL image to base64."""

    # Image format
    format = re.search("\.(.*?)'", str(image))

    if format is None:
        format = None
        binary = None
    else:
        format = format.group(1)
        # Convert image
        pic = Image.open(image)
        buffered = BytesIO()
        pic.save(buffered, format="PNG")

        # Clean up result string
        binary = str(base64.b64encode(buffered.getvalue()))
        binary = re.search("'(.*)'", binary).group(1)

    return format, binary