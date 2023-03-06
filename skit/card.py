from collections.abc import Sequence
from enum import Enum
import logging
from pathlib import Path
from typing import Mapping
from PIL import Image, ImageDraw, ImageFont
from skit._types import Real, LayoutDef, Color, FreeTypeFont, Alignment
from abc import ABC, abstractmethod


logger = logging.getLogger(__file__)


# some defaults for fallback
_DEFAULT_FONT = ImageFont.truetype('Helvetica', 16)
_DEFAULT_COLOR = 'black'
_DEFAULT_THICKNESS = 1

class _DrawCommand(Enum):
    TEXT = 'text'
    RECTANGLE = 'rect'
    IMAGE = 'image'


class CardManipulation(ABC):
    @abstractmethod
    def background(self, color: str): pass

    @abstractmethod
    def layout(self, name: str, layoutdef: LayoutDef): pass

    @abstractmethod
    def layouts(self, names: Sequence[str], layoutdefs: Sequence[LayoutDef]): pass

    @abstractmethod
    def layouts_map(self, layouts: Mapping[str, LayoutDef]): pass

    @abstractmethod
    def text(
        self, text: str,
        layout: str,
        font: FreeTypeFont | None,
        color: Color | None,
    ): pass

    @abstractmethod
    def rectangle(
        self,
        layout: str,
        color: Color | None,
        thickness: Real | None,
    ): pass

    @abstractmethod
    def image(
        self,
        image: Path,
        layout: str,
    ): pass

    @abstractmethod
    def render_png(self, filename: str): pass


class Card(CardManipulation):
    "A single card."
    def __init__(self, width: int = 750, height: int = 1050):
        self._width = width
        self._height = height
        self._layouts = {}
        self._background = '#ffffff00'
        self._commands = []

    def background(self, color: str):
        "Set the background color for this card."
        assert type(color) is str

        logger.debug(f"setting background to {color}")
        self._background = color

    def layout(self, name: str, layoutdef: LayoutDef):
        "Create a new layout for this card."
        assert Alignment(layoutdef.h_align)
        assert Alignment(layoutdef.v_align)

        logger.debug(f"creating layout area {name}")
        self._layouts[name] = {
            'x': layoutdef.x,
            'y': layoutdef.y,
            'width': layoutdef.width,
            'height': layoutdef.height,
            'h_align': layoutdef.h_align,
            'v_align': layoutdef.v_align,
        }
    
    def layouts(self, names: Sequence[str], layoutdefs: Sequence[LayoutDef]):
        "Create multiple layouts for this card."
        assert len(names) == len(layoutdefs), "mismatched names/layoutdefs arguments"
        
        for name, layoutdef in zip(names, layoutdefs):
            self.layout(name, layoutdef)

    def layouts_map(self, layouts: Mapping[str, LayoutDef]):
        "Create multiple layouts from a dictionary."
        for name, layoutdef in layouts.items():
            self.layout(name, layoutdef)

    def text(self, text: str, layout: str, font: FreeTypeFont | None = None, color: Color | None = None):
        "Add text to this card."
        assert type(text) is str

        if layout in self._layouts:
            logger.debug(f"adding '{text}' in {layout}")
            self._commands.append({
                'op': _DrawCommand.TEXT,
                'layout': layout,
                'text': text,
                'font': font,
                'color': color,
            })
        else:
            raise KeyError(f"missing layout '{layout}'")

    def rectangle(self, layout: str, color: Color | None = None, thickness: Real | None = None):
        "Draw a rectangle on this card."
        if layout in self._layouts:
            logger.debug(f"adding rectangle for {layout}")
            self._commands.append({
                'op': _DrawCommand.RECTANGLE,
                'layout': layout,
                'color': color,
                'thickness': thickness,
            })
        else:
            raise KeyError(f"missing layout '{layout}'")

    def image(self, image: Path, layout: str):
        "Draw an external image on this card."
        if layout in self._layouts:
            logger.debug(f"adding image for {layout}")
            self._commands.append({
                'op': _DrawCommand.IMAGE,
                'layout': layout,
                'image': image,
            })
        else:
            raise KeyError(f"missing layout '{layout}'")

    def render_png(self, filename: str):
        "Render this card as a PNG."
        logger.debug(f"rendering {filename}")

        with Image.new('RGBA', (self._width, self._height), self._background) as im:
            d = ImageDraw.Draw(im)

            for cmd in self._commands:
                op = cmd.pop('op')
                match op:
                    case _DrawCommand.TEXT:
                        self._render_png_text(d, **cmd)
                    case _DrawCommand.RECTANGLE:
                        self._render_png_rectangle(d, **cmd)
                    case _DrawCommand.IMAGE:
                        self._render_png_image(im, **cmd)
                    case _:
                        raise ValueError(cmd)

            im.save(filename)

    def _render_png_text(self, d, layout, text, color, font):
        logger.debug(f"rendering text '{text}' at {layout}")
        layout = self._layouts[layout]
        d.text(
            [layout['x'], layout['y']],
            text,
            fill=color if color else _DEFAULT_COLOR,
            font=font if font else _DEFAULT_FONT,
        )
    
    def _render_png_rectangle(self, d, layout, color, thickness):
        logger.debug(f"rendering rectangle on {layout}")
        layout = self._layouts[layout]
        d.rectangle(
            [
                layout['x'],
                layout['y'],
                layout['x'] + layout['width'],
                layout['y'] + layout['height'],
            ],
            outline=color if color else _DEFAULT_COLOR,
            width=thickness if thickness else _DEFAULT_THICKNESS,
        )

    def _render_png_image(self, im, layout, image):
        logger.debug(f"rendering image at {layout}")
        layout = self._layouts[layout]
        with Image.open(image) as art:
            match layout['h_align']:
                case Alignment.BEGIN:
                    left = layout['x']
                case Alignment.MIDDLE:
                    left = layout['x'] + (layout['width'] - art.width) // 2
                case Alignment.END:
                    left = layout['x'] + layout['width'] - art.width
                case _:
                    raise ValueError(f"h_align value '{layout['h_align']}' unrecognized")

            match layout['v_align']:
                case Alignment.BEGIN:
                    top = layout['y']
                case Alignment.MIDDLE:
                    top = layout['y'] + (layout['height'] - art.height) // 2
                case Alignment.END:
                    top = layout['y'] + layout['height'] - art.height
                case _:
                    raise ValueError(f"v_align value '{layout['v_align']}' unrecognized")

            im.alpha_composite(art, (left, top))
