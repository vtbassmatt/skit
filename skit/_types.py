from typing import NamedTuple
from PIL.ImageFont import FreeTypeFont

# type hint for numbers
Numeric = int | float

class Rect(NamedTuple):
    x: Numeric
    y: Numeric
    width: Numeric
    height: Numeric
