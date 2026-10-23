import json
from PIL import Image

im = Image.open("map_rendered.png")
pix = im.load()

with open("cells_dump.json", "r") as f:
    cells = json.load(f)

min_x = -34
min_y = -24

grid = {(c["x"], c["y"]): c for c in cells}

# A path pixel is brown (r > g)
# A grass pixel is green (g > r)
# A water pixel is blue (b > g)

# In the tileset:
# The border between grass and path has a dark green outline: (25, 60, 62) or (38, 92, 66)
# If a brown path pixel (r > 150, g > 100, r > g) is immediately adjacent (distance 1) to a light grass pixel (g > 100, g > r)
# without the dark outline, THAT IS A FLAT CUTOFF!

flat_cuts = []

# Check horizontal boundaries between cell (x, y) and (x+1, y)
# and vertical boundaries between (x, y) and (x, y+1)
for y in range(min_y, 28):
    for x in range(min_x, 38):
        c1 = grid.get((x, y))
        c_right = grid.get((x+1, y))
        c_down = grid.get((x, y+1))
        
        px1 = (x - min_x) * 16
        py1 = (y - min_y) * 16
        
        # Check vertical boundary between (x, y) and (x+1, y)
        if c1 and c_right:
            # check the 16 pixels at column 15 of c1 and column 0 of c_right
            for r in range(16):
                p_left = pix[px1 + 15, py1 + r]
                p_right = pix[px1 + 16, py1 + r]
                
                # Path cutting into Grass:
                # one is brown path (p[0] > 180 and p[1] > 120 and p[0] > p[1])
                # other is light grass (p[1] > 100 and p[0] < 80)
                is_path_l = p_left[0] > 180 and p_left[1] > 120 and p_left[0] > p_left[1]
                is_grass_r = p_right[1] > 100 and p_right[0] < 80
                is_path_r = p_right[0] > 180 and p_right[1] > 120 and p_right[0] > p_right[1]
                is_grass_l = p_left[1] > 100 and p_left[0] < 80
                
                # Water cutting into Grass/Path:
                # one is water (p[2] > 200 and p[0] < 50)
                # other is grass or path
                is_water_l = p_left[2] > 200 and p_left[0] < 50
                is_water_r = p_right[2] > 200 and p_right[0] < 50
                
                if (is_path_l and is_grass_r) or (is_path_r and is_grass_l):
                    flat_cuts.append((x, y, f"Path-Grass vertical cut between ({x},{y}) and ({x+1},{y}) at row {r}"))
                    break
                elif (is_water_l and (is_grass_r or is_path_r)) or (is_water_r and (is_grass_l or is_path_l)):
                    flat_cuts.append((x, y, f"Water-Land vertical cut between ({x},{y}) and ({x+1},{y}) at row {r}"))
                    break
                    
        # Check horizontal boundary between (x, y) and (x, y+1)
        if c1 and c_down:
            for c in range(16):
                p_top = pix[px1 + c, py1 + 15]
                p_bot = pix[px1 + c, py1 + 16]
                
                is_path_t = p_top[0] > 180 and p_top[1] > 120 and p_top[0] > p_top[1]
                is_grass_b = p_bot[1] > 100 and p_bot[0] < 80
                is_path_b = p_bot[0] > 180 and p_bot[1] > 120 and p_bot[0] > p_bot[1]
                is_grass_t = p_top[1] > 100 and p_top[0] < 80
                
                is_water_t = p_top[2] > 200 and p_top[0] < 50
                is_water_b = p_bot[2] > 200 and p_bot[0] < 50
                
                if (is_path_t and is_grass_b) or (is_path_b and is_grass_t):
                    flat_cuts.append((x, y, f"Path-Grass horizontal cut between ({x},{y}) and ({x},{y+1}) at col {c}"))
                    break
                elif (is_water_t and (is_grass_b or is_path_b)) or (is_water_b and (is_grass_t or is_path_t)):
                    flat_cuts.append((x, y, f"Water-Land horizontal cut between ({x},{y}) and ({x},{y+1}) at col {c}"))
                    break

print(f"Total flat cut boundaries detected: {len(flat_cuts)}")
for fc in flat_cuts:
    print(f"  ({fc[0]:2d},{fc[1]:2d}): {fc[2]}")
