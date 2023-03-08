from collections.abc import MutableSequence, Sequence
import logging
from pathlib import Path
from typing import Iterator, Self, Mapping
import warnings
from skit.card import Card, CardManipulation
from skit._types import Real, LayoutDef, Color, FreeTypeFont


logger = logging.getLogger(__file__)

class Deck(MutableSequence, CardManipulation):
    "A deck of one or more cards."
    def __init__(self, card_count: int = 1, width: int | None = None, height: int | None = None):
        opts = {}
        if width: opts['width'] = width
        if height: opts['height'] = height
        self._cards: list[Card] = [Card(**opts) for _ in range(card_count)]
    
    #region MutableSequence
    def __getitem__(self, index) -> Card:
        return self._cards[index]
    
    def __delitem__(self, index) -> None:
        del self._cards[index]
    
    def __iter__(self) -> Iterator[Card]:
        return self._cards.__iter__()

    def __len__(self) -> int:
        return len(self._cards)
    
    def __setitem__(self, index, value) -> None:
        self._cards[index] = value
    
    def insert(self, index, value) -> None:
        self._cards.insert(index, value)
    #endregion

    #region Container convenience
    def __add__(self, other: Self) -> Self:
        if not issubclass(type(other), Deck):
            raise NotImplemented

        d = Deck(0)
        d._cards = self._cards + other._cards
        return d
    #endregion

    #region Card manipulation
    def background(self, color: str):
        "Set the background color for all cards in this deck."
        logger.debug(f"Deck.background({color})")
        for card in self._cards:
            card.background(color)
    
    def layout(self, name: str, layoutdef: LayoutDef):
        "Add a layout to every card in this deck."
        logger.debug(f"Deck.layout({name}, ...)")
        for card in self._cards:
            card.layout(name, layoutdef)
    
    def layouts(self, names: Sequence[str], layoutdefs: Sequence[LayoutDef]):
        "Add multiple layouts to every card in this deck."
        logger.debug(f"Deck.layouts(sequence of layouts)")
        for card in self._cards:
            card.layouts(names, layoutdefs)

    def layouts_map(self, layouts: Mapping[str, LayoutDef]):
        "Add multiple layouts from a dictionary to every card in this deck."
        logger.debug(f"Deck.layouts_map(map of name->layouts)")
        for card in self._cards:
            card.layouts_map(layouts)

    def text(self, text: str, layout: str, font: FreeTypeFont | None = None, color: Color | None = None):
        "Add a text string to every card in this deck."
        logger.debug(f"Deck.text({text})")
        for card in self._cards:
            card.text(text, layout, font, color)
    
    def rectangle(self, layout: str, color: Color | None = None, thickness: Real | None = None):
        "Draw a rectangle on every card in this deck."
        logger.debug(f"Deck.rect({layout})")
        for card in self._cards:
            card.rectangle(layout, color, thickness)

    def image(self, image: Path, layout: str):
        "Draw an image on every card in this deck."
        logger.debug(f"Deck.image({image})")
        for card in self._cards:
            card.image(image, layout)

    def render_png(self, filename: str):
        """
        Render every card in this deck as a PNG.

        You may use `{index}` as part of the filename to ensure each card gets
        a unique name.
        """
        logger.debug(f"Deck.render_png({filename})")

        if '{index}' not in filename:
            warnings.warn("'{index}' isn't in the filename, so images may overwrite one another")

        for index, card in enumerate(self._cards):
            card.render_png(filename.format_map({
                'index': index,
            }))
    #endregion

    #region Card sequence manipulation
    def backgrounds(self, colors: Sequence[str]):
        "Add (potentially different) backgrounds to each card in this deck."
        logger.debug(f"Deck.backgrounds(sequence of colors)")
        for card, color in zip(self._cards, colors):
            card.background(color)

    def texts(self, texts: Sequence[str], layout: str, font: FreeTypeFont | None = None, color: Color | None = None):
        "Add (potentially different) text strings to each card in this deck."
        logger.debug(f"Deck.texts(sequence of strings)")
        for card, text in zip(self._cards, texts):
            card.text(text, layout, font, color)

    def images(self, images: Sequence[Path], layout: str):
        "Draw (potentially different) external images on each card in this deck."
        logger.debug(f"Deck.images(sequence of images)")
        for card, image in zip(self._cards, images):
            card.image(layout, image, layout)
    #endregion

    def __str__(self):
        return ", ".join([f"{idx}: {c}" for idx, c in enumerate(self._cards)])
