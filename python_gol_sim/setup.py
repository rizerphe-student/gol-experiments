from PIL import Image
import numpy as np

from .codegen import generate_custom_shape_setup
from .decode import decode
from .simulate_against import simulate_against


field = np.zeros((100, 125))
top_left_x = -125
top_left_y = 0

# Generate the great wall of China
field[0, :249] = 1
# field[-1, :249] = 1

for i in range(125):
    if i % 3 != 1:
        field[2, i] = 1
        field[3, i] = 1
        # field[-3, i] = 1
        # field[-4, i] = 1

field[6:8, 2:4] = 1
# field[-9:-7, 2:4] = 1
field[6:8, 14:16] = 1
# field[-9:-7, 14:16] = 1

# Gun prot
for x in range(15, 60):
    for y in range(28, 48):
        if x % 3 and 0 < (y % 10) < 3:
            field[x, y] = 1

# Spaceship
spaceship = decode("""x = 5, y = 4, rule = B3/S23
bo2bo$o$o3bo$4o!""").T

for y in range(34, 110, 6):
    field[-5:, y : y + 4] = spaceship[::-1, :]
    field[-13:-8, y : y + 4] = spaceship[::-1, :]

for y in range(112, 125, 7):
    for x in range(-5, -30, -8):
        field[x : x + 5 or None, y : y + 4] = spaceship[::-1, :]

# Glider
glider = decode("""x = 3, y = 3, rule = B3/S23
bo$2bo$3o!""").T

for y in range(70, 110, 5):
    for x in range(-39, -14, 5):
        field[x : x + 3, y : y + 3] = glider[:, ::-1]

# Rake
rake = decode("""x = 22, y = 19, rule = B3/S23
11b2o5b4o$9b2ob2o3bo3bo$9b4o8bo$10b2o5bo2bo2$8bo$7b2o8b2o$6bo9bo2bo$7b
5o4bo2bo$8b4o3b2ob2o$11bo4b2o4$18b4o$o2bo13bo3bo$4bo16bo$o3bo12bo2bo$
b4o!""").T

# field[-22:, 0:19] = rake[:, ::-1]

# Orthogonal
gliderless_gun = decode("""x = 40, y = 29, rule = B3/S23
6bo$6b3o$9bo$8b2o$2b2o$3bo$2bo$2b2o2$2b2o7bobo2bobo$2bobo6bo2bo3bo$3b
o5b2o3bobobo$3o7b3obo$o6b2o5b2o8b3o$7b2o4b2o8bo3bo$7b2o3bo9bo5bo$7b2o
bobo8bo3bo3bo$7b2obobo8bo7bo5b2o$21bobo3bobo5b2o$17b2o3b2o3b2o$10b2o4b
obo$6b2o2b2o4bo19b2o$5bobo7b2o19bo$5bo31b3o$4b2o19bo13bo$19b2obobobo$
19bob2ob2obo$27bo$27b2o!
""").T

field[-40:, :29] = gliderless_gun[:, :]
0
# Flip the bottom (first coordinate positive) to copy it over to the top (first coordinate negative)
field = np.hstack((field, field[:, -2::-1]))
field = np.hstack((field, np.zeros((100, 1), dtype=np.bool_)))

# Generate the guns
gun = decode("""x = 34, y = 24, rule = B3/S23
10b2o$10b2o3$4b2o$2bob2o3b3o$bo7b3o$4bo5b2o$2obo23b2o$2o7bo17bobo$8bo
bo7b2o4b2obobo$9bo7b3o4bobobo$18bo7bo$15b2o9b2o$15b2obo7b3o$15bo2bo7b
3o$15bo3bo6b3obo$16bo2bo6b2obobo$17b2o7b2o2bobo$28bo3bo$14b2o9bob4ob2o
$15bo9bo7bo$12b3o11b3ob3o$12bo15bobo!
""").T

field[20:54, 0:24] = gun
# field[20:54, 40:64] = gun
field[20:54, -24:] = gun[::-1, ::-1]
# field[20:54, -64:-40] = gun[::-1, ::-1]

# Max:
max_ = decode("""x = 27, y = 27, rule = B3/S23
18bo$17b3o$12b3o4b2o$11bo2b3o2bob2o$10bo3bobo2bobo$10bo4bobobobob2o$12b
o4bobo3b2o$4o5bobo4bo3bob3o$o3b2obob3ob2o9b2o$o5b2o5bo$bo2b2obo2bo2bo
b2o$7bobobobobobo5b4o$bo2b2obo2bo2bo2b2obob2o3bo$o5b2o3bobobo3b2o5bo$
o3b2obob2o2bo2bo2bob2o2bo$4o5bobobobobobo$10b2obo2bo2bob2o2bo$13bo5b2o
5bo$b2o9b2ob3obob2o3bo$2b3obo3bo4bobo5b4o$2b2o3bobo4bo$2b2obobobobo4b
o$5bobo2bobo3bo$4b2obo2b3o2bo$6b2o4b3o$7b3o$8bo!""")

# Place it directly in the middle
field[
    field.shape[0] // 2 - max_.shape[0] // 2 : field.shape[0] // 2
    + max_.shape[0] // 2
    + 1,
    field.shape[1] // 2 - max_.shape[1] // 2 : field.shape[1] // 2
    + max_.shape[1] // 2
    + 1,
] = max_

# Glider row in the bottom right
for i in range(80, 100, 5):
    field[i : i + 3, -3:] = glider

# Transpose the field to match the orientation of the image
field = field.T

# Display the image
Image.fromarray(field * 255).resize((400, 1000), resample=Image.BOX).show()


netlogo_code = generate_custom_shape_setup(field, top_left_x, top_left_y)

netlogo_code = open("head.txt").read() + netlogo_code + open("tail.txt").read()

with open("out.txt", "w") as output:
    output.write(netlogo_code)


# Setup max as the second field
field2 = np.zeros((100, 250))
starting_point = 0
field2[
    field2.shape[0] // 2 - max_.shape[0] // 2 : field2.shape[0] // 2
    + max_.shape[0] // 2
    + 1,
    field2.shape[1] // 2 - max_.shape[1] // 2 + starting_point : field2.shape[1] // 2
    + max_.shape[1] // 2
    + 1
    + starting_point,
] = max_
field3 = np.zeros((100, 250))

simulate_against(field, field2.T)
