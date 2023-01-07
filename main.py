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

class LineDirection(Enum):
    HORIZONTAL = 1
    VERTICAL = 2

class LineAppearance:
    def __init__(self, line_weight: LineWeight, line_something: LineSomething):
        self.line_weight = line_weight
        self.line_something = line_something

class CornerDirection(Enum):
    NORTH_WEST = 1
    NORTH_EAST = 2
    SOUTH_EAST = 3
    SOUTH_WEST = 4

def unicode_name_to_str(unicode_name):
    return u"\\N{{{}}}".format(unicode_name).encode().decode('unicode-escape')

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

        if self.line_appearance.line_something != LineSomething.SOLID:
            parts.append(self.line_appearance.line_something.unicode_name)

        parts.append(self.direction.name)

        return " ".join(parts)

class Corner:
    def __init__(self, direction: CornerDirection, line_weights=None,
                 line_somethings=None):
        self.direction = direction

        if line_weights is None:
            self.line_weights = {
                "h": LineWeight.LIGHT,
                "v": LineWeight.LIGHT,
            }
        else:
            self.line_weights = line_weights


        if line_somethings is None:
            self.line_somethings = {
                "h": LineSomething.SOLID,
                "v": LineSomething.SOLID,
            }
        else:
            self.line_somethings = line_somethings

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
        line_somethings = {
            "h": horizontal.line_something,
            "v": vertical.line_something,
        }
        return cls(direction, line_weights, line_somethings)

# TODO: use a match here...
class BoxDrawing:
    def __init__(self, *args: LineAppearance):
        arg_count = len(args)

        if arg_count in {0, 3}:
            raise Exception
        elif arg_count == 1:  # Same lines on all sides
            self.top = args[0]
            self.bottom = args[0]
            self.left = args[0]
            self.right = args[0]
        elif arg_count == 2:  # Horizontal lines the same, vertical lines the same
            self.top = args[0]
            self.bottom = args[0]
            self.left = args[1]
            self.right = args[1]
        elif arg_count == 4:  # All lines distinct
            self.top = args[0]
            self.bottom = args[1]
            self.left = args[2]
            self.right = args[3]
        else:
            raise Exception

        # TODO: Check DOUBLE vs. HEAVY weights
        # TODO: Check DASH corners

        self._build_corners()
        self._build_edges()

    def _build_corners(self):
        self.nw_corner = Corner.from_line_appearance(CornerDirection.NORTH_WEST, self.top, self.left)
        self.ne_corner = Corner.from_line_appearance(CornerDirection.NORTH_EAST, self.top, self.right)
        self.se_corner = Corner.from_line_appearance(CornerDirection.SOUTH_EAST, self.bottom, self.right)
        self.sw_corner = Corner.from_line_appearance(CornerDirection.SOUTH_WEST, self.bottom, self.left)

    def _build_edges(self):
        self.north = Line(LineDirection.HORIZONTAL, self.top)
        self.south = Line(LineDirection.HORIZONTAL, self.bottom)
        self.east = Line(LineDirection.VERTICAL, self.right)
        self.west = Line(LineDirection.VERTICAL, self.left)

    def print_box(self):
        strs = {
            "nw_corner": self.nw_corner,
            "ne_corner": self.ne_corner,
            "se_corner": self.se_corner,
            "sw_corner": self.sw_corner,
            "north": self.north,
            "south": self.south,
            "east": self.east,
            "west": self.west,
        }

        strs = {k: unicode_name_to_str(v.unicode_name) for k, v in strs.items()}
        
        format_string = "\n".join([
            "{nw_corner}{north}{north}{north}{ne_corner}",
            "{west}   {east}",
            "{sw_corner}{south}{south}{south}{se_corner}",
        ])

        print(format_string.format(**strs))

    def to_telescope_collection(self):
        # top, right, bottom, left, NW, NE, SE, SW
        chars = [
            self.north,
            self.east,
            self.south,
            self.west,
            self.nw_corner,
            self.ne_corner,
            self.se_corner,
            self.sw_corner,
        ]

        return [unicode_name_to_str(char.unicode_name) for char in chars]

