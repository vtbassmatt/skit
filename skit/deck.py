from collections.abc import MutableSequence, Sequence
import logging
from skit.card import Card
from skit._types import Numeric


logger = logging.getLogger(__file__)

class Deck(MutableSequence):
    def __init__(self, card_count: 1):
        self._cards: list[Card] = [Card()] * card_count
    
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
    def background(self, color: str | Sequence[str]):
        if type(color) is str:
            logger.debug(f"Deck.background({color})")
            for card in self._cards:
                card.background(color)
        else:
            logger.debug(f"Deck.background(sequence of colors)")
            for card, _color in zip(self._cards, color):
                card.background(_color)
    
    def layout(self, name: str, x: Numeric, y: Numeric, width: Numeric, height: Numeric):
        logger.debug(f"Deck.layout({name}, ...)")
        for card in self._cards:
            card.layout(name, x, y, width, height)
    
    def text(self, text: str | Sequence[str], layout: str):
        if type(text) is str:
            logger.debug(f"Deck.text({text})")
            for card in self._cards:
                card.text(text, layout)
        else:
            logger.debug(f"Deck.text(sequence of strings)")
            for card, _text in zip(self._cards, text):
                card.text(_text, layout)
    #endregion

    def __str__(self):
        return ", ".join([f"{idx}: {c}" for idx, c in enumerate(self._cards)])
