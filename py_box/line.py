from enum import Enum

from py_box.appearance import LineAppearance, LinePattern
from py_box.common import IUnicode

class LineDirection(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

class Line(IUnicode):
    def __init__(self, direction: LineDirection, line_appearance: LineAppearance):
        self.direction = direction
        self.line_appearance = line_appearance

        # TODO: check `unicode_name_to_str`, raise exception

    def __repr__(self) -> str:
        return f'<Line: {self.unicode_name}>'

    @property
    def unicode_name(self) -> str:
        parts = ["BOX DRAWINGS", self.line_appearance.line_weight.name]

        if self.line_appearance.line_pattern != LinePattern.SOLID:
            parts.append(self.line_appearance.line_pattern.unicode_name)

        parts.append(self.direction.name)

        return " ".join(parts)

