import numpy as np


def generate_custom_shape_setup(
    shape: np.ndarray[np.bool_], top_left_x: int, top_left_y: int, color: str = "black"
) -> str:
    """
    Generate NetLogo code to set up a custom shape.

    Args:
    shape (np.ndarray[np.bool_]): 2D boolean array representing the shape.
    top_left_x (int): X-coordinate of the top-left corner.
    top_left_y (int): Y-coordinate of the top-left corner.
    color (str, optional): Color of the cells. Defaults to "black".

    Returns:
    str: NetLogo code to set up the custom shape.
    """
    height, width = shape.shape
    setup_code = []

    for y in range(height):
        for x in range(width):
            if shape[y, x]:
                setup_code.append((x, y))
    return " ".join([f"[{x} {y}]" for x, y in setup_code])
