import logging
from skit._types import Numeric


logger = logging.getLogger(__file__)

class Card:
    def __init__(self):
        self.layouts = {}

    def background(self, color: str):
        assert type(color) is str

        print(f"setting background to {color}")

    def layout(self, name: str, x: Numeric, y: Numeric, width: Numeric, height: Numeric):
        print(f"creating layout area {name}")
        self.layouts[name] = {
            'x': x,
            'y': y,
            'width': width,
            'height': height,
        }
    
    def text(self, text: str, layout: str):
        assert type(text) is str

        if layout in self.layouts:
            print(f"writing '{text}' in {layout}")
        else:
            raise KeyError(f"missing layout '{layout}'")
