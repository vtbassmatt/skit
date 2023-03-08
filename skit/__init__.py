from .deck import Deck
from .card import Card
from ._types import Rect, Color, Alignment, LayoutDef

from PIL import ImageFont


# expose ImageFont.truetype() as skit.load_font()
load_font = ImageFont.truetype


def json_layout_hook(incoming_dict: dict) -> dict | Rect:
    """
    A helper for parsing layouts from JSON.

    Pass this to the `object_hook` parameter of `json.load()` to automatically
    convert dictionaries with the correct keys  into `LayoutDefs`s.
    Correct keys are `x`, `y`, `width`, and `height`, plus optional
    `h_align` and `v_align`.

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
    #   'mybox': LayoutDef(
    #       x=0, y=0, width=100, height=25,
    #       h_align=Alignment.BEGIN, v_align=Alignment.BEGIN,
    #   )
    # }

    ```
    """
    match incoming_dict:
        case { 'x': _, 'y': _, 'width': _, 'height': _, **rest } if len(rest) == 0:
            return LayoutDef(**incoming_dict)
        case { 'x': _, 'y': _, 'width': _, 'height': _, 'h_align': _, **rest } if len(rest) == 0:
            incoming_dict['h_align'] = Alignment(incoming_dict['h_align'])
            return LayoutDef(**incoming_dict)
        case { 'x': _, 'y': _, 'width': _, 'height': _, 'v_align': _, **rest } if len(rest) == 0:
            incoming_dict['v_align'] = Alignment(incoming_dict['v_align'])
            return LayoutDef(**incoming_dict)
        case { 'x': _, 'y': _, 'width': _, 'height': _, 'h_align': _, 'v_align': _, **rest } if len(rest) == 0:
            incoming_dict['h_align'] = Alignment(incoming_dict['h_align'])
            incoming_dict['v_align'] = Alignment(incoming_dict['v_align'])
            return LayoutDef(**incoming_dict)
        case _:
            return incoming_dict


__all__ = [
    'Deck',
    'Card',
    'Rect',
    'Color',
    'Alignment',
    'LayoutDef',
    'load_font',
    'json_layout_hook',
]
