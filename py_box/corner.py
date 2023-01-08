from enum import Enum

from .appearance import LineWeight, LinePattern, LineAppearance


KEY_HORIZONTAL = "h"
KEY_VERTICAL = "v"


class CornerDirection(Enum):
    NORTH_WEST = 1
    NORTH_EAST = 2
    SOUTH_EAST = 3
    SOUTH_WEST = 4


class CornerException(Exception):
    pass


class Corner:
    DEFAULT_LINE_WEIGHTS = {
        KEY_HORIZONTAL: LineWeight.LIGHT,
        KEY_VERTICAL: LineWeight.LIGHT,
    }

    DEFAULT_LINE_PATTERNS = {
        KEY_HORIZONTAL: LinePattern.SOLID,
        KEY_VERTICAL: LinePattern.SOLID,
    }

    def __init__(self, direction: CornerDirection, line_weights=DEFAULT_LINE_WEIGHTS,
                 line_patterns=DEFAULT_LINE_PATTERNS):
        self.direction = direction
        self.line_weights = line_weights
        self.line_patterns = line_patterns

    def __repr__(self):
        return f"<Corner: {self.unicode_name}>"

    @property
    def unicode_name(self):
        parts = ["BOX DRAWINGS"]

        # TODO: use match!
        vertical_direction = horizontal_direction = ""
        if self.direction == CornerDirection.NORTH_WEST:
            vertical_direction = "DOWN"
            horizontal_direction = "RIGHT"
        elif self.direction == CornerDirection.NORTH_EAST:
            vertical_direction = "DOWN"
            horizontal_direction = "LEFT"
        elif self.direction == CornerDirection.SOUTH_EAST:
            vertical_direction = "UP"
            horizontal_direction = "LEFT"
        elif self.direction == CornerDirection.SOUTH_WEST:
            vertical_direction = "UP"
            horizontal_direction = "RIGHT"

        # check if the weights are the same; we only want one if so.
        if self.line_weights[KEY_HORIZONTAL] == self.line_weights[KEY_VERTICAL]:
            parts.extend([
                self.line_weights[KEY_VERTICAL].name,
                vertical_direction,
                "AND",
                horizontal_direction,
            ])
        elif self.line_weights[KEY_VERTICAL] == LineWeight.DOUBLE and self.line_weights[KEY_HORIZONTAL] == LineWeight.LIGHT:
            parts.extend([
                vertical_direction,
                self.line_weights[KEY_VERTICAL].name,
                "AND",
                horizontal_direction,
                "SINGLE"
            ])
        elif self.line_weights[KEY_HORIZONTAL] == LineWeight.DOUBLE and self.line_weights[KEY_VERTICAL] == LineWeight.LIGHT:
            parts.extend([
                vertical_direction,
                "SINGLE",
                "AND",
                horizontal_direction,
                self.line_weights[KEY_HORIZONTAL].name,
            ])
        else:
            parts.extend([
                vertical_direction,
                self.line_weights[KEY_VERTICAL].name,
                "AND",
                horizontal_direction,
                self.line_weights[KEY_HORIZONTAL].name,
            ])

        return " ".join(parts)

    @classmethod
    def from_line_appearance(cls, direction: CornerDirection, horizontal: LineAppearance,
                             vertical: LineAppearance):
        line_weights = {
            KEY_HORIZONTAL: horizontal.line_weight,
            KEY_VERTICAL: vertical.line_weight,
        }
        line_patterns = {
            KEY_HORIZONTAL: horizontal.line_pattern,
            KEY_VERTICAL: vertical.line_pattern,
        }
        return cls(direction, line_weights, line_patterns)
