import json

with open("cells_dump.json", "r") as f:
    cells = json.load(f)

grid = {(c["x"], c["y"]): c for c in cells}

print("=== SEARCHING FOR NARROW PATHS AND CORNERS ===")
for c in cells:
    if c["source_id"] != 13: # Path
        continue
    x, y = c["x"], c["y"]
    ax, ay = c["atlas_x"], c["atlas_y"]
    
    # Check neighbors that are path OR farmland (since farmland is surrounded by path)
    # Actually let's check what neighbors are path:
    n_up = grid.get((x, y-1), {}).get("source_id") in [13]
    n_down = grid.get((x, y+1), {}).get("source_id") in [13]
    n_left = grid.get((x-1, y), {}).get("source_id") in [13]
    n_right = grid.get((x+1, y), {}).get("source_id") in [13]
    
    # Narrow path conditions:
    # 1) Vertical narrow path: up and down are path, but left and right are NOT path!
    # 2) Horizontal narrow path: left and right are path, but up and down are NOT path!
    # 3) Turn in a narrow path: e.g. up and right are path, but down and left are NOT path, AND the path is width 1!
    # 4) Dead end / end of path: only 1 neighbor is path!
    # 5) Isolated tile: 0 neighbors are path!
    
    cardinals_count = sum([n_up, n_down, n_left, n_right])
    
    if (n_up and n_down and not n_left and not n_right):
        print(f"VERTICAL NARROW: ({x}, {y}) current atlas=({ax}, {ay})")
    elif (n_left and n_right and not n_up and not n_down):
        print(f"HORIZONTAL NARROW: ({x}, {y}) current atlas=({ax}, {ay})")
    elif cardinals_count == 1:
        print(f"DEAD END / END: ({x}, {y}) current atlas=({ax}, {ay}), neighbor={'U' if n_up else 'D' if n_down else 'L' if n_left else 'R'}")
    elif cardinals_count == 0:
        print(f"ISOLATED: ({x}, {y}) current atlas=({ax}, {ay})")
