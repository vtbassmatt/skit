from typing import NamedTuple

# type hint for numbers
Numeric = int | float

class Rect(NamedTuple):
    x: Numeric
    y: Numeric
    width: Numeric
    height: Numeric
