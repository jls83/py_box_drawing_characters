from typing import List

from py_box.appearance import LineAppearance
from py_box.corner import Corner, CornerDirection
from py_box.line import Line, LineDirection


class BoxDrawingException(Exception):
    pass


class BoxDrawing:
    def __init__(self, *args: LineAppearance):
        arg_count = len(args)

        correct_arg_count = (arg_count in {1, 2, 4})
        all_are_line_appearance = all(type(arg) == LineAppearance for arg in args)

        if not (correct_arg_count and all_are_line_appearance):
            raise BoxDrawingException(
                f"Cannot create `BoxDrawing` from these items: {args}"
            )
        elif arg_count == 1:  # Same lines on all sides.
            self.top = self.bottom = self.left = self.right = args[0]
        elif arg_count == 2:  # Parallel lines match.
            self.top, self.left = args
            self.bottom, self.right = self.top, self.left
        elif arg_count == 4:  # All lines distinct.
            self.top, self.bottom, self.left, self.right = args

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

    @property
    def preview_string(self) -> str:
        strs = {
            "nw_corner": self.nw_corner.unicode_str,
            "ne_corner": self.ne_corner.unicode_str,
            "se_corner": self.se_corner.unicode_str,
            "sw_corner": self.sw_corner.unicode_str,
            "north": self.north.unicode_str,
            "south": self.south.unicode_str,
            "east": self.east.unicode_str,
            "west": self.west.unicode_str,
        }

        format_string = "\n".join([
            "{nw_corner}{north}{north}{north}{ne_corner}",
            "{west}   {east}",
            "{sw_corner}{south}{south}{south}{se_corner}",
        ])

        return format_string.format(**strs)

    def print_box(self):
        print(self.preview_string)

    def to_telescope_collection(self) -> List[str]:
        # top, right, bottom, left, NW, NE, SE, SW
        chars = [
            self.north.unicode_str,
            self.east.unicode_str,
            self.south.unicode_str,
            self.west.unicode_str,
            self.nw_corner.unicode_str,
            self.ne_corner.unicode_str,
            self.se_corner.unicode_str,
            self.sw_corner.unicode_str,
        ]

        return chars
