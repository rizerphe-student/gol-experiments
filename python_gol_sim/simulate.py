import cv2
import numpy as np

from python_gol_sim.decode import decode


def simulate(grid: np.ndarray[np.bool_]):
    # Run the game of life simulation, expanding the edges as needed and showing the entire grid

    grid = grid.astype(np.uint8)

    while True:
        # Check if any cells are near the borders, if so - expand 2x in each of the occupied directions
        if grid[0].any():
            grid = np.vstack((np.zeros(grid.shape, dtype=np.bool_), grid))
        if grid[-1].any():
            grid = np.vstack((grid, np.zeros(grid.shape, dtype=np.bool_)))
        if grid[:, 0].any():
            grid = np.hstack((np.zeros(grid.shape, dtype=np.bool_), grid))
        if grid[:, -1].any():
            grid = np.hstack((grid, np.zeros(grid.shape, dtype=np.bool_)))

        # Sum up the neighbors of each cell, by rolling the grid and adding it to itself
        neighbors = (
            np.roll(grid, (-1, -1), (0, 1))
            + np.roll(grid, (-1, 0), (0, 1))
            + np.roll(grid, (-1, 1), (0, 1))
            + np.roll(grid, (0, -1), (0, 1))
            + np.roll(grid, (0, 1), (0, 1))
            + np.roll(grid, (1, -1), (0, 1))
            + np.roll(grid, (1, 0), (0, 1))
            + np.roll(grid, (1, 1), (0, 1))
        )

        # Apply the game of life rules
        grid = (grid & (neighbors == 2)) | (neighbors == 3)

        # Display the grid
        cv2.imshow("Game of Life", grid * 255)

        # Break if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


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
    simulate(decoded)
