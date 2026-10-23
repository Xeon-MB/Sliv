import json
from PIL import Image

im = Image.open("map_rendered.png")
pix = im.load()

with open("cells_dump.json", "r") as f:
    cells = json.load(f)

min_x = -34
min_y = -24

grid = {(c["x"], c["y"]): c for c in cells}

path_cuts = []

for y in range(min_y, 28):
    for x in range(min_x, 38):
        c1 = grid.get((x, y))
        c_right = grid.get((x+1, y))
        c_down = grid.get((x, y+1))
        
        px1 = (x - min_x) * 16
        py1 = (y - min_y) * 16
        
        # Check vertical boundary between (x, y) and (x+1, y)
        if c1 and c_right:
            for r in range(16):
                p_left = pix[px1 + 15, py1 + r]
                p_right = pix[px1 + 16, py1 + r]
                
                is_path_l = p_left[0] > 180 and p_left[1] > 120 and p_left[0] > p_left[1]
                is_grass_r = p_right[1] > 100 and p_right[0] < 80
                is_path_r = p_right[0] > 180 and p_right[1] > 120 and p_right[0] > p_right[1]
                is_grass_l = p_left[1] > 100 and p_left[0] < 80
                
                if (is_path_l and is_grass_r) or (is_path_r and is_grass_l):
                    path_cuts.append((x, y, x+1, y, "V", r))
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
                
                if (is_path_t and is_grass_b) or (is_path_b and is_grass_t):
                    path_cuts.append((x, y, x, y+1, "H", c))
                    break

print(f"Total PATH-GRASS cuts: {len(path_cuts)}")
for pc in path_cuts:
    c1 = grid.get((pc[0], pc[1]))
    c2 = grid.get((pc[2], pc[3]))
    t1 = f"{c1['source_id']}({c1['atlas_x']},{c1['atlas_y']})" if c1 else "None"
    t2 = f"{c2['source_id']}({c2['atlas_x']},{c2['atlas_y']})" if c2 else "None"
    print(f"  ({pc[0]:2d},{pc[1]:2d}) [{t1}] to ({pc[2]:2d},{pc[3]:2d}) [{t2}] ({pc[4]})")
