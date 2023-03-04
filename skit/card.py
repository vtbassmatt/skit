from enum import Enum
import logging
from PIL import Image, ImageDraw, ImageFont
from skit._types import Numeric
from abc import ABC, abstractmethod


logger = logging.getLogger(__file__)


class DrawCommand(Enum):
    TEXT = 'text'


class CardManipulation(ABC):
    @abstractmethod
    def background(self, color: str): pass

    @abstractmethod
    def layout(self, name: str, x: Numeric, y: Numeric, width: Numeric, height: Numeric): pass

    @abstractmethod
    def text(self, text: str, layout: str): pass

    @abstractmethod
    def render_png(self, filename: str): pass


class Card(CardManipulation):
    def __init__(self, width: int = 750, height: int = 1050, dpi: int = 300):
        self._width = width
        self._height = height
        self._dpi = dpi
        self._layouts = {}
        self._background = '#ffffff00'
        self._commands = []

    def background(self, color: str):
        assert type(color) is str

        logger.debug(f"setting background to {color}")
        self._background = color

    def layout(self, name: str, x: Numeric, y: Numeric, width: Numeric, height: Numeric):
        logger.debug(f"creating layout area {name}")
        self._layouts[name] = {
            'x': x,
            'y': y,
            'width': width,
            'height': height,
        }
    
    def text(self, text: str, layout: str):
        assert type(text) is str

        if layout in self._layouts:
            logger.debug(f"adding '{text}' in {layout}")
            self._commands.append({
                'op': DrawCommand.TEXT,
                'layout': layout,
                'text': text,
            })
        else:
            raise KeyError(f"missing layout '{layout}'")

    def render_png(self, filename: str):
        logger.debug(f"rendering {filename}")

        # some defaults for fallback
        default_font = ImageFont.truetype('Helvetica', 16)
        default_color = 'black'

        with Image.new('RGBA', (self._width, self._height), self._background) as im:
            d = ImageDraw.Draw(im)

            for cmd in self._commands:
                match cmd:
                    case {'op': DrawCommand.TEXT, 'layout': layout, 'text': text}:
                        logger.debug(f"rendering text '{text}' at {layout}")
                        layout = self._layouts[layout]
                        d.text((layout['x'], layout['y']), text, fill=default_color, font=default_font)
                    case _:
                        raise ValueError(cmd)

            im.save(filename)
