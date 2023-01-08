from enum import Enum

from .appearance import LineAppearance, LineSomething

class LineDirection(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

class Line:
    def __init__(self, direction: LineDirection, line_appearance: LineAppearance):
        self.direction = direction
        self.line_appearance = line_appearance

        # TODO: check `unicode_name_to_str`, raise exception

    def __repr__(self):
        return f'<Line: {self.unicode_name}>'

    @property
    def unicode_name(self):
        parts = ["BOX DRAWINGS", self.line_appearance.line_weight.name]

        if self.line_appearance.line_pattern != LineSomething.SOLID:
            parts.append(self.line_appearance.line_pattern.unicode_name)

        parts.append(self.direction.name)

        return " ".join(parts)

