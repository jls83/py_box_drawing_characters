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


class LineAppearanceException(Exception):
    pass


class LineAppearance:
    def __init__(self, line_weight: LineWeight, line_pattern: LinePattern):
        if line_weight == LineWeight.DOUBLE and line_pattern != LinePattern.SOLID:
            raise LineAppearanceException(
                f"Cannot create `LineAppearance` with `DOUBLE` line weight and "
                f"`{line_pattern.name}` line pattern"
            )

        self.line_weight = line_weight
        self.line_pattern = line_pattern

    def __repr__(self):
        return f"<LineAppearance: {self.line_weight.name}-{self.line_pattern.name}>"
