from enum import Enum
from typing import NamedTuple, NewType
from numbers import Real
from PIL.ImageFont import FreeTypeFont

class Rect(NamedTuple):
    "A rectangle, the basic data structure used throughout Skit."
    x: Real
    y: Real
    width: Real
    height: Real


class Alignment(Enum):
    "Where to align items in a layout."
    BEGIN = 'begin' # left or top
    MIDDLE = 'middle'
    END = 'end' # right or bottom


class LayoutDef(NamedTuple):
    "A rectangle plus alignment information."
    x: Real
    y: Real
    width: Real
    height: Real
    h_align: Alignment = Alignment.BEGIN
    v_align: Alignment = Alignment.BEGIN

# color - thin wrapper on str right now, and there are only
# some forms that PIL allows, so this should be smarter one day
# https://pillow.readthedocs.io/en/stable/reference/ImageColor.html
Color = NewType('Color', str)

__all__ = [
    'Real',
    'FreeTypeFont',
    'Rect',
    'Alignment',
    'LayoutDef',
    'Color',
]