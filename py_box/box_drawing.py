from .appearance import LineAppearance
from .corner import Corner, CornerDirection
from .line import Line, LineDirection

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

    @staticmethod
    def unicode_name_to_str(unicode_name):
        return u"\\N{{{}}}".format(unicode_name).encode().decode('unicode-escape')

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

        strs = {k: self.unicode_name_to_str(v.unicode_name) for k, v in strs.items()}
        
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

        return [self.unicode_name_to_str(char.unicode_name) for char in chars]
