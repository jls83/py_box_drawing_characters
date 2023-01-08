from enum import Enum

from py_box.appearance import LineWeight, LinePattern, LineAppearance
from py_box.common import IUnicode


KEY_HORIZONTAL = "h"
KEY_VERTICAL = "v"


class CornerDirection(Enum):
    NORTH_WEST = 1
    NORTH_EAST = 2
    SOUTH_EAST = 3
    SOUTH_WEST = 4


class CornerException(Exception):
    pass


class CornerLineWeights:
    def __init__(self, horizontal, vertical):
        self.horizontal = horizontal
        self.vertical = vertical


class CornerLinePatterns:
    def __init__(self, horizontal, vertical):
        self.horizontal = horizontal
        self.vertical = vertical


class Corner(IUnicode):
    DEFAULT_LINE_WEIGHTS = CornerLineWeights(
        LineWeight.LIGHT,
        LineWeight.LIGHT,
    )

    DEFAULT_LINE_PATTERNS = CornerLinePatterns(
        LinePattern.SOLID,
        LinePattern.SOLID,
    )

    def __init__(self, direction: CornerDirection, line_weights=DEFAULT_LINE_WEIGHTS,
                 line_patterns=DEFAULT_LINE_PATTERNS):
        self.direction = direction
        self.line_weights = line_weights
        self.line_patterns = line_patterns

    def __repr__(self) -> str:
        return f"<Corner: {self.unicode_name}>"

    @property
    def unicode_name(self) -> str:
        parts = ["BOX DRAWINGS"]

        match self.direction:
            case CornerDirection.NORTH_WEST:
                vertical_direction, horizontal_direction = "DOWN", "RIGHT"
            case CornerDirection.NORTH_EAST:
                vertical_direction, horizontal_direction = "DOWN", "LEFT"
            case CornerDirection.SOUTH_EAST:
                vertical_direction, horizontal_direction = "UP", "LEFT"
            case CornerDirection.SOUTH_WEST:
                vertical_direction, horizontal_direction = "UP", "RIGHT"
            # Because we match against the enum cases, we should never get here!
            case _:
                raise Exception

        match self.line_weights:
            # check if the weights are the same; we only want one if so.
            case CornerLineWeights(horizontal=h, vertical=v) if h == v:
                chg = [v.name, vertical_direction, "AND", horizontal_direction]
            # We can't build `Corner` objects if one weight is `DOUBLE` and the other is not `LIGHT` or `DOUBLE`.
            case CornerLineWeights(horizontal=LineWeight.DOUBLE, vertical=other)\
                    | CornerLineWeights(horizontal=other, vertical=LineWeight.DOUBLE)\
                    if other != LineWeight.LIGHT:
                raise CornerException(f"Cannot build `Corner` with line_weights `{other.name}` and `DOUBLE`")
            # if we have a DOUBLE weight and a LIGHT weight, change the LIGHT name to "SINGLE"
            case CornerLineWeights(horizontal=LineWeight.DOUBLE, vertical=_):
                chg = [vertical_direction, LineWeight.DOUBLE.name, "AND", horizontal_direction, "SINGLE"]
            # Same here
            case CornerLineWeights(horizontal=_, vertical=LineWeight.DOUBLE):
                chg = [vertical_direction, "SINGLE", "AND", horizontal_direction, LineWeight.DOUBLE.name]
            # The "regular" case
            case CornerLineWeights(horizontal=h, vertical=v):
                chg = [vertical_direction, v.name, "AND", horizontal_direction, h.name]
            # Because we match against the enum cases, we should never get here!
            case _:
                raise Exception

        parts.extend(chg)

        return " ".join(parts)

    @classmethod
    def from_line_appearance(cls, direction: CornerDirection, horizontal: LineAppearance,
                             vertical: LineAppearance):
        line_weights = CornerLineWeights(
            horizontal=horizontal.line_weight,
            vertical=vertical.line_weight,
        )
        line_patterns = CornerLinePatterns(
            horizontal=horizontal.line_pattern,
            vertical=vertical.line_pattern,
        )
        return cls(direction, line_weights, line_patterns)
