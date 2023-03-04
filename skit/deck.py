from collections.abc import MutableSequence, Sequence
import logging
import warnings
from skit.card import Card, CardManipulation
from skit._types import Numeric


logger = logging.getLogger(__file__)

class Deck(MutableSequence, CardManipulation):
    def __init__(self, card_count: 1):
        self._cards: list[Card] = [Card() for _ in range(card_count)]
    
    #region MutableSequence
    def __getitem__(self, index):
        return self._cards[index]
    
    def __delitem__(self, index):
        del self._cards[index]
    
    def __iter__(self):
        return self._cards.__iter__()

    def __len__(self) -> int:
        return len(self._cards)
    
    def __setitem__(self, index, value):
        self._cards[index] = value
    
    def insert(self, index, value):
        self._cards.insert(index, value)
    #endregion

    #region Card manipulation
    def background(self, color: str):
        logger.debug(f"Deck.background({color})")
        for card in self._cards:
            card.background(color)
    
    def layout(self, name: str, x: Numeric, y: Numeric, width: Numeric, height: Numeric):
        logger.debug(f"Deck.layout({name}, ...)")
        for card in self._cards:
            card.layout(name, x, y, width, height)
    
    def text(self, text: str, layout: str):
        logger.debug(f"Deck.text({text})")
        for card in self._cards:
            card.text(text, layout)
    
    def render_png(self, filename: str):
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
        logger.debug(f"Deck.backgrounds(sequence of colors)")
        for card, color in zip(self._cards, colors):
            card.background(color)

    def texts(self, texts: Sequence[str], layout: str):
        logger.debug(f"Deck.texts(sequence of strings)")
        for card, text in zip(self._cards, texts):
            card.text(text, layout)
    #endregion

    def __str__(self):
        return ", ".join([f"{idx}: {c}" for idx, c in enumerate(self._cards)])
