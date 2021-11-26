from PIL import Image
from io import BytesIO
import base64
import re


'''
    Utility function for converting a PIL image
    to base64
'''
def image_to_base64(profile_pic: str):
    format = re.search("\.(.*?)'", str(profile_pic)).group(1)

    pic = Image.open(profile_pic)
    buffered = BytesIO()
    pic.save(buffered, format="PNG")
    binary = str(base64.b64encode(buffered.getvalue()))
    binary = re.search("'(.*)'", binary).group(1)

    return format, binary