from typing import NamedTuple, NewType
from PIL.ImageFont import FreeTypeFont

# type hint for numbers
Numeric = int | float

class Rect(NamedTuple):
    x: Numeric
    y: Numeric
    width: Numeric
    height: Numeric

# color - thin wrapper on str right now, and there are only
# some forms that PIL allows, so this should be smarter one day
# https://pillow.readthedocs.io/en/stable/reference/ImageColor.html
Color = NewType('Color', str)
