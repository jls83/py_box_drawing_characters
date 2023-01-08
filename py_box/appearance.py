from enum import Enum

class LineWeight(Enum):
    LIGHT = 1
    HEAVY = 2
    DOUBLE = 3

class LinePattern(Enum):
    SOLID = 1
    DOUBLE_DASH = 2
    TRIPLE_DASH = 3
    QUAD_DASH = 4

    @property
    def unicode_name(self):
        if self is LinePattern.DOUBLE_DASH:
            return "DOUBLE DASH"
        elif self is LinePattern.TRIPLE_DASH:
            return "TRIPLE DASH"
        elif self is LinePattern.QUAD_DASH:
            return "QUADRUPLE DASH"
        return "SOLID"

class LineAppearance:
    def __init__(self, line_weight: LineWeight, line_pattern: LinePattern):
        self.line_weight = line_weight
        self.line_pattern = line_pattern
