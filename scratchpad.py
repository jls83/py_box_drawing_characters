from py_box.appearance import LineAppearance, LineAppearanceException, LinePattern, LineWeight
from py_box.box_drawing import BoxDrawing, BoxDrawingException
from py_box.corner import CornerException

appearances = []

for line_weight in LineWeight:
    for line_pattern in LinePattern:
        try:
            appearances.append(LineAppearance(line_weight, line_pattern))
        except LineAppearanceException:
            continue

simple_boxes = [BoxDrawing(line_appearance) for line_appearance in appearances]

two_part_boxes = []
for horiz in appearances:
    for verti in appearances:
        try:
            two_part_boxes.append(BoxDrawing(horiz, verti))
        except (BoxDrawingException, CornerException):
            continue

four_part_boxes = []
for top in appearances:
    for bottom in appearances:
        for left in appearances:
            for right in appearances:
                try:
                    four_part_boxes.append(BoxDrawing(top, bottom, left, right))
                except (BoxDrawingException, CornerException):
                    continue
