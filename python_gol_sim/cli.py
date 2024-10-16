import sys

from PIL import Image
import click
import numpy as np

from .codegen import generate_custom_shape_setup
from .decode import decode


@click.command()
@click.option(
    "--output", "-o", type=click.File("w"), help="Output file (default: stdout)"
)
def main(output):
    """Generate NetLogo code for a custom shape."""
    shape_lines = []
    for line in sys.stdin:
        shape_lines.append(line.strip())
        if line.strip()[-1] == "!":
            break

    shape = decode("\n".join(shape_lines))
    height, width = shape.shape

    # Calculate center position
    center_x = -75
    center_y = 0
    top_left_x = center_x - width // 2
    top_left_y = center_y + height // 2

    # Check if shape is too large
    if (
        top_left_x < -125
        or top_left_x + width > -25
        or top_left_y > 125
        or top_left_y - height < -125
    ):
        click.echo(
            "Warning: Shape is too large for the specified area. Centering at (0, 0).",
            err=True,
        )
        top_left_x = -width // 2
        top_left_y = height // 2

    # Display the shape
    Image.fromarray(shape.astype(np.uint8) * 255).resize(
        (shape.shape[1] * 4, shape.shape[0] * 4),
        resample=Image.BOX,
    ).show()

    netlogo_code = generate_custom_shape_setup(shape, top_left_x, top_left_y)

    netlogo_code = open("head.txt").read() + netlogo_code + open("tail.txt").read()

    if output:
        output.write(netlogo_code)
    else:
        click.echo(netlogo_code)


if __name__ == "__main__":
    main()
