import json

with open("cells_dump_prev.json", "r") as f:
    prev_cells = json.load(f)

prev_grid = {(c["x"], c["y"]): c for c in prev_cells}

with open("cells_dump.json", "r") as f:
    curr_cells = json.load(f)

curr_grid = {(c["x"], c["y"]): c for c in curr_cells}

# Check top path in prev_grid:
print("=== PREV TOP PATH (x=-5..5, y=-22..-10) ===")
for y in range(-22, -9):
    line = []
    for x in range(-5, 6):
        c = prev_grid.get((x, y))
        if c:
            line.append(f"{c['source_id']}:({c['atlas_x']},{c['atlas_y']})")
        else:
            line.append("   empty   ")
    print(f"{y:3d}: " + " ".join(line))
