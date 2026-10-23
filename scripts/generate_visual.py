import json

with open("cells_dump.json", "r") as f:
    cells = json.load(f)

grid = {(c["x"], c["y"]): c for c in cells}

# Print map showing path cells with their atlas coordinates
# and empty/grass as spaces/dots
min_x = -34
max_x = 37
min_y = -24
max_y = 27

with open("path_map_visual.txt", "w") as f:
    for y in range(min_y, max_y + 1):
        line = f"{y:3d}: "
        for x in range(min_x, max_x + 1):
            c = grid.get((x, y))
            if not c:
                line += "   "
            elif c["source_id"] == 13: # Path
                line += f"{c['atlas_x']}{c['atlas_y']} "
            elif c["source_id"] == 10: # Farm
                line += "== "
            elif c["source_id"] == 8: # Cliff
                line += "^^ "
            elif c["source_id"] == 15: # Water
                line += "~~ "
            elif c["source_id"] == 9: # Beach
                line += ".. "
            elif c["source_id"] == 11: # Grass
                line += "   "
            else:
                line += "?? "
        f.write(line + "\n")
print("Saved path_map_visual.txt")
