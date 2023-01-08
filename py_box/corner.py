from enum import Enum

from .appearance import LineWeight, LinePattern, LineAppearance

class CornerDirection(Enum):
    NORTH_WEST = 1
    NORTH_EAST = 2
    SOUTH_EAST = 3
    SOUTH_WEST = 4

class Corner:
    def __init__(self, direction: CornerDirection, line_weights=None,
                 line_patterns=None):
        self.direction = direction

        if line_weights is None:
            self.line_weights = {
                "h": LineWeight.LIGHT,
                "v": LineWeight.LIGHT,
            }
        else:
            self.line_weights = line_weights


        if line_patterns is None:
            self.line_patterns = {
                "h": LinePattern.SOLID,
                "v": LinePattern.SOLID,
            }
        else:
            self.line_patterns = line_patterns

    def __repr__(self):
        return f'<Corner: {self.unicode_name}>'

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
        if self.line_weights["h"] == self.line_weights["v"]:
            parts.extend([
                self.line_weights["v"].name,
                vertical_direction,
                "AND",
                horizontal_direction,
            ])
        elif self.line_weights["v"] == LineWeight.DOUBLE and self.line_weights["h"] == LineWeight.LIGHT:
            parts.extend([
                vertical_direction,
                self.line_weights["v"].name,
                "AND",
                horizontal_direction,
                "SINGLE"
            ])
        elif self.line_weights["h"] == LineWeight.DOUBLE and self.line_weights["v"] == LineWeight.LIGHT:
            parts.extend([
                vertical_direction,
                "SINGLE",
                "AND",
                horizontal_direction,
                self.line_weights["h"].name,
            ])
        else:
            parts.extend([
                vertical_direction,
                self.line_weights["v"].name,
                "AND",
                horizontal_direction,
                self.line_weights["h"].name,
            ])

        return " ".join(parts)

    @classmethod
    def from_line_appearance(cls, direction: CornerDirection, horizontal: LineAppearance,
                             vertical: LineAppearance):
        line_weights = {
            "h": horizontal.line_weight,
            "v": vertical.line_weight,
        }
        line_patterns = {
            "h": horizontal.line_pattern,
            "v": vertical.line_pattern,
        }
        return cls(direction, line_weights, line_patterns)


