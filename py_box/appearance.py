from enum import Enum

class LineWeight(Enum):
    LIGHT = 1
    HEAVY = 2
    DOUBLE = 3

class LineSomething(Enum):
    SOLID = 1
    DOUBLE_DASH = 2
    TRIPLE_DASH = 3
    QUAD_DASH = 4

    @property
    def unicode_name(self):
        if self is LineSomething.DOUBLE_DASH:
            return "DOUBLE DASH"
        elif self is LineSomething.TRIPLE_DASH:
            return "TRIPLE DASH"
        elif self is LineSomething.QUAD_DASH:
            return "QUADRUPLE DASH"
        return "SOLID"

class LineAppearance:
    def __init__(self, line_weight: LineWeight, line_something: LineSomething):
        self.line_weight = line_weight
        self.line_something = line_something
