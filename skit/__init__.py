from .deck import Deck
from .card import Card
from ._types import Rect, Color

from PIL import ImageFont


# expose ImageFont.truetype() as skit.load_font()
load_font = ImageFont.truetype


def json_layout_hook(incoming_dict: dict) -> dict | Rect:
    """
    A helper for parsing layouts from JSON.

    Pass this to the `object_hook` parameter of `json.load()` to automatically
    convert dictionaries with keys `x`, `y`, `width`, and `height` into `Rect`s.

    Example:

    ```
    with open('my_layout.json') as json_in:
        layouts = json.load(json_in, object_hook=skit.json_layout_hook)
    
    # assuming my_layout.json looked like this:
    # {
    #   "mybox": {
    #     "x": 0,
    #     "y": 0,
    #     "width": 100,
    #     "height": 25
    # }
    #
    # then layouts will be equivalent to this:
    # {
    #   'mybox': Rect(x=0, y=0, width=100, height=25)
    # }

    ```
    """
    match incoming_dict:
        case { 'x': _, 'y': _, 'width': _, 'height': _, **rest } if len(rest) == 0:
            return Rect(**incoming_dict)
        case _:
            return incoming_dict


__all__ = [
    'Deck',
    'Card',
    'Rect',
    'Color',
    'load_font',
    'json_layout_hook',
]
