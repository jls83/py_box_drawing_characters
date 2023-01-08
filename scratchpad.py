from py_box.appearance import LineAppearance, LinePattern, LineWeight
from py_box.box_drawing import BoxDrawing

appearances = []

for line_weight in LineWeight:
    for line_pattern in LinePattern:
        appearances.append(LineAppearance(line_weight, line_pattern))

simple_boxes = [BoxDrawing(line_appearance) for line_appearance in appearances]

two_part_boxes = []
for horiz in appearances:
    for verti in appearances:
        two_part_boxes.append(BoxDrawing(horiz, verti))

four_part_boxes = []
for top in appearances:
    for bottom in appearances:
        for left in appearances:
            for right in appearances:
                four_part_boxes.append(BoxDrawing(top, bottom, left, right))
