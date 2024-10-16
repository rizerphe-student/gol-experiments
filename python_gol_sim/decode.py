import re

from PIL import Image
import numpy as np


def decode(encoded: str) -> np.ndarray:
    # Extract the dimensions from the second line
    width, height = map(
        lambda x: int(x.split(" = ")[1]), encoded.split(", rule = ")[0].split(", ")
    )

    # Create an empty grid
    grid = np.zeros((height, width), dtype=np.bool_)

    # Extract the pattern from the remaining lines
    pattern = "".join(encoded.split("\n")[1:])

    # Fill the grid with the pattern
    y = 0
    for _, line in enumerate(pattern.split("$")):
        # XXb = XX dead cells; XXo = XX alive cells; b - dead cell, o - alive cell
        x = 0
        for _, cell in enumerate(re.findall(r"\d*[bo]", line)):
            delta = 1 if len(cell) == 1 else int(cell[:-1])
            if cell[-1] == "o":
                if len(cell) == 1:
                    grid[y, x] = True
                else:
                    grid[y, x : x + delta] = True
            x += delta
        # If line ends with a number, increment y by that digit
        if line[-1].isdigit():
            y += int(line[-1])
        else:
            y += 1

    return grid


if __name__ == "__main__":
    decoded = decode(
        """x = 27, y = 27, rule = B3/S23
    18bo$17b3o$12b3o4b2o$11bo2b3o2bob2o$10bo3bobo2bobo$10bo4bobobobob2o$12b
    o4bobo3b2o$4o5bobo4bo3bob3o$o3b2obob3ob2o9b2o$o5b2o5bo$bo2b2obo2bo2bo
    b2o$7bobobobobobo5b4o$bo2b2obo2bo2bo2b2obob2o3bo$o5b2o3bobobo3b2o5bo$
    o3b2obob2o2bo2bo2bob2o2bo$4o5bobobobobobo$10b2obo2bo2bob2o2bo$13bo5b2o
    5bo$b2o9b2ob3obob2o3bo$2b3obo3bo4bobo5b4o$2b2o3bobo4bo$2b2obobobobo4b
    o$5bobo2bobo3bo$4b2obo2b3o2bo$6b2o4b3o$7b3o$8bo!"""
    )

    # Display the decoded pattern
    Image.fromarray(decoded.astype(np.uint8) * 255).resize(
        (decoded.shape[1] * 10, decoded.shape[0] * 10),
        resample=Image.NEAREST,
    ).show()
